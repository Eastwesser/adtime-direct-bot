import os
import re

from aiogram import (
    types,
    Dispatcher,
    Router,
    Bot,
)
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils import markdown
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

bot_token = os.getenv('BOT_TOKEN')
load_dotenv()

bot = Bot(token=bot_token)
dp = Dispatcher()

router = Router(name=__name__)


@router.message(Command("code", prefix="/!%"))
async def handle_command_code(message: types.Message):
    text = markdown.text(
        "Here's Python code:",
        "",
        markdown.markdown_decoration.pre_language(
            markdown.text("def is_palindrome(word):",
                          "    # Remove spaces and convert to lowercase",
                          "    word = word.lower().replace(' ', '')",
                          "    # Check if the string is a palindrome",
                          "    return word == word[::-1]",
                          "",
                          "# Example usage:",
                          'word = "level"',
                          "print(is_palindrome(word))  # Output: True",
                          sep="\n",
                          ),
            language="python",
        ),
        "And here's some JS:",
        "",
        markdown.markdown_decoration.pre_language(
            markdown.text('function isPalindrome(word) {',
                          '    // Remove spaces and convert to lowercase',
                          '    word = word.toLowerCase().replace(" ", "");',
                          '    // Check if the string is a palindrome',
                          '    return word === word.split("").reverse().join("");',
                          '}',
                          '',
                          '// Example usage:',
                          'let word = "level";',
                          'console.log(isPalindrome(word)); // Output: True',
                          sep="\n",
                          ),
            language="javascript",
        ),
        sep="\n",
    )
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)


# TASTY FOOD SHOP ======================================================================================================

# TODO: ПРИМЕР МАГАЗИНА
def create_inline_keyboard(options):
    keyboard = InlineKeyboardBuilder()
    for option in options:
        keyboard.row(types.InlineKeyboardButton(text=option, callback_data=option))
    return keyboard.as_markup()


# Email validation regex pattern
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Phone number validation regex pattern
PHONE_REGEX = r'^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$'

available_food_names = ["Суши", "Спагетти", "Хачапури"]
available_food_sizes = ["Маленькую", "Среднюю", "Большую"]
available_drink_names = ["Чай", "Кофе", "Сок"]

user_data = {}


class OrderStates(StatesGroup):
    waiting_for_food_choice = State()
    waiting_for_food_size = State()
    waiting_for_drink_choice = State()
    waiting_for_additional_choice = State()
    waiting_for_contact_info = State()


def calculate_total_price(chosen_food: str, chosen_drink: str = None) -> int:
    """
    Calculate the total price of the order based on the selected food and drink items.

    Args:
        chosen_food (str): The chosen food item.
        chosen_drink (str, optional): The chosen drink item. Defaults to None if no drink is chosen.

    Returns:
        int: The total price of the order.
    """
    food_prices = {
        "Суши": 300,
        "Спагетти": 250,
        "Хачапури": 200,
    }

    drink_prices = {
        "Чай": 100,
        "Кофе": 150,
        "Сок": 120,
    }

    total_price = food_prices.get(chosen_food, 0)

    if chosen_drink:
        total_price += drink_prices.get(chosen_drink, 0)

    return total_price


def validate_email(email: str) -> bool:
    """
    Validate the email address format using regex.
    """
    return bool(re.match(EMAIL_REGEX, email))


def validate_phone(phone: str) -> bool:
    """
    Validate the phone number format using regex.
    """
    return bool(re.match(PHONE_REGEX, phone))


@router.message(Command("food"))
async def cmd_food(message: types.Message, state: FSMContext):
    await state.set_state(OrderStates.waiting_for_food_choice)
    await message.answer(
        text="Выберите блюдо:",
        reply_markup=create_inline_keyboard(available_food_names)
    )


@router.callback_query(StateFilter(OrderStates.waiting_for_food_choice))
async def process_food_choice(callback: types.CallbackQuery, state: FSMContext):
    chosen_food = callback.data
    await state.update_data(chosen_food=chosen_food)
    await state.set_state(OrderStates.waiting_for_food_size)
    await callback.message.edit_text(
        text=f"Вы выбрали {chosen_food}. Теперь выберите размер порции:",
        reply_markup=create_inline_keyboard(available_food_sizes)
    )


