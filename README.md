```markdown
# 📘 Project Bot Guide (agora 프로젝트)
## Notifier 앱 구조 및 실행 방식 (최신)

Notifier는 독립적인 알림 중앙 서비스로, HTTP API를 통해 다양한 Provider(Telegram, Email 등)로 알림을 전송합니다.

### 실행
```bash
cd apps/notifier
uvicorn api.main:app --reload --port 8001
```

환경변수는 `.env` 또는 시스템 환경변수로 관리하며, Pydantic Settings를 사용해 부수효과 없는 구조를 유지합니다.

### Provider 추가 방법
1. `providers/`에 새 파일 생성 (예: `slack.py`)
2. `NotificationProvider`를 상속받아 `async def send(self, text)` 구현
3. `providers/__init__.py`의 `_providers` 딕셔너리에 추가
4. 필요시 core/config.py에 환경변수 추가

기존 API 코드는 수정할 필요 없습니다.

### 구조적 특징
- channels/, server.py, config.py 등 legacy 코드/폴더는 완전히 제거됨
- main.py 기준 실행, providers/ 기반 구조로 통일
- 각 앱은 완전히 독립적으로 동작하며, core/에는 순수 라이브러리와 추상 베이스 클래스만 존재
- 앱 간 통신은 HTTP API로만 연결, requirements.txt, README.md, .env 등 각 앱별로 관리

---

이 문서는 여러 개의 독립적인 앱(봇)을 느슨하게 연결하여 운영하는 구체적인 방법을 다룹니다.  
환경변수 기반 설정, 디렉토리 구조, 로깅, 통신 방식, 운영 환경에서의 시스템 디렉토리 활용, PM2 watch 자동 재시작 전략, 테스트 파일 관리, ignore 파일 설정, 그리고 단계별 적용 계획까지 모두 포함합니다.

---

## 1. 프로젝트 개요

`agora`는 여러 독립적인 봇 애플리케이션들이 느슨하게 연결된 프로젝트입니다. 각 봇은 자체 코드, 설정, 데이터 디렉토리를 가지며, HTTP API, Redis 큐, 공유 폴더를 통해 통신합니다.

**구성 앱**:
- `chronicle` - 메인 문서 앱
- `lean` - 토큰 최적화
- `metrics` - (보류)
- `omnibot` - 웹 AI 대화 수집
- `telegrambot` - 텔레그램 봇 (PM2 운영)

---

## 2. 디렉토리 구조

```
agora/                          # 프로젝트 루트
├── apps/                       # 개별 앱 디렉토리
│   ├── chronicle/
│   ├── lean/
│   ├── metrics/                # (보류)
│   ├── omnibot/
│   └── telegrambot/
├── data/                       # 영구 데이터 (각 앱별 하위 디렉토리)
│   ├── chronicle/
│   ├── lean/
│   ├── omnibot/
│   ├── telegrambot/
│   └── exchange/                # 앱 간 데이터 교환용
├── logs/                        # 개발 환경 로그 (각 앱별 하위 디렉토리)
│   ├── chronicle/
│   ├── lean/
│   ├── omnibot/
│   └── telegrambot/
├── temp/                         # 개발 환경 임시 파일 (각 앱별 하위 디렉토리)
│   ├── chronicle/
│   └── ...
├── ecosystem.config.js          # PM2 설정
├── .env.example                 # 공통 환경변수 예제
├── .gitignore                   # Git 제외 목록
├── .stignore                    # Syncthing 동기화 제외 목록
└── README.md
```

> **참고**: 운영 서버에서는 `logs/`, `temp/` 대신 시스템 디렉토리(`/var/log/agora`, `/var/tmp/agora`)를 사용합니다. 환경변수로 경로를 제어하므로 개발 환경과 운영 환경의 구조가 달라도 무방합니다.

---

## 3. 환경변수 관리 원칙 (3-Tier Rule)

모든 설정값은 다음 우선순위로 결정됩니다.

| 우선순위 | 출처 | 설명 |
|----------|------|------|
| 1순위 | 시스템 환경변수 | 운영체제, PM2, Docker, systemd 등에서 주입 |
| 2순위 | `.env` 파일 | 로컬 개발 전용 (각 앱 디렉토리에 위치, Git 제외) |
| 3순위 | 하드코딩 기본값 | 개발 환경에 적합한 안전한 기본값 |

**원칙**: 모든 설정값은 코드에 직접 적지 않고 `os.getenv()`로 읽어옵니다. 민감 정보(토큰, 비밀번호)는 절대 코드에 하드코딩하지 않습니다.

---

## 4. 각 앱의 `config.py` 패턴

모든 앱은 동일한 방식으로 환경변수를 읽어 경로와 설정을 구성합니다.

```python
# apps/telegrambot/config.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent  # ~/agora/apps/telegrambot

