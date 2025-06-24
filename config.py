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
    # Основные настройки
    bot_token: str = os.getenv('BOT_TOKEN')
    fusion_brain_token: str = os.getenv('FUSION_BRAIN_TOKEN')
    fb_key: str = os.getenv('FB_KEY')
    admin_ids: frozenset[int] = frozenset({42})

    # Webhook настройки
    webhook_domain: str = os.getenv('WEBHOOK_DOMAIN', 'localhost')
    webhook_host: str = os.getenv('WEBHOOK_HOST', '0.0.0.0')
    webhook_port: int = int(os.getenv('WEBHOOK_PORT', 8080))
    webhook_path: str = os.getenv('WEBHOOK_PATH', '/webhook')  # Добавлено
    webhook_url: str = os.getenv('WEBHOOK_URL', f'http://{webhook_domain}:{webhook_port}{webhook_path}')
    ssl_cert_path: str = os.getenv('SSL_CERT_PATH', '')
    ssl_key_path: str = os.getenv('SSL_KEY_PATH', '')


settings = Settings()
