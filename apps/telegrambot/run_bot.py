import sys
from core import config
from core.kernel.services.bot import TelegramBotService
from core.kernel.services.usage_counter import UsageCounter
from core.kernel.agents.manager import get_ai_agent
from telegram.ext import CommandHandler, MessageHandler, filters

if __name__ == "__main__":
    # Gemini 에이전트 생성
    ai_agent = get_ai_agent("gemini", config.GEMINI_KEY)

    # 텔레그램 봇 서비스 생성
    bot = TelegramBotService(
        name=config.BOT_NAMES["TELEGRAM"],
        token=config.TELEGRAM_TOKEN,
        ai_agent=ai_agent,
        log_dir=config.LOG_DIR
    )

    # 핸들러 래핑/교체 불필요. TelegramBotService 내부에서 사용량 카운트 처리

    # 메시지 전송 CLI 옵션 처리 (필요시)
    if len(sys.argv) > 2 and sys.argv[1] == "--send":
        msg = sys.argv[2]
        chat_id = config.ADMIN_CHAT_ID
        bot.send_message(chat_id, msg)
        sys.exit(0)

    # 실행!
    bot.run()
