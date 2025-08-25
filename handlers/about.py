import logging
from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest
from keyboards import start_kb

# Настройка логирования для этого модуля
logger = logging.getLogger(__name__)

router = Router()


@router.message(F.text == "👨‍🔧 О нас")
async def about_callback(message: Message):
    try:
        logger.info(f"User {message.from_user.id} ({message.from_user.username}) requested prices")

        await message.delete()

        await message.answer(
            "*О нас*\n\n"
            "Мы специализируемся на инженерных системах, которые делают дом и бизнес "
            "комфортными и безопасными. С конца 90-х годов устанавливаем и меняем "
            "газовые котлы, колонки и бойлеры, проектируем и монтируем системы "
            "отопления и водоснабжения под ключ.\n\n"
            "Работаем как с частными клиентами, так и с организациями. Для одних это "
            "гарантия тёплого и надёжного дома, для других — бесперебойная работа "
            "объекта без простоя и лишних затрат.\n\n"
            "Наша команда не только монтирует новое оборудование, но и продлевает срок "
            "службы существующего: промываем системы отопления и водоснабжения, чистим "
            "бойлеры, устраняем засоры и повышаем эффективность работы.\n\n"
            "Опыт более 25 лет — это умение решать задачи разного масштаба: от квартиры "
            "и коттеджа до производственного помещения. Мы знаем, что от инженерных "
            "сетей зависит каждый день жизни, и поэтому делаем их максимально надёжными, "
            "экономичными и простыми в обслуживании.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=start_kb
        )

        logger.info(f"Prices message successfully updated for user {message.from_user.id}")

    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            logger.debug(f"Message not modified for user {message.from_user.id} - same content")
            await message.answer()
        else:
            logger.error(f"TelegramBadRequest for user {message.from_user.id}: {e}")
            await message.answer("Произошла ошибка при обновлении сообщения", show_alert=False)

    except Exception as e:
        logger.error(f"Unexpected error for user {message.from_user.id}: {e}", exc_info=True)
        await message.answer("Произошла непредвиденная ошибка", show_alert=False)