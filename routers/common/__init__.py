from aiogram import Router

from .navigation import router as nav_router

router = Router(name=__name__)
router.include_router(nav_router)

__all__ = ("router",)
