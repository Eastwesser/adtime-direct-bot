import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.on_start import ButtonText, get_on_start_kb
from routers.common.states import MainStates
from routers.navigation.back_handler import handle_back_button
from routers.services.tickets import generate_ticket_number
from ...navigation.core import NavigationCore
from ...navigation.state_keyboards import get_keyboard_for_state
from ...services.notifications import notify_admin

router = Router()
logger = logging.getLogger(__name__)


@router.message(StateFilter(MainStates.main_menu), F.text == ButtonText.LEATHER)
async def handle_leather(message: Message, state: FSMContext):
    # Сохраняем текущее состояние в историю
    await NavigationCore.add_to_history(state, await state.get_state())

    # Переходим в новое состояние
    await state.set_state(MainStates.leather)
    await message.answer(
        "Какие изделия из кожи вы бы хотели заказать? "
        "Можете прислать фото или описать текстом.\n"
        "Для вдохновения используйте /start_kandinsky",
        reply_markup=get_keyboard_for_state(MainStates.leather)
    )


@router.message(MainStates.leather)
async def process_leather_order(message: Message, state: FSMContext):
    if message.text == ButtonText.BACK:
        return await handle_back_button(message, state)

    # Если это фото с текстом - пропускаем (обрабатывается медиа-хендлером)
    if message.photo and message.caption:
        return

    ticket_number = generate_ticket_number()

    # Сохраняем данные заказа
    await state.update_data(
        ticket_number=ticket_number,
        order_type="leather",
        description=message.text
    )

    # await message.answer(
    #     f"✅ Заказ оформлен!\n"
    #     f"Номер: {ticket_number}\n"
    #     f"Статус: https://atdart.online/order/{ticket_number}"
    # )

    # Здесь должна быть отправка данных админу
    await notify_admin(
        bot=message.bot,
        user_id=message.from_user.id,
        ticket_number=ticket_number,
        order_type="leather",
        description=message.text,
        message=message,
    )

    # Ответ пользователю (одно сообщение вместо двух)
    await message.answer(
        f"✅ Заказ оформлен!\n"
        f"Номер: {ticket_number}\n"
        f"Статус: https://atdart.online/order/{ticket_number}\n\n"
        "Спасибо! Администратор свяжется с вами в ближайшее время.",
        reply_markup=get_on_start_kb()
    )
    await state.clear()
    await state.set_state(MainStates.main_menu)
