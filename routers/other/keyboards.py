from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_other_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Назад")],
            [KeyboardButton(text="Сгенерировать изображение")]
        ],
        resize_keyboard=True
    )
