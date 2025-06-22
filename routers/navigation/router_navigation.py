from aiogram import Router

from .back_handler import router as back_router

router = Router(name=__name__)
router.include_router(back_router)
