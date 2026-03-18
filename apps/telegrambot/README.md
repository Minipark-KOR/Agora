## ⚡️ pm2로 봇 관리하기

pm2는 Node.js 기반 프로세스 관리자이지만, Python 실행도 지원합니다. 서버 재부팅 시 자동 실행, 로그 관리, 프로세스 모니터링이 가능합니다.

### 1. pm2 설치

```bash
npm install -g pm2
```

### 2. 봇 실행 (루트 .env 기준)

```bash
cd ~/app/telegrambot
source .venv/bin/activate
pm2 start run_bot.py --interpreter $(which python) --name telegrambot
```

### 3. 환경변수(.env) 적용

pm2는 기본적으로 .env를 자동으로 로드하지 않으므로, python-dotenv를 코드에서 사용하거나 아래처럼 환경변수 파일을 명시할 수 있습니다.

#### 방법1: 코드에서 load_dotenv 사용 (이미 적용됨)
#### 방법2: pm2 ecosystem 파일 사용

```bash
pm2 init
```
ecosystem.config.js에서 env 섹션에 환경변수 직접 입력하거나 dotenv-flow 패키지 활용 가능

### 4. pm2 관리 명령어

| 작업 | 명령어 |
|------|--------|
| 시작 | `pm2 start run_bot.py --interpreter $(which python) --name telegrambot` |
| 중지 | `pm2 stop telegrambot` |
| 재시작 | `pm2 restart telegrambot` |
| 상태 확인 | `pm2 status` |
| 로그 확인 | `pm2 logs telegrambot` |
| 전체 로그 | `pm2 logs` |
| 자동 재시작 활성화 | `pm2 startup` 후 안내대로 실행 |
| pm2 설정 저장 | `pm2 save` |

### 5. pm2 자동 시작 설정

```bash
pm2 startup
pm2 save
```

서버 재부팅 후에도 봇이 자동 실행됩니다.

---
```markdown
# Telegram Bot Setup Guide

이 문서는 텔레그램 봇을 서버에 설치하고 systemd 서비스로 등록하여 재부팅 후에도 자동 실행되도록 설정하는 방법을 설명합니다.  
또한 사용량 모니터링, 로그 관리, 임시 파일 자동 정리 기능에 대해 안내합니다.

## 📁 디렉토리 구조 (최종)

```
/home/azureuser/app/telegrambot/
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── .env
│   ├── kernel/
│   │   ├── __init__.py
│   │   ├── service_base.py
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── manager.py
│   │   │   └── gemini.py
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── bot.py
│   │       └── usage_counter.py      # 사용량 카운트 모듈
├── data/                               # 데이터 저장 폴더 (자동 생성)
│   ├── logs/                           # 로그 파일 저장
│   │   └── mesids_bot/
│   ├── temp/                            # 임시 파일 저장 (24시간 후 자동 삭제)
│   ├── usage_count.json                 # 일일 사용량 기록
│   └── notified.json                    # 알림 전송 기록
├── .venv/
├── requirements.txt
├── run_bot.py
```

## 🚀 설치 및 초기 설정

### 1. 필수 패키지 설치

```bash
cd ~/app/telegrambot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt`:

```txt
python-dotenv>=1.0.0
google-genai>=1.0.0
python-telegram-bot>=20.0
python-telegram-bot[job-queue]
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 입력하세요.

```bash
nano .env
```

```
TELEGRAM_TOKEN=여기에_텔레그램_봇_토큰_입력
GEMINI_KEY=여기에_구글_Gemini_API_키_입력
TELEGRAM_CHAT_ID=관리자_텔레그램_ID          # 사용량 알림을 받을 계정
TOTAL_QUOTA=1000                          # 일일 최대 요청 수 (모델에 따라 조정)
```

**보안을 위해 권한 설정:**

```bash
chmod 600 .env
```

### 3. 파이썬 패키지 임포트 경로 설정

```bash
touch core/__init__.py
touch core/kernel/__init__.py
touch core/kernel/services/__init__.py
touch core/kernel/agents/__init__.py
```

필요시 기존 파일의 임포트 경로를 수정합니다.

```bash
sed -i 's/from kernel\./from core.kernel./g' core/kernel/**/*.py
```

## 📊 사용량 모니터링 및 데이터 관리

이 봇은 다음과 같은 자체 모니터링 기능을 포함합니다.

### 사용량 카운트
- 모든 메시지 응답 성공 시 `data/usage_count.json`에 일일 사용량이 기록됩니다.
- 파일 형식: `{"date": "2026-03-17", "count": 123}`

### 관리자 알림
- 일일 할당량(`TOTAL_QUOTA`) 대비 남은 비율이 **50%, 20%, 10%** 에 도달하면 관리자(`TELEGRAM_CHAT_ID`)에게 텔레그램 알림이 전송됩니다.
- 중복 알림을 방지하기 위해 `data/notified.json`에 오늘 날짜와 전송한 임계치가 저장됩니다.

### 임시 파일 자동 정리
- `data/temp/` 디렉토리에 저장된 파일은 **24시간 이상 경과 시 매일 0시에 자동 삭제**됩니다.
- 이 기능은 봇 실행 시 내부적으로 `JobQueue`를 사용하여 구현되어 있습니다.
- 별도의 크론탭 설정 없이, 봇이 실행 중이면 자동으로 동작합니다.

### 로그 파일 위치
- 모든 로그는 `data/logs/mesids_bot/`에 저장됩니다. (기존 `logs/` 폴더에서 변경됨)

## 🏃 수동 실행

