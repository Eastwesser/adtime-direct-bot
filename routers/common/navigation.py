from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.on_start import get_on_start_kb
from ..common.states import MainStates

router = Router(name=__name__)


@router.message(F.text == "Назад")
async def back_to_main(message: Message, state: FSMContext):
    await state.set_state(MainStates.main_menu)
    await message.answer(
        text="Возвращаемся в главное меню",
        reply_markup=get_on_start_kb(),
        parse_mode="HTML"
    )
