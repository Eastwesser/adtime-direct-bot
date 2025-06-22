from aiogram import Bot
from aiogram.types import Message

from config import settings
from routers.commands.basic_commands import logger


async def notify_admin(
        bot: Bot,
        user_id: int,
        ticket_number: str,
        order_type: str,
        description: str,
        message: Message = None,
):
    if description is None:
        description = "Не указано"

    # Формируем информацию о пользователе
    user_info = f"ID: {user_id}"
    if message:
        if message.from_user.username:
            user_info = f"@{message.from_user.username} (ID: {user_id})"
        elif message.from_user.full_name:
            user_info = f"{message.from_user.full_name} (ID: {user_id})"

    text = (
        f"📌 Новый заказ!\n"
        f"Тип: {order_type}\n"
        f"Номер: {ticket_number}\n"
        f"Пользователь: {user_info}\n"
        f"Описание: {description}"
    )

    for admin_id in settings.admin_ids:
        try:
            # Проверяем, существует ли чат
            chat = await bot.get_chat(admin_id)
            if chat:
                await bot.send_message(admin_id, text)
        except Exception as e:
            logger.error(f"Ошибка отправки админу {admin_id}: {e}")
