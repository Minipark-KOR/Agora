module.exports = {
  apps: [
    {
      name: "telegrambot",
      // cwd를 사용하거나, script 경로를 최상위 루트 기준으로 한 번만 적어야 합니다.
      script: "./apps/telegrambot/run_bot.py", 
      cwd: "/home/azureuser/agora", // 기준 디렉토리를 프로젝트 루트로 고정
      interpreter: "./apps/telegrambot/.venv/bin/python3",
      watch: ["apps/telegrambot"],
      ignore_watch: ["logs", "data", "temp", "node_modules"],
      env_production: {
        NODE_ENV: "production",
        TELEGRAM_TOKEN: process.env.TELEGRAM_TOKEN,
        TELEGRAM_CHAT_ID: process.env.TELEGRAM_CHAT_ID,
        GEMINI_KEY: process.env.GEMINI_KEY
      }
    }
  ]
};
