
# from pathlib import Path
from typing import Optional
from pathlib import Path
# 프로젝트 루트 경로 제공 (하위 호환)
BASE_DIR = Path(__file__).parent.parent

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    TELEGRAM_TEST_TOKEN: Optional[str] = None
    ADMIN_CHAT_ID: str
    GEMINI_KEY: str
    LOG_DIR: Path = Path("/var/log/agora/telegrambot")  # 운영 표준 경로 (필요시 .env에서 덮어쓰기)
    TEMP_DIR: Path = Path("/var/tmp/agora/telegrambot")
    DATA_DIR: Path = Path("/data/agora/telegrambot")
    TOTAL_QUOTA: int = 1000
    LOG_LEVEL: str = "WARNING"
    BOT_NAME: str = "mesids_bot"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


Settings.model_rebuild()
settings = Settings()

# 하위 호환성: 기존 변수명 유지 (필요시)
LOG_DIR = settings.LOG_DIR
TEMP_DIR = settings.TEMP_DIR
TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
ADMIN_CHAT_ID = settings.ADMIN_CHAT_ID
GEMINI_KEY = settings.GEMINI_KEY
TOTAL_QUOTA = settings.TOTAL_QUOTA
BOT_NAMES = {"TELEGRAM": settings.BOT_NAME}
os.makedirs(TEMP_DIR, exist_ok=True)
