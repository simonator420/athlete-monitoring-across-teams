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
    add_skill_vs_persistence,
    calibration_summary,
    feature_blocks,
    inner_cv_for_split,
    make_catboost,
    metrics,
    paired_delta_mae_ci,
    player_cluster_bootstrap_metrics,
    split_predictions,
    summarize_predictions,
)


PRIMARY_MODEL = "M5_wellness_subjective_load_gps_external_load_elastic_net"
SUBJECTIVE_LOAD_MODEL = "M3_wellness_subjective_load_elastic_net"
CATBOOST_PRIMARY_MODEL = "M5_wellness_subjective_load_gps_external_load_catboost"
CATBOOST_SUBJECTIVE_LOAD_MODEL = "M3_wellness_subjective_load_catboost"
PERSISTENCE_MODEL = "M1_persistence"


def catboost_block_permutation_importance(data: pd.DataFrame, blocks: dict[str, list[str]]) -> pd.DataFrame:
    columns = [
        "split",
        "model",
        "block",
        "baseline_mae",
        "permuted_mae_delta",
        "permuted_mae_delta_sd",
    ]
    features = blocks["wellness"] + blocks["subjective_load"] + blocks["gps_external_load"]
    block_defs = {
        "wellness_history": blocks["wellness"],
        "subjective_load_history": blocks["subjective_load"],
        "gps_external_load": blocks["gps_external_load"],
    }
    year = data["date"].dt.year
    split_defs = [
        ("temporal_2020_train_2021_test", year == 2020, year == 2021),
        ("cross_team_train_A_test_B", data["team"] == "TeamA", data["team"] == "TeamB"),
        ("cross_team_train_B_test_A", data["team"] == "TeamB", data["team"] == "TeamA"),
    ]
    rng = np.random.default_rng(20260905)
    rows = []
    for split, train_mask, test_mask in split_defs:
        train = data[train_mask]
        test = data[test_mask]
        if len(train) < 2 or test.empty:
            continue
        x_train = train[features].replace([np.inf, -np.inf], np.nan)
        y_train = train["readiness_t_plus_1"].to_numpy(dtype=float)
        x_test = test[features].replace([np.inf, -np.inf], np.nan)
        y_test = test["readiness_t_plus_1"].to_numpy(dtype=float)
        cv, groups = inner_cv_for_split(split, train)
        model = make_catboost(cv=cv)
        if groups is None:
            model.fit(x_train, y_train)
        else:
            model.fit(x_train, y_train, groups=groups)
        base_pred = np.clip(model.predict(x_test), 1, 10)
        base_mae = metrics(y_test, base_pred)["mae"]
        for block_name, cols in block_defs.items():
            cols = [col for col in cols if col in x_test.columns]
            if not cols:
                continue
            deltas = []
            for _ in range(30):
                permuted = x_test.copy()
                order = rng.permutation(len(permuted))
                permuted.loc[:, cols] = x_test[cols].iloc[order].to_numpy()
                perm_pred = np.clip(model.predict(permuted), 1, 10)
                deltas.append(metrics(y_test, perm_pred)["mae"] - base_mae)
            rows.append(
                {
                    "split": split,
                    "model": CATBOOST_PRIMARY_MODEL,
                    "block": block_name,
                    "baseline_mae": base_mae,
                    "permuted_mae_delta": float(np.mean(deltas)),
                    "permuted_mae_delta_sd": float(np.std(deltas, ddof=1)) if len(deltas) > 1 else 0.0,
                }
            )
    return pd.DataFrame.from_records(rows, columns=columns)


