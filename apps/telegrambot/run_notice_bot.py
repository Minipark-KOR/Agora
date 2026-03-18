import sys
import os
from core import config
from core.kernel.services.bot import TelegramBotService
from core.kernel.services.usage_counter import UsageCounter
from core.kernel.agents.manager import get_ai_agent
from telegram.ext import CommandHandler, MessageHandler, filters

if __name__ == "__main__":
    # Gemini 에이전트 생성
    ai_agent = get_ai_agent("gemini", config.GEMINI_KEY)

    # 운영 알림용 토큰 우선 적용
    notice_token = os.environ.get("TELEGRAM_NOTICE_TOKEN")
    if not notice_token:
        raise ValueError("TELEGRAM_NOTICE_TOKEN 환경변수가 필요합니다.")

    # 텔레그램 봇 서비스 생성 (운영 알림 토큰)
    bot = TelegramBotService(
        name="notice_bot",
        token=notice_token,
        ai_agent=ai_agent,
        log_dir=config.LOG_DIR
    )

    # 메시지 전송 CLI 옵션 처리 (필요시)
    if len(sys.argv) > 2 and sys.argv[1] == "--send":
        msg = sys.argv[2]
        chat_id = config.ADMIN_CHAT_ID
        bot.send_message(chat_id, msg)
        sys.exit(0)

    # 실행!
    bot.run()
