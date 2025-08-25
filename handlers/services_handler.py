import logging
from aiogram import types, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from keyboards import services_kb

# Настройка логирования для этого модуля
logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(lambda c: c.data == "services")
async def services_callback(query: CallbackQuery):
    try:
        # Логируем информацию о пользователе
        user_info = f"ID: {query.from_user.id}, "
        if query.from_user.username:
            user_info += f"Username: @{query.from_user.username}, "
        user_info += f"Name: {query.from_user.first_name}"
        if query.from_user.last_name:
            user_info += f" {query.from_user.last_name}"

        logger.info(f"Services callback received from user: {user_info}")

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

        logger.info(f"Services message successfully updated for user {query.from_user.id}")

    except TelegramBadRequest as e:
        # Обрабатываем ошибку "message is not modified"
        if "message is not modified" in str(e):
            logger.debug(f"Message not modified for user {query.from_user.id} - same content")
            await query.answer()  # Убираем часики у кнопки
        else:
            logger.error(f"TelegramBadRequest for user {query.from_user.id}: {e}")
            await query.answer("Произошла ошибка при обновлении сообщения", show_alert=False)

    except Exception as e:
        # Логируем другие ошибки с полной информацией
        logger.error(
            f"Unexpected error in services callback for user {query.from_user.id}: {e}",
            exc_info=True
        )

        # Дополнительная информация об ошибке
        error_context = {
            'user_id': query.from_user.id,
            'chat_id': query.message.chat.id if query.message else 'unknown',
            'error_type': type(e).__name__,
            'error_message': str(e)
        }
        logger.debug(f"Error context: {error_context}")

        await query.answer("Произошла непредвиденная ошибка", show_alert=False)