@router.callback_query(StateFilter(OrderStates.waiting_for_food_size))
async def process_food_size(callback: types.CallbackQuery, state: FSMContext):
    chosen_food_size = callback.data
    chosen_food = (await state.get_data()).get('chosen_food')
    await state.set_state(OrderStates.waiting_for_drink_choice)
    await callback.message.edit_text(
        text=f"Вы выбрали {chosen_food_size} порцию {chosen_food}. Теперь выберите напиток:",
        reply_markup=create_inline_keyboard(available_drink_names)
    )


@router.message(Command("drinks"), StateFilter(OrderStates.waiting_for_drink_choice))
async def cmd_drinks(message: types.Message, state: FSMContext):
    await message.answer(
        text="Выберите напиток:",
        reply_markup=create_inline_keyboard(available_drink_names)
    )


@router.callback_query(StateFilter(OrderStates.waiting_for_drink_choice))
async def process_drink_choice(callback: types.CallbackQuery, state: FSMContext):
    chosen_drink = callback.data
    await state.update_data(chosen_drink=chosen_drink)
    await state.set_state(OrderStates.waiting_for_additional_choice)
    await callback.message.edit_text(
        text=f"Вы выбрали напиток {chosen_drink}. Что-нибудь еще?",
        reply_markup=create_inline_keyboard(["Добавить порцию", "Да, всё"])
    )


@router.callback_query(StateFilter(OrderStates.waiting_for_additional_choice))
async def process_additional_choice(callback: types.CallbackQuery, state: FSMContext):
    choice = callback.data
    if choice == "Добавить порцию":
        await state.set_state(OrderStates.waiting_for_food_choice)
        await callback.message.edit_text(
            text="Выберите блюдо:",
            reply_markup=create_inline_keyboard(available_food_names)
        )
    elif choice == "Да, всё":
        data = await state.get_data()
        chosen_food = data.get("chosen_food")
        chosen_drink = data.get("chosen_drink")
        total_price = calculate_total_price(chosen_food, chosen_drink)
        order_summary = (
            f"Ваш заказ:\n\n"
            f"- Блюдо: {chosen_food}\n"
            f"- Напиток: {chosen_drink or 'Нет'}\n"
            f"Общая стоимость: {total_price} руб.\n\n"
            "Введите ваше имя и фамилию, адрес электронной почты и номер телефона для связи:"
        )
        await callback.message.edit_text(text=order_summary)
        await state.set_state(OrderStates.waiting_for_contact_info)


@router.message(StateFilter(OrderStates.waiting_for_contact_info))
async def handle_contact_info(message: types.Message, state: FSMContext):
    await message.answer(
        text="Благодарим за заказ. Мы свяжемся с вами в ближайшее время!",
        reply_markup=create_inline_keyboard(available_drink_names)
    )
    await state.clear()


@router.message(StateFilter(OrderStates.waiting_for_contact_info))
async def handle_contact_info(message: types.Message, state: FSMContext):
    contact_info = message.text.split("\n")
    if len(contact_info) == 3:
        name, email, phone = contact_info
        if validate_email(email) and validate_phone(phone):
            await state.update_data(contact_info={"name": name, "email": email, "phone": phone})
            await message.answer("Спасибо за ваш заказ! Мы свяжемся с вами в ближайшее время.\n"
                                 "Вы можете продолжить далее, выбрав напиток.")
            await state.clear()
        else:
            await message.answer(
                "Неверный формат электронной почты или номера телефона. Пожалуйста, попробуйте еще раз.")
    else:
        await message.answer(
            "Пожалуйста, введите ваше имя, адрес электронной почты и номер телефона в следующем формате:\n\n"
            "Имя Фамилия\n"
            "example@example.com\n"
            "+7(XXX)XXX-XX-XX"
        )
