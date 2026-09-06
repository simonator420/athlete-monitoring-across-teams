from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
_LOCAL_PROCESSED_DIR = DATA_DIR / "processed"
_RELEASE_PROCESSED_DIR = DATA_DIR / "processed_release"
_DEFAULT_PROCESSED_DIR = _LOCAL_PROCESSED_DIR if _LOCAL_PROCESSED_DIR.exists() else _RELEASE_PROCESSED_DIR
PROCESSED_DIR = Path(os.environ.get("SOCCERMON_PROCESSED_DIR", _DEFAULT_PROCESSED_DIR))
REPORTS_DIR = PROJECT_ROOT / "reports"
TMP_DIR = Path(os.environ.get("SOCCERMON_TMP_DIR", PROJECT_ROOT / "tmp"))


def ensure_project_dirs() -> None:
    for path in [DATA_DIR, PROCESSED_DIR, REPORTS_DIR, TMP_DIR]:
        path.mkdir(parents=True, exist_ok=True)
