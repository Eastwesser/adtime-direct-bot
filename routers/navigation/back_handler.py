from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.on_start import get_on_start_kb
from routers.common.states import MainStates
from routers.navigation.state_keyboards import get_keyboard_for_state

router = Router(name=__name__)


@router.message(F.text == "Назад")
async def handle_back_button(message: Message, state: FSMContext):
    current_state = await state.get_state()
    data = await state.get_data()
    history = data.get("state_history", [])

    # Если уже в главном меню
    if current_state == MainStates.main_menu:
        await message.answer("Вы уже в главном меню")
        return

    # Если история состояний пустая или мы в состоянии Kandinsky
    if not history or current_state.startswith("KandinskyStates"):
        await state.clear()
        await state.set_state(MainStates.main_menu)
        await message.answer("Вы в главном меню", reply_markup=get_on_start_kb())
        return

    # Возврат к предыдущему состоянию из истории
    previous_state = history.pop()
    await state.set_state(previous_state)
    await state.update_data(state_history=history)

    keyboard = get_keyboard_for_state(previous_state)
    await message.answer("⬅️ Возврат назад", reply_markup=keyboard)
