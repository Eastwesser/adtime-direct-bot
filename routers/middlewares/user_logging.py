from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Update


class UserLoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data):
        user = event.event.from_user
        state = data.get("state")

        if state:
            state_data = await state.get_data()
            state_data.setdefault("user_path", [])
            state_data["user_path"].append(handler.__name__)
            await state.set_data(state_data)

        return await handler(event, data)
