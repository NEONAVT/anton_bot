from handlers.start_hendler import router as start_router
from handlers.services_handler import router as about_router
from handlers.prices_handler import router as prices_router
from handlers.web_app_data_handler import router as web_app_data_router

__all__ = ["start_router", "about_router", "prices_router", "web_app_data_router"]