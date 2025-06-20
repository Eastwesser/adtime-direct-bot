import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# dotenv_path = os.path.join(os.getcwd(), ".venv", ".env") # old
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

load_dotenv(dotenv_path)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
    )

    bot_token: str = os.getenv('BOT_TOKEN')
    fusion_brain_token: str = os.getenv('FUSION_BRAIN_TOKEN')
    fb_key: str = os.getenv('FB_KEY')
    admin_ids: frozenset[int] = frozenset({42, 5756911009})


settings = Settings()
