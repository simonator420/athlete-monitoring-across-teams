from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


def markdown_table(frame: pd.DataFrame, max_rows: int | None = None) -> str:
    if max_rows is not None:
        frame = frame.head(max_rows)
    if frame.empty:
        return "_No rows._"

    display = frame.copy()
    display.columns = [str(col) for col in display.columns]
    rows: list[list[str]] = [list(display.columns)]
    for values in display.astype(object).itertuples(index=False, name=None):
        rows.append(["" if pd.isna(value) else str(value) for value in values])

    widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]

    def fmt(row: Iterable[str]) -> str:
        return "| " + " | ".join(str(value).ljust(widths[i]) for i, value in enumerate(row)) + " |"

    header = fmt(rows[0])
    sep = "| " + " | ".join("-" * width for width in widths) + " |"
    body = [fmt(row) for row in rows[1:]]
    return "\n".join([header, sep, *body])
