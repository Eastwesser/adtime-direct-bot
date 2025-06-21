from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web
import ssl

from config import settings
from routers import router

bot = Bot(settings.bot_token, parse_mode="HTML")
dp = Dispatcher()
dp.include_router(router)


async def on_startup(app):
    await bot.set_webhook(
        url=f"https://{settings.webhook_domain}/webhook",
        certificate=open(settings.ssl_cert_path, "rb"),
        drop_pending_updates=True
    )


app = web.Application()
app.on_startup.append(on_startup)

webhook_handler = SimpleRequestHandler(dp, bot)
webhook_handler.register(app, path="/webhook")

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(settings.ssl_cert_path, settings.ssl_key_path)

    web.run_app(
        app,
        host=settings.webhook_host,
        port=settings.webhook_port,
        ssl_context=context
    )
