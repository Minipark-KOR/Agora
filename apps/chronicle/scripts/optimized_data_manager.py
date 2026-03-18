import subprocess

import os
import json
from pathlib import Path
from datetime import datetime

TITLE_LIST_PATH = Path(__file__).parent.parent / "config/title_list.json"
OPTIMIZED_DIR = Path(__file__).parent.parent / "optimized"
MAX_FILE_SIZE_MB = 10

# 파일명 넘버링: 01, 02 형식
PART_FORMAT = "_{:02d}"

# 객체 구조 예시
# {
#   "year": 2026,
#   "month": 3,
#   "step": 1,
#   "user": "...",
#   "assistant": "...",
#   "reason": "...",
#   "branch": [ {...}, ... ]
# }

def load_title_list():
    with open(TITLE_LIST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_file_path(title, part=1):
    base = OPTIMIZED_DIR / f"{title}.jsonl"
    if part > 1:
        return OPTIMIZED_DIR / f"{title}{PART_FORMAT.format(part)}.jsonl"
    return base

def save_jsonl(title, data):
    part = 1
    file_path = get_file_path(title, part)
    buffer = []
    size = 0
    for obj in data:
        line = json.dumps(obj, ensure_ascii=False)
        size += len(line.encode("utf-8"))
        buffer.append(line)
        if size >= MAX_FILE_SIZE_MB * 1024 * 1024:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(buffer) + "\n")
            part += 1
            file_path = get_file_path(title, part)
            buffer = []
            size = 0
    if buffer:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(buffer) + "\n")

def vacuum(data):
    seen = set()
    result = []
    for obj in data:
        key = json.dumps(obj, sort_keys=True, ensure_ascii=False)
        if key.strip() and key not in seen:
            seen.add(key)
            result.append(obj)
    return result

def retry_unknown(data, title_list):
    unknown_data = [obj for obj in data if obj.get("title") == "unknown"]
    return unknown_data

def send_telegram_message(message):
    """
    run_bot.py를 subprocess로 호출하여 메시지 전송
    message: str (보낼 텍스트)
    """
    try:
        subprocess.run([
            "python3",
            str(Path.home() / "bots/telegram_bot/run_bot.py"),
            "--send",
            message
        ], check=True)
    except Exception as e:
        print(f"텔레그램 메시지 전송 실패: {e}")


def merge_files(title):
    files = sorted(OPTIMIZED_DIR.glob(f"{title}*.jsonl"))
    merged = []
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    merged.append(obj)
                except Exception:
                    continue
    return vacuum(merged)

def main():
    title_list = load_title_list()
    for title in title_list:
        merged = merge_files(title)
        save_jsonl(title, merged)
    # unknown retry 예시
    unknown_data = retry_unknown(merge_files("unknown"), title_list)
    # unknown 데이터 푸쉬 예시 (최대 5개만)
    for obj in unknown_data[:5]:
        msg = f"[unknown] {obj.get('user', '')}\n{obj.get('assistant', '')}"
        send_telegram_message(msg)

if __name__ == "__main__":
    main()
