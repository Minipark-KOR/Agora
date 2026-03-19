# Notifier 앱

독립적인 알림 중앙 서비스입니다. HTTP API를 통해 다양한 Provider(Telegram, Email 등)로 알림을 전송합니다.

## 환경변수 설정


`.env` 파일 또는 시스템 환경변수로 설정:

```
# Notifier API
NOTIFIER_API_KEY=your-secret-key
NOTIFIER_HOST=127.0.0.1
NOTIFIER_PORT=8001

# Telegram 알림
TELEGRAM_NOTICE_TOKEN=your_telegram_notice_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# Email 알림 (선택)
SMTP_HOST=smtp.example.com
SMTP_PORT=465
SMTP_USER=your_smtp_user
SMTP_PASSWORD=your_smtp_password
EMAIL_FROM=your@email.com
EMAIL_TO=receiver@email.com

# 기타
DEBUG=False
LOG_DIR=logs
```

## 실행

```bash
cd apps/notifier
uvicorn api.main:app --reload --port 8001
```

또는 PM2로 실행 (`ecosystem.config.js`에 등록)

## API 사용법

**엔드포인트**: `POST /v1/notify`  
**헤더**: `Authorization: Bearer {API_KEY}`  

**바디**:
```json
{
  "text": "알림 내용",
  "channel": "telegram"
}
```

**응답**:
```json
{"status": "ok", "channel": "telegram"}
```

## 채널 추가 방법
1. `providers/`에 새 파일 생성 (예: `slack.py`)
2. `NotificationProvider`를 상속받아 `async def send(self, text)` 구현
3. `providers/__init__.py`의 `_providers` 딕셔너리에 추가
4. 필요시 core/config.py에 환경변수 추가

기존 API 코드는 수정할 필요 없습니다.
