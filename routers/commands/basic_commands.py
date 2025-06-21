import os

from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils import markdown
from dotenv import load_dotenv

from keyboards.on_start import (
    get_on_start_kb,
)

bot_token = os.getenv('BOT_TOKEN')

load_dotenv()

router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: types.Message):
    welcome_sticker_id = "CAACAgIAAxkBAg_ve2hVrnrix_zqwZ0hFwOa_PIpI5o4AAKXeQACdWSwSoZqs8snryMWNgQ"
    await message.answer_sticker(sticker=welcome_sticker_id)

    await message.answer(
        text=f"{markdown.hide_link(welcome_sticker_id)}Привет, я - AdTime Direct Bot!\n"
             f"Что бы вы хотели заказать?",
        parse_mode=ParseMode.HTML,
        reply_markup=get_on_start_kb(),
    )
