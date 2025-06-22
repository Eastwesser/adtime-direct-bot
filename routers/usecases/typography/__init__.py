from aiogram import Router

from .handlers import router as handlers_router

router = Router(name="typography_router")
router.include_router(handlers_router)

__all__ = ("router",)
