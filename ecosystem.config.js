module.exports = {
  apps: [{
    name: "telegrambot",
    cwd: "/home/azureuser/agora",
    script: "apps/telegrambot/run_bot.py",
    out_file: '/dev/null',   // 일반 출력 로그 기록 안 함
    error_file: '/home/azureuser/.pm2/logs/telegrambot-error.log',
    interpreter: "/home/azureuser/agora/apps/telegrambot/.venv/bin/python3",
    env_production: {
      NODE_ENV: "production",    }
  }]
}
