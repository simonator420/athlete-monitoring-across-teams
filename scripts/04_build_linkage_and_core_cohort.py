#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from soccermon.config import PROCESSED_DIR, REPORTS_DIR, ensure_project_dirs
from soccermon.io import write_csv, write_text
from soccermon.markdown import markdown_table
from soccermon.modeling import add_transparent_history_features


def main() -> None:
    ensure_project_dirs()
    source = PROCESSED_DIR / "subjective_player_day.csv"
    if not source.exists():
        raise FileNotFoundError(f"Run scripts/01_audit_subjective.py first: {source}")

    data = pd.read_csv(source, parse_dates=["date"])
    data = add_transparent_history_features(data)
    core = data.dropna(subset=["team", "date", "player_id", "readiness", "readiness_t_plus_1"]).copy()
    core["year"] = core["date"].dt.year
    write_csv(core, PROCESSED_DIR / "core_subjective_cohort.csv", index=False)

    by_team_year = (
        core.groupby(["team", "year"], as_index=False)
        .agg(core_rows=("player_id", "size"), players=("player_id", "nunique"))
        .sort_values(["team", "year"])
    )
    report = f"""# Linkage And Core Cohort

## Outputs

- Subjective player-day rows: {len(data):,}
- Historical wellness/load variables calculated on full subjective longitudinal data before outcome/GPS filtering.
- Core next-day readiness rows: {len(core):,}
- Core players: {core["player_id"].nunique():,}
- Date range: {core["date"].min().date()} to {core["date"].max().date()}

## Core Rows By Team And Year

{markdown_table(by_team_year)}
"""
    write_text(REPORTS_DIR / "linkage_audit.md", report, encoding="utf-8")
    print(f"Wrote {PROCESSED_DIR / 'core_subjective_cohort.csv'}")
    print(f"Wrote {REPORTS_DIR / 'linkage_audit.md'}")


if __name__ == "__main__":
    main()
