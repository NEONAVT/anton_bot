from handlers.start_hendler import router as start_router
from handlers.services_handler import router as about_router
from handlers.prices_handler import router as prices_router

__all__ = ["start_router", "about_router", "prices_router"]