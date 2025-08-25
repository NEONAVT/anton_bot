from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import WebAppInfo

projects_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💬 Хочу консультацию", web_app=WebAppInfo(url="https://neonavt.github.io/anton_bot/request-callback.html"))],
        [
            KeyboardButton(text="Очистка котлов и труб"),
            KeyboardButton(text="Монтаж тёплого пола")
        ],
        [
            KeyboardButton(text="Водопроводная разводка"),
            KeyboardButton(text="Установка котлов и бойлеров")
        ],
        [KeyboardButton(text="В начало")
        ],

    ],
    resize_keyboard=True,
    one_time_keyboard=False
)