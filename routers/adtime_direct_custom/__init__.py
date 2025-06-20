from aiogram import Router

router = Router(name=__name__)


def include_photobot_router():
    from .adtime_direct_kandinskiy import router as photobot_router
    router.include_router(photobot_router)
