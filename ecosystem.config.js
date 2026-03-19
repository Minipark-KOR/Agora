module.exports = {
  apps: [
    {
      name: "telegrambot",
      script: "./apps/telegrambot/run_bot.py",
      // 서버 내 가상환경의 파이썬 실행 파일 경로 지정
      interpreter: "./apps/telegrambot/.venv/bin/python3",
      instances: 1,
      autorestart: true,
      watch: false,
      env_production: {
        NODE_ENV: "production",
        // GitHub Actions에서 export한 변수를 PM2가 받아옴
        TELEGRAM_TOKEN: process.env.TELEGRAM_TOKEN,
        TELEGRAM_CHAT_ID: process.env.TELEGRAM_CHAT_ID,
        GEMINI_KEY: process.env.GEMINI_KEY
      }
    }
  ]
}
