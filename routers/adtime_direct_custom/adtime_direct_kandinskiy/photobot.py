import base64
import json
import os
import time

import requests
from aiogram import (
    Bot,
    types,
    Dispatcher,
    F,
)
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InputFile
from aiogram.types import Message
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.types import (
    ReplyKeyboardRemove,
)
from dotenv import load_dotenv

from keyboards.on_start import ButtonText

bot_token = os.getenv('BOT_TOKEN')
fusion_brain_token = os.getenv('FUSION_BRAIN_TOKEN')
fusion_brain_key = os.getenv('FB_KEY')

load_dotenv()

bot = Bot(token=bot_token)
dp = Dispatcher()

router = Router(name=__name__)


class InputFileBytes(InputFile):
    def __init__(self, file_data: bytes, filename: str):
        """
        Represents the contents of a file to be uploaded from bytes data.

        :param file_data: Bytes data of the file
        :param filename: Name of the file
        """
        super().__init__(filename=filename)
        self.file_data = file_data

    async def read(self, bot):
        """
        Implementation of the read method to yield bytes data of the file.
        """
        yield self.file_data


class AIfilters(StatesGroup):
    Maskings = State()
    Filterings = State()
    Framings = State()
    Rembg = State()


# KANDINSKIY ===========================================================================================================
class KandinskyStates(StatesGroup):
    Intro = State()
    TextToImage = State()


class ButtonTextKandinsky:
    TEXT_TO_IMAGE = "Text to image"


API_URL = "https://api-key.fusionbrain.ai/"

MODELS_ENDPOINT = API_URL + "key/api/v1/models"
GENERATE_ENDPOINT = API_URL + "key/api/v1/text2image/run"
STATUS_ENDPOINT = API_URL + "key/api/v1/text2image/status/"

headers = {
    'X-Key': f'Key {fusion_brain_token}',
    'X-Secret': f'Secret {fusion_brain_key}',
}


def get_text_to_image_kb() -> ReplyKeyboardMarkup:
    text_to_image_button = KeyboardButton(text="Text to image")
    buttons_row_1 = [text_to_image_button]
    markup_keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons_row_1],
        resize_keyboard=True
    )
    return markup_keyboard


class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        try:
            response = requests.get(
                self.URL + 'key/api/v1/pipelines',
                headers=self.AUTH_HEADERS
            )
            response.raise_for_status()
            data = response.json()
            print(f"Pipelines response: {data}")  # Логируем ответ
            return data[0]['id']
        except Exception as e:
            print(f"Error getting pipeline: {str(e)}")
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
            response = requests.post(
                self.URL + 'key/api/v1/pipeline/run',
                headers=self.AUTH_HEADERS,
                files=data
            )
            response.raise_for_status()
            data = response.json()
            print(f"Generate response: {data}")  # Логируем ответ
            return data['uuid']
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            return None

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            try:
                response = requests.get(
                    self.URL + 'key/api/v1/pipeline/status/' + request_id,
                    headers=self.AUTH_HEADERS
                )
                data = response.json()
                print(f"Status check: {data}")  # Логируем статус

                if data['status'] == 'DONE':
                    return data['result']['files'][0]  # Берем первую картинку
                elif data['status'] == 'FAIL':
                    print(f"Generation failed: {data.get('errorDescription')}")
                    return None

                attempts -= 1
                time.sleep(delay)
            except Exception as e:
                print(f"Error checking status: {str(e)}")
                return None
        return None


@router.message(F.text == ButtonText.KANDINSKY)
async def handle_kandinskiy_message(message: types.Message):
    await message.answer(
        text="Meow! If you want draw with me,\n"
             "click /start_kandinsky any time! :3",
        reply_markup=ReplyKeyboardRemove(),
        one_time_keyboard=True
    )


@router.message(Command("start_kandinsky", prefix="!/"))
async def start(message: types.Message):
    await message.answer(
        "Welcome to the Kandinsky bot! Please, press on the button 'Text to Image' ^w^\n"
        "And please, don't ask me to draw violent or forbidden things!\n"
        "I have paws 😿",
        reply_markup=get_text_to_image_kb()
    )


@router.message(F.text == ButtonTextKandinsky.TEXT_TO_IMAGE)
async def handle_text_to_image(message: Message, state: FSMContext):
    await state.set_state(KandinskyStates.Intro)
    await message.answer("Please enter the text you want to generate an image for.\n"
                         "It may take some time, almost 30-40 seconds, so be patient UwU")
    await state.set_state(KandinskyStates.TextToImage)


@router.message(KandinskyStates.TextToImage)
async def process_text_for_image(message: types.Message, state: FSMContext):
    await state.set_state(KandinskyStates.TextToImage)
    text = message.text
    api = Text2ImageAPI(
        "https://api-key.fusionbrain.ai/",
        fusion_brain_token,
        fusion_brain_key
    )

    pipeline_id = api.get_pipeline()
    if not pipeline_id:
        await message.answer("⚠️ Ошибка получения модели. Попробуйте позже.")
        return

    uuid = api.generate(text, pipeline_id)
    if not uuid:
        await message.answer("⚠️ Ошибка запуска генерации. Попробуйте позже.")
        return

    image_base64 = api.check_generation(uuid)
    if not image_base64:
        await message.answer("⚠️ Ошибка генерации изображения. Попробуйте позже.")
        return

    try:
        image_data = base64.b64decode(image_base64)
        buffered_input_file = types.input_file.BufferedInputFile(
            file=image_data,
            filename="image.jpg"
        )
        await message.answer_photo(buffered_input_file)
    except Exception as e:
        print(f"Error sending photo: {str(e)}")
        await message.answer("⚠️ Ошибка отправки изображения.")

    await state.clear()
