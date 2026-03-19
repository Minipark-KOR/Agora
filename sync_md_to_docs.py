import os
import json
from glob import glob

# 루트 경로 설정 (agora 폴더 기준)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APPS_DIR = os.path.join(BASE_DIR, "apps")
DOCS_DIR = os.path.join(BASE_DIR, "Docs")

# Docs 폴더가 없으면 생성
os.makedirs(DOCS_DIR, exist_ok=True)

def find_md_files(apps_dir):
    md_files = []
    for app_name in os.listdir(apps_dir):
        app_path = os.path.join(apps_dir, app_name)
        if os.path.isdir(app_path):
            # 앱 폴더 내 모든 md 파일 탐색 (서브폴더 포함)
            for root, _, files in os.walk(app_path):
                for file in files:
                    if file.lower().endswith(".md"):
                        md_files.append((app_name, os.path.join(root, file)))
    return md_files

def sync_md_to_docs():
    md_files = find_md_files(APPS_DIR)
    for app_name, md_path in md_files:
        file_name = os.path.splitext(os.path.basename(md_path))[0]
        json_name = f"{app_name}.{file_name}.json"
        json_path = os.path.join(DOCS_DIR, json_name)
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        data = {"content": content}
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Synced: {json_path}")

if __name__ == "__main__":
    sync_md_to_docs()
    print("모든 md 파일이 Docs 폴더에 json으로 변환되어 저장되었습니다.")
