from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import WebAppInfo
prices_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📤 Отправить заявку на расчет", web_app=WebAppInfo(url="https://neonavt.github.io/anton_bot/make-order.html"))],
    [InlineKeyboardButton(text="🔧 Услуги", callback_data="services"),
     InlineKeyboardButton(text="👨‍🔧 О нас", callback_data="about")],
    [InlineKeyboardButton(text="🧾 Стоимость", callback_data="prices"),
     InlineKeyboardButton(text="✅ Проекты", callback_data="projects")]
])