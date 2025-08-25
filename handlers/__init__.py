from handlers.start_hendler import router as start_router
from handlers.services_handler import router as about_router
from handlers.prices_handler import router as prices_router
from handlers.callback_web_app_data_handler import router as callback_web_app_router

__all__ = ["start_router", "about_router", "prices_router", "callback_web_app_router"]