import json
from aiogram import types, Router, F
from bot_config import telegram_client
from settings import settings

router = Router()
active_requests = {}

@router.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    data = json.loads(message.web_app_data.data)
    form_type = data.get("form")

    if form_type == "callback":
        # Обратный звонок
        text_msg = (
            f"🔔Заказан обратный звонок от {data['name'].capitalize()}\n"
            f"на номер телефона {data['phone']} в {data.get('time', 'не указано')}\n"
            f'с темой звонка "{data["topic"].capitalize()}".\n\n'
            f"Для связи в чате @{message.from_user.username or 'нет username'}"
        )

        admin_ids = [int(chat_id) for chat_id in settings.admin_chat_id.split(",") if chat_id]
        for chat_id in admin_ids:
            await telegram_client.post(
                method="sendMessage",
                chat_id=chat_id,
                text=text_msg
            )
        await message.answer(
            f"{message.from_user.first_name}, спасибо!\n"
            "📨 Ваша заявка на обратный звонок передана!\n"
            "С вами свяжутся наши специалисты в удобное для вас время."
        )

    elif form_type == "problem":
        # Заявка с описанием проблемы
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
            "Пришлите фото или видео вашей проблемы одним или несколькими сообщениями."
        )

# Приём файлов остаётся прежним
@router.message(F.photo | F.video | F.document)
async def handle_files(message: types.Message):
    if message.chat.id not in active_requests:
        await message.answer("У вас нет активной заявки. Сначала заполните форму.")
        return

    req = active_requests[message.chat.id]

    if message.photo:
        req["files"].append(("photo", message.photo[-1].file_id))
    elif message.video:
        req["files"].append(("video", message.video.file_id))
    elif message.document:
        req["files"].append(("document", message.document.file_id))

    await message.answer("Файл добавлен к заявке.")

async def finalize_request(chat_id: int, message: types.Message):
    req = active_requests.pop(chat_id, None)
    if not req:
        await message.answer("У вас нет активной заявки.")
        return

    text_msg = (
        f"🔔 Новая заявка от {req['name'].capitalize()}\n"
        f"Телефон: {req['phone']}\n"
        f"Проблема: {req['problem']}\n\n"
        f"Для связи: @{message.from_user.username or 'нет username'}"
    )

    admin_ids = [int(chat_id) for chat_id in settings.admin_chat_id.split(",") if chat_id]
    for admin_id in admin_ids:
        await telegram_client.post(method="sendMessage", chat_id=admin_id, text=text_msg)
        for ftype, fid in req["files"]:
            if ftype == "photo":
                await telegram_client.post(method="sendPhoto", chat_id=admin_id, photo=fid)
            elif ftype == "video":
                await telegram_client.post(method="sendVideo", chat_id=admin_id, video=fid)
            elif ftype == "document":
                await telegram_client.post(method="sendDocument", chat_id=admin_id, document=fid)

    await message.answer("✅ Ваша заявка передана администратору.")
