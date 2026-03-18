# Drive API Sync Setup (No Desktop App)

이 문서는 Google Drive 앱 설치 없이 API만으로 동기화하는 방법입니다.

## 1) 서비스 계정 키 파일 준비
- Google Cloud Console에서 서비스 계정 생성
- JSON 키 다운로드
- 아래 경로에 저장
  - /Users/minipark4u/app/chronicle/config/drive-service-account.json

## 2) Drive 폴더 2개 준비
- incoming 폴더: 로컬 로그 업로드 대상
- processed 폴더: 서버 처리 결과 저장 대상

## 3) 폴더 공유
- 서비스 계정 이메일에 두 폴더 모두 편집 권한 공유
- 서비스 계정 이메일은 아래 명령으로 확인 가능
  - ./scripts/misc/setup_workspace_backup_launchd.sh check-drive-config

## 4) 폴더 ID 입력
- config/drive_sync.json 파일 수정
  - incoming_folder_id
  - processed_folder_id

## 5) 설정 검증
- 아래 명령 실행
  - ./scripts/misc/setup_workspace_backup_launchd.sh check-drive-config

성공 시 다음 메시지가 표시됩니다.
- OK: Drive sync configuration is valid

## 6) 수동 동기화 테스트
- ./scripts/misc/setup_workspace_backup_launchd.sh run-drive-sync-once

## 7) 자동 실행 상태 확인
- ./scripts/misc/setup_workspace_backup_launchd.sh status

Drive sync 항목이 보여야 정상입니다.
- com.hidunkey.chat-drive-sync

## 저장소 역할 분리 정책
  - Google Drive: chat_backup/daily 업로드/다운로드 관리
- OneDrive: raw 원본 업로드 전용 관리

## OneDrive raw 업로드 + 로컬 7일 보관

기본 원격 저장 경로:
chronicle/

### 1) 설정 파일 준비
- 기본 파일: config/onedrive_raw_sync.json
- 예시 파일: config/onedrive_raw_sync.example.json

필수 항목:
- tenant_id
- client_id
- client_secret
- drive_id

기본 정책:
- retention_days = 7
- delete_uploaded_only = true

의미:
- 업로드가 확인된 raw 파일만, 로컬에서 7일 지난 뒤 삭제

### 2) 수동 실행 테스트
- ./scripts/misc/setup_workspace_backup_launchd.sh run-onedrive-raw-once

설정 점검:
- ./scripts/misc/setup_workspace_backup_launchd.sh check-onedrive-config

drive_id 찾기:
- ./scripts/misc/setup_workspace_backup_launchd.sh list-onedrive-drives

출력 지표:
- upload_scanned / upload_uploaded
- prune_scanned / prune_deleted / prune_skipped_not_uploaded

### 3) 자동 실행 상태 확인
- ./scripts/misc/setup_workspace_backup_launchd.sh install
- ./scripts/misc/setup_workspace_backup_launchd.sh status

OneDrive raw 항목이 보여야 정상입니다.
- com.hidunkey.chat-onedrive-raw

## 권장 로컬 데이터 경로
 /Users/minipark4u/app/chronicle/data/daily
 /Users/minipark4u/app/chronicle/data/daily
 /Users/minipark4u/app/chronicle/data/processed_from_drive
 /Users/minipark4u/app/chronicle/data/state
 /Users/minipark4u/app/chronicle/data/logs
