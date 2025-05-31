#!/usr/bin/env python3

import json
import os
import re
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

API_KEY = os.getenv("N8N_API_KEY")
BASE_URL = os.getenv("N8N_BASE_URL", "http://localhost:5678")
EXPORT_DIR = Path("exported_workflows")
HEADERS = {"X-N8N-API-KEY": API_KEY, "accept": "application/json"}

if not API_KEY:
    raise ValueError("❌ N8N_API_KEY is not set in .env")

EXPORT_DIR.mkdir(exist_ok=True)


def sanitize_filename(name):
    # Replace spaces and special characters with underscores
    return re.sub(r"[^a-zA-Z0-9_-]", "_", name)


def main():
    try:
        response = requests.get(f"{BASE_URL}/api/v1/workflows", headers=HEADERS)
        response.raise_for_status()
        workflows = response.json().get("data", [])

        for wf in workflows:
            if wf.get("isArchived", False):
                continue  # Skip archived workflows

            wf_id = wf["id"]
            detail_resp = requests.get(
                f"{BASE_URL}/api/v1/workflows/{wf_id}", headers=HEADERS
            )
            detail_resp.raise_for_status()
            detail = detail_resp.json()

            name = detail.get("name", f"workflow_{wf_id}")
            safe_name = sanitize_filename(name)
            file_path = EXPORT_DIR / f"{safe_name}.json"

            with open(file_path, "w") as f:
                json.dump(detail, f, indent=2)

            print(f"✅ Saved: {file_path}")

        print(f"\n🎉 All active, non-archived workflows exported to '{EXPORT_DIR}'")

    except requests.RequestException as e:
        print(f"❌ Request error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
