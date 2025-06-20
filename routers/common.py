from aiogram import F, Router, types
from aiogram.enums import ChatAction
from aiogram.types import ReplyKeyboardRemove

from keyboards.on_start import (
    ButtonText,
)

router = Router(name=__name__)


@router.message(F.text == ButtonText.HELLO)
async def handle_hello_message(message: types.Message):
    await message.answer(
        text="Привет еще раз! Пожалуйста, выбери то, что хочешь заказать!",
        reply_markup=ReplyKeyboardRemove(),
        one_time_keyboard=True
    )


@router.message(F.text == ButtonText.BYE)
async def handle_bye_message(message: types.Message):
    await message.answer(
        text="See you later! Click /start any time! :3",
        reply_markup=ReplyKeyboardRemove(),
        one_time_keyboard=True
    )


# ECHO BOT
@router.message()
async def echo_message(message: types.Message):
    if message.poll:
        await message.forward(chat_id=message.chat.id)
        return
    await message.answer(
        text="Погоди-ка...",
        parse_mode=None,
    )

    if message.sticker:
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.CHOOSE_STICKER,
        )
    try:
        await message.copy_to(chat_id=message.chat.id)

    except TypeError:
        await message.reply(text="Something new!!! Thanks 🙂")
