from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.on_start import ButtonText
from .keyboards import get_leather_kb
from ..common.states import MainStates
from ..services.tickets import generate_ticket_number

router = Router()


@router.message(F.text == ButtonText.LEATHER, MainStates.main_menu)
async def handle_leather(message: Message, state: FSMContext):
    await state.set_state(MainStates.leather)
    await message.answer(
        text="Какие изделия из кожи вы бы хотели заказать? Можете прислать фото или описать текстом.\n"
             "Если возникли трудности, можете воспользоваться нашим ботом для вдохновения /start_kandinsky",
        reply_markup=get_leather_kb()
    )


@router.message(MainStates.leather)
async def process_leather_order(message: Message, state: FSMContext):
    # Здесь логика обработки заказа
    ticket_number = generate_ticket_number()
    await message.answer(
        f"Отлично! Ваш номер заявки: {ticket_number}\n"
        f"Вы можете отслеживать статус на сайте: https://atdart.online/order/{ticket_number}"
    )
    await state.update_data(ticket_number=ticket_number)
    await message.answer("Отлично, наш администратор свяжется с вами в ближайшее время!")
    await state.set_state(MainStates.main_menu)
