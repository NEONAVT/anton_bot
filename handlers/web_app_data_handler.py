import json
import logging
from aiogram import types, Router, F
from aiogram.exceptions import TelegramBadRequest
from bot_config import telegram_client
from settings import settings
from aiogram.enums import ParseMode

# Настройка логирования для этого модуля
logger = logging.getLogger(__name__)

router = Router()
active_requests = {}


@router.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    try:
        logger.info(f"Web app data received from user {message.from_user.id}")
        logger.debug(f"Raw web app data: {message.web_app_data.data}")

        data = json.loads(message.web_app_data.data)
        form_type = data.get("form", "unknown")

        logger.info(f"Form type: {form_type}")
        logger.debug(f"Parsed data: {data}")

        if form_type == "callback":
            # Всегда используем get() с дефолтом
            name = data.get("name", "не указано")
            phone = data.get("phone", "не указано")
            topic = data.get("topic", "не указано")
            time = data.get("time", "не указано")

            text_msg = (
                f"🔔Заказан обратный звонок от {name.capitalize()}\n"
                f"на номер телефона {phone} в {time}\n"
                f'с темой звонка "{topic.capitalize()}".\n\n'
                f"Для связи в чате @{message.from_user.username or 'нет username'}"
            )

            admin_ids = [int(chat_id) for chat_id in settings.admin_chat_id.split(",") if chat_id]
            logger.info(f"Sending callback request to admins: {admin_ids}")

            for admin_id in admin_ids:
                try:
                    await telegram_client.post(method="sendMessage", chat_id=admin_id, text=text_msg)
                    logger.info(f"Callback request sent to admin {admin_id}")
                except Exception as e:
                    logger.error(f"Failed to send callback request to admin {admin_id}: {e}")

            await message.answer(
                f"{message.from_user.first_name}, спасибо!\n"
                "📨 Ваша заявка на обратный звонок передана!\n"
                "С вами свяжутся наши специалисты в удобное для вас время."
            )
            logger.info(f"Callback confirmation sent to user {message.from_user.id}")

        elif form_type == "problem":
            name = data.get("name", "не указано")
            phone = data.get("phone", "не указано")
            problem = data.get("topic", "не указано")

            active_requests[message.chat.id] = {
                "name": name,
                "phone": phone,
                "problem": problem,
                "files": []
            }

            logger.info(f"Problem request started for user {message.from_user.id}: name={name}, phone={phone}")
            logger.debug(f"Problem description: {problem}")

            await message.answer(
                f"Заявка сохранена:\n"
                f"Имя: {name}\n"
                f"Телефон: {phone}\n"
                f"Описание проблемы: {problem}\n\n"
                "*📷 Пришлите одно фото или одно видео вашей проблемы одним или несколькими сообщениями.*",
                parse_mode=ParseMode.MARKDOWN,
            )
            logger.info(f"Problem request instructions sent to user {message.from_user.id}")

        else:
            logger.warning(f"Unknown form type from user {message.from_user.id}: {form_type}")
            await message.answer("Неизвестный тип формы. Пожалуйста, попробуйте снова.")

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error from user {message.from_user.id}: {e}")
        await message.answer("Ошибка обработки данных. Пожалуйста, попробуйте снова.")
    except Exception as e:
        logger.error(f"Unexpected error in web_app_data_handler for user {message.from_user.id}: {e}", exc_info=True)
        await message.answer("Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже.")


# Приём файлов
@router.message(F.photo | F.video | F.document)
async def handle_files(message: types.Message):
    try:
        if message.chat.id not in active_requests:
            logger.warning(f"File received from user {message.from_user.id} without active request")
            await message.answer("У вас нет активной заявки. Сначала заполните форму.")
            return

        req = active_requests[message.chat.id]
        file_type = None
        file_id = None

        if message.photo:
            file_type = "photo"
            file_id = message.photo[-1].file_id
            req["files"].append(("photo", file_id))
        elif message.video:
            file_type = "video"
            file_id = message.video.file_id
            req["files"].append(("video", file_id))
        elif message.document:
            file_type = "document"
            file_id = message.document.file_id
            req["files"].append(("document", file_id))

        logger.info(f"File added to request for user {message.from_user.id}: type={file_type}, id={file_id}")
        logger.debug(f"Total files in request: {len(req['files'])}")

        await message.answer("Файл добавлен к заявке. Отправьте еще файлы или нажмите /done для завершения.")

    except Exception as e:
        logger.error(f"Error handling file from user {message.from_user.id}: {e}", exc_info=True)
        await message.answer("Произошла ошибка при обработке файла. Пожалуйста, попробуйте снова.")


@router.message(F.text == "/done")
async def finalize_request_command(message: types.Message):
    await finalize_request(message.chat.id, message)


async def finalize_request(chat_id: int, message: types.Message):
    try:
        req = active_requests.pop(chat_id, None)
        if not req:
            logger.warning(f"Finalize request called for user {message.from_user.id} but no active request found")
            await message.answer("У вас нет активной заявки.")
            return

        text_msg = (
            f"🔔 Новая заявка от {req['name'].capitalize()}\n"
            f"Телефон: {req['phone']}\n"
            f"Проблема: {req['problem']}\n\n"
            f"Для связи: @{message.from_user.username or 'нет username'}"
        )

        admin_ids = [int(chat_id) for chat_id in settings.admin_chat_id.split(",") if chat_id]
        logger.info(f"Sending problem request to admins: {admin_ids}, files count: {len(req['files'])}")

        for admin_id in admin_ids:
            try:
                # Отправляем текстовое сообщение
                await telegram_client.post(method="sendMessage", chat_id=admin_id, text=text_msg)
                logger.info(f"Problem request text sent to admin {admin_id}")

                # Отправляем файлы
                for ftype, fid in req["files"]:
                    try:
                        if ftype == "photo":
                            await telegram_client.post(method="sendPhoto", chat_id=admin_id, photo=fid)
                        elif ftype == "video":
                            await telegram_client.post(method="sendVideo", chat_id=admin_id, video=fid)
                        elif ftype == "document":
                            await telegram_client.post(method="sendDocument", chat_id=admin_id, document=fid)
                        logger.info(f"File sent to admin {admin_id}: type={ftype}")
                    except Exception as file_e:
                        logger.error(f"Failed to send file to admin {admin_id}: {file_e}")

            except Exception as admin_e:
                logger.error(f"Failed to send request to admin {admin_id}: {admin_e}")

        await message.answer("✅ Ваша заявка передана администратору.")
        logger.info(f"Request finalized for user {message.from_user.id}")

    except Exception as e:
        logger.error(f"Error finalizing request for user {message.from_user.id}: {e}", exc_info=True)
        await message.answer("Произошла ошибка при отправке заявки. Пожалуйста, попробуйте снова.")