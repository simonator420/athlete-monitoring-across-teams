#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from soccermon.config import PROCESSED_DIR, REPORTS_DIR, ensure_project_dirs
from soccermon.io import write_csv, write_text
from soccermon.markdown import markdown_table


SHIFT_VARIABLES = [
    "readiness",
    "readiness_t_plus_1",
    "fatigue",
    "fatigue_t_plus_1",
    "soreness",
    "soreness_t_plus_1",
    "mood",
    "stress",
    "sleep_quality",
    "sleep_duration",
    "session_count",
    "session_srpe_sum",
    "session_duration_sum",
    "session_rpe_mean",
    "readiness_past_3d_mean",
    "readiness_past_7d_mean",
    "session_srpe_sum_past_7d_sum",
    "session_srpe_sum_past_28d_sum",
    "objective_duration_min",
    "objective_distance_m",
    "objective_distance_m_per_min",
    "objective_hsr_distance_m",
    "objective_hsr_m_per_min",
    "objective_sprint_distance_m",
    "objective_sprint_m_per_min",
    "objective_speed_max",
    "objective_accel_distance_m",
    "objective_decel_distance_m",
]


def standardized_mean_difference(frame: pd.DataFrame, group_col: str, positive_value: object, variables: list[str]) -> pd.DataFrame:
    rows = []
    mask = frame[group_col] == positive_value
    for variable in variables:
        if variable not in frame.columns:
            continue
        exposed = pd.to_numeric(frame.loc[mask, variable], errors="coerce").dropna()
        reference = pd.to_numeric(frame.loc[~mask, variable], errors="coerce").dropna()
        if exposed.empty or reference.empty:
            continue
        pooled = np.sqrt((exposed.var(ddof=1) + reference.var(ddof=1)) / 2)
        smd = (exposed.mean() - reference.mean()) / pooled if pooled and np.isfinite(pooled) else np.nan
        rows.append(
            {
                "comparison": f"{group_col}_{positive_value}_vs_other",
                "variable": variable,
                "n_positive": int(exposed.size),
                "n_reference": int(reference.size),
                "mean_positive": float(exposed.mean()),
                "mean_reference": float(reference.mean()),
                "smd": float(smd),
                "abs_smd": float(abs(smd)) if np.isfinite(smd) else np.nan,
            }
        )
    columns = [
        "comparison",
        "variable",
        "n_positive",
        "n_reference",
        "mean_positive",
        "mean_reference",
        "smd",
        "abs_smd",
    ]
    if not rows:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame.from_records(rows, columns=columns).sort_values("abs_smd", ascending=False)


def main() -> None:
    ensure_project_dirs()
    core_path = PROCESSED_DIR / "core_subjective_cohort.csv"
    objective_path = PROCESSED_DIR / "objective_player_day_features.csv"
    cohort_path = PROCESSED_DIR / "multimodal_modeling_cohort.csv"
    for path in [core_path, objective_path, cohort_path]:
        if not path.exists():
            raise FileNotFoundError(f"Missing required processed file: {path}")

    core = pd.read_csv(core_path, parse_dates=["date"])
    cohort = pd.read_csv(cohort_path, parse_dates=["date"])
    objective = pd.read_csv(objective_path, parse_dates=["date"])
    gps_keys = cohort[["date", "team", "player_id"]].drop_duplicates()
    gps_keys["has_gps"] = True
    core = core.merge(gps_keys, on=["date", "team", "player_id"], how="left")
    core["has_gps"] = core["has_gps"].eq(True)

    core_summary = (
        core.assign(year=core["date"].dt.year)
        .groupby(["team", "year"], as_index=False)
        .agg(core_rows=("player_id", "size"), players=("player_id", "nunique"))
    )
    gps_summary = (
        cohort.assign(year=cohort["date"].dt.year)
        .groupby(["team", "year"], as_index=False)
        .agg(gps_rows=("player_id", "size"), gps_players=("player_id", "nunique"))
    )
    table1 = core_summary.merge(gps_summary, on=["team", "year"], how="left").fillna(0)
    table1["gps_share_pct"] = (table1["gps_rows"] / table1["core_rows"] * 100).round(1)
    write_csv(table1, PROCESSED_DIR / "table1_cohort_summary.csv", index=False)

    coverage = (
        objective.assign(year=objective["date"].dt.year)
        .groupby(["team", "year"], as_index=False)
        .agg(
            objective_player_days=("player_id", "size"),
            objective_players=("player_id", "nunique"),
            median_distance_m=("objective_distance_m", "median"),
            median_duration_min=("objective_duration_min", "median"),
            median_hr_coverage=("objective_heart_rate_coverage", "median"),
        )
        .round(3)
    )
    write_csv(coverage, PROCESSED_DIR / "objective_coverage_by_team_year.csv", index=False)

    gps_selection = standardized_mean_difference(core, "has_gps", True, SHIFT_VARIABLES)
    write_csv(gps_selection, PROCESSED_DIR / "gps_selection_smd.csv", index=False)
    team_shift_core = standardized_mean_difference(core, "team", "TeamA", SHIFT_VARIABLES)
    team_shift_core["sample"] = "core_subjective_cohort"
    team_shift_matched = standardized_mean_difference(cohort, "team", "TeamA", SHIFT_VARIABLES)
    team_shift_matched["sample"] = "gps_matched_cohort"
    team_shift = pd.concat([team_shift_core, team_shift_matched], ignore_index=True)
    write_csv(team_shift, PROCESSED_DIR / "team_shift_smd.csv", index=False)

    report = f"""# Descriptive Tables

## Cohort Summary

{markdown_table(table1)}

## Objective Coverage And Training Characteristics

{markdown_table(coverage)}

## GPS Selection SMD

{markdown_table(gps_selection.round(3), max_rows=20)}

## Team Shift SMD

{markdown_table(team_shift.round(3), max_rows=20)}
"""
    write_text(REPORTS_DIR / "descriptive_tables.md", report, encoding="utf-8")
    print(f"Wrote {PROCESSED_DIR / 'table1_cohort_summary.csv'}")
    print(f"Wrote {PROCESSED_DIR / 'objective_coverage_by_team_year.csv'}")
    print(f"Wrote {PROCESSED_DIR / 'gps_selection_smd.csv'}")
    print(f"Wrote {PROCESSED_DIR / 'team_shift_smd.csv'}")
    print(f"Wrote {REPORTS_DIR / 'descriptive_tables.md'}")


if __name__ == "__main__":
    main()
