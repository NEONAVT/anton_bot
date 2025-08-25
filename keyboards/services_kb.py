# services_kb.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import WebAppInfo

services_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💬 Хочу консультацию", web_app=WebAppInfo(url="https://neonavt.github.io/anton_bot/request-callback.html"))],
        [
            KeyboardButton(text="🔧 Услуги"),
            KeyboardButton(text="👨‍🔧 О нас")
        ],
        [
            KeyboardButton(text="🧾 Стоимость"),
            KeyboardButton(text="✅ Проекты")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)