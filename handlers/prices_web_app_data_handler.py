import json

from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards import start_kb
from bot_config import telegram_client
from settings import settings

router = Router()
active_requests = {}


@router.message(F.web_app_data)
async def prices_web_app_data_handler(message: Message):
    data = json.loads(message.web_app_data.data)
    active_requests[message.chat.id] = {
        "name": data["name"],
        "phone": data["phone"],
        "problem": data["topic"],
        "files": []
    }
    await message.answer(
        f"Заявка сохранена:\n"
        f"Имя: {data['name']}\n"
        f"Телефон: {data['phone']}\n"
        f"Описание проблемы: {data['topic']}\n"
        f"Пришлите фото или видео вашей проблемы одним или несколькими сообщениями."
    )


# Приём файлов
@router.message(F.photo | F.video | F.document)
async def handle_files(message: Message):
    if message.chat.id not in active_requests:
        await message.answer("У вас нет активной заявки. Сначала заполните форму.")
        return

    req = active_requests[message.chat.id]

    if message.photo:
        file_id = message.photo[-1].file_id
        req["files"].append(("photo", file_id))
    elif message.video:
        file_id = message.video.file_id
        req["files"].append(("video", file_id))
    elif message.document:
        file_id = message.document.file_id
        req["files"].append(("document", file_id))

    await message.answer("Файл добавлен к заявке.")

    # Если хочешь завершать сразу после первого файла:
    # await finalize_request(msg.chat.id)


async def finalize_request(chat_id: int, message: Message):
    req = active_requests.pop(chat_id, None)
    if not req:
        await message.answer("У вас нет активной заявки.")
        return

    # Основной текст
    text_msg = (
        f"🔔 Новая заявка от {req['name'].capitalize()}\n"
        f"Телефон: {req['phone']}\n"
        f"Проблема: {req['problem']}\n\n"
        f"Для связи: @{message.from_user.username or 'нет username'}"
    )

    admin_ids = [int(chat_id) for chat_id in settings.admin_chat_id.split(",") if chat_id]
    for admin_id in admin_ids:
        # Отправляем текст
        await telegram_client.post(
            method="sendMessage",
            chat_id=admin_id,
            text=text_msg
        )

        # Отправляем все файлы
        for ftype, fid in req["files"]:
            if ftype == "photo":
                await telegram_client.post(
                    method="sendPhoto",
                    chat_id=admin_id,
                    photo=fid
                )
            elif ftype == "video":
                await telegram_client.post(
                    method="sendVideo",
                    chat_id=admin_id,
                    video=fid
                )
            elif ftype == "document":
                await telegram_client.post(
                    method="sendDocument",
                    chat_id=admin_id,
                    document=fid
                )

    await message.answer("✅ Ваша заявка передана администратору.")
