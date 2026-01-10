#!/usr/bin/env -S uv run --script
# Script at /whoami/whoami.py in this repository, https://github.com/isotopp/uv-class
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx>=0.28",
# ]
# ///

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import httpx

def main() -> None:
    with httpx.Client(timeout=10.0) as client:
        r = client.get("https://httpbin.org/get")
        r.raise_for_status()


    print(f"Your apparent IP: {r.json().get('origin', 'unknown')}")

if __name__ == "__main__":
    main()

