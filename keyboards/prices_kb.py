# prices_kb.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import WebAppInfo

prices_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📤 Отправить заявку на расчет", web_app=WebAppInfo(url="https://neonavt.github.io/anton_bot/make-order.html"))],
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