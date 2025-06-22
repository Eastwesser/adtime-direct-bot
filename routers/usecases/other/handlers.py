import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.on_start import ButtonText
from routers.common.states import MainStates
from routers.services.tickets import generate_ticket_number
from .keyboards import get_other_kb

router = Router()
logger = logging.getLogger(__name__)


@router.message(StateFilter(MainStates.main_menu), F.text == ButtonText.OTHERCASE)
async def handle_other(message: Message, state: FSMContext):
    current_state = await state.get_state()
    logger.info(f"OTHER pressed. Current state: {current_state}")

    if current_state != MainStates.main_menu:
        await message.answer("Пожалуйста, вернитесь в главное меню (/start)")
        return

    logger.info(f"Handling other button, current state: {await state.get_state()}")
    await state.set_state(MainStates.other)
    await message.answer(
        text="Что бы вы хотели заказать? Можете прислать фото или описать текстом.\n"
             "Если возникли трудности, можете воспользоваться нашим ботом для вдохновения /start_kandinsky",
        reply_markup=get_other_kb()
    )


@router.message(MainStates.other)
async def process_other_order(message: Message, state: FSMContext):
    # Здесь логика обработки заказа
    ticket_number = generate_ticket_number()
    await message.answer(
        f"Отлично! Ваш номер заявки: {ticket_number}\n"
        f"Вы можете отслеживать статус на сайте: https://atdart.online/order/{ticket_number}"
    )
    await state.update_data(ticket_number=ticket_number)
    await message.answer("Отлично, наш администратор свяжется с вами в ближайшее время!")
    await state.set_state(MainStates.main_menu)
