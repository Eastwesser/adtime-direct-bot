from aiogram import Bot
from aiogram.types import Message

from config import settings


async def notify_admin(bot: Bot, user_id: int, ticket_number: str, order_type: str, description: str,
                       message: Message = None):
    if description is None:
        description = "Не указано"

    # Формируем информацию о пользователе
    user_info = f"ID: {user_id}"
    if message and message.from_user.username:
        user_info = f"@{message.from_user.username} (ID: {user_id})"
    elif message and message.from_user.full_name:
        user_info = f"{message.from_user.full_name} (ID: {user_id})"

    notification_text = (
        f"📌 Новый заказ!\n"
        f"Тип: {order_type}\n"
        f"Номер: {ticket_number}\n"
        f"Пользователь: {user_info}\n"
        f"Описание: {description}"
    )

    for admin_id in settings.admin_ids:
        try:
            await bot.send_message(admin_id, notification_text)
        except Exception as e:
            print(f"Error sending to admin {admin_id}: {e}")
