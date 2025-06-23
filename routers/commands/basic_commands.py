import logging

from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from keyboards.on_start import get_on_start_kb
from routers.common.states import MainStates

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):
    logger.info("CommandStart received")
    await state.set_state(MainStates.main_menu)
    logger.info(f"State set to: {await state.get_state()}")
    await message.answer_sticker("CAACAgIAAxkBAg_ve2hVrnrix_zqwZ0hFwOa_PIpI5o4AAKXeQACdWSwSoZqs8snryMWNgQ")
    await message.answer(
        text="Привет, я - AdTime Direct Bot!\nЧто бы вы хотели заказать?",
        reply_markup=get_on_start_kb(),
    )


ABOUT_TEXT = """
AdTime Direct Bot

🎨 Заказывайте изделия из кожи, стикеры и открытки через бота!
✨ Генерация уникальных изображений с помощью нейросети Kandinsky

Команды:
/start - Главное меню
/start_kandinsky - Генерация изображений
/about - Обо мне

Что можно заказать:
💼 Кожаные аксессуары (кошельки, обложки, ремни)
🎫 Виниловые наклейки любого дизайна
🔖 Поздравительные открытки и полиграфию

Как работать с ботом:
🔹 Выберите тип товара
🔹 Опишите что вам нужно или отправьте пример
🔹 Для вдохновения создайте изображение через Kandinsky
🔹 Оформите заказ - мы свяжемся с вами!

Генерация изображений:
🖼 Превращайте текстовые описания в картинки
🔄 Можно перегенерировать результат
📤 Отправляйте понравившиеся варианты администратору
"""


@router.message(Command("about"))
async def handle_about(message: types.Message):
    await message.answer(ABOUT_TEXT)
