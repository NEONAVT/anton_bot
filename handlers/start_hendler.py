import logging
from aiogram import types, Router
from aiogram.filters import CommandStart
from keyboards import start_kb

# Настройка логирования для этого модуля
logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    try:
        # Логируем информацию о пользователе
        user_info = f"ID: {message.from_user.id}, "
        if message.from_user.username:
            user_info += f"Username: @{message.from_user.username}, "
        user_info += f"Name: {message.from_user.first_name}"
        if message.from_user.last_name:
            user_info += f" {message.from_user.last_name}"

        logger.info(f"Start command received from user: {user_info}")
        logger.info(f"Chat ID: {message.chat.id}, Chat type: {message.chat.type}")

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
            ),
            reply_markup=start_kb
        )

        logger.info(f"Start message successfully sent to user {message.from_user.id}")

    except Exception as e:
        # Логируем ошибку с полной информацией
        logger.error(
            f"Error sending start message to user {message.from_user.id}: {e}",
            exc_info=True
        )

        # Дополнительная информация об ошибке
        error_context = {
            'user_id': message.from_user.id,
            'chat_id': message.chat.id,
            'error_type': type(e).__name__,
            'error_message': str(e)
        }
        logger.debug(f"Error context: {error_context}")

        # Можно также отправить сообщение пользователю об ошибке
        try:
            await message.answer(
                "⚠️ Произошла ошибка при обработке запроса. Попробуйте позже."
            )
        except Exception as inner_e:
            logger.error(f"Failed to send error message to user: {inner_e}")