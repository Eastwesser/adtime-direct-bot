from aiogram.fsm.state import StatesGroup, State


class MainStates(StatesGroup):
    main_menu = State()
    stickers = State()
    leather = State()
    typography = State()
    other = State()
