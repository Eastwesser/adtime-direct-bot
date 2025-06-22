from aiogram import Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()  # Создаем роутер


def get_leather_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Назад")],
            [KeyboardButton(text="Сгенерировать изображение")]
        ],
        resize_keyboard=True
    )


__all__ = ['router', 'get_leather_kb']
