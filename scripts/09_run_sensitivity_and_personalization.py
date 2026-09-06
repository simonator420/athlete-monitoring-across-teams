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
from soccermon.modeling import (
    available,
    elastic_net_prediction,
    feature_blocks,
    metrics,
    paired_delta_mae_ci,
    player_cluster_bootstrap_metrics,
    summarize_predictions,
)


PRIMARY_MODEL = "M5_wellness_subjective_load_gps_external_load_elastic_net"


def prediction_records(
    split: str,
    model: str,
    test: pd.DataFrame,
    pred: np.ndarray,
    target_col: str = "readiness_t_plus_1",
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "split": split,
            "model": model,
            "row_id": test.index.astype(int),
            "player_id": test["player_id"].to_numpy(),
            "team": test["team"].to_numpy(),
            "date": test["date"].to_numpy(),
            "y_true": test[target_col].to_numpy(dtype=float),
            "y_pred": pred.astype(float),
        }
    )


def evaluate_feature_set(
    split: str,
    train: pd.DataFrame,
    test: pd.DataFrame,
    features: list[str],
    model: str,
    target_col: str = "readiness_t_plus_1",
) -> pd.DataFrame:
    if train.empty or test.empty:
        return pd.DataFrame()
    train_model = train.dropna(subset=[target_col]).copy()
    test_model = test.dropna(subset=[target_col]).copy()
    if train_model.empty or test_model.empty:
        return pd.DataFrame()
    return prediction_records(
        split,
        model,
        test_model,
        elastic_net_prediction(train_model, test_model, features, split=split, target_col=target_col),
        target_col=target_col,
    )


def sensitivity_predictions(data: pd.DataFrame, blocks: dict[str, list[str]]) -> pd.DataFrame:
    year = data["date"].dt.year
    base_features = blocks["wellness"] + blocks["subjective_load"] + blocks["gps_external_load"]
    derived_features = base_features + blocks["derived_load_sensitivity"]
    hr_features = base_features + blocks["hr"]
    definitions = [
        ("temporal_2020_train_2021_test", year == 2020, year == 2021),
        ("cross_team_train_A_test_B", data["team"] == "TeamA", data["team"] == "TeamB"),
        ("cross_team_train_B_test_A", data["team"] == "TeamB", data["team"] == "TeamA"),
    ]

    chunks = []
    for split, train_mask, test_mask in definitions:
        train = data[train_mask]
        test = data[test_mask]
        chunks.append(evaluate_feature_set(split, train, test, base_features, PRIMARY_MODEL))
        chunks.append(
            evaluate_feature_set(
                split,
                train,
                test,
                derived_features,
                "sensitivity_M5_plus_ACWR_ATL_CTL_monotony_strain",
            )
        )

    hr_data = data[data["objective_heart_rate_coverage"].fillna(0) > 0].copy()
    if blocks["hr"] and not hr_data.empty:
        hr_year = hr_data["date"].dt.year
        hr_definitions = [
            ("hr_available_cross_team_A_to_B", hr_data["team"] == "TeamA", hr_data["team"] == "TeamB"),
            ("hr_available_cross_team_B_to_A", hr_data["team"] == "TeamB", hr_data["team"] == "TeamA"),
            (
                "hr_available_temporal_2021_train_test",
                (hr_year == 2021) & (hr_data["date"] < pd.Timestamp("2021-07-01")),
                (hr_year == 2021) & (hr_data["date"] >= pd.Timestamp("2021-07-01")),
            ),
        ]
        for split, train_mask, test_mask in hr_definitions:
            train = hr_data[train_mask]
            test = hr_data[test_mask]
            chunks.append(evaluate_feature_set(split, train, test, base_features, PRIMARY_MODEL))
            chunks.append(evaluate_feature_set(split, train, test, hr_features, "sensitivity_M5_plus_HR_available"))

    return pd.concat([chunk for chunk in chunks if not chunk.empty], ignore_index=True)


