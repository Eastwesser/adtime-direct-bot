import base64
import json
import logging
import os
import time

import requests
from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    Message, ReplyKeyboardMarkup, KeyboardButton,
    ReplyKeyboardRemove, BufferedInputFile
)
from dotenv import load_dotenv

from config import settings
from keyboards.on_start import ButtonText
from routers.common.states import MainStates

logger = logging.getLogger(__name__)
router = Router(name=__name__)

# Загрузка переменных окружения
load_dotenv()
FUSION_BRAIN_TOKEN = os.getenv('FUSION_BRAIN_TOKEN')
FB_KEY = os.getenv('FB_KEY')

# Добавляем логирование загруженных переменных
logger.info(f"FUSION_BRAIN_TOKEN loaded: {FUSION_BRAIN_TOKEN is not None}")
logger.info(f"FB_KEY loaded: {FB_KEY is not None}")


class KandinskyStates(StatesGroup):
    TextToImage = State()
    ReviewImage = State()


class Text2ImageAPI:
    def __init__(self, api_key, secret_key):
        self.API_URL = "https://api-key.fusionbrain.ai/"
        self.HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }
        logger.info(f"Initialized Text2ImageAPI with URL: {self.API_URL}")

    def get_pipeline(self):
        try:
            logger.info("Trying to get pipeline...")
            response = requests.get(
                f"{self.API_URL}key/api/v1/pipelines",
                headers=self.HEADERS,
                timeout=(10, 30)  # Таймаут на подключение и чтение
            )

            # Детальное логирование ответа
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response headers: {response.headers}")

            response.raise_for_status()
            data = response.json()
            logger.info(f"Pipelines response: {data}")

            if not data:
                logger.error("No pipelines available")
                return None

            return data[0]['id']

        except requests.exceptions.RequestException as e:
            # Детальное логирование ошибок requests
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"HTTP Error {e.response.status_code}: {e.response.text}")
            else:
                logger.error(f"Connection error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in get_pipeline: {str(e)}", exc_info=True)
            return None

    def generate(self, prompt, pipeline, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }

        try:
            logger.info(f"Generating image with prompt: {prompt}")
            response = requests.post(
                f"{self.API_URL}key/api/v1/pipeline/run",
                headers=self.HEADERS,
                files=data,
                timeout=(10, 30),
            )

            # Детальное логирование ответа
            logger.info(f"Generate response status: {response.status_code}")

            response.raise_for_status()
            data = response.json()
            logger.info(f"Generate response data: {data}")
            return data['uuid']

        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"HTTP Error {e.response.status_code}: {e.response.text}")
            else:
                logger.error(f"Connection error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in generate: {str(e)}", exc_info=True)
            return None

    def check_status(self, request_id, attempts=10, delay=3):  # Уменьшили delay с 10 до 3 сек
        while attempts > 0:
            try:
                logger.info(f"Checking status for request {request_id} (attempts left: {attempts})")

                response = requests.get(
                    f"{self.API_URL}key/api/v1/pipeline/status/{request_id}",
                    headers=self.HEADERS,
                    timeout=(3, 5),  # Таймаут подключения и чтения
                )

                # Детальное логирование ответа
                logger.info(f"Status check response: {response.status_code}")
                logger.debug(f"Status headers: {response.headers}")

                data = response.json()
                logger.info(f"Status data: {data}")

                if data['status'] == 'DONE':
                    logger.info("Generation completed successfully")
                    return data['result']['files'][0]
                elif data['status'] == 'FAIL':
                    error_desc = data.get('errorDescription', 'No error description')
                    logger.error(f"Generation failed: {error_desc}")
                    return None

                attempts -= 1
                time.sleep(delay)

            except requests.exceptions.RequestException as e:
                if hasattr(e, 'response') and e.response is not None:
                    logger.error(f"HTTP Error {e.response.status_code}: {e.response.text}")
                else:
                    logger.error(f"Connection error: {str(e)}")
                attempts -= 1
                time.sleep(delay)
            except Exception as e:
                logger.error(f"Unexpected error in check_status: {str(e)}", exc_info=True)
                attempts -= 1
                time.sleep(delay)

        logger.error("All attempts to check status failed")
        return None


def get_kandinsky_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Нарисовать картинку")],
            [KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )


def get_review_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить администратору")],
            [KeyboardButton(text="Сгенерировать заново")],
            [KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )


@router.message(F.text == ButtonText.KANDINSKY)
async def handle_kandinsky(message: types.Message):
    try:
        logger.info("Checking Kandinsky API availability...")
        test_response = requests.get(
            "https://api-key.fusionbrain.ai/key/api/v1/pipelines",
            headers={
                'X-Key': f'Key {FUSION_BRAIN_TOKEN}',
                'X-Secret': f'Secret {FB_KEY}',
            },
            timeout=10,
        )
        logger.info(f"API check response: {test_response.status_code}")
        if test_response.status_code == 200:
            logger.info("Kandinsky API is available")
            await message.answer("Для генерации изображений нажмите: /start_kandinsky")
        else:
            error_msg = f"API недоступен, статус: {test_response.status_code}"
            logger.error(error_msg)
            raise Exception(error_msg)
    except Exception as e:
        logger.error(f"Error checking Kandinsky API: {str(e)}", exc_info=True)
        await message.answer(
            "⚠️ Сервис генерации изображений временно недоступен\n"
            "Попробуйте позже или обратитесь к администратору"
        )


