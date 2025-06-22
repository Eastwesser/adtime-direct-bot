from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.on_start import get_on_start_kb
from routers.common.states import MainStates


class NavigationCore:
    @staticmethod
    async def handle_back(message: Message, state: FSMContext):
        data = await state.get_data()
        history = data.get("state_history", [])

        if not history:
            await state.set_state(MainStates.main_menu)
            await message.answer("Вы в главном меню", reply_markup=get_on_start_kb())
            return None

        previous_state = history.pop()
        await state.set_state(previous_state)
        await state.update_data(state_history=history)
        return previous_state

    @staticmethod
    async def add_to_history(state: FSMContext, current_state: str):
        data = await state.get_data()
        history = data.get("state_history", [])
        history.append(current_state)
        await state.update_data(state_history=history)
