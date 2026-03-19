module.exports = {
  apps: [{
    name: "telegrambot",
    script: "./apps/telegrambot/run_bot.py",
    cwd: "/home/azureuser/agora",
    interpreter: "./apps/telegrambot/.venv/bin/python3",
    // 핵심: 시스템 환경변수를 PM2 내부 변수로 '매핑'만 합니다.
    env_production: {
      NODE_ENV: "production",
      TELEGRAM_TOKEN: process.env.TELEGRAM_TOKEN,
      TELEGRAM_CHAT_ID: process.env.TELEGRAM_CHAT_ID,
      GEMINI_KEY: process.env.GEMINI_KEY
    }
  }]
}
