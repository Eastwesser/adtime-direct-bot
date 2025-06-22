import logging
import ssl
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web

from config import settings
from routers import main_router as router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(
    settings.bot_token,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()
dp.include_router(router)


async def on_startup(app):
    webhook_url = f"https://{settings.webhook_domain}{settings.webhook_path}"
    await bot.set_webhook(
        url=webhook_url,
        certificate=open(settings.ssl_cert_path, 'rb') if settings.ssl_cert_path else None,
        drop_pending_updates=True
    )
    logger.info(f"Webhook set to: {webhook_url}")


app = web.Application()
app.on_startup.append(on_startup)

webhook_handler = SimpleRequestHandler(dp, bot)
webhook_handler.register(app, path=settings.webhook_path)

if __name__ == '__main__':
    context = None
    if settings.ssl_cert_path and settings.ssl_key_path:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(settings.ssl_cert_path, settings.ssl_key_path)

    web.run_app(
        app,
        host=settings.webhook_host,
        port=settings.webhook_port,
        ssl_context=context
    )
