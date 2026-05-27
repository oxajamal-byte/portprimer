from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path


def safe_target_name(target: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9]+", "-", target.strip()).strip("-")
    return safe or "target"


def utc_timestamp() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def filename_timestamp() -> str:
    return datetime.utcnow().strftime("%Y%m%d-%H%M")


def ensure_reports_dir(path: Path = Path("reports")) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path
