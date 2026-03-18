
# 📘 lean 앱 (agora) & token_utils 라이브러리

이 앱은 토큰 최적화 및 메시지 전처리(token_utils.py) 기능을 담당합니다.

- 표준 환경변수/경로/구조는 agora 루트 README.md를 따릅니다.
- config.py에서 LOG_DIR, TEMP_DIR, DATA_DIR, REDIS_URL 등 환경변수 사용
- 개발/운영 환경 모두 동일한 구조로 관리

## 폴더 구조
 데이터: agora/data/lean/

- 실제 운영은 시스템 환경변수 권장

## 개발/운영 가이드
- 자세한 내용은 agora/README.md 참고

---

# 📘 token_utils — Token Optimization & Message Preprocessing Toolkit

이 라이브러리는 AI 대화 시스템에서 **토큰 비용을 줄이고 메시지를 안정적으로 전처리**하기 위해 설계되었습니다.

## ✨ 주요 기능
- `[THOUGHT]…[/THOUGHT]` 구간 자동 추출 및 분리
- 메시지 content 정제(clean)
- 멀티모달 메시지(text/image 혼합) 처리
- tiktoken 기반 정확한 토큰 계산 (미설치 시 fallback)
- 내부 필드(reasoning 등) 자동 제거

## 주요 함수 예시
```python
from token_utils import (
	process_messages_for_token_saving,
	strip_internal_fields,
	count_tokens,
)

raw = [
	{
		"role": "user",
		"content": [
			{"type": "text", "text": "hello [THOUGHT]x[/THOUGHT] world"},
			{"type": "image_url", "image_url": {"url": "..."}},
		],
	}
]

# 1) 정제 + reasoning 추출
processed = process_messages_for_token_saving(raw, return_reasoning_list=True)

# 2) 전송 전 내부 필드 제거
ready = strip_internal_fields(processed)

# 3) 토큰 확인
tokens = count_tokens(ready)
print(ready)
print("tokens =", tokens)
```

## 테스트
```bash
python test_token_utils.py
```

## 참고
- Python 3.8 이상 권장, tiktoken(선택)
- 자세한 함수 설명 및 정책은 token_utils.py, test_token_utils.py 참고
