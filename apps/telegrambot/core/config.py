import os
from dotenv import load_dotenv

# 1. 경로 기준 설정
# 현재 파일(core/config.py)의 위치를 기준으로 상위 디렉토리를 BASE_DIR로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. 봇 이름 정의 (최상단으로 이동!)
# 아래 경로 설정에서 BOT_NAMES를 참조하므로 반드시 먼저 선언되어야 합니다.
BOT_NAMES = {
    "TELEGRAM": "mesids_bot"
}

# 3. 환경변수 로드 (시크릿 우선 적용)
if not os.environ.get("TELEGRAM_TOKEN") or not os.environ.get("GEMINI_KEY"):
    dotenv_path = os.path.join(BASE_DIR, ".env")
    load_dotenv(dotenv_path)

# 4. 로그 및 임시 디렉토리 경로 설정 (이제 BOT_NAMES 참조 가능)
LOG_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../data/telegrambot/logs", BOT_NAMES["TELEGRAM"]))
TEMP_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../data/telegrambot/temp", BOT_NAMES["TELEGRAM"]))

# 5. 토큰 및 ID 설정
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TEST_TOKEN") or os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")
ADMIN_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if not ADMIN_CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID must be set in 환경변수 또는 .env (관리자 알림용)")

# 6. 기타 설정
TOTAL_QUOTA = int(os.getenv("TOTAL_QUOTA", "1000"))

# 7. 디렉토리 실제 생성
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
