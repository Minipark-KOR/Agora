# lean 앱 환경설정 예시 (agora 표준)
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent  # ~/agora/apps/lean

LOG_DIR = Path(os.getenv("LOG_DIR", BASE_DIR.parent.parent / "logs" / "lean"))
TEMP_DIR = Path(os.getenv("TEMP_DIR", BASE_DIR.parent.parent / "temp" / "lean"))
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR.parent.parent / "data" / "lean"))
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# 디렉토리 생성
for d in [LOG_DIR, TEMP_DIR, DATA_DIR]:
    d.mkdir(parents=True, exist_ok=True, mode=0o750)

# 필수 환경변수 검증 (예시)
REQUIRED = []
missing = [v for v in REQUIRED if os.getenv(v) is None]
if missing:
    raise RuntimeError(f"Missing required env vars: {missing}")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
