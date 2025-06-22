from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import settings
from routers.common.states import MainStates
from routers.services.tickets import generate_ticket_number

router = Router(name=__name__)


@router.message(F.photo & F.caption)
async def handle_photo_with_caption(message: Message, state: FSMContext, bot: Bot):
    # Получаем информацию о фото
    photo = message.photo[-1]
    caption = message.caption

    # Генерируем номер заявки
    ticket_number = generate_ticket_number()

    # Формируем информацию о пользователе
    username = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
    admin_caption = (
        f"📸 Новый заказ с фото!\n"
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
            print(f"Error sending to admin {admin_id}: {e}")

    # Ответ пользователю
    from keyboards.on_start import get_on_start_kb
    await message.answer(
        f"✅ Фото с описанием принято!\nНомер заявки: {ticket_number}",
        reply_markup=get_on_start_kb()
    )

    # Возвращаем в главное меню
    await state.clear()
    await state.set_state(MainStates.main_menu)
