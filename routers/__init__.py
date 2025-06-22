from aiogram import Router

# Импортируем все роутеры
from routers import common
from routers.admin_handlers import router as admin_router
from routers.adtime_direct_custom.adtime_direct_kandinskiy import router as photobot_router
from routers.callback_handlers import router as callback_router
from routers.commands import router as commands_router
from routers.media_handlers import router as media_router
from routers.usecases.leather import router as leather_router
from routers.usecases.other import router as other_router
from routers.usecases.stickers import router as stickers_router
from routers.usecases.typography import router as typography_router

# Основной роутер
main_router = Router(name="main_router")

# Включаем все роутеры
main_router.include_routers(
    commands_router,
    callback_router,
    admin_router,
    media_router,
    stickers_router,
    leather_router,
    typography_router,
    other_router,
    photobot_router,
    common.router  # Добавьте этот роутер, если его нет
)

__all__ = ("main_router",)
