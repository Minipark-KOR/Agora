# ~/core/kernel/service_base.py
import logging
import os

class KernelService:
    """커널 기반 서비스 클래스: 모든 서비스(봇, 웹 등)의 공통 부모"""
    def __init__(self, name, log_dir):
        self.name = name
        self.log_dir = os.path.join(log_dir, name)
        os.makedirs(self.log_dir, exist_ok=True)
        self._setup_logging()

    def _setup_logging(self):
        logger = logging.getLogger(self.name)
        if not logger.hasHandlers():
            logging.basicConfig(
                level=logging.WARNING,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(os.path.join(self.log_dir, 'service.log')),
                    logging.StreamHandler()
                ]
            )
        self.logger = logger
