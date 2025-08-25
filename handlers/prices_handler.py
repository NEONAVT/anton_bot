from aiogram import types, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from keyboards import prices_kb

router = Router()


@router.callback_query(lambda c: c.data == "prices")
async def prices_callback(query: CallbackQuery):
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
