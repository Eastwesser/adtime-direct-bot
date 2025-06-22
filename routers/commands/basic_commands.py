import logging

from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.on_start import get_on_start_kb
from routers.common.states import MainStates

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):
    logger.info("CommandStart received")
    await state.set_state(MainStates.main_menu)
    logger.info(f"State set to: {await state.get_state()}")
    await message.answer_sticker("CAACAgIAAxkBAg_ve2hVrnrix_zqwZ0hFwOa_PIpI5o4AAKXeQACdWSwSoZqs8snryMWNgQ")
    await message.answer(
        text="Привет, я - AdTime Direct Bot!\nЧто бы вы хотели заказать?",
        reply_markup=get_on_start_kb(),
    )
