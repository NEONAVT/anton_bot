from aiogram import types, Router, F
from aiogram.filters import CommandStart
from keyboards import start_kb

router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    try:
        await message.answer(
            text=(
                f"Добрый день, {message.from_user.first_name}!\n\n"
                f"Мы помогаем с заменой и установкой газовых котлов, колонок, бойлеров, "
                f"а также с монтажом систем отопления и водоснабжения с нуля.\n\n"
                f"Звонки принимаются с 8:00 до 10:00. В остальное время мы занимаемся выполнением заказов, "
                f"чтобы всё было сделано качественно и в срок.\n\n"
                f"Вы можете быстро узнать о наших услугах, ориентировочную стоимость или заказать обратный звонок — "
                f"с вами свяжутся в ближайшее время.\n\n"
                f"Для получения информации воспользуйтесь кнопками ниже."
            )
            ,
            reply_markup=start_kb
        )
    except Exception as e:
        # Обработка ошибок через логирование или сервис
        print(f"Ошибка при отправке сообщения: {e}")
