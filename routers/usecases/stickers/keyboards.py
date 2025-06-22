from aiogram import Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()  # Создаем роутер


def get_stickers_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Назад")],
            [KeyboardButton(text="Сгенерировать изображение")]
        ],
        resize_keyboard=True
    )


__all__ = ['router', 'get_stickers_kb']  # Явно указываем экспортируемые объекты
