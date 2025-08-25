import logging
from pathlib import Path
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, InputMediaPhoto, FSInputFile
from bot_config import bot
from handlers.start_hendler import start
from keyboards import projects_kb

logger = logging.getLogger(__name__)

router = Router()


@router.message(F.text == "✅ Проекты")
async def projects_callback(message: Message):
    try:
        # Логируем информацию о пользователе
        user_info = f"ID: {message.from_user.id}, "
        if message.from_user.username:
            user_info += f"Username: @{message.from_user.username}, "
        user_info += f"Name: {message.from_user.first_name}"
        if message.from_user.last_name:
            user_info += f" {message.from_user.last_name}"

        logger.info(f"Services callback received from user: {user_info}")

        await message.delete()

        await message.answer(
            f"*Вы можете ознакомиться с нашими проектами ниже, нажимая кнопки.*\n\n"
            "Если у вас появились вопросы - нажмите на кнопку 'Хочу консультацию' и мы подробно на них ответим",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=projects_kb
        )
    except Exception as e:
        # Логируем другие ошибки с полной информацией
        logger.error(
            f"Unexpected error in services callback for user {message.from_user.id}: {e}",
            exc_info=True
        )

@router.message(F.text == "Очистка котлов и труб")
async def pipes_cleaning_callback(message: Message):
    await message.delete()
    try:
        # Абсолютный путь к папке с фото
        PROJECT_ROOT = Path(__file__).parent.parent  # поднимаемся на 2 уровня вверх
        PHOTO_DIR = PROJECT_ROOT / "projects_images" / "calc_plaque"

        file_names = [
            "5289569554843957948.jpg",
            "5289569554843957950.jpg",
            "5289569554843957951.jpg",
            "5289569554843957952.jpg",
            "5289569554843957956.jpg",
            "5289569554843957957.jpg",
            "5289569554843957958.jpg",
            "5289569554843957960.jpg",
            "5289569554843957961.jpg",
            "5289569554843957962.jpg",
        ]

        file_paths = [PHOTO_DIR / fname for fname in file_names]

        # Проверка существования файлов
        for path in file_paths:
            if not path.exists():
                logger.error(f"Файл не найден: {path}")
                return

        # Подпись только для первого фото
        caption = (
            "🚨 *Что это?*\n\n"
            "*Накипь, ржавчина, мусор — всё, что съедает ваш котёл, бойлер и трубы изнутри.*\n\n"
            "Мы вычищаем — до состояния 'как новый'.\n"
            "🛠️ Чистка котлов, бойлеров, труб — без разборки, быстро и качественно.\n"
            "👉 Не ждите аварии! Проверьте своё оборудование уже сегодня.\n"
            "📩 Напишите — сделаем чистку за 1 день."
        )

        media = []
        for i, path in enumerate(file_paths):
            if i == 0:
                media.append(
                    InputMediaPhoto(
                        media=FSInputFile(path),
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=projects_kb
                    )
                )
            else:
                media.append(InputMediaPhoto(media=FSInputFile(path)))

        await bot.send_media_group(chat_id=message.chat.id, media=media)

    except Exception as e:
        # Логируем другие ошибки с полной информацией
        logger.error(
            f"Unexpected error in services callback for user {message.from_user.id}: {e}",
            exc_info=True
        )


@router.message(F.text == "Монтаж тёплого пола")
async def warm_floor_callback(message: Message):
    await message.delete()
    try:
        # Абсолютный путь к папке с фото
        PROJECT_ROOT = Path(__file__).parent.parent  # поднимаемся на 2 уровня вверх
        PHOTO_DIR = PROJECT_ROOT / "projects_images" / "warm_floor_installation"

        file_names = [
            "1.jpg",
            "2.jpg",
            "3.jpg",
            "4.jpg",
        ]

        file_paths = [PHOTO_DIR / fname for fname in file_names]

        # Проверка существования файлов
        for path in file_paths:
            if not path.exists():
                logger.error(f"Файл не найден: {path}")
                return

        # Подпись только для первого фото
        caption = (
            "🔥 *Теплый пол — комфорт и экономия круглый год*\n\n"
            "*Холодные полы, сквозняки, высокая влажность — всё это делает ваш дом неудобным.*\n\n"
            "Мы укладываем тёплые полы — ровно, надёжно, безопасно.\n"
            "🛠️ Монтаж теплых полов под любые покрытия: плитка, ламинат, паркет.\n"
            "⚡ Быстрое подключение к системе отопления и управление через терморегулятор.\n"
            "👉 Забудьте про холод и сырость — сделайте дом комфортным уже сегодня.\n"
            "📩 Свяжитесь с нами — проконсультируем и рассчитаем стоимость за 1 день."
        )

        media = []
        for i, path in enumerate(file_paths):
            if i == 0:
                media.append(
                    InputMediaPhoto(
                        media=FSInputFile(path),
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=projects_kb
                    )
                )
            else:
                media.append(InputMediaPhoto(media=FSInputFile(path)))

        await bot.send_media_group(chat_id=message.chat.id, media=media)

    except Exception as e:
        # Логируем другие ошибки с полной информацией
        logger.error(
            f"Unexpected error in services callback for user {message.from_user.id}: {e}",
            exc_info=True
        )


