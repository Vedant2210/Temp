import json
import os
import time
import logging
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def save_json(path: str, data: Any):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(path: str):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_checkpoint(project: str, last_index: int):
    save_json(f"data/{project}_checkpoint.json", {"last_index": last_index})

def load_checkpoint(project: str):
    ckpt = load_json(f"data/{project}_checkpoint.json")
    return ckpt["last_index"] if ckpt else 0

def retry_request(session, url, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = session.get(url, timeout=10)
            if response.status_code == 429:  # rate limit
                logging.warning("Rate limited, waiting...")
                time.sleep(30)
                continue
            response.raise_for_status()
            return response
        except Exception as e:
            logging.warning(f"Attempt {attempt+1} failed: {e}")
            time.sleep(delay)
    return None
