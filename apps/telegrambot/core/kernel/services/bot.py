from core.kernel.service_base import KernelService
import asyncio
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from core.kernel.services.usage_counter import UsageCounter
import pytz
import datetime
import os
import time

class TelegramBotService(KernelService):
    def __init__(self, name, token, ai_agent, log_dir):
        super().__init__(name, log_dir)
        self.token = token
        self.ai_agent = ai_agent
        self.application = Application.builder().token(self.token).build()
        self.usage_counter = UsageCounter(self.application, self.logger)
        self._register_handlers()

    def _register_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start(self, update, context):
        await update.message.reply_text(f"안녕하세요! {self.name}입니다. 무엇을 도와드릴까요?")

    async def handle_message(self, update, context):
        print("handle_message called")
        user_text = update.message.text
        self.logger.info(f"Received message: {user_text}")
        try:
            print("before generate")
            response = self.ai_agent.generate(user_text)
            print("after generate")
            await update.message.reply_text(response)
        except Exception as e:
            print(f"handle_message error: {e}")
            self.logger.error(f"Gemini error: {e}", exc_info=True)
            await update.message.reply_text(f"오류 발생: {e}")
        # 응답 후 사용량 카운트 (이제 정상적으로 실행됨!)
        await self.usage_counter.increment()

    async def cleanup_temp(self, context):
        temp_dir = getattr(self, 'TEMP_DIR', None) or getattr(config, 'TEMP_DIR', None)
        if not temp_dir or not os.path.exists(temp_dir):
            return
        now = time.time()
        for f in os.listdir(temp_dir):
            path = os.path.join(temp_dir, f)
            try:
                if os.path.isfile(path) and os.stat(path).st_mtime < now - 86400:
                    os.remove(path)
            except Exception as e:
                self.logger.error(f"Temp cleanup error: {e}")

    def run(self):
        self.logger.info(f"{self.name} starting...")
        kst = pytz.timezone('Asia/Seoul')
        job_queue = self.application.job_queue
        # 한국 시간 기준 자정에 정상 작동
        job_queue.run_daily(self.cleanup_temp, time=datetime.time(hour=0, minute=0, tzinfo=kst))
        self.application.run_polling()

    async def send_message_async(self, chat_id, text):
        bot = Bot(token=self.token)
        await bot.send_message(chat_id=chat_id, text=text)

    def send_message(self, chat_id, text):
        asyncio.run(self.send_message_async(chat_id, text))
from core.kernel.service_base import KernelService
import asyncio
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from core.kernel.services.usage_counter import UsageCounter
import pytz


class TelegramBotService(KernelService):
    def __init__(self, name, token, ai_agent, log_dir):
        super().__init__(name, log_dir)
        self.token = token
        self.ai_agent = ai_agent
        self.application = Application.builder().token(self.token).build()
        self.usage_counter = UsageCounter(self.application, self.logger)
        self._register_handlers()

    def _register_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start(self, update, context):
        await update.message.reply_text(f"안녕하세요! {self.name}입니다. 무엇을 도와드릴까요?")

    async def handle_message(self, update, context):
        user_text = update.message.text
        self.logger.info(f"Received message: {user_text}")
        try:
            response = self.ai_agent.generate(user_text)
            await update.message.reply_text(response)
        except Exception as e:
            self.logger.error(f"Gemini error: {e}", exc_info=True)
            await update.message.reply_text("죄송합니다. 오류가 발생했습니다.")
        # 응답 후 사용량 카운트
        await self.usage_counter.increment()

    async def cleanup_temp(self, context):
        import os, time
        from core import config
        temp_dir = getattr(self, 'TEMP_DIR', None) or getattr(config, 'TEMP_DIR', None)
        if not temp_dir or not os.path.exists(temp_dir):
            return
        now = time.time()
        for f in os.listdir(temp_dir):
            path = os.path.join(temp_dir, f)
            try:
                if os.path.isfile(path) and os.stat(path).st_mtime < now - 86400:
                    os.remove(path)
            except Exception as e:
                self.logger.error(f"Temp cleanup error: {e}")

    def run(self):
        self.logger.info(f"{self.name} starting...")
        import datetime
        kst = pytz.timezone('Asia/Seoul')
        job_queue = self.application.job_queue
        job_queue.run_daily(self.cleanup_temp, time=datetime.time(hour=0, minute=0, tzinfo=kst))
        self.application.run_polling()

    async def send_message_async(self, chat_id, text):
        bot = Bot(token=self.token)
        await bot.send_message(chat_id=chat_id, text=text)

    def send_message(self, chat_id, text):
        asyncio.run(self.send_message_async(chat_id, text))

    def _register_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start(self, update, context):
        await update.message.reply_text(f"안녕하세요! {self.name}입니다. 무엇을 도와드릴까요?")

    async def handle_message(self, update, context):
        user_text = update.message.text
        self.logger.info(f"Received message: {user_text}")
        try:
            response = self.ai_agent.generate(user_text)
            await update.message.reply_text(response)
        except Exception as e:
            self.logger.error(f"Gemini error: {e}", exc_info=True)
            await update.message.reply_text("죄송합니다. 오류가 발생했습니다.")

    def run(self):
        self.logger.info(f"{self.name} starting...")
        # 임시 파일 정리 JobQueue 등록 (매일 0시)
        import datetime
        job_queue = self.application.job_queue
        job_queue.run_daily(self.cleanup_temp, time=datetime.time(hour=0, minute=0))
        self.application.run_polling()

    async def send_message_async(self, chat_id, text):
        bot = Bot(token=self.token)
        await bot.send_message(chat_id=chat_id, text=text)

    def send_message(self, chat_id, text):
        # CLI 전용: 이미 실행 중인 이벤트 루프가 없을 때만 사용
        asyncio.run(self.send_message_async(chat_id, text))