# 환경변수 우선, 없으면 기본값 (개발 환경 기준 상대경로)
LOG_DIR = Path(os.getenv("LOG_DIR", BASE_DIR.parent.parent / "logs" / "telegrambot"))
TEMP_DIR = Path(os.getenv("TEMP_DIR", BASE_DIR.parent.parent / "temp" / "telegrambot"))
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR.parent.parent / "data" / "telegrambot"))
PORT = int(os.getenv("PORT", 5001))
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # 필수

# 디렉토리 생성 (권한 문제 발생 시 명확히 실패)
for d in [LOG_DIR, TEMP_DIR, DATA_DIR]:
    d.mkdir(parents=True, exist_ok=True, mode=0o750)

# 필수 환경변수 검증
REQUIRED = ["TELEGRAM_TOKEN"]
missing = [v for v in REQUIRED if os.getenv(v) is None]
if missing:
    raise RuntimeError(f"Missing required env vars: {missing}")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
```

> **설명**: `BASE_DIR.parent.parent`는 `agora` 루트를 가리킵니다. 개발 환경에서는 상대경로가 기본값으로 사용되며, 운영 환경에서는 환경변수로 절대경로를 주입합니다.

---

## 5. 로깅 정책 (JSONL)

각 앱은 `LOG_DIR/unified.jsonl` 파일에 JSONL 형식으로 로그를 기록합니다.

### 로깅 설정 예시 (Python)

```python
# apps/common/logger.py (각 앱에 복사해서 사용)
import json
import logging
from pathlib import Path

class JsonlFormatter(logging.Formatter):
    def __init__(self, app_name):
        super().__init__()
        self.app_name = app_name

    def format(self, record):
        return json.dumps({
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
            "level": record.levelname,
            "app": self.app_name,
            "message": record.getMessage(),
            # 필요시 추가 필드 (예: request_id)
        })