```bash
cd ~/app/telegrambot
source .venv/bin/activate
python run_bot.py
```

- 실행 중지는 `Ctrl+C`를 누릅니다.
- 최초 실행 시 `data/` 폴더와 하위 디렉토리가 자동 생성됩니다.

## ⚙️ systemd 서비스 등록 (재부팅 시 자동 실행)

### 1. 서비스 파일 생성

```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

```ini
[Unit]
Description=Telegram Bot Service
After=network.target

[Service]
User=azureuser
WorkingDirectory=/home/azureuser/app/telegrambot
Environment="PATH=/home/azureuser/app/telegrambot/.venv/bin"
EnvironmentFile=/home/azureuser/app/telegrambot/.env
ExecStart=/home/azureuser/app/telegrambot/.venv/bin/python /home/azureuser/app/telegrambot/run_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. 서비스 활성화 및 시작

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot.service
sudo systemctl start telegram-bot.service
```

### 3. 서비스 상태 확인

```bash
sudo systemctl status telegram-bot.service
```

### 4. 실시간 로그 확인

```bash
sudo journalctl -u telegram-bot.service -f
```

## 🔧 서비스 관리 명령어

| 작업 | 명령어 |
|------|--------|
| 서비스 시작 | `sudo systemctl start telegram-bot.service` |
| 서비스 중지 | `sudo systemctl stop telegram-bot.service` |
| 서비스 재시작 | `sudo systemctl restart telegram-bot.service` |
| 서비스 상태 확인 | `sudo systemctl status telegram-bot.service` |
| 부팅 시 자동 실행 활성화 | `sudo systemctl enable telegram-bot.service` |
| 부팅 시 자동 실행 비활성화 | `sudo systemctl disable telegram-bot.service` |
| 실시간 로그 확인 | `sudo journalctl -u telegram-bot.service -f` |
| 최근 로그 50줄 보기 | `sudo journalctl -u telegram-bot.service -n 50` |

## 📂 데이터 파일 확인

```bash
# 사용량 확인
cat ~/app/telegrambot/data/usage_count.json

# 알림 기록 확인
cat ~/app/telegrambot/data/notified.json

# 로그 파일 확인
ls -la ~/app/telegrambot/data/logs/mesids_bot/
```

## 🔄 재부팅 테스트

서버를 재부팅하여 봇이 자동으로 실행되는지 확인합니다.

```bash
sudo reboot
```

재접속 후 서비스 상태 확인:

```bash
sudo systemctl status telegram-bot.service
```

## 🧹 불필요한 파일 정리 (선택)

```bash
# 백업 파일 삭제
rm ~/app/telegrambot/config.py.bak
rm ~/app/telegrambot/run_bot.py.bak

# 이전 로그 디렉토리 삭제 (모든 로그가 data/logs/로 이전된 경우)
rm -rf ~/app/telegrambot/logs

# 파이썬 캐시 삭제
find ~/app/telegrambot -type d -name "__pycache__" -exec rm -rf {} +
```

## 📝 참고 사항

- 봇 이름은 `mesids_bot`으로 설정되어 있습니다. (`core/config.py`의 `BOT_NAMES`에서 변경 가능)
- 로그 파일은 `~/app/telegrambot/data/logs/mesids_bot/`에 저장됩니다.
- Gemini AI 모델은 `gemini-2.5-flash-lite`를 사용합니다. (필요시 `core/kernel/agents/gemini.py`에서 변경)
- 사용량 카운트 및 알림 기능은 별도 모듈(`usage_counter.py`)로 분리되어 있어 유지보수가 용이합니다.

## 🎉 완료

이제 텔레그램 봇이 서버에서 안정적으로 실행되며, 사용량 모니터링, 자동 로그 관리, 임시 파일 정리 기능이 함께 동작합니다.

---

## 🧪 테스트/로컬 실행 및 관리 규칙 (2026-03 최신)

### 테스트 전용 실행 파일 관리
- 테스트용 진입점(run_testbot.py, run_test_bot.py 등)은 .gitignore와 .stignore에 추가하여 git/Syncthing 동기화에서 제외합니다.
- 필요시 복사/이름변경하여 사용하고, 운영 배포에는 포함하지 않습니다.

### 테스트 토큰 우선 적용
- 테스트 실행 파일은 `.env`의 `TELEGRAM_TEST_TOKEN`이 있으면 우선 사용, 없으면 `TELEGRAM_TOKEN`을 사용합니다.
- 운영/테스트 봇을 완전히 분리하여 실험할 수 있습니다.

### 로컬 실행과 서버 실행의 차이
- 로컬에서 `python run_testbot.py`로 실행하면 터미널이 점유(폴링 대기)되고, 실시간 로그가 콘솔에 바로 찍힙니다.
- 서버에서는 systemd/supervisor/docker 등으로 백그라운드 실행되어 터미널이 즉시 반환되고, 로그는 파일로 기록됩니다.
- 로컬에서 운영처럼 "대기창+실시간 로그"를 원하면 `nohup python run_testbot.py > testbot.log 2>&1 &`로 백그라운드 실행 후, `tail -f testbot.log`로 로그를 확인하세요.

### 기타 변경점 요약
- requirements.txt에 `python-telegram-bot[job-queue]` 명시 (JobQueue 필수)
- 테스트 실행 파일(run_testbot.py 등)은 .gitignore, .stignore 모두에 추가
- .env에서 TELEGRAM_TEST_TOKEN 등 테스트 토큰은 필요시만 유지, 테스트 종료 후 삭제 권장

---