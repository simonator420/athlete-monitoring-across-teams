from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import pandas as pd


def _is_retryable(error: OSError) -> bool:
    return isinstance(error, TimeoutError) or getattr(error, "errno", None) in {35, 60}


def write_csv(frame: pd.DataFrame, path: Path, retries: int = 5, delay: float = 2.0, **kwargs: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    last_error: OSError | None = None
    for attempt in range(retries):
        try:
            frame.to_csv(path, **kwargs)
            return
        except OSError as error:
            last_error = error
            if not _is_retryable(error) or attempt == retries - 1:
                raise
            wait = delay * (attempt + 1)
            print(f"Write timed out for {path}; retrying in {wait:.0f}s...", flush=True)
            time.sleep(wait)
    if last_error is not None:
        raise last_error


def write_text(path: Path, text: str, retries: int = 5, delay: float = 2.0, **kwargs: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    last_error: OSError | None = None
    for attempt in range(retries):
        try:
            path.write_text(text, **kwargs)
            return
        except OSError as error:
            last_error = error
            if not _is_retryable(error) or attempt == retries - 1:
                raise
            wait = delay * (attempt + 1)
            print(f"Write timed out for {path}; retrying in {wait:.0f}s...", flush=True)
            time.sleep(wait)
    if last_error is not None:
        raise last_error
