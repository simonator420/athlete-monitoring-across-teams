#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from soccermon.config import PROCESSED_DIR, REPORTS_DIR, ensure_project_dirs
from soccermon.io import write_csv, write_text
from soccermon.markdown import markdown_table
from soccermon.modeling import evaluate_models, feature_blocks


def main() -> None:
    ensure_project_dirs()
    path = PROCESSED_DIR / "core_subjective_cohort.csv"
    if not path.exists():
        raise FileNotFoundError(f"Run scripts/04_build_linkage_and_core_cohort.py first: {path}")

    data = pd.read_csv(path, parse_dates=["date"])
    blocks = feature_blocks(data)
    subjective_cols = blocks["wellness"] + blocks["subjective_load"]
    rows: list[dict[str, object]] = []
    temporal_cutoff = pd.Timestamp("2021-01-01")
    rows.extend(
        evaluate_models(
            "temporal_2020_train_2021_test",
            data[data["date"] < temporal_cutoff],
            data[data["date"] >= temporal_cutoff],
            subjective_cols,
        )
    )
    rows.extend(
        evaluate_models("cross_team_train_A_test_B", data[data["team"] == "TeamA"], data[data["team"] == "TeamB"], subjective_cols)
    )
    rows.extend(
        evaluate_models("cross_team_train_B_test_A", data[data["team"] == "TeamB"], data[data["team"] == "TeamA"], subjective_cols)
    )

    results = pd.DataFrame.from_records(rows)
    results["n"] = results["n"].astype(int)
    results = results.sort_values(["split", "mae", "rmse"]).reset_index(drop=True)
    write_csv(results, PROCESSED_DIR / "subjective_baseline_results.csv", index=False)

    report = f"""# Subjective Baseline Results

These are first-pass baseline models on the audited core subjective cohort only.
They do not include objective GPS features yet.

## Results

{markdown_table(results.round(3))}

## Features

{", ".join(subjective_cols)}
"""
    write_text(REPORTS_DIR / "subjective_baselines.md", report, encoding="utf-8")
    print(f"Wrote {PROCESSED_DIR / 'subjective_baseline_results.csv'}")
    print(f"Wrote {REPORTS_DIR / 'subjective_baselines.md'}")


if __name__ == "__main__":
    main()
