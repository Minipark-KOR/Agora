from .config import settings

# 하위 호환성: 기존 변수명 유지 (필요시)
LOG_DIR = settings.LOG_DIR
TEMP_DIR = settings.TEMP_DIR
TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
ADMIN_CHAT_ID = settings.ADMIN_CHAT_ID
GEMINI_KEY = settings.GEMINI_KEY
TOTAL_QUOTA = settings.TOTAL_QUOTA
BOT_NAMES = {"TELEGRAM": settings.BOT_NAME}