@router.message(Command("start_kandinsky"))
async def start_kandinsky(message: types.Message, state: FSMContext):
    await state.set_state(KandinskyStates.TextToImage)
    await message.answer(
        "Нажмите кнопку ниже, чтобы начать генерацию изображения:",
        reply_markup=get_kandinsky_keyboard()
    )


@router.message(F.text == "Нарисовать картинку", KandinskyStates.TextToImage)
async def request_prompt(message: Message, state: FSMContext):
    await message.answer(
        "Опишите, что вы хотите нарисовать:",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(KandinskyStates.TextToImage)
async def generate_image(message: Message, state: FSMContext):
    # Игнорируем только специфичные кнопки
    if message.text in ["Сгенерировать заново", "Отправить администратору"]:
        return

    # Если нажата кнопка "Назад" - выходим
    if message.text == "Назад":
        await state.clear()
        from keyboards.on_start import get_on_start_kb
        await message.answer(
            "Возвращаемся в главное меню",
            reply_markup=get_on_start_kb()
        )
        await state.set_state(MainStates.main_menu)
        return

    prompt = message.text
    if not prompt:
        await message.answer("Пожалуйста, введите описание для генерации изображения.")
        return

    await message.answer("🔄 Генерация изображения... Это может занять до 30 секунд.")

    api = Text2ImageAPI(FUSION_BRAIN_TOKEN, FB_KEY)
    pipeline_id = api.get_pipeline()
    if not pipeline_id:
        await message.answer("⚠️ Ошибка: не удалось получить pipeline.")
        return

    task_id = api.generate(prompt, pipeline_id)
    if not task_id:
        await message.answer("⚠️ Ошибка: не удалось начать генерацию.")
        return

    image_base64 = api.check_status(task_id)
    if not image_base64:
        await message.answer("⚠️ Ошибка: генерация изображения не удалась.")
        return

    try:
        image_data = base64.b64decode(image_base64)
        await message.answer_photo(
            BufferedInputFile(image_data, "generated_image.jpg"),
            caption=f"Результат для: '{prompt}'"
        )

        await state.update_data(
            generated_image=image_data,
            prompt=prompt
        )

        await message.answer(
            "Нравится результат?",
            reply_markup=get_review_keyboard()
        )
        await state.set_state(KandinskyStates.ReviewImage)
    except Exception as e:
        logger.error(f"Error sending image: {e}")
        await message.answer("⚠️ Ошибка при отправке изображения.")


@router.message(F.text == "Сгенерировать заново", KandinskyStates.ReviewImage)
async def regenerate_image(message: Message, state: FSMContext):
    data = await state.get_data()
    prompt = data.get("prompt", "")

    if not prompt:
        await message.answer(
            "Не удалось найти предыдущий запрос. Пожалуйста, введите новый:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(KandinskyStates.TextToImage)
        return

    # Уведомляем пользователя о повторной генерации
    await message.answer(
        f"🔄 Повторная генерация для: '{prompt}'",
        reply_markup=ReplyKeyboardRemove()
    )

    # Генерируем изображение напрямую, без создания фейкового сообщения
    api = Text2ImageAPI(FUSION_BRAIN_TOKEN, FB_KEY)
    pipeline_id = api.get_pipeline()
    if not pipeline_id:
        await message.answer("⚠️ Ошибка: не удалось получить pipeline.")
        return

    task_id = api.generate(prompt, pipeline_id)
    if not task_id:
        await message.answer("⚠️ Ошибка: не удалось начать генерацию.")
        return

    image_base64 = api.check_status(task_id)
    if not image_base64:
        await message.answer("⚠️ Ошибка: генерация изображения не удалась.")
        return

    try:
        image_data = base64.b64decode(image_base64)
        await message.answer_photo(
            BufferedInputFile(image_data, "generated_image.jpg"),
            caption=f"Результат для: '{prompt}'"
        )

        await state.update_data(
            generated_image=image_data,
            prompt=prompt
        )

        await message.answer(
            "Нравится результат?",
            reply_markup=get_review_keyboard()
        )
        await state.set_state(KandinskyStates.ReviewImage)
    except Exception as e:
        logger.error(f"Error sending image: {e}")
        await message.answer("⚠️ Ошибка при отправке изображения.")


@router.message(F.text == "Отправить администратору", KandinskyStates.ReviewImage)
async def send_to_admin(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    image_data = data.get("generated_image")
    prompt = data.get("prompt", "")

    if image_data:
        # Формируем информацию о пользователе
        username = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
        admin_caption = (
            f"Сгенерировано по запросу: {prompt}\n"
            f"Пользователь: {username}"
        )

        # Отправляем админам
        for admin_id in settings.admin_ids:
            try:
                await bot.send_photo(
                    admin_id,
                    BufferedInputFile(image_data, "image.jpg"),
                    caption=admin_caption
                )
            except Exception as e:
                logger.error(f"Error sending to admin {admin_id}: {e}")

        # Возврат в главное меню
        from keyboards.on_start import get_on_start_kb
        await message.answer(
            "✅ Изображение отправлено администратору!",
            reply_markup=get_on_start_kb()
        )
        await state.clear()
        await state.set_state(MainStates.main_menu)
    else:
        await message.answer("⚠️ Ошибка: изображение не найдено.")


# Глобальный обработчик кнопки "Назад" для Kandinsky
@router.message(F.text == "Назад")
async def handle_back_kandinsky(message: Message, state: FSMContext):
    from keyboards.on_start import get_on_start_kb
    await state.clear()
    await state.set_state(MainStates.main_menu)
    await message.answer(
        "Возвращаемся в главное меню",
        reply_markup=get_on_start_kb()
    )
