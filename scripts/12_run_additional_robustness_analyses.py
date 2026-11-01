#!/usr/bin/env python3
"""Post-hoc robustness analyses for the cross-team GNSS study.

These analyses intentionally reuse the frozen row-level predictions. They do
not retune or refit the outcome models and therefore cannot improve their
apparent performance by model selection.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from soccermon.config import PROCESSED_DIR, PROJECT_ROOT, REPORTS_DIR, ensure_project_dirs
from soccermon.io import write_csv, write_text
from soccermon.markdown import markdown_table
from soccermon.modeling import feature_blocks


SEED = 20260905
N_BOOTSTRAP = 2000
M3 = "M3_wellness_subjective_load_elastic_net"
M5 = "M5_wellness_subjective_load_gps_external_load_elastic_net"
PERSISTENCE = "M1_persistence"
EXTERNAL_SPLITS = ["cross_team_train_A_test_B", "cross_team_train_B_test_A"]


def percentile_ci(values: list[float]) -> tuple[float, float]:
    return float(np.percentile(values, 2.5)), float(np.percentile(values, 97.5))


def paired_error_frame(group: pd.DataFrame, baseline: str = M3, comparator: str = M5) -> pd.DataFrame:
    subset = group[group["model"].isin([baseline, comparator])]
    pivot = subset.pivot(index=["row_id", "player_id"], columns="model", values=["y_true", "y_pred"])
    required = [("y_pred", baseline), ("y_pred", comparator), ("y_true", baseline)]
    if any(column not in pivot for column in required):
        return pd.DataFrame()
    truth = pivot[("y_true", baseline)]
    return pd.DataFrame(
        {
            "row_id": pivot.index.get_level_values("row_id").astype(int),
            "player_id": pivot.index.get_level_values("player_id"),
            "y_true": truth.to_numpy(dtype=float),
            "baseline_abs_error": (pivot[("y_pred", baseline)] - truth).abs().to_numpy(dtype=float),
            "comparator_abs_error": (pivot[("y_pred", comparator)] - truth).abs().to_numpy(dtype=float),
        }
    ).assign(delta_abs_error=lambda x: x["comparator_abs_error"] - x["baseline_abs_error"])


def cluster_bootstrap_weighted_delta(frame: pd.DataFrame, weight_col: str, seed: int) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    players = frame["player_id"].dropna().unique()
    by_player = {player: frame[frame["player_id"] == player] for player in players}
    boot: list[float] = []
    for _ in range(N_BOOTSTRAP):
        sampled = rng.choice(players, size=len(players), replace=True)
        sample = pd.concat([by_player[player] for player in sampled], ignore_index=True)
        boot.append(float(np.average(sample["delta_abs_error"], weights=sample[weight_col])))
    return percentile_ci(boot)


def weighted_mean_variance(values: np.ndarray, weights: np.ndarray) -> tuple[float, float]:
    mask = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    values, weights = values[mask], weights[mask]
    if not len(values):
        return float("nan"), float("nan")
    mean = float(np.average(values, weights=weights))
    variance = float(np.average(np.square(values - mean), weights=weights))
    return mean, variance


def selection_balance(selection: pd.DataFrame, numeric: list[str]) -> pd.DataFrame:
    rows = []
    for (team, year), group in selection.groupby(["team", "year"], dropna=False):
        selected = group[group["has_gnss"].eq(1)]
        for feature in numeric:
            target = pd.to_numeric(group[feature], errors="coerce").to_numpy(dtype=float)
            observed = pd.to_numeric(selected[feature], errors="coerce").to_numpy(dtype=float)
            target_mean, target_var = weighted_mean_variance(target, np.ones(len(target)))
            observed_mean, observed_var = weighted_mean_variance(observed, np.ones(len(observed)))
            weighted_mean, weighted_var = weighted_mean_variance(
                observed, selected["stabilized_ipw_trimmed"].to_numpy(dtype=float)
            )
            unweighted_denom = np.sqrt((target_var + observed_var) / 2)
            weighted_denom = np.sqrt((target_var + weighted_var) / 2)
            rows.append(
                {
                    "team": team,
                    "year": year,
                    "feature": feature,
                    "target_mean": target_mean,
                    "gnss_mean_unweighted": observed_mean,
                    "gnss_mean_ipw": weighted_mean,
                    "smd_unweighted": (observed_mean - target_mean) / unweighted_denom if unweighted_denom else 0.0,
                    "smd_ipw": (weighted_mean - target_mean) / weighted_denom if weighted_denom else 0.0,
                }
            )
    return pd.DataFrame.from_records(rows)


def build_propensity_scores(
    core: pd.DataFrame, multimodal: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    keys = ["date", "team", "player_id"]
    gnss_keys = multimodal[keys].drop_duplicates().assign(has_gnss=1)
    selection = core.merge(gnss_keys, on=keys, how="left")
    selection["has_gnss"] = selection["has_gnss"].fillna(0).astype(int)
    selection["year"] = selection["date"].dt.year.astype(str)

    blocks = feature_blocks(selection)
    numeric = list(dict.fromkeys(blocks["wellness"] + blocks["subjective_load"]))
    categorical = ["team", "year"]
    preprocess = ColumnTransformer(
        [
            (
                "numeric",
                Pipeline([("imputer", SimpleImputer(strategy="median")), ("scale", StandardScaler())]),
                numeric,
            ),
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
        ]
    )
    model = Pipeline(
        [
            ("preprocess", preprocess),
            ("model", LogisticRegression(max_iter=5000, random_state=SEED)),
        ]
    )

    x = selection[numeric + categorical]
    y = selection["has_gnss"].to_numpy()
    propensity = np.full(len(selection), np.nan)
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    for train_idx, test_idx in folds.split(x, y):
        model.fit(x.iloc[train_idx], y[train_idx])
        propensity[test_idx] = model.predict_proba(x.iloc[test_idx])[:, 1]

    selection["gnss_propensity"] = propensity
    selection["gnss_propensity_clipped"] = np.clip(propensity, 0.02, 0.98)
    prevalence = float(selection["has_gnss"].mean())
    selection["stabilized_ipw"] = np.where(
        selection["has_gnss"].eq(1), prevalence / selection["gnss_propensity_clipped"], np.nan
    )
    selection["stabilized_ipw_trimmed"] = selection["stabilized_ipw"]
    selected = selection["has_gnss"].eq(1)
    lower, upper = selection.loc[selected, "stabilized_ipw"].quantile([0.01, 0.99])
    selection.loc[selected, "stabilized_ipw_trimmed"] = selection.loc[selected, "stabilized_ipw"].clip(lower, upper)

    summary_rows = []
    for labels, group in selection.groupby(["team", "year"], dropna=False):
        selected_group = group[group["has_gnss"].eq(1)]
        weights = selected_group["stabilized_ipw_trimmed"].dropna().to_numpy(dtype=float)
        summary_rows.append(
            {
                "team": labels[0],
                "year": labels[1],
                "n_core": len(group),
                "n_gnss": int(group["has_gnss"].sum()),
                "gnss_prevalence": float(group["has_gnss"].mean()),
                "propensity_auc_overall": float(roc_auc_score(y, propensity)),
                "propensity_min": float(group["gnss_propensity"].min()),
                "propensity_max": float(group["gnss_propensity"].max()),
                "trimmed_weight_min": float(weights.min()),
                "trimmed_weight_max": float(weights.max()),
                "effective_sample_size": float(weights.sum() ** 2 / np.square(weights).sum()),
            }
        )
    balance = selection_balance(selection, numeric)
    return selection, pd.DataFrame.from_records(summary_rows), balance


def ipw_delta_results(predictions: pd.DataFrame, propensity: pd.DataFrame) -> pd.DataFrame:
    weight_lookup = propensity[propensity["has_gnss"].eq(1)][
        ["date", "team", "player_id", "stabilized_ipw", "stabilized_ipw_trimmed"]
    ].drop_duplicates(["date", "team", "player_id"])
    rows = []
    for split in EXTERNAL_SPLITS:
        frame = paired_error_frame(predictions[predictions["split"].eq(split)])
        dates = predictions[
            predictions["split"].eq(split) & predictions["model"].eq(M3)
        ][["row_id", "date", "team", "player_id"]].drop_duplicates("row_id")
        frame = frame.merge(dates, on=["row_id", "player_id"], how="left").merge(
            weight_lookup, on=["date", "team", "player_id"], how="left", validate="many_to_one"
        )
        if frame[["stabilized_ipw", "stabilized_ipw_trimmed"]].isna().any().any():
            raise RuntimeError(f"Missing propensity weights after merging split {split}")
        for label, weight_col in [
            ("unweighted", "unit_weight"),
            ("ipw_untrimmed", "stabilized_ipw"),
            ("ipw_trimmed_1_99", "stabilized_ipw_trimmed"),
        ]:
            frame["unit_weight"] = 1.0
            point = float(np.average(frame["delta_abs_error"], weights=frame[weight_col]))
            low, high = cluster_bootstrap_weighted_delta(frame, weight_col, SEED + len(rows))
            weights = frame[weight_col].to_numpy(dtype=float)
            rows.append(
                {
                    "split": split,
                    "analysis": label,
                    "n": len(frame),
                    "players": frame["player_id"].nunique(),
                    "effective_sample_size": float(weights.sum() ** 2 / np.square(weights).sum()),
                    "delta_mae_m5_minus_m3": point,
                    "ci_low": low,
                    "ci_high": high,
                }
            )
    return pd.DataFrame.from_records(rows)


def player_heterogeneity(predictions: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    player_rows = []
    summary_rows = []
    influence_rows = []
    rng = np.random.default_rng(SEED)
    for split in EXTERNAL_SPLITS:
        frame = paired_error_frame(predictions[predictions["split"].eq(split)])
        per_player = (
            frame.groupby("player_id")
            .agg(
                n=("delta_abs_error", "size"),
                m3_mae=("baseline_abs_error", "mean"),
                m5_mae=("comparator_abs_error", "mean"),
                delta_mae_m5_minus_m3=("delta_abs_error", "mean"),
            )
            .reset_index()
        )
        per_player.insert(0, "split", split)
        player_rows.append(per_player)

        boot_median, boot_mean, boot_prop = [], [], []
        values = per_player["delta_mae_m5_minus_m3"].to_numpy(dtype=float)
        for _ in range(N_BOOTSTRAP):
            sample = rng.choice(values, size=len(values), replace=True)
            boot_median.append(float(np.median(sample)))
            boot_mean.append(float(np.mean(sample)))
            boot_prop.append(float(np.mean(sample < 0)))
        median_low, median_high = percentile_ci(boot_median)
        mean_low, mean_high = percentile_ci(boot_mean)
        prop_low, prop_high = percentile_ci(boot_prop)
        summary_rows.append(
            {
                "split": split,
                "players": len(per_player),
                "player_weighted_mean_delta": float(values.mean()),
                "player_weighted_mean_ci_low": mean_low,
                "player_weighted_mean_ci_high": mean_high,
                "median_player_delta": float(np.median(values)),
                "median_ci_low": median_low,
                "median_ci_high": median_high,
                "player_delta_q1": float(np.percentile(values, 25)),
                "player_delta_q3": float(np.percentile(values, 75)),
                "players_improved_n": int(np.sum(values < 0)),
                "players_improved_proportion": float(np.mean(values < 0)),
                "players_improved_ci_low": prop_low,
                "players_improved_ci_high": prop_high,
            }
        )

        for omitted in per_player["player_id"]:
            subset = frame[frame["player_id"].ne(omitted)]
            influence_rows.append(
                {
                    "split": split,
                    "omitted_player_id": omitted,
                    "n_remaining": len(subset),
                    "delta_mae_m5_minus_m3": float(subset["delta_abs_error"].mean()),
                }
            )
    return (
        pd.concat(player_rows, ignore_index=True),
        pd.DataFrame.from_records(summary_rows),
        pd.DataFrame.from_records(influence_rows),
    )


def calibration_bootstrap(predictions: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(SEED)
    rows, bin_rows = [], []
    subset = predictions[
        predictions["split"].isin(EXTERNAL_SPLITS) & predictions["model"].isin([PERSISTENCE, M3, M5])
    ].copy()
    for (split, model), group in subset.groupby(["split", "model"], sort=False):
        players = group["player_id"].unique()
        by_player = {player: group[group["player_id"] == player] for player in players}

        def calibration(frame: pd.DataFrame) -> tuple[float, float]:
            if frame["y_pred"].nunique() < 2:
                return float("nan"), float("nan")
            slope, intercept = np.polyfit(frame["y_pred"], frame["y_true"], deg=1)
            return float(intercept), float(slope)

        intercept, slope = calibration(group)
        intercept_boot, slope_boot = [], []
        for _ in range(N_BOOTSTRAP):
            sampled = rng.choice(players, size=len(players), replace=True)
            sample = pd.concat([by_player[player] for player in sampled], ignore_index=True)
            b_intercept, b_slope = calibration(sample)
            intercept_boot.append(b_intercept)
            slope_boot.append(b_slope)
        intercept_low, intercept_high = percentile_ci(intercept_boot)
        slope_low, slope_high = percentile_ci(slope_boot)
        rows.append(
            {
                "split": split,
                "model": model,
                "n": len(group),
                "players": len(players),
                "calibration_intercept": intercept,
                "intercept_ci_low": intercept_low,
                "intercept_ci_high": intercept_high,
                "calibration_slope": slope,
                "slope_ci_low": slope_low,
                "slope_ci_high": slope_high,
                "mean_observed": float(group["y_true"].mean()),
                "mean_predicted": float(group["y_pred"].mean()),
                "bias": float((group["y_pred"] - group["y_true"]).mean()),
            }
        )
        group = group.copy()
        group["prediction_bin"] = pd.qcut(group["y_pred"], q=10, duplicates="drop")
        binned = group.groupby("prediction_bin", observed=True).agg(
            n=("y_true", "size"), mean_predicted=("y_pred", "mean"), mean_observed=("y_true", "mean")
        )
        for bin_number, (_, values) in enumerate(binned.iterrows(), start=1):
            bin_rows.append({"split": split, "model": model, "bin": bin_number, **values.to_dict()})
    return pd.DataFrame.from_records(rows), pd.DataFrame.from_records(bin_rows)


def residual_strata(predictions: pd.DataFrame, cohort: pd.DataFrame) -> pd.DataFrame:
    lookup = cohort[["row_id", "readiness"]].drop_duplicates("row_id")
    subset = predictions[
        predictions["split"].isin(EXTERNAL_SPLITS) & predictions["model"].isin([PERSISTENCE, M3, M5])
    ].merge(lookup, on="row_id", how="left", validate="many_to_one")
    subset["absolute_change"] = (subset["y_true"] - subset["readiness"]).abs()
    subset["change_stratum"] = pd.cut(
        subset["absolute_change"], bins=[-0.01, 0.01, 1.01, np.inf], labels=["unchanged", "one_point", "two_or_more"]
    )
    rows = []
    rng = np.random.default_rng(SEED)
    for (split, model, stratum), group in subset.groupby(["split", "model", "change_stratum"], observed=True):
        players = group["player_id"].unique()
        by_player = {player: group[group["player_id"] == player] for player in players}
        errors = (group["y_pred"] - group["y_true"]).abs()
        boot = []
        for _ in range(1000):
            sampled = rng.choice(players, size=len(players), replace=True)
            sample = pd.concat([by_player[player] for player in sampled], ignore_index=True)
            boot.append(float((sample["y_pred"] - sample["y_true"]).abs().mean()))
        low, high = percentile_ci(boot)
        rows.append(
            {
                "split": split,
                "model": model,
                "change_stratum": str(stratum),
                "n": len(group),
                "players": len(players),
                "mae": float(errors.mean()),
                "mae_ci_low": low,
                "mae_ci_high": high,
                "bias": float((group["y_pred"] - group["y_true"]).mean()),
            }
        )
    return pd.DataFrame.from_records(rows)


def hierarchical_week_bootstrap(predictions: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    rows = []
    for split in EXTERNAL_SPLITS:
        frame = paired_error_frame(predictions[predictions["split"].eq(split)])
        dates = predictions[
            predictions["split"].eq(split) & predictions["model"].eq(M3)
        ][["row_id", "date"]].drop_duplicates("row_id")
        frame = frame.merge(dates, on="row_id", how="left")
        date = pd.to_datetime(frame["date"])
        iso = date.dt.isocalendar()
        frame["week"] = iso.year.astype(str) + "-W" + iso.week.astype(str).str.zfill(2)
        players = frame["player_id"].unique()
        player_weeks = {
            player: {week: rows for week, rows in group.groupby("week")}
            for player, group in frame.groupby("player_id")
        }
        boot = []
        for _ in range(N_BOOTSTRAP):
            sampled_players = rng.choice(players, size=len(players), replace=True)
            chunks = []
            for player in sampled_players:
                weeks = list(player_weeks[player])
                sampled_weeks = rng.choice(weeks, size=len(weeks), replace=True)
                chunks.extend(player_weeks[player][week] for week in sampled_weeks)
            sample = pd.concat(chunks, ignore_index=True)
            boot.append(float(sample["delta_abs_error"].mean()))
        low, high = percentile_ci(boot)
        rows.append(
            {
                "split": split,
                "n": len(frame),
                "players": len(players),
                "weeks": frame["week"].nunique(),
                "delta_mae_m5_minus_m3": float(frame["delta_abs_error"].mean()),
                "hierarchical_player_week_ci_low": low,
                "hierarchical_player_week_ci_high": high,
            }
        )
    return pd.DataFrame.from_records(rows)


def main() -> None:
    ensure_project_dirs()
    core = pd.read_csv(PROCESSED_DIR / "core_subjective_cohort.csv", parse_dates=["date"])
    cohort = pd.read_csv(PROCESSED_DIR / "multimodal_modeling_cohort.csv", parse_dates=["date"])
    cohort = cohort.dropna(subset=["readiness", "readiness_t_plus_1", "team", "date"]).copy()
    cohort["row_id"] = cohort.index.astype(int)
    predictions = pd.read_csv(PROCESSED_DIR / "multimodal_model_predictions.csv", parse_dates=["date"])

    propensity, propensity_summary, propensity_balance = build_propensity_scores(core, cohort)
    ipw = ipw_delta_results(predictions, propensity)
    per_player, heterogeneity_summary, influence = player_heterogeneity(predictions)
    calibration, calibration_bins = calibration_bootstrap(predictions)
    residuals = residual_strata(predictions, cohort)
    hierarchical = hierarchical_week_bootstrap(predictions)

    outputs = {
        "gnss_selection_propensity_scores.csv": propensity,
        "gnss_selection_propensity_summary.csv": propensity_summary,
        "gnss_selection_balance.csv": propensity_balance,
        "ipw_gnss_increment.csv": ipw,
        "player_level_gnss_increment.csv": per_player,
        "player_heterogeneity_summary.csv": heterogeneity_summary,
        "leave_one_player_out_influence.csv": influence,
        "external_calibration_with_ci.csv": calibration,
        "external_calibration_bins.csv": calibration_bins,
        "error_by_readiness_change.csv": residuals,
        "hierarchical_player_week_bootstrap.csv": hierarchical,
    }
    for name, frame in outputs.items():
        write_csv(frame, PROCESSED_DIR / name, index=False)

    report = f"""# Additional robustness analyses

