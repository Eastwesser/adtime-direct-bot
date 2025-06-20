import os

from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from dotenv import load_dotenv

from keyboards.inline_keyboards.info_kb import build_info_kb
from keyboards.on_start import (
    ButtonText,
    get_on_start_kb,
    get_on_help_kb,
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


@router.message(F.text == ButtonText.WHATS_NEXT)
@router.message(Command("help", prefix="!/"))
async def handle_help(message: types.Message):
    text = markdown.text(
        markdown.markdown_decoration.quote("Let's see what we can do!"),
        markdown.text(
            "Send me",
            markdown.markdown_decoration.bold(
                markdown.text(
                    markdown.underline("literally"),
                    "any",
                ),
            ),
            markdown.markdown_decoration.quote("message!"),
        ),
        sep="\n",
    )
    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=get_on_help_kb()
    )


@router.message(Command("more", prefix="!/"))
async def handle_more(message: types.Message):
    markup = get_actions_kb()
    await message.answer(
        text="Choose action",
        reply_markup=markup,
    )


@router.message(Command("info", prefix="!/"))
async def handle_info_command(message: types.Message):
    markup = build_info_kb()
    await message.answer(
        text="Ссылки и прочие ресурсы:",
        reply_markup=markup,
    )
