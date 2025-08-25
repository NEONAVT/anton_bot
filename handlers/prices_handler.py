import logging
from aiogram import types, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from keyboards import prices_kb

# Настройка логирования для этого модуля
logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(lambda c: c.data == "prices")
async def prices_callback(query: CallbackQuery):
    try:
        logger.info(f"User {query.from_user.id} ({query.from_user.username}) requested prices")

        await query.message.edit_text(
            "💰 *Стоимость услуг*\n\n"
            "Мы занимаемся заменой и установкой газовых котлов, колонок, бойлеров, "
            "монтажом систем отопления и водоснабжения с нуля, а также ремонтом сантехники.\n\n"
            "Каждый проект уникален, поэтому стоимость рассчитывается индивидуально "
            "в зависимости от ваших потребностей и условий.\n\n"
            "Вы можете описать свою проблему или прислать фото — "
            "мы внимательно рассмотрим заявку и свяжемся с вами для точного расчета.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=prices_kb
        )

        logger.info(f"Prices message successfully updated for user {query.from_user.id}")

    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            logger.debug(f"Message not modified for user {query.from_user.id} - same content")
            await query.answer()
        else:
            logger.error(f"TelegramBadRequest for user {query.from_user.id}: {e}")
            await query.answer("Произошла ошибка при обновлении сообщения", show_alert=False)

    except Exception as e:
        logger.error(f"Unexpected error for user {query.from_user.id}: {e}", exc_info=True)
        await query.answer("Произошла непредвиденная ошибка", show_alert=False)