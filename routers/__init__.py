__all__ = ("router",)  # THIS IS THE MAIN ROUTER

from aiogram import Router

from .admin_handlers import router as admin_router
from .adtime_direct_custom.adtime_direct_kandinskiy import router as photobot_router
from .callback_handlers import router as callback_router
from .commands import router as commands_router
from .common import router as common_router
from .common.navigation import router as nav_router
from .leather import router as leather_router
from .media_handlers import router as media_router
from .other import router as other_router
from .stickers import router as stickers_router
from .typography import router as typography_router

router = Router(name=__name__)

router.include_routers(callback_router,
                       commands_router,
                       photobot_router,
                       media_router,
                       nav_router,
                       stickers_router,
                       leather_router,
                       typography_router,
                       other_router,
                       # add your router here (if you want)
                       admin_router,
                       )

# the router below has to be the final, echo-bot command!!!
router.include_router(common_router)  # THIS ECHO BOT MUST BE THE LAST!!!
