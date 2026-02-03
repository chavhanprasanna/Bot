import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str = os.getenv("MONGO_URI", "")
    mongo_db_name: str = os.getenv("MONGO_DB_NAME", "support_ai")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    faq_confidence_threshold: float = float(os.getenv("FAQ_CONFIDENCE_THRESHOLD", "0.7"))
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    discord_bot_token: str = os.getenv("DISCORD_BOT_TOKEN", "")


settings = Settings()