def focused_sensitivity_predictions(data: pd.DataFrame, blocks: dict[str, list[str]]) -> pd.DataFrame:
    year = data["date"].dt.year
    base_features = blocks["wellness"] + blocks["subjective_load"] + blocks["gps_external_load"]
    no_current_readiness = [feature for feature in base_features if feature != "readiness"]
    definitions = [
        ("temporal_2020_train_2021_test", year == 2020, year == 2021),
        ("cross_team_train_A_test_B", data["team"] == "TeamA", data["team"] == "TeamB"),
        ("cross_team_train_B_test_A", data["team"] == "TeamB", data["team"] == "TeamA"),
    ]
    chunks = []
    for split, train_mask, test_mask in definitions:
        train = data[train_mask]
        test = data[test_mask]
        chunks.append(
            evaluate_feature_set(
                split,
                train,
                test,
                no_current_readiness,
                "sensitivity_next_day_readiness_without_current_readiness",
            )
        )
        complete_train = train.dropna(subset=base_features)
        complete_test = test.dropna(subset=base_features)
        chunks.append(
            evaluate_feature_set(
                split,
                train,
                complete_test,
                base_features,
                "sensitivity_imputed_M5_on_complete_case_rows",
            )
        )
        chunks.append(evaluate_feature_set(split, complete_train, complete_test, base_features, "sensitivity_complete_case_M5"))
        if "session_match_day" in data.columns and data["session_match_day"].notna().any():
            no_match_train = train[~train["session_match_day"].fillna(False).astype(bool)]
            no_match_test = test[~test["session_match_day"].fillna(False).astype(bool)]
            chunks.append(
                evaluate_feature_set(
                    split,
                    no_match_train,
                    no_match_test,
                    base_features,
                    "sensitivity_excluding_match_days",
                )
            )
        for target_col, label in [
            ("fatigue_t_plus_1", "sensitivity_next_day_fatigue"),
            ("soreness_t_plus_1", "sensitivity_next_day_soreness"),
            ("readiness_delta_t_plus_1", "sensitivity_delta_readiness_without_current_readiness"),
        ]:
            if target_col in data.columns:
                features = no_current_readiness if target_col == "readiness_delta_t_plus_1" else base_features
                chunks.append(evaluate_feature_set(split, train, test, features, label, target_col=target_col))
    return pd.concat([chunk for chunk in chunks if not chunk.empty], ignore_index=True)


