from aiogram import Router

# Импортируем все роутеры
from routers.common import router as common_router
from routers.admin_handlers import router as admin_router
from routers.navigation.router_navigation import router as nav_router
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
    commands_router,    # /start и другие команды
    callback_router,    # inline-кнопки
    admin_router,       # админские команды
    photobot_router,    # Kandinsky
    media_router,       # обработка медиа
    stickers_router,    # наклейки
    leather_router,     # кожа
    typography_router,  # открытки
    other_router,       # другое
    nav_router,
    common.router       # общие хэндлеры (ДОЛЖЕН БЫТЬ ПОСЛЕДНИМ!)
)

__all__ = ("main_router",)
