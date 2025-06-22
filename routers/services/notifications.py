from aiogram import Bot

from config import settings


async def notify_admin(bot: Bot, user_id: int, ticket_number: str, order_type: str, description: str):
    if description is None:
        description = "Не указано"
    message = (
        f"📌 Новый заказ!\n"
        f"Тип: {order_type}\n"
        f"Номер: {ticket_number}\n"
        f"Пользователь: {user_id}\n"
        f"Описание: {description}"
    )

    for admin_id in settings.admin_ids:
        try:
            await bot.send_message(admin_id, message)
        except Exception as e:
            print(f"Error sending to admin {admin_id}: {e}")
