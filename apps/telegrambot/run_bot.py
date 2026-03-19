
import sys
import logging
from core import config
from core.kernel.services.bot import TelegramBotService
from core.kernel.services.usage_counter import UsageCounter
from core.kernel.agents.manager import get_ai_agent
from telegram.ext import CommandHandler, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("run_bot")

if __name__ == "__main__":
    # Gemini 에이전트 생성
    ai_agent = get_ai_agent("gemini", config.GEMINI_KEY)

    # TELEGRAM_TEST_TOKEN이 없거나 공백이면 실행 중단 (pydantic settings에서 읽음)
    token = config.settings.TELEGRAM_TEST_TOKEN
    if token and token.strip():
        logger.info("테스트 토큰(TELEGRAM_TEST_TOKEN)으로 실행됩니다.")
    else:
        logger.error("운영 토큰(TELEGRAM_TOKEN)으로는 실행할 수 없습니다. .env에 TELEGRAM_TEST_TOKEN을 정확히 설정하세요.")
        sys.exit(1)

    # 텔레그램 봇 서비스 생성
    bot = TelegramBotService(
        name=config.BOT_NAMES["TELEGRAM"],
        token=token,
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
