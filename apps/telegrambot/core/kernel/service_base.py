# service_base.py
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger
from core.config import settings

class KernelService:
    def __init__(self, name, log_dir):
        self.name = name
        self.log_dir = os.path.join(log_dir, name)
        os.makedirs(self.log_dir, exist_ok=True)
        self._setup_logging()

    def _setup_logging(self):
        logger = logging.getLogger(self.name)

        # 로그 레벨 환경변수 제어
        log_level_str = str(settings.LOG_LEVEL).upper()
        log_level = getattr(logging, log_level_str, logging.WARNING)
        logger.setLevel(log_level)

        # 핸들러 중복 방지: 기존 핸들러 모두 제거 후 재설정
        if logger.handlers:
            logger.handlers.clear()

        # 로그 파일 경로 (service.jsonl)
        log_file = os.path.join(self.log_dir, 'service.jsonl')

        # JSON 포맷터 생성
        formatter = jsonlogger.JsonFormatter(
            fmt='%(asctime)s %(name)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            json_ensure_ascii=False
        )

        # RotatingFileHandler: 10MB, 백업 5개
        fh = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # 콘솔 핸들러 (stdout) - PM2 로그 수집용 (JSON 유지)
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

        # 상위 로거로 전파되지 않도록 설정 (중복 방지)
        logger.propagate = False

        self.logger = logger

        