def setup_logger(app_name, log_dir):
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_dir / "unified.jsonl")
    handler.setFormatter(JsonlFormatter(app_name))
    logger = logging.getLogger(app_name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
```

사용 예:
```python
from config import LOG_DIR
logger = setup_logger("telegrambot", LOG_DIR)
logger.info("Bot started", extra={"chat_id": 12345})
```

### logrotate 설정 (운영 환경)

`/etc/logrotate.d/agora`:

```
/var/log/agora/*/unified.jsonl {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0640 myuser mygroup
    sharedscripts
    postrotate
        # 앱에 로그 파일 재오픈 신호를 보내려면 여기에 추가
        # 예: systemctl reload myapp
    endscript
}
```

---

## 6. PM2 설정 및 watch 자동 재시작 전략

### 6.1. 앱 상태별 watch 설정 권장사항

| 앱 상태 | watch 옵션 | 재시작 방식 | 설명 |
|--------|-----------|------------|------|
| **안정화된 완성 앱** | `watch: true` (단, 불필요한 파일 제외) | 파일 변경 시 자동 재시작 | 개발 중 코드 변경을 즉시 반영 |
| **업데이트 중인 앱** | `watch: false` | syncthing 완료 후 수동 또는 전체 재시작 | 불필요한 재시작 방지 |
| **운영 환경** | `watch: false` | CI/CD 또는 수동 배포 후 재시작 | 안정성 최우선 |

### 6.2. `ecosystem.config.js` 예시

```javascript
const commonEnv = {
  REDIS_URL: 'redis://localhost:6379',
};

module.exports = {
  apps: [
    {
      name: 'telegrambot',
      script: './apps/telegrambot/main.py',
      interpreter: 'python3',
      cwd: './apps/telegrambot',
      watch: true,
      ignore_watch: [
        'logs',
        'temp',
        '.env',
        '__pycache__',
        '*.pyc',
        '../../logs',
        '../../temp'
      ],
      watch_options: {
        followSymlinks: false,
        usePolling: true,   // 파일 시스템 이벤트 불안정 시 사용
      },
      env: {
        ...commonEnv,
        PORT: 5001,
        LOG_DIR: '../../logs/chronicle',
        TEMP_DIR: '../../temp/chronicle',
        DATA_DIR: '../../data/chronicle',
        TELEGRAM_TOKEN: '개발용토큰',
      },
      env_production: {
        LOG_DIR: '/var/log/agora/chronicle',
        TEMP_DIR: '/var/tmp/agora/chronicle',
        DATA_DIR: '/data/agora/chronicle',
        TELEGRAM_TOKEN: process.env.TELEGRAM_TOKEN,  // 시스템 환경변수 참조
      },
      error_file: '/dev/null',   // PM2 자체 로그 비활성화
      out_file: '/dev/null',
    },
    // chronicle, lean, omnibot 등 동일 패턴 반복
  ],
};
```

> **참고**: `pm2 start ecosystem.config.js --env production`으로 운영 환경 설정 적용 가능.

---

## 7. syncthing 연동 및 재시작 전략

파일 동기화(syncthing)로 업데이트하는 환경에서는 `watch: true` 대신 syncthing 완료 후 재시작합니다.

### 7.1. syncthing 폴더 완료 후 명령 실행
syncthing 웹 UI에서 해당 폴더의 **"폴더 완료 후 명령 실행"** 에 등록:

```bash
cd /home/user/agora && pm2 restart ecosystem.config.js
```

### 7.2. 특정 앱만 재시작
```bash
cd /home/user/agora && pm2 restart lean omnibot
```

---

## 8. 앱 간 통신 명세 (느슨한 결합)

| 앱 | 제공 기능 | 통신 방식 | 상세 |
|----|----------|-----------|------|
| **telegrambot** | 사용자 메시지 수신/응답 | HTTP API, Redis | - `POST /api/message` (body: `{ chat_id, text }`)<br>- Redis 구독 `telegram:outgoing`으로 응답 발행 |
| **chronicle** | 데이터 저장/조회 | HTTP API, Redis 큐 | - `GET /api/entries?date=YYYY-MM-DD`<br>- Redis 큐 `chronicle:process`로 데이터 처리 요청 |
| **lean** | 토큰 최적화 | Redis 큐 | - `lean:optimize` 큐 요청, 결과는 `lean:result` 큐 반환 |
| **omnibot** | 웹 대화 수집 | Redis 큐, 공유 폴더 | - `omnibot:collect` 큐 요청, 결과는 `data/exchange/`에 저장 후 Redis 알림 |

**Redis 메시지 예시**:
```json
{
  "msg_id": "uuid-1234",
  "timestamp": "2025-03-18T10:00:01Z",
  "type": "optimize_request",
  "payload": { "text": "...", "options": {} }
}
```

**공유 폴더 규칙**:
- 파일명: `{앱명}_{YYYYMMDD}_{HHMMSS}.json`
- 저장 후 Redis 채널 `exchange:new`에 알림

---

## 9. ignore 파일 가이드

### 9.1. `.gitignore` 핵심 내용
- OS 생성 파일 (`.DS_Store`, `Thumbs.db`)
- IDE 설정 (`.vscode/`, `.idea/`)
- Python 캐시 (`__pycache__/`, `*.pyc`)
- 가상환경 (`venv/`, `.venv/`)
- 환경변수 파일 (`.env`)
- 데이터/로그/임시 디렉토리 (`data/`, `logs/`, `temp/`)
- 테스트 파일 패턴 (선택사항):
  ```
  test_*.*
  *_test.*
  *_test_*.*
  ```
  > **참고**: 테스트 코드 자체를 제외하려면 추가, 보통은 테스트 실행 결과물만 제외 권장.

### 9.2. `.stignore` 핵심 내용
- `.stignore` 자체는 동기화 대상에 포함(절대 제외 금지)
- `logs/`, `temp/`, `data/`, `.env` 제외
- OS 임시 파일 및 캐시 제외

> 자세한 내용은 각 ignore 파일을 직접 참조하세요.

---

## 10. 개발 환경 설정 (맥북)

1. 각 앱 디렉토리로 이동하여 가상환경 생성 및 패키지 설치
2. `.env` 파일 생성 (각 앱 디렉토리에)
3. Redis 설치 및 실행: `brew install redis && redis-server`
4. PM2로 앱 실행:
   ```bash
   cd /path/to/agora
   pm2 start ecosystem.config.js
   ```

---

## 11. 운영 환경 배포 순서

1. 서버에 프로젝트 클론 (git 또는 syncthing)
2. 전용 서비스 계정 생성 및 디렉토리 권한 설정:
   ```bash
   sudo useradd -m -s /bin/bash agora
   sudo mkdir -p /var/log/agora /var/tmp/agora /data/agora
   sudo chown -R agora:agora /var/log/agora /var/tmp/agora /data/agora
   sudo chmod 750 /var/log/agora /var/tmp/agora /data/agora
   ```
3. Redis 설치 및 실행 (로컬 바인딩, 암호 설정 권장)
4. `ecosystem.config.js`에 운영 환경변수 설정 (시스템 환경변수 참조)
5. `agora` 계정으로 PM2 앱 시작:
   ```bash
   sudo -u agora pm2 start ecosystem.config.js --env production
   sudo -u agora pm2 save
   sudo -u agora pm2 startup
   ```
6. logrotate 설정 확인
7. 모니터링 도구에 `/health` 엔드포인트 등록

---

## 12. 보안 체크리스트

- [ ] `.gitignore`에 `.env`, `data/`, `logs/`, `temp/`, 테스트 패턴 등 포함 확인
- [ ] 각 앱의 `.env` 파일 권한 `600`
- [ ] 운영 환경에서는 `.env` 파일 사용 금지, 시스템 환경변수로 대체
- [ ] Redis는 `bind 127.0.0.1` 및 암호 설정, 방화벽 차단
- [ ] 운영 서버는 root 계정 사용 금지, 전용 서비스 계정(`agora`) 사용
- [ ] PM2 프로세스는 `agora` 계정으로 실행
- [ ] 로그 출력 시 민감 정보(비밀번호, 토큰) 마스킹 처리
- [ ] 정기적인 보안 업데이트 및 취약점 점검

---

## 13. 단계별 적용 계획 (실무적 로드맵)

### 1단계: 지금 바로 적용 (최소 실무 안정성 확보)
- 각 앱별 `.env` 관리 (개발 환경)
- 운영 환경에서는 시스템 환경변수만 사용(PM2, systemd 등으로 주입)
- `.gitignore`에 `.env`, `data/`, `logs/`, `temp/`, 테스트 파일 패턴 등 포함(이미 적용)
- 전용 서비스 계정 생성 및 디렉토리 권한 설정(운영 서버)
- 각 앱의 `config.py`에서 환경변수 우선, 없으면 안전한 기본값(상대경로) 사용
- 민감 정보는 코드/설정에 직접 쓰지 않고 반드시 환경변수로만 관리

### 2단계: 프로젝트 안정화 후 (운영 자동화/모니터링)
- health check 엔드포인트 확장(DB/Redis 연결 상태, 큐 길이 등)
- 장애/이벤트 발생 시 중앙 알림(텔레그램 봇 등) 연동
- pre-commit 훅(lint, test) 도입으로 코드 품질 자동화

### 3단계: 프로젝트 확장/팀 협업 시
- CI/CD 도입 (GitHub Actions, GitLab CI)
- 비밀 관리 서비스(Vault, AWS Secrets Manager) 연동
- 문서화 자동화 도구(MkDocs, Sphinx) 도입

> **핵심**: 1단계만 적용해도 실무적으로 매우 안전하며, 이후 프로젝트 성장에 따라 2~3단계를 점진적으로 도입하면 됩니다.

---

## 14. 결론

이 가이드를 따라 `agora` 프로젝트를 구성하면 확장성, 유지보수성, 보안이 뛰어난 시스템을 구축할 수 있습니다.  
특히 1단계 항목을 먼저 적용하여 안정적인 기반을 마련하고, 필요에 따라 단계적으로 고도화해 나가시기 바랍니다.

**문서 버전**: 2.0 (최종판)  
**최종 업데이트**: 2025년 3월
```