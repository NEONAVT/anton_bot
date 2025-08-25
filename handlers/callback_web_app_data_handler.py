import json

from aiogram import types, Router, F
from aiogram.filters import CommandStart
from keyboards import start_kb
from bot_config import telegram_client
from settings import settings

router = Router()

@router.message(F.web_app_data)
async def callback_web_app_data_handler(message: types.Message):
    import json
    result = json.loads(message.web_app_data.data)
    text_msg = (
        f"🔔Заказан обратный звонок от {result['name'].capitalize()} \n"
        f"на номер телефона {result['phone']} в {result['time']} \n"
        f'с темой звонка "{result['topic'].capitalize()}". \n\n'
        f"Для связи в чате @{message.from_user.username}"
    )

    admin_ids = [int(chat_id) for chat_id in settings.admin_chat_id.split(",") if chat_id]
    for chat_id in admin_ids:
        await telegram_client.post(
            method="sendMessage",
            chat_id=chat_id,
            text=text_msg
        )
    await message.answer(
        f"{message.from_user.first_name}, спасибо! \n\n"
        f"📨Ваша заявка на обратный звонок передана! \n\n"
        f"С вами свяжутся наши специалисты в удобное для вас время или напишут в личные сообщения в Телеграм."
    )
