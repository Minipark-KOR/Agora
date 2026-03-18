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

    # 테스트용 토큰 우선 적용
    test_token = os.getenv("TELEGRAM_TEST_TOKEN") or config.TELEGRAM_TOKEN

    # 텔레그램 봇 서비스 생성 (테스트 토큰)
    bot = TelegramBotService(
        name=config.BOT_NAMES["TELEGRAM"],
        token=test_token,
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