These analyses were added after the primary analysis plan was frozen. They are
therefore labelled post-hoc robustness or exploratory analyses. The frozen
Elastic Net predictions were reused without model refitting or retuning.

## GNSS selection and inverse-probability weighting

GNSS availability was modelled from current and historical wellness,
subjective-load variables, team and season using five-fold cross-fitted logistic
regression. Next-day readiness was not included. Stabilised inverse-probability
weights were clipped through propensity bounds of 0.02 and 0.98; the trimmed
analysis additionally winsorised weights at the first and 99th percentiles.

{markdown_table(propensity_summary.round(3))}

Across the covariates entered into the selection model, the maximum absolute
standardised difference before and after weighting was
{propensity_balance['smd_unweighted'].abs().max():.3f} and
{propensity_balance['smd_ipw'].abs().max():.3f}, respectively. Full balance
diagnostics are provided in `gnss_selection_balance.csv`.

{markdown_table(ipw.round(3))}

## Player-level heterogeneity

Negative values indicate lower absolute error for M5 than M3. The main model
comparison remains observation-weighted; the summaries below give each player
equal weight and should be interpreted as exploratory descriptions of
heterogeneity.

{markdown_table(heterogeneity_summary.round(3))}

## Calibration in external validation

Calibration intercepts and slopes use player-cluster bootstrap confidence
intervals. Ideal values are 0 and 1, respectively.

{markdown_table(calibration.round(3))}

## Performance by magnitude of next-day readiness change

These post-hoc strata describe unchanged readiness, a one-point change, and a
change of at least two points. They were not used for model selection.

{markdown_table(residuals.round(3))}

## Hierarchical player-week bootstrap

This sensitivity analysis resamples players and, within sampled players,
calendar weeks. It supplements rather than replaces the prespecified
player-cluster bootstrap.

{markdown_table(hierarchical.round(3))}
"""
    write_text(REPORTS_DIR / "additional_robustness_analyses.md", report, encoding="utf-8")
    print(f"Wrote {len(outputs)} CSV outputs and {REPORTS_DIR / 'additional_robustness_analyses.md'}")


if __name__ == "__main__":
    main()