def target_team_recalibration_predictions(data: pd.DataFrame, blocks: dict[str, list[str]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    features = blocks["wellness"] + blocks["subjective_load"] + blocks["gps_external_load"]
    year = data["date"].dt.year
    designs = [
        (
            "source_A2020_calibrate_B2020_test_B2021",
            (data["team"] == "TeamA") & (year == 2020),
            (data["team"] == "TeamB") & (year == 2020),
            (data["team"] == "TeamB") & (year == 2021),
        ),
        (
            "source_B2020_calibrate_A2020_test_A2021",
            (data["team"] == "TeamB") & (year == 2020),
            (data["team"] == "TeamA") & (year == 2020),
            (data["team"] == "TeamA") & (year == 2021),
        ),
    ]
    chunks = []
    for split, source_mask, calibration_mask, test_mask in designs:
        source = data[source_mask]
        calibration = data[calibration_mask]
        test = data[test_mask]
        if source.empty or calibration.empty or test.empty:
            continue
        cal_pred = elastic_net_prediction(source, calibration, features, split=split)
        test_pred = elastic_net_prediction(source, test, features, split=split)
        y_cal = calibration["readiness_t_plus_1"].to_numpy(dtype=float)
        if len(calibration) >= 3 and np.nanstd(cal_pred) > 0:
            slope, intercept = np.polyfit(cal_pred, y_cal, deg=1)
        else:
            slope, intercept = 1.0, 0.0
        recalibrated = np.clip(intercept + slope * test_pred, 1, 10)
        chunks.append(prediction_records(split, "zero_shot_source_team_M5", test, test_pred))
        chunks.append(prediction_records(split, "target_team_intercept_slope_recalibrated_M5", test, recalibrated))
    predictions = pd.concat(chunks, ignore_index=True) if chunks else pd.DataFrame()
    if predictions.empty:
        delta = pd.DataFrame()
    else:
        delta = paired_delta_mae_ci(
            predictions,
            baseline_model="zero_shot_source_team_M5",
            comparator_model="target_team_intercept_slope_recalibrated_M5",
            delta_name="target_recalibrated_minus_zero_shot",
        )
    return predictions, delta


def cold_start_personalization(data: pd.DataFrame, blocks: dict[str, list[str]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    features = blocks["wellness"] + blocks["subjective_load"] + blocks["gps_external_load"]
    records = []
    for player_id in sorted(data["player_id"].dropna().unique()):
        train = data[data["player_id"] != player_id]
        test = data[data["player_id"] == player_id].sort_values("date")
        if train.empty or test.empty:
            continue
        base_pred = elastic_net_prediction(train, test, features, split="leave_one_player_out_cold_start")
        truth = test["readiness_t_plus_1"].to_numpy(dtype=float)
        residuals = truth - base_pred
        for threshold in [0, 7, 14, 28]:
            for pos, (idx, row) in enumerate(test.iterrows()):
                if pos < threshold:
                    continue
                correction = float(residuals[:pos].mean()) if threshold and pos > 0 else 0.0
                base_record = {
                    "split": f"leave_one_player_out_after_{threshold}_observations",
                    "model": f"population_prediction_after_{threshold}_observations",
                    "row_id": int(idx),
                    "player_id": player_id,
                    "team": row["team"],
                    "date": row["date"],
                    "y_true": float(row["readiness_t_plus_1"]),
                    "y_pred": float(np.clip(base_pred[pos], 1, 10)),
                }
                records.append(
                    {
                        "split": f"leave_one_player_out_after_{threshold}_observations",
                        "model": f"personalized_residual_after_{threshold}_observations",
                        "row_id": int(idx),
                        "player_id": player_id,
                        "team": row["team"],
                        "date": row["date"],
                        "y_true": float(row["readiness_t_plus_1"]),
                        "y_pred": float(np.clip(base_pred[pos] + correction, 1, 10)),
                    }
                )
                records.append(base_record)
    predictions = pd.DataFrame.from_records(records)
    if predictions.empty:
        return predictions, pd.DataFrame()
    summary = summarize_predictions(predictions)
    with_ci = player_cluster_bootstrap_metrics(predictions)
    summary = summary.merge(
        with_ci[["split", "model", "mae_ci_low", "mae_ci_high"]],
        on=["split", "model"],
        how="left",
    )
    return predictions, summary.sort_values(["split", "model"])


def main() -> None:
    ensure_project_dirs()
    path = PROCESSED_DIR / "multimodal_modeling_cohort.csv"
    if not path.exists():
        raise FileNotFoundError(f"Run scripts/06_merge_objective_player_day_features.py first: {path}")

    data = pd.read_csv(path, parse_dates=["date"])
    data = data.dropna(subset=["readiness", "readiness_t_plus_1", "team", "date"]).copy()
    blocks = feature_blocks(data)
    if "session_match_day" in data.columns and data["session_match_day"].notna().any():
        match_day_note = "Match-day sensitivity was run on splits with match-day rows excluded."
    else:
        match_day_note = (
            "Match-day sensitivity was not run because session/activity type metadata were not available "
            "for defensible match classification."
        )
    missing_history = [
        feature
        for feature in [
            "readiness_past_3d_mean",
            "readiness_past_7d_mean",
            "session_srpe_sum_past_3d_sum",
            "session_srpe_sum_past_7d_sum",
            "session_srpe_sum_past_28d_sum",
        ]
        if feature not in data.columns
    ]
    if missing_history:
        raise RuntimeError(
            "Subjective history features need to be regenerated on the full longitudinal subjective dataset "
            f"before GPS matching. Rerun scripts/04_build_linkage_and_core_cohort.py. Missing: {', '.join(missing_history)}"
        )
    missing_primary = [
        feature
        for feature in ["objective_hsr_distance_m", "objective_sprint_distance_m", "objective_accel_distance_m"]
        if feature not in data.columns
    ]
    if missing_primary:
        raise RuntimeError(
            "Objective features need to be regenerated from raw GPS before v2 sensitivity analysis. "
            f"Missing: {', '.join(missing_primary)}"
        )

    predictions = sensitivity_predictions(data, blocks)
    results = summarize_predictions(predictions).sort_values(["split", "mae"]).reset_index(drop=True)
    with_ci = player_cluster_bootstrap_metrics(predictions).sort_values(["split", "mae"]).reset_index(drop=True)
    write_csv(predictions, PROCESSED_DIR / "sensitivity_model_predictions.csv", index=False)
    write_csv(results, PROCESSED_DIR / "sensitivity_personalization_results.csv", index=False)
    write_csv(with_ci, PROCESSED_DIR / "sensitivity_personalization_results_with_ci.csv", index=False)

    hr_delta = paired_delta_mae_ci(
        predictions,
        baseline_model=PRIMARY_MODEL,
        comparator_model="sensitivity_M5_plus_HR_available",
        delta_name="HR_available_minus_primary_HR_free",
    )
    write_csv(hr_delta, PROCESSED_DIR / "heart_rate_sensitivity_mae.csv", index=False)

    focused_predictions = focused_sensitivity_predictions(data, blocks)
    focused_results = (
        summarize_predictions(focused_predictions).sort_values(["split", "model"]).reset_index(drop=True)
        if not focused_predictions.empty
        else pd.DataFrame()
    )
    focused_with_ci = (
        player_cluster_bootstrap_metrics(focused_predictions).sort_values(["split", "model"]).reset_index(drop=True)
        if not focused_predictions.empty
        else pd.DataFrame()
    )
    write_csv(focused_predictions, PROCESSED_DIR / "focused_sensitivity_predictions.csv", index=False)
    write_csv(focused_results, PROCESSED_DIR / "focused_sensitivity_results.csv", index=False)
    write_csv(focused_with_ci, PROCESSED_DIR / "focused_sensitivity_results_with_ci.csv", index=False)

    recalibration_predictions, recalibration_delta = target_team_recalibration_predictions(data, blocks)
    recalibration_results = (
        summarize_predictions(recalibration_predictions).sort_values(["split", "mae"]).reset_index(drop=True)
        if not recalibration_predictions.empty
        else pd.DataFrame()
    )
    write_csv(recalibration_predictions, PROCESSED_DIR / "target_team_recalibration_predictions.csv", index=False)
    write_csv(recalibration_results, PROCESSED_DIR / "target_team_recalibration_results.csv", index=False)
    write_csv(recalibration_delta, PROCESSED_DIR / "target_team_recalibration_delta_mae.csv", index=False)

    personalized_predictions, personalization = cold_start_personalization(data, blocks)
    write_csv(personalized_predictions, PROCESSED_DIR / "cold_start_personalization_predictions.csv", index=False)
    write_csv(personalization, PROCESSED_DIR / "cold_start_personalization_mae.csv", index=False)
    if personalized_predictions.empty:
        cold_start_delta = pd.DataFrame()
    else:
        cold_start_deltas = []
        for threshold in [7, 14, 28]:
            cold_start_deltas.append(
                paired_delta_mae_ci(
                    personalized_predictions[
                        personalized_predictions["split"] == f"leave_one_player_out_after_{threshold}_observations"
                    ],
                    baseline_model=f"population_prediction_after_{threshold}_observations",
                    comparator_model=f"personalized_residual_after_{threshold}_observations",
                    delta_name=f"personalized_minus_population_after_{threshold}",
                )
            )
        cold_start_delta_frames = [delta for delta in cold_start_deltas if not delta.empty]
        cold_start_delta = pd.concat(cold_start_delta_frames, ignore_index=True) if cold_start_delta_frames else pd.DataFrame()
    write_csv(cold_start_delta, PROCESSED_DIR / "cold_start_personalization_delta_mae.csv", index=False)

    report = f"""# Sensitivity And Personalization Results

## Results

{markdown_table(results.round(3))}

## Results With Player-Cluster 95% CI

{markdown_table(with_ci.round(3))}

## Heart-Rate Availability Sensitivity

The primary multimodal model is HR-free. These rows add HR only where HR is
available and compare the paired MAE change against the primary HR-free model.

{markdown_table(hr_delta.round(3))}

## Cold-Start Personalization

Each player is held out from population model fitting. The personalization
variant adds only a simple athlete-specific residual/intercept correction. For
each threshold, the population and personalized predictions are evaluated on
identical post-threshold observations.

{markdown_table(personalization.round(3))}

## Cold-Start Paired Delta MAE

{markdown_table(cold_start_delta.round(3))}

## Target-Team Recalibration

The model is fit on the source-team 2020 data. Target-team 2020 data are used
only to estimate a calibration intercept/slope, then evaluation is performed on
the target-team 2021 observations.

{markdown_table(recalibration_results.round(3) if not recalibration_results.empty else recalibration_results)}

## Target-Team Recalibration Paired Delta MAE

{markdown_table(recalibration_delta.round(3) if not recalibration_delta.empty else recalibration_delta)}

## Focused Sensitivity Analyses

{match_day_note}

{markdown_table(focused_with_ci.round(3))}

## Feature Blocks

Primary model features: {", ".join(blocks["wellness"] + blocks["subjective_load"] + blocks["gps_external_load"])}

Derived-load sensitivity features: {", ".join(available(data, blocks["derived_load_sensitivity"]))}

HR sensitivity features: {", ".join(blocks["hr"])}
"""
    write_text(REPORTS_DIR / "sensitivity_personalization_results.md", report, encoding="utf-8")
    print(f"Wrote {PROCESSED_DIR / 'sensitivity_personalization_results.csv'}")
    print(f"Wrote {PROCESSED_DIR / 'sensitivity_personalization_results_with_ci.csv'}")
    print(f"Wrote {PROCESSED_DIR / 'heart_rate_sensitivity_mae.csv'}")
    print(f"Wrote {PROCESSED_DIR / 'focused_sensitivity_results_with_ci.csv'}")
    print(f"Wrote {PROCESSED_DIR / 'target_team_recalibration_delta_mae.csv'}")
    print(f"Wrote {PROCESSED_DIR / 'cold_start_personalization_mae.csv'}")
    print(f"Wrote {PROCESSED_DIR / 'cold_start_personalization_delta_mae.csv'}")
    print(f"Wrote {REPORTS_DIR / 'sensitivity_personalization_results.md'}")


if __name__ == "__main__":
    main()
