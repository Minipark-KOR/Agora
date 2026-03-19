import os
from dotenv import load_dotenv

# 1. BASE_DIR 먼저 정의
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. 항상 .env 파일 로드 (시스템 환경변수가 우선)
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

# 3. 봇 이름
BOT_NAMES = {
    "TELEGRAM": "mesids_bot"
}

# 4. 로그/임시 디렉토리 기본값 (봇 이름 미포함)
DEFAULT_LOG_BASE = os.path.abspath(os.path.join(BASE_DIR, "../../data/telegrambot/logs"))
DEFAULT_TEMP_BASE = os.path.abspath(os.path.join(BASE_DIR, "../../data/telegrambot/temp"))

# 5. 환경변수로 오버라이드 가능 (값이 없으면 기본값)
LOG_BASE = os.getenv("LOG_DIR", DEFAULT_LOG_BASE)
TEMP_BASE = os.getenv("TEMP_DIR", DEFAULT_TEMP_BASE)

# KernelService가 내부에서 봇 이름을 추가하므로 부모 경로만 전달
LOG_DIR = LOG_BASE
TEMP_DIR = TEMP_BASE

# 6. 토큰 및 ID 설정
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TEST_TOKEN") or os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")
ADMIN_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if not ADMIN_CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID must be set in 환경변수 또는 .env (관리자 알림용)")

# 7. 기타 설정
TOTAL_QUOTA = int(os.getenv("TOTAL_QUOTA", "1000"))

# 8. 부모 디렉토리만 생성 (하위는 KernelService가 생성)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
