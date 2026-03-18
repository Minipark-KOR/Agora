# optimized_data_manager 사용법 및 데이터 구조 예시

## 타이틀 리스트
- config/title_list.json에서 관리
- 예시: dev, news, health, economy, stock, forex, realestate, retire, edu, travel, hobby, world, unknown

## 데이터 구조 예시 (jsonl)
각 줄마다 아래와 같은 객체가 저장됨:

```
{
  "year": 2026,
  "month": 3,
  "step": 1,
  "title": "dev",
  "user": "파이썬에서 리스트를 정렬하는 방법 알려줘.",
  "assistant": "sorted() 함수를 사용하면 리스트를 정렬할 수 있습니다.",
  "reason": "sorted()는 파이썬 내장 함수로 초보자도 쉽게 사용할 수 있기 때문입니다.",
  "branch": [
    {
      "user": "내림차순으로 정렬하려면?",
      "assistant": "sorted(my_list, reverse=True)로 내림차순 정렬이 가능합니다.",
      "reason": "reverse=True 옵션을 사용하면 내림차순이 됩니다."
    }
  ]
}
```

- unknown 타이틀은 "title": "unknown"으로 자동 분류
- optimized 폴더에 타이틀별로 저장, 10MB 넘으면 part 넘버링(01, 02...)
- vacuum(중복/불필요 데이터 제거), retry(unknown 분류), 병합(파일 합치기) 자동화

## 관리 규칙
- 모든 데이터는 UTF-8, LF 줄바꿈, 표준 jsonl 포맷
- vacuum, retry, 병합 등 자동화 스크립트에서 관리
- unknown 데이터는 텔레그램으로 푸쉬, 사용자가 분류하면 규칙에 자동 반영
## 임시파일 관리 및 자동 정리
예시:
```bash
python scripts/cleanup_temp_files.py
```
스케줄러 예시(cron):
```
0 3 * * * /Users/minipark4u/project/agora/apps/chronicle/.venv/bin/python /Users/minipark4u/project/agora/apps/chronicle/scripts/cleanup_temp_files.py
```
# chronicle LLM 데이터 파이프라인 가이드 (2026-03-16)

## 폴더 구조 및 데이터 흐름
```
chronicle/
├── scripts/           # 데이터 처리/정제/분석 코드
├── data/
│   ├── raw/           # 원본 데이터 (실시간/Drive 등에서 수집)
│   ├── processed/     # 정제·최종본 (LLM 학습/분석용)
│   ├── refined/       # 추가 가공본 (실험/후처리)
│   ├── logs/          # 실행/분석 로그
│   └── state/         # 처리 이력, resume, 중복 방지
```

1. 원본(raw) → scripts/process_raw_chat_snapshots.py 실행 → processed/에 chat_ko_review.jsonl, chat_manifest.json 등 생성
2. processed/ 폴더는 Google Drive와 동기화 (최신본만 업로드)
3. refined/ 폴더는 추가 실험·후처리 결과 저장
4. state/ 폴더는 처리 이력, 중복 방지, resume 정보 관리
5. logs/ 폴더는 실행/분석 로그 저장

## 데이터 읽기/쓰기 정책
- LLM 학습/분석/추론 시에는 반드시 processed/ 폴더(최신본)만 읽음
- Google Drive에서 최신 processed/만 받아 사용 (raw, backup 등은 무시)
- 필요시 날짜/버전별로 processed/ 데이터 관리(롤백/이력 추적)
- refined/는 실험·후처리 결과만 사용

## state 관리
- 데이터 처리/동기화 진행상황(state)은 별도 state/ 폴더에 저장
- 예시: processed/state/raw_process_state.json (처리 이력, 중복 방지, resume)
- state는 최종 데이터와 분리하여 관리

## 장점
- 데이터 혼선/중복/실수 방지, 협업·자동화·백업 효율적
- 실험/정제/학습 환경 분리로 관리 용이
- 코드(automation)는 git 등으로 버전 관리

## 주요 예시
- 정제 스크립트 실행:
  ```bash
  python scripts/process_raw_chat_snapshots.py --raw-dir data/raw/ --output-dir data/processed/
  ```
- unknown 토큰 분석:
  ```bash
  python scripts/unknown_token_analyzer.py --vocab vocab_test.txt --input data/processed/chat_ko_review.jsonl
  ```
- state 파일 관리:
  - 처리 이력: data/state/raw_process_state.json
  - 중복 방지: .seen_hashes.jsonl
  - resume: state 정보 활용
- processed/ 폴더 주요 파일:
  - chat_ko_review.jsonl: 정제된 대화 데이터
  - chat_manifest.json: 생성 이력/메타
  - chat_en.jsonl: 영문 요약본 (옵션)
  - 날짜별 파일: chat_daily_YYYY-MM-DD.json 등

---

---
이 가이드와 구조를 따르면, chronicle LLM 데이터 파이프라인을 안전하고 효율적으로 운영할 수 있습니다.
