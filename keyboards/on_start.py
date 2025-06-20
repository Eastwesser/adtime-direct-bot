from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class ButtonText:
    HELLO = "Hello!"
    WHATS_NEXT = "What's next?"
    BYE = "Goodbye!"
    # Основные выборы услуг
    LEATHER = "Аксессуары из кожи"
    STICKERS = "Наклейки"
    TYPOGRAPHY = "Открытки"
    OTHERCASE = "Другое..."
    # Для рисования Кандинским
    KANDINSKY = "Сгенерировать изображение" # /start_kandinsky


def get_on_start_kb() -> ReplyKeyboardMarkup:
    button_hello = KeyboardButton(
        text=ButtonText.HELLO
    )
    button_help = KeyboardButton(
        text=ButtonText.WHATS_NEXT
    )
    button_bye = KeyboardButton(
        text=ButtonText.BYE
    )

    buttons_row_1 = [button_hello, button_help]
    buttons_row_2 = [button_bye]

    markup_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            buttons_row_1,
            buttons_row_2,
        ],
        resize_keyboard=True,
    )
    return markup_keyboard


def get_on_help_kb() -> ReplyKeyboardMarkup:
    button_leather_shop = KeyboardButton(
        text=ButtonText.LEATHER
    )
    button_sticker_shop = KeyboardButton(
        text=ButtonText.STICKERS
    )
    button_typography_shop = KeyboardButton(
        text=ButtonText.TYPOGRAPHY
    )
    button_other_shop = KeyboardButton(
        text=ButtonText.OTHERCASE
    )
    button_kandinsky = KeyboardButton(
        text=ButtonText.KANDINSKY
    )

    buttons_row_1 = [button_leather_shop, button_sticker_shop]
    buttons_row_2 = [button_typography_shop, button_other_shop]
    buttons_row_3 = [button_kandinsky]

    markup_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            buttons_row_1,
            buttons_row_2,
            buttons_row_3,
        ],
        resize_keyboard=True,
    )
    return markup_keyboard
