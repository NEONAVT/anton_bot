from bot_config import bot, dp
import asyncio
from handlers import start_router


async def main():
    dp.include_router(start_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())