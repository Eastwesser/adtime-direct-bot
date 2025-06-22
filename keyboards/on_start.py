from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class ButtonText:
    LEATHER = "Аксессуары из кожи"
    STICKERS = "Наклейки"
    TYPOGRAPHY = "Открытки"
    OTHERCASE = "Другое..."
    KANDINSKY = "Сгенерировать изображение"  # /start_kandinsky
    BACK = "Назад"


def get_on_start_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=ButtonText.LEATHER), KeyboardButton(text=ButtonText.STICKERS)],
            [KeyboardButton(text=ButtonText.TYPOGRAPHY), KeyboardButton(text=ButtonText.OTHERCASE)],
            [KeyboardButton(text=ButtonText.KANDINSKY)],
        ],
        resize_keyboard=True,
    )