@router.message(F.text == "Водопроводная разводка")
async def pipes_routing_callback(message: Message):
    await message.delete()
    try:
        # Абсолютный путь к папке с фото
        PROJECT_ROOT = Path(__file__).parent.parent  # поднимаемся на 2 уровня вверх
        PHOTO_DIR = PROJECT_ROOT / "projects_images" / "water_supply_routing"

        file_names = [
            "1.jpg",

        ]

        file_paths = [PHOTO_DIR / fname for fname in file_names]

        # Проверка существования файлов
        for path in file_paths:
            if not path.exists():
                logger.error(f"Файл не найден: {path}")
                return

        # Подпись только для первого фото
        caption = (
            "🔧 *Профессиональная разводка труб — залог надежного отопления*\n\n"
            "*Хаотичная прокладка и некачественные соединения приводят к утечкам, шуму и поломкам.*\n\n"
            "Мы делаем аккуратную, продуманную разводку — надёжно, эстетично, безопасно.\n"
            "🛠️ Монтаж труб любой сложности, под ключ, с гарантией на работу.\n"
            "⚡ Оптимальная схема для котельного оборудования и бойлеров.\n"
            "👉 Забудьте про проблемы с отоплением — всё будет работать идеально.\n"
            "📩 Свяжитесь с нами — проект и монтаж за 1 день."
        )

        media = []
        for i, path in enumerate(file_paths):
            if i == 0:
                media.append(
                    InputMediaPhoto(
                        media=FSInputFile(path),
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=projects_kb
                    )
                )
            else:
                media.append(InputMediaPhoto(media=FSInputFile(path)))

        await bot.send_media_group(chat_id=message.chat.id, media=media)

    except Exception as e:
        # Логируем другие ошибки с полной информацией
        logger.error(
            f"Unexpected error in services callback for user {message.from_user.id}: {e}",
            exc_info=True
        )


@router.message(F.text == "Установка котлов и бойлеров")
async def heater_installation_callback(message: Message):
    await message.delete()
    try:
        # Абсолютный путь к папке с фото
        PROJECT_ROOT = Path(__file__).parent.parent  # поднимаемся на 2 уровня вверх
        PHOTO_DIR = PROJECT_ROOT / "projects_images" / "heater_installation"

        file_names = [
            "1.jpg",
            "2.jpg",

        ]

        file_paths = [PHOTO_DIR / fname for fname in file_names]

        # Проверка существования файлов
        for path in file_paths:
            if not path.exists():
                logger.error(f"Файл не найден: {path}")
                return

        # Подпись только для первого фото
        caption = (
            "🔥 *Установка котлов и бойлеров — надёжное тепло в доме*\n\n"
            "*Неправильная установка оборудования приводит к поломкам, авариям и лишним расходам.*\n\n"
            "Мы устанавливаем котлы и бойлеры — точно, безопасно, с гарантией.\n"
            "🛠️ Подключение к системе отопления и водоснабжения, настройка и пуск под ключ.\n"
            "⚡ Оптимальная работа и долгий срок службы оборудования.\n"
            "👉 Забудьте про перебои с горячей водой и отоплением — всё будет работать без проблем.\n"
            "📩 Свяжитесь с нами — монтаж и настройка за 1 день."
        )

        media = []
        for i, path in enumerate(file_paths):
            if i == 0:
                media.append(
                    InputMediaPhoto(
                        media=FSInputFile(path),
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=projects_kb
                    )
                )
            else:
                media.append(InputMediaPhoto(media=FSInputFile(path)))

        await bot.send_media_group(chat_id=message.chat.id, media=media)

    except Exception as e:
        # Логируем другие ошибки с полной информацией
        logger.error(
            f"Unexpected error in services callback for user {message.from_user.id}: {e}",
            exc_info=True
        )


@router.message(F.text == "В начало")
async def main_callback(message: Message):
    await message.delete()
    await start(message)