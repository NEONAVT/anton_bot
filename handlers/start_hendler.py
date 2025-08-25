import json

from aiogram import types, Router, F
from aiogram.filters import CommandStart
from keyboards import start_kb
from bot_config import telegram_client
from settings import settings

router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    try:
        print(message.chat.id)
        await message.answer(
            text=(
                f"👋Добрый день, {message.from_user.first_name}!\n\n"
                f"Мы помогаем с заменой и установкой газовых котлов, колонок, бойлеров, "
                f"а также с монтажом систем отопления и водоснабжения с нуля.\n\n"
                f"📞Звонки принимаются с 8:00 до 10:00. \n"
                f"В остальное время мы занимаемся выполнением заказов, "
                f"чтобы всё было сделано качественно и в срок.\n\n"
                f"Вы можете быстро узнать о наших услугах или заказать обратный звонок — "
                f"с вами свяжутся в ближайшее время.\n\n"
                f"⬇️Для получения информации воспользуйтесь кнопками ниже."
            )
            ,
            reply_markup=start_kb
        )
    except Exception as e:
        # Обработка ошибок через логирование или сервис
        print(f"Ошибка при отправке сообщения: {e}")

@router.message(F.web_app_data)
async def callback_web_app_data_handler(message: types.Message):
    """Handle data sent from the WebApp."""
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
