import logging

from bot_config import bot, dp
import asyncio
from handlers import (start_router,
                      services_router,
                      prices_router,
                      web_app_data_router,
                      projecs_router,
                      about_router
                      )

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # уровень логирования: INFO, DEBUG, WARNING, ERROR
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    dp.include_router(start_router)
    dp.include_router(services_router)
    dp.include_router(prices_router)
    dp.include_router(web_app_data_router)
    dp.include_router(projecs_router)
    dp.include_router(about_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