def main() -> None:
    ensure_project_dirs()
    path = PROCESSED_DIR / "multimodal_modeling_cohort.csv"
    if not path.exists():
        raise FileNotFoundError(f"Run scripts/06_merge_objective_player_day_features.py first: {path}")

    data = pd.read_csv(path, parse_dates=["date"])
    data = data.dropna(subset=["readiness", "readiness_t_plus_1", "team", "date"]).copy()
    blocks = feature_blocks(data)

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

    missing_gps = [
        feature
        for feature in [
            "objective_hsr_distance_m",
            "objective_hsr_m_per_min",
            "objective_sprint_distance_m",
            "objective_sprint_m_per_min",
            "objective_accel_distance_m",
            "objective_decel_distance_m",
        ]
        if feature not in data.columns
    ]
    if missing_gps:
        raise RuntimeError(
            "Objective features need to be regenerated from raw GPS before the v2 model ladder. "
            f"Missing: {', '.join(missing_gps)}"
        )

    predictions = split_predictions(data, blocks)
    write_csv(predictions, PROCESSED_DIR / "multimodal_model_predictions.csv", index=False)

    results = add_skill_vs_persistence(summarize_predictions(predictions))
    results = results.sort_values(["split", "mae", "rmse"]).reset_index(drop=True)
    write_csv(results, PROCESSED_DIR / "multimodal_model_results.csv", index=False)

    with_ci = add_skill_vs_persistence(player_cluster_bootstrap_metrics(predictions))
    with_ci = with_ci.sort_values(["split", "mae"]).reset_index(drop=True)
    write_csv(with_ci, PROCESSED_DIR / "multimodal_model_results_with_ci.csv", index=False)

    calibration = calibration_summary(predictions).sort_values(["split", "model"]).reset_index(drop=True)
    write_csv(calibration, PROCESSED_DIR / "multimodal_calibration_summary.csv", index=False)

    block_importance = catboost_block_permutation_importance(data, blocks).sort_values(
        ["split", "permuted_mae_delta"], ascending=[True, False]
    )
    write_csv(block_importance, PROCESSED_DIR / "catboost_block_permutation_importance.csv", index=False)

    primary_delta = paired_delta_mae_ci(
        predictions,
        baseline_model=SUBJECTIVE_LOAD_MODEL,
        comparator_model=PRIMARY_MODEL,
        delta_name="M5_minus_M3_primary_gps_increment",
    )
    catboost_delta = paired_delta_mae_ci(
        predictions,
        baseline_model=CATBOOST_SUBJECTIVE_LOAD_MODEL,
        comparator_model=CATBOOST_PRIMARY_MODEL,
        delta_name="CatBoost_M5_minus_M3_gps_increment",
    )
    persistence_delta = paired_delta_mae_ci(
        predictions,
        baseline_model=PERSISTENCE_MODEL,
        comparator_model=PRIMARY_MODEL,
        delta_name="M5_minus_persistence",
    )
    deltas = pd.concat([primary_delta, catboost_delta, persistence_delta], ignore_index=True)
    write_csv(deltas, PROCESSED_DIR / "multimodal_delta_mae_with_ci.csv", index=False)

    compact = results[results["model"].isin([SUBJECTIVE_LOAD_MODEL, PRIMARY_MODEL])].pivot(
        index="split", columns="model", values="mae"
    )
    incremental = pd.DataFrame(
        {
            "split": compact.index,
            "mae_subjective_load": compact[SUBJECTIVE_LOAD_MODEL].values,
            "mae_subjective_load_gps": compact[PRIMARY_MODEL].values,
            "mae_delta_gps_minus_subjective_load": (compact[PRIMARY_MODEL] - compact[SUBJECTIVE_LOAD_MODEL]).values,
        }
    ).round(3)
    write_csv(incremental, PROCESSED_DIR / "multimodal_incremental_mae.csv", index=False)

    report = f"""# Multimodal Model Results

Models are evaluated on the same GPS-matched player-day cohort. The primary
multimodal model is HR-free and uses football-interpretable external-load GPS
features only; heart-rate and signal-quality variables are retained for QC and
sensitivity analysis, not the main physiological predictor block.

## Modality Ladder

- M0: training-set mean
- M1: persistence, current readiness
- M2: wellness and recent wellness history
- M3: wellness plus transparent subjective load/history
- M4: wellness plus GPS external load
- M5: wellness plus subjective load/history plus GPS external load

## Results

{markdown_table(results.round(3))}

## Results With Player-Cluster 95% CI

{markdown_table(with_ci.round(3))}

## Calibration Summary

Calibration is summarized by regressing observed readiness on predicted
readiness within each validation split and model.

{markdown_table(calibration.round(3))}

## Incremental GPS Comparison

Negative delta means the HR-free GPS external-load block improved MAE over the
wellness plus subjective-load model on the same split.

{markdown_table(incremental)}

## Paired Delta MAE With Player-Cluster 95% CI

{markdown_table(deltas.round(3))}

## CatBoost Block Permutation Importance

Positive values mean MAE became worse when the held-out block was permuted.

{markdown_table(block_importance.round(3))}

## Feature Blocks

Wellness: {", ".join(blocks["wellness"])}

Subjective load/history: {", ".join(blocks["subjective_load"])}

GPS external load: {", ".join(blocks["gps_external_load"])}

HR sensitivity candidates: {", ".join(blocks["hr"])}

GPS QC variables excluded from primary model: {", ".join(blocks["gps_qc"])}
"""
    write_text(REPORTS_DIR / "multimodal_model_results.md", report, encoding="utf-8")
    print(f"Wrote {PROCESSED_DIR / 'multimodal_model_predictions.csv'}")
    print(f"Wrote {PROCESSED_DIR / 'multimodal_model_results.csv'}")
    print(f"Wrote {PROCESSED_DIR / 'multimodal_model_results_with_ci.csv'}")
    print(f"Wrote {PROCESSED_DIR / 'multimodal_calibration_summary.csv'}")
    print(f"Wrote {PROCESSED_DIR / 'multimodal_delta_mae_with_ci.csv'}")
    print(f"Wrote {PROCESSED_DIR / 'catboost_block_permutation_importance.csv'}")
    print(f"Wrote {PROCESSED_DIR / 'multimodal_incremental_mae.csv'}")
    print(f"Wrote {REPORTS_DIR / 'multimodal_model_results.md'}")


if __name__ == "__main__":
    main()
