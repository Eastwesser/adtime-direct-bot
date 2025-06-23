from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import settings
from keyboards.on_start import get_on_start_kb
from routers.commands.basic_commands import logger
from routers.common.states import MainStates
from routers.services.tickets import generate_ticket_number

router = Router(name=__name__)


@router.message(F.photo)
async def handle_photo(message: Message, state: FSMContext, bot: Bot):
    # Получаем информацию о фото
    photo = message.photo[-1]
    caption = message.caption or "Без описания"

    # Генерируем номер заявки
    ticket_number = generate_ticket_number()

    # Определяем тип заказа из текущего состояния
    current_state = await state.get_state()
    order_type = "unknown"
    if current_state == MainStates.leather:
        order_type = "leather"
    elif current_state == MainStates.stickers:
        order_type = "stickers"
    elif current_state == MainStates.typography:
        order_type = "typography"
    elif current_state == MainStates.other:
        order_type = "other"

    # Формируем информацию о пользователе
    username = f"@{message.from_user.username}" \
        if message.from_user.username \
        else f"{message.from_user.full_name} (ID: {message.from_user.id})"

    admin_caption = (
        f"📸 Новый заказ с фото!\n"
        f"Тип: {order_type}\n"
        f"Номер: {ticket_number}\n"
        f"Описание: {caption}\n"
        f"От: {username}"
    )

    # Отправляем админам
    for admin_id in settings.admin_ids:
        try:
            await bot.send_photo(
                admin_id,
                photo.file_id,
                caption=admin_caption
            )
        except Exception as e:
            logger.error(f"Error sending to admin {admin_id}: {e}")

    # Ответ пользователю
    await message.answer(
        f"✅ Заказ оформлен!\n"
        f"Номер: {ticket_number}\n"
        f"Статус: https://atdart.online/order/{ticket_number}\n"
        f"Тип: {order_type}\n"
        f"Описание: {caption}\n\n"
        "Спасибо! Администратор свяжется с вами в ближайшее время.",
        reply_markup=get_on_start_kb()
    )

    # Возвращаем в главное меню
    await state.clear()
    await state.set_state(MainStates.main_menu)
