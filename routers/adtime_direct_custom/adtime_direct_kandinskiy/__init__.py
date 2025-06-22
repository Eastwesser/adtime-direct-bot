from aiogram import Router

from . import kandinsky

router = Router()

router.include_router(kandinsky.router)
