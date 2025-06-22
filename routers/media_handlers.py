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

    # Отправляем админам
    for admin_id in settings.admin_ids:
        try:
            await bot.send_photo(
                admin_id,
                photo.file_id,
                caption=f"📸 Новый заказ с фото!\n"
                        f"Номер: {ticket_number}\n"
                        f"Описание: {caption}\n"
                        f"От: @{message.from_user.username}"
            )
        except Exception as e:
            print(f"Error sending to admin: {e}")

    # Ответ пользователю
    await message.answer(
        f"✅ Фото с описанием принято!\n"
        f"Номер заявки: {ticket_number}"
    )

    # Возвращаем в главное меню
    await state.set_state(MainStates.main_menu)
