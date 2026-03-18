import os
from dotenv import load_dotenv

# 현재 파일(core/config.py)의 위치를 기준으로 상위 디렉토리(telegrambot)를 BASE_DIR로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 1. GitHub Actions 등 환경변수(시크릿) 우선 적용
# 2. 환경변수 없으면 .env 파일에서 로드 (개발환경)
if not os.environ.get("TELEGRAM_TOKEN") or not os.environ.get("GEMINI_KEY"):
    dotenv_path = os.path.join(BASE_DIR, ".env")
    load_dotenv(dotenv_path)


# 로그 디렉토리: ~/data/telegrambot/logs
LOG_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../data/telegrambot/logs"))

# 임시 파일 디렉토리: ~/data/telegrambot/temp (1일마다 자동 삭제)
TEMP_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../data/telegrambot/temp"))


# 환경변수에서 토큰과 ID 읽기 (시크릿 우선)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TEST_TOKEN") or os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

# 관리자 ID (이전 TELEGRAM_CHAT_ID와 호환되도록)
# .env에 ADMIN_CHAT_ID가 있으면 사용, 없으면 TELEGRAM_CHAT_ID 사용

ADMIN_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
if not ADMIN_CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID must be set in 환경변수 또는 .env (관리자 알림용)")

# 일일 할당량 (기본값 1000)
TOTAL_QUOTA = int(os.getenv("TOTAL_QUOTA", "1000"))

# 봇 이름 (원하는 대로 설정, 예: telegram_bot)
BOT_NAMES = {
    "TELEGRAM": "mesids_bot"
}

# 로그 디렉토리 생성 (봇 이름 하위 폴더까지)
os.makedirs(os.path.join(LOG_DIR, BOT_NAMES["TELEGRAM"]), exist_ok=True)

# 임시 디렉토리 생성
os.makedirs(TEMP_DIR, exist_ok=True)
