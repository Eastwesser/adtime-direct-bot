from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.on_start import get_on_start_kb, ButtonText
from routers.common.states import MainStates

router = Router(name=__name__)


@router.message(StateFilter(), F.text == ButtonText.BACK)
async def handle_back_button(message: Message, state: FSMContext):
    await state.set_state(MainStates.main_menu)
    await message.answer("Возвращаемся в главное меню", reply_markup=get_on_start_kb())
