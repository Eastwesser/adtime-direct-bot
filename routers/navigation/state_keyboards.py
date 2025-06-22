from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from routers.common.states import MainStates


def get_keyboard_for_state(state: str):
    if state == MainStates.main_menu:
        from keyboards.on_start import get_on_start_kb
        return get_on_start_kb()

    # Ленивая загрузка клавиатур
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )

    if state in [MainStates.leather, MainStates.stickers,
                 MainStates.typography, MainStates.other]:
        kb.keyboard.append([KeyboardButton(text="Сгенерировать изображение")])

    return kb
