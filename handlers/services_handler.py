from aiogram import types, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from keyboards import services_kb

router = Router()

@router.callback_query(lambda c: c.data == "services")
async def services_callback(query: CallbackQuery):
    await query.message.edit_text(
        "*Ремонт и установка котлов:*\n"
        "Меняем и устанавливаем газовые котлы, колонки и бойлеры. "
        "_Гарантируем безопасную и надёжную работу оборудования._\n\n"
        "*Системы отопления:*\n"
        "Проектируем и монтируем системы отопления с нуля. "
        "_Эффективно, долговечно, с учётом всех норм._\n\n"
        "*Сантехника:*\n"
        "Устанавливаем и ремонтируем водоснабжение, трубы и сантехническое оборудование. "
        "_Работа без протечек и с долгим сроком службы._\n\n"
        "*Если хотите получить консультацию или точную оценку, нажмите кнопку «Хочу консультацию».*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=services_kb
    )
