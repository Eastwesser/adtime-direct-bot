from aiogram import Router

from .handlers import router as handlers_router
from .keyboards import router as keyboards_router

router = Router(name=__name__)
router.include_router(handlers_router)
router.include_router(keyboards_router)

__all__ = ("router",)
