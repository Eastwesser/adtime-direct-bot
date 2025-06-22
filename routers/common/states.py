from aiogram.fsm.state import StatesGroup, State


class MainStates(StatesGroup):
    main_menu = State()
    leather = State()
    stickers = State()
    typography = State()
    other = State()
    kandinsky = State()
