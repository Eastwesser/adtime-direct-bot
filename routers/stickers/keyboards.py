from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_stickers_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Назад")],
            [KeyboardButton(text="Сгенерировать изображение")]
        ],
        resize_keyboard=True
    )
