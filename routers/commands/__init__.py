__all__ = ("router",)  # Is needed for commands package

from aiogram import Router

from .basic_commands import router as base_commands_router

router = Router(name=__name__)

router.include_routers(
    base_commands_router,
)
