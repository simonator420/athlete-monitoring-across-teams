#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from soccermon.config import PROCESSED_DIR, REPORTS_DIR, ensure_project_dirs
from soccermon.io import write_csv, write_text
from soccermon.markdown import markdown_table


def main() -> None:
    ensure_project_dirs()
    subjective_path = PROCESSED_DIR / "core_subjective_cohort.csv"
    objective_path = PROCESSED_DIR / "objective_session_features.csv"
    if not subjective_path.exists():
        raise FileNotFoundError(f"Run scripts/04_build_linkage_and_core_cohort.py first: {subjective_path}")
    if not objective_path.exists():
        raise FileNotFoundError(f"Run scripts/03_extract_objective_session_features.py first: {objective_path}")

    core = pd.read_csv(subjective_path, parse_dates=["date"])
    objective = pd.read_csv(objective_path, parse_dates=["date"])
    objective = objective.dropna(subset=["date", "team", "player_id"]).copy()

    grouped = (
        objective.groupby(["date", "team", "player_id"], as_index=False)
        .agg(
            objective_day_session_count=("member", "size"),
            objective_day_archives=("archive", "nunique"),
            objective_gps_tick_count=("gps_tick_count", "sum"),
            objective_valid_speed_tick_count=("valid_speed_tick_count", "sum"),
            objective_duration_min=("duration_min_est", "sum"),
            objective_distance_m=("distance_m_est", "sum"),
            objective_hsr_distance_m=("hsr_distance_m", "sum"),
            objective_sprint_distance_m=("sprint_distance_m", "sum"),
            objective_accel_distance_m=("accel_distance_m", "sum"),
            objective_decel_distance_m=("decel_distance_m", "sum"),
            objective_speed_max=("speed_max", "max"),
            objective_heart_rate_max=("heart_rate_max", "max"),
            objective_heart_rate_nonzero_ticks=("heart_rate_nonzero_ticks", "sum"),
            objective_num_satellites_min=("num_satellites_min", "min"),
            objective_num_satellites_max=("num_satellites_max", "max"),
            objective_implausible_speed_ticks=("implausible_speed_ticks", "sum"),
            objective_implausible_heart_rate_ticks=("implausible_heart_rate_ticks", "sum"),
            objective_raw_row_count=("raw_row_count", "sum"),
            objective_moving_ticks_est=("moving_fraction", lambda s: float((s * objective.loc[s.index, "gps_tick_count"]).sum())),
            objective_speed_mean=(
                "speed_mean",
                lambda s: float((s * objective.loc[s.index, "valid_speed_tick_count"]).sum() / objective.loc[s.index, "valid_speed_tick_count"].sum()),
            ),
            objective_hacc_mean=(
                "hacc_mean",
                lambda s: float((s * objective.loc[s.index, "gps_tick_count"]).sum() / objective.loc[s.index, "gps_tick_count"].sum()),
            ),
            objective_hdop_mean=(
                "hdop_mean",
                lambda s: float((s * objective.loc[s.index, "gps_tick_count"]).sum() / objective.loc[s.index, "gps_tick_count"].sum()),
            ),
            objective_signal_quality_mean=(
                "signal_quality_mean",
                lambda s: float((s * objective.loc[s.index, "gps_tick_count"]).sum() / objective.loc[s.index, "gps_tick_count"].sum()),
            ),
            objective_num_satellites_mean=(
                "num_satellites_mean",
                lambda s: float((s * objective.loc[s.index, "gps_tick_count"]).sum() / objective.loc[s.index, "gps_tick_count"].sum()),
            ),
            objective_accl_x_abs_mean=("accl_x_abs_mean", "mean"),
            objective_accl_y_abs_mean=("accl_y_abs_mean", "mean"),
            objective_accl_z_abs_mean=("accl_z_abs_mean", "mean"),
            objective_gyro_x_abs_mean=("gyro_x_abs_mean", "mean"),
            objective_gyro_y_abs_mean=("gyro_y_abs_mean", "mean"),
            objective_gyro_z_abs_mean=("gyro_z_abs_mean", "mean"),
            objective_heart_rate_mean=(
                "heart_rate_mean",
                lambda s: float(
                    (s * objective.loc[s.index, "heart_rate_nonzero_ticks"]).sum()
                    / objective.loc[s.index, "heart_rate_nonzero_ticks"].sum()
                )
                if objective.loc[s.index, "heart_rate_nonzero_ticks"].sum() > 0
                else pd.NA,
            ),
        )
    )
    grouped["objective_moving_fraction"] = grouped["objective_moving_ticks_est"] / grouped["objective_gps_tick_count"]
    grouped["objective_heart_rate_coverage"] = grouped["objective_heart_rate_nonzero_ticks"] / grouped["objective_gps_tick_count"]
    grouped["objective_distance_m_per_min"] = grouped["objective_distance_m"] / grouped["objective_duration_min"].replace(0, pd.NA)
    grouped["objective_hsr_m_per_min"] = grouped["objective_hsr_distance_m"] / grouped["objective_duration_min"].replace(0, pd.NA)
    grouped["objective_sprint_m_per_min"] = grouped["objective_sprint_distance_m"] / grouped["objective_duration_min"].replace(0, pd.NA)
    grouped["objective_implausible_speed_tick_rate"] = grouped["objective_implausible_speed_ticks"] / grouped["objective_gps_tick_count"]
    grouped["objective_implausible_heart_rate_tick_rate"] = grouped["objective_implausible_heart_rate_ticks"] / grouped["objective_gps_tick_count"]

    write_csv(grouped, PROCESSED_DIR / "objective_player_day_features.csv", index=False)
    merged = core.merge(grouped, on=["date", "team", "player_id"], how="left")
    matched = merged[merged["objective_gps_tick_count"].notna()].copy()
    write_csv(matched, PROCESSED_DIR / "multimodal_modeling_cohort.csv", index=False)

    matched_by_team_year = (
        matched.assign(year=matched["date"].dt.year)
        .groupby(["team", "year"], as_index=False)
        .agg(
            rows=("player_id", "size"),
            players=("player_id", "nunique"),
            median_distance_m=("objective_distance_m", "median"),
            median_duration_min=("objective_duration_min", "median"),
            median_hr_coverage=("objective_heart_rate_coverage", "median"),
        )
        .round(3)
    )
    report = f"""# Objective Player-Day Feature Merge

## Outputs

- Objective player-day rows: {len(grouped):,}
- Core rows with objective features: {len(matched):,}
- Core rows total: {len(core):,}
- Objective feature share of core rows: {len(matched) / len(core) * 100:.1f}%

## Matched Rows By Team And Year

{markdown_table(matched_by_team_year)}

## Objective Features

{", ".join(col for col in grouped.columns if col.startswith("objective_"))}
"""
    write_text(REPORTS_DIR / "objective_player_day_merge.md", report, encoding="utf-8")
    print(f"Wrote {PROCESSED_DIR / 'objective_player_day_features.csv'}")
    print(f"Wrote {PROCESSED_DIR / 'multimodal_modeling_cohort.csv'}")
    print(f"Wrote {REPORTS_DIR / 'objective_player_day_merge.md'}")


if __name__ == "__main__":
    main()
