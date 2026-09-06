from __future__ import annotations

import warnings
from collections.abc import Iterable

import numpy as np
import pandas as pd
from sklearn.exceptions import ConvergenceWarning
from sklearn.impute import SimpleImputer
from sklearn.linear_model import ElasticNet
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV, GroupKFold, KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


CURRENT_WELLNESS_FEATURES = [
    "readiness",
    "fatigue",
    "soreness",
    "mood",
    "stress",
    "sleep_quality",
    "sleep_duration",
]

WELLNESS_HISTORY_BASE = [
    "readiness",
    "fatigue",
    "soreness",
    "sleep_quality",
    "sleep_duration",
]

CURRENT_LOAD_FEATURES = [
    "session_count",
    "session_srpe_sum",
    "session_duration_sum",
    "session_rpe_mean",
    "session_rpe_max",
]

LOAD_HISTORY_BASE = ["session_srpe_sum"]

DERIVED_LOAD_SENSITIVITY_FEATURES = [
    "daily_load",
    "weekly_load",
    "atl",
    "ctl28",
    "ctl42",
    "acwr",
    "monotony",
    "strain",
]

GPS_EXTERNAL_LOAD_FEATURES = [
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

HR_FEATURES = [
    "objective_heart_rate_mean",
    "objective_heart_rate_max",
    "objective_heart_rate_coverage",
]

GPS_QC_FEATURES = [
    "objective_gps_tick_count",
    "objective_valid_speed_tick_count",
    "objective_raw_row_count",
    "objective_hacc_mean",
    "objective_hdop_mean",
    "objective_signal_quality_mean",
    "objective_num_satellites_mean",
    "objective_num_satellites_min",
    "objective_num_satellites_max",
    "objective_implausible_speed_tick_rate",
    "objective_implausible_heart_rate_tick_rate",
]

TARGET_BOUNDS = {
    "readiness_t_plus_1": (1.0, 10.0),
    "fatigue_t_plus_1": (1.0, 5.0),
    "soreness_t_plus_1": (1.0, 5.0),
    "readiness_delta_t_plus_1": (-9.0, 9.0),
}

# Backwards-compatible names used by older scripts.
SUBJECTIVE_FEATURES = CURRENT_WELLNESS_FEATURES + CURRENT_LOAD_FEATURES + DERIVED_LOAD_SENSITIVITY_FEATURES
OBJECTIVE_FEATURES = GPS_EXTERNAL_LOAD_FEATURES


def available(frame: pd.DataFrame, columns: Iterable[str]) -> list[str]:
    return [col for col in columns if col in frame.columns]


def add_transparent_history_features(data: pd.DataFrame) -> pd.DataFrame:
    out = data.copy()
    out["date"] = pd.to_datetime(out["date"])
    out = out.sort_values(["player_id", "date"]).reset_index(drop=True)

    def calendar_rolling(group: pd.DataFrame, col: str, window: int, agg: str) -> pd.Series:
        series = pd.to_numeric(group[col], errors="coerce")
        indexed = pd.Series(series.to_numpy(dtype=float), index=pd.to_datetime(group["date"]))
        rolling = indexed.rolling(f"{window}D", closed="left", min_periods=1)
        values = rolling.mean() if agg == "mean" else rolling.sum()
        return pd.Series(values.to_numpy(dtype=float), index=group.index)

    grouped = out.groupby("player_id", group_keys=False)

    def assign_calendar_history(col: str, window: int, agg: str) -> pd.Series:
        values = pd.Series(index=out.index, dtype=float)
        for _, group in grouped:
            values.loc[group.index] = calendar_rolling(group, col, window, agg)
        return values

    for col in WELLNESS_HISTORY_BASE:
        if col not in out.columns:
            continue
        for window in [3, 7]:
            name = f"{col}_past_{window}d_mean"
            out[name] = assign_calendar_history(col, window, "mean")
    for col in LOAD_HISTORY_BASE:
        if col not in out.columns:
            continue
        for window in [3, 7, 28]:
            name = f"{col}_past_{window}d_sum"
            out[name] = assign_calendar_history(col, window, "sum")
    return out


def feature_blocks(data: pd.DataFrame) -> dict[str, list[str]]:
    wellness_history = [col for col in data.columns if col.endswith(("past_3d_mean", "past_7d_mean"))]
    load_history = [col for col in data.columns if col.endswith(("past_3d_sum", "past_7d_sum", "past_28d_sum"))]
    wellness = available(data, CURRENT_WELLNESS_FEATURES) + wellness_history
    subjective_load = available(data, CURRENT_LOAD_FEATURES) + load_history
    gps = available(data, GPS_EXTERNAL_LOAD_FEATURES)
    hr = available(data, HR_FEATURES)
    derived_load = available(data, DERIVED_LOAD_SENSITIVITY_FEATURES)
    return {
        "wellness": wellness,
        "subjective_load": subjective_load,
        "gps_external_load": gps,
        "hr": hr,
        "derived_load_sensitivity": derived_load,
        "gps_qc": available(data, GPS_QC_FEATURES),
    }


def metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    error = y_pred - y_true
    return {
        "n": float(len(y_true)),
        "mae": float(np.mean(np.abs(error))),
        "rmse": float(np.sqrt(np.mean(error**2))),
        "bias": float(np.mean(error)),
        "r2": float(r2_score(y_true, y_pred)) if len(np.unique(y_true)) > 1 else float("nan"),
        "within_1": float(np.mean(np.abs(error) <= 1.0)),
    }


def apply_target_bounds(pred: np.ndarray, target_col: str, fallback: float) -> np.ndarray:
    lower, upper = TARGET_BOUNDS.get(target_col, (float("-inf"), float("inf")))
    pred = np.asarray(pred, dtype=float)
    finite_lower = lower if np.isfinite(lower) else fallback
    finite_upper = upper if np.isfinite(upper) else fallback
    pred = np.nan_to_num(pred, nan=fallback, posinf=finite_upper, neginf=finite_lower)
    return np.clip(pred, lower, upper)


def make_elastic_net(cv: int | list[tuple[np.ndarray, np.ndarray]] | GroupKFold, random_state: int = 20260905) -> GridSearchCV:
    pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "model",
                ElasticNet(
                    max_iter=5000,
                    random_state=random_state,
                    tol=1e-3,
                ),
            ),
        ]
    )
    tuned = GridSearchCV(
        pipeline,
        param_grid={
            "model__alpha": np.logspace(-2, 1, 8),
            "model__l1_ratio": [0.2, 0.8, 1.0],
        },
        scoring="neg_mean_absolute_error",
        cv=cv,
        n_jobs=1,
    )
    return tuned


def make_catboost(cv: int | list[tuple[np.ndarray, np.ndarray]] | GroupKFold, random_state: int = 20260905) -> GridSearchCV:
    try:
        from catboost import CatBoostRegressor
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "CatBoost is required for the final v2 model comparison. "
            "Install requirements.txt in the notebook runtime first."
        ) from exc

    pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            (
                "model",
                CatBoostRegressor(
                    loss_function="MAE",
                    random_seed=random_state,
                    verbose=False,
                    allow_writing_files=False,
                    thread_count=-1,
                ),
            ),
        ]
    )
    tuned = GridSearchCV(
        pipeline,
        param_grid={
            "model__depth": [3, 5, 7],
            "model__learning_rate": [0.03, 0.05],
            "model__iterations": [300, 600],
            "model__l2_leaf_reg": [3, 10],
        },
        scoring="neg_mean_absolute_error",
        cv=cv,
        n_jobs=1,
    )
    return tuned


def date_blocked_forward_cv(train: pd.DataFrame, n_splits: int = 3) -> list[tuple[np.ndarray, np.ndarray]]:
    dates = pd.Series(pd.to_datetime(train["date"]).dropna().unique()).sort_values().to_numpy()
    if len(dates) < 2:
        return []
    blocks = np.array_split(dates, min(n_splits + 1, len(dates)))
    splits: list[tuple[np.ndarray, np.ndarray]] = []
    train_dates = pd.to_datetime(train["date"])
    for validation_block_pos in range(1, len(blocks)):
        train_block_dates = np.concatenate(blocks[:validation_block_pos])
        validation_block = blocks[validation_block_pos]
        if len(train_block_dates) == 0 or len(validation_block) == 0:
            continue
        development_dates = set(pd.Timestamp(date) for date in train_block_dates)
        validation_dates = set(pd.Timestamp(date) for date in validation_block)
        train_idx = np.flatnonzero(train_dates.isin(development_dates).to_numpy())
        validation_idx = np.flatnonzero(train_dates.isin(validation_dates).to_numpy())
        if len(train_idx) and len(validation_idx):
            splits.append((train_idx, validation_idx))
    return splits


def inner_cv_for_split(split: str, train: pd.DataFrame) -> tuple[int | list[tuple[np.ndarray, np.ndarray]] | GroupKFold, np.ndarray | None]:
    if split == "random_observation_5fold":
        return min(3, len(train)), None
    if "unseen_player" in split or "leave_one_player" in split:
        groups = train["player_id"].to_numpy()
        n_groups = len(pd.unique(groups))
        if n_groups >= 2:
            return GroupKFold(n_splits=min(3, n_groups)), groups
        return min(3, len(train)), None
    blocked = date_blocked_forward_cv(train)
    if blocked:
        return blocked, None
    return min(3, len(train)), None


def model_prediction(
    train: pd.DataFrame,
    test: pd.DataFrame,
    feature_cols: list[str],
    algorithm: str,
    split: str = "random_observation_5fold",
    target_col: str = "readiness_t_plus_1",
) -> np.ndarray:
    fallback = float(train[target_col].median())
    if not feature_cols:
        return apply_target_bounds(np.repeat(fallback, len(test)), target_col, fallback)
    x_train = train[feature_cols].replace([np.inf, -np.inf], np.nan)
    y_train = train[target_col].to_numpy(dtype=float)
    x_test = test[feature_cols].replace([np.inf, -np.inf], np.nan)
    cv, groups = inner_cv_for_split(split, train)
    if isinstance(cv, int) and cv < 2:
        return apply_target_bounds(np.repeat(fallback, len(test)), target_col, fallback)
    if algorithm == "elastic_net":
        model = make_elastic_net(cv=cv)
    elif algorithm == "catboost":
        model = make_catboost(cv=cv)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        if groups is None:
            model.fit(x_train, y_train)
        else:
            model.fit(x_train, y_train, groups=groups)
        pred = model.predict(x_test)
    return apply_target_bounds(pred, target_col, fallback)


def elastic_net_prediction(
    train: pd.DataFrame,
    test: pd.DataFrame,
    feature_cols: list[str],
    split: str = "random_observation_5fold",
    target_col: str = "readiness_t_plus_1",
) -> np.ndarray:
    return model_prediction(train, test, feature_cols, "elastic_net", split=split, target_col=target_col)


def catboost_prediction(
    train: pd.DataFrame,
    test: pd.DataFrame,
    feature_cols: list[str],
    split: str = "random_observation_5fold",
    target_col: str = "readiness_t_plus_1",
) -> np.ndarray:
    return model_prediction(train, test, feature_cols, "catboost", split=split, target_col=target_col)


def linear_prediction(train: pd.DataFrame, test: pd.DataFrame, feature_cols: list[str]) -> np.ndarray:
    return elastic_net_prediction(train, test, feature_cols)


def global_mean_prediction(train: pd.DataFrame, test: pd.DataFrame) -> np.ndarray:
    return np.repeat(float(train["readiness_t_plus_1"].mean()), len(test))


def persistence_prediction(_: pd.DataFrame, test: pd.DataFrame) -> np.ndarray:
    return test["readiness"].to_numpy(dtype=float)


def evaluate_models(
    split: str,
    train: pd.DataFrame,
    test: pd.DataFrame,
    subjective_cols: list[str],
    objective_cols: list[str] | None = None,
) -> list[dict[str, object]]:
    if train.empty or test.empty:
        return []

    y = test["readiness_t_plus_1"].to_numpy(dtype=float)
    rows = [
        {"split": split, "model": "M0_training_mean", **metrics(y, global_mean_prediction(train, test))},
        {"split": split, "model": "M1_persistence", **metrics(y, persistence_prediction(train, test))},
        {
            "split": split,
            "model": "elastic_net_subjective",
            **metrics(y, elastic_net_prediction(train, test, subjective_cols, split=split)),
        },
    ]
    if objective_cols:
        rows.append(
            {
                "split": split,
                "model": "elastic_net_subjective_gps",
                **metrics(y, elastic_net_prediction(train, test, subjective_cols + objective_cols, split=split)),
            }
        )
    return rows


def ladder_feature_sets(blocks: dict[str, list[str]]) -> dict[str, list[str]]:
    wellness = blocks["wellness"]
    load = blocks["subjective_load"]
    gps = blocks["gps_external_load"]
    return {
        "M2_wellness_elastic_net": wellness,
        "M3_wellness_subjective_load_elastic_net": wellness + load,
        "M4_wellness_gps_external_load_elastic_net": wellness + gps,
        "M5_wellness_subjective_load_gps_external_load_elastic_net": wellness + load + gps,
    }


def predict_ladder(
    split: str,
    train: pd.DataFrame,
    test: pd.DataFrame,
    blocks: dict[str, list[str]],
) -> dict[str, np.ndarray]:
    predictions = {
        "M0_training_mean": global_mean_prediction(train, test),
        "M1_persistence": persistence_prediction(train, test),
    }
    feature_sets = ladder_feature_sets(blocks)
    for model_name, cols in feature_sets.items():
        predictions[model_name] = elastic_net_prediction(train, test, cols, split=split)
    predictions["M3_wellness_subjective_load_catboost"] = catboost_prediction(
        train, test, feature_sets["M3_wellness_subjective_load_elastic_net"], split=split
    )
    predictions["M5_wellness_subjective_load_gps_external_load_catboost"] = catboost_prediction(
        train, test, feature_sets["M5_wellness_subjective_load_gps_external_load_elastic_net"], split=split
    )
    return predictions


def evaluate_ladder_predictions(
    split: str,
    train: pd.DataFrame,
    test: pd.DataFrame,
    blocks: dict[str, list[str]],
) -> pd.DataFrame:
    if train.empty or test.empty:
        return pd.DataFrame()
    records: list[dict[str, object]] = []
    for model, pred in predict_ladder(split, train, test, blocks).items():
        for row, y_pred in zip(test.itertuples(), pred):
            records.append(
                {
                    "split": split,
                    "model": model,
                    "row_id": int(row.Index),
                    "player_id": row.player_id,
                    "team": row.team,
                    "date": row.date,
                    "y_true": float(row.readiness_t_plus_1),
                    "y_pred": float(y_pred),
                }
            )
    return pd.DataFrame.from_records(records)


def summarize_predictions(predictions: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (split, model), group in predictions.groupby(["split", "model"], sort=False):
        rows.append({"split": split, "model": model, **metrics(group["y_true"].to_numpy(), group["y_pred"].to_numpy())})
    out = pd.DataFrame.from_records(rows)
    if not out.empty:
        out["n"] = out["n"].astype(int)
    return out


def add_skill_vs_persistence(results: pd.DataFrame) -> pd.DataFrame:
    if results.empty:
        return results
    persistence = results[results["model"] == "M1_persistence"][["split", "mae"]].rename(
        columns={"mae": "persistence_mae"}
    )
    out = results.merge(persistence, on="split", how="left")
    out["skill_vs_persistence"] = 1 - (out["mae"] / out["persistence_mae"])
    out.loc[out["model"] == "M1_persistence", "skill_vs_persistence"] = 0.0
    return out.drop(columns=["persistence_mae"])


def calibration_summary(predictions: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (split, model), group in predictions.groupby(["split", "model"], sort=False):
        y_pred = group["y_pred"].to_numpy(dtype=float)
        y_true = group["y_true"].to_numpy(dtype=float)
        if len(group) < 3 or np.nanstd(y_pred) == 0:
            slope = float("nan")
            intercept = float("nan")
        else:
            slope, intercept = np.polyfit(y_pred, y_true, deg=1)
        rows.append(
            {
                "split": split,
                "model": model,
                "n": int(len(group)),
                "calibration_intercept": float(intercept),
                "calibration_slope": float(slope),
                "mean_observed": float(np.mean(y_true)),
                "mean_predicted": float(np.mean(y_pred)),
            }
        )
    return pd.DataFrame.from_records(rows)


def random_observation_5fold_predictions(data: pd.DataFrame, blocks: dict[str, list[str]]) -> pd.DataFrame:
    chunks = []
    fold = KFold(n_splits=5, shuffle=True, random_state=20260905)
    for train_idx, test_idx in fold.split(data):
        train = data.iloc[train_idx]
        test = data.iloc[test_idx]
        chunks.append(evaluate_ladder_predictions("random_observation_5fold", train, test, blocks))
    return pd.concat(chunks, ignore_index=True)


def grouped_player_5fold_predictions(data: pd.DataFrame, blocks: dict[str, list[str]]) -> pd.DataFrame:
    players = data["player_id"].dropna().unique()
    n_splits = min(5, len(players))
    if n_splits < 2:
        return pd.DataFrame()
    chunks = []
    fold = GroupKFold(n_splits=n_splits)
    groups = data["player_id"].to_numpy()
    for train_idx, test_idx in fold.split(data, groups=groups):
        train = data.iloc[train_idx]
        test = data.iloc[test_idx]
        chunks.append(evaluate_ladder_predictions("unseen_player_grouped_5fold", train, test, blocks))
    return pd.concat(chunks, ignore_index=True)


def split_predictions(data: pd.DataFrame, blocks: dict[str, list[str]]) -> pd.DataFrame:
    year = data["date"].dt.year
    definitions = [
        ("temporal_2020_train_2021_test", year == 2020, year == 2021),
        ("teamA_temporal_2020_train_2021_test", (data["team"] == "TeamA") & (year == 2020), (data["team"] == "TeamA") & (year == 2021)),
        ("teamB_temporal_2020_train_2021_test", (data["team"] == "TeamB") & (year == 2020), (data["team"] == "TeamB") & (year == 2021)),
        ("cross_team_train_A_test_B", data["team"] == "TeamA", data["team"] == "TeamB"),
        ("cross_team_train_B_test_A", data["team"] == "TeamB", data["team"] == "TeamA"),
        ("temporal_org_train_A2020_test_B2021", (data["team"] == "TeamA") & (year == 2020), (data["team"] == "TeamB") & (year == 2021)),
        ("temporal_org_train_B2020_test_A2021", (data["team"] == "TeamB") & (year == 2020), (data["team"] == "TeamA") & (year == 2021)),
    ]
    chunks = [random_observation_5fold_predictions(data, blocks), grouped_player_5fold_predictions(data, blocks)]
    for split, train_mask, test_mask in definitions:
        chunks.append(evaluate_ladder_predictions(split, data[train_mask], data[test_mask], blocks))
    return pd.concat([chunk for chunk in chunks if not chunk.empty], ignore_index=True)


def player_cluster_bootstrap_metrics(
    predictions: pd.DataFrame,
    n_bootstrap: int = 2000,
    seed: int = 20260905,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for (split, model), group in predictions.groupby(["split", "model"], sort=False):
        players = group["player_id"].dropna().unique()
        groups = {player: group.index[group["player_id"] == player].to_numpy() for player in players}
        mae = []
        for _ in range(n_bootstrap):
            sampled = rng.choice(players, size=len(players), replace=True)
            idx = np.concatenate([groups[player] for player in sampled])
            sample = group.loc[idx]
            mae.append(float(np.mean(np.abs(sample["y_pred"] - sample["y_true"]))))
        point = metrics(group["y_true"].to_numpy(), group["y_pred"].to_numpy())
        rows.append(
            {
                "split": split,
                "model": model,
                **point,
                "mae_ci_low": float(np.percentile(mae, 2.5)),
                "mae_ci_high": float(np.percentile(mae, 97.5)),
            }
        )
    out = pd.DataFrame.from_records(rows)
    if not out.empty:
        out["n"] = out["n"].astype(int)
    return out


def paired_delta_mae_ci(
    predictions: pd.DataFrame,
    baseline_model: str,
    comparator_model: str,
    delta_name: str,
    n_bootstrap: int = 2000,
    seed: int = 20260905,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for split, group in predictions.groupby("split", sort=False):
        pivot = group[group["model"].isin([baseline_model, comparator_model])].pivot(
            index=["row_id", "player_id"], columns="model", values=["y_true", "y_pred"]
        )
        if ("y_pred", baseline_model) not in pivot or ("y_pred", comparator_model) not in pivot:
            continue
        truth = pivot[("y_true", baseline_model)]
        baseline_abs = (pivot[("y_pred", baseline_model)] - truth).abs()
        comparator_abs = (pivot[("y_pred", comparator_model)] - truth).abs()
        frame = pd.DataFrame(
            {
                "player_id": pivot.index.get_level_values("player_id"),
                "delta": comparator_abs.to_numpy() - baseline_abs.to_numpy(),
            }
        )
        players = frame["player_id"].dropna().unique()
        groups = {player: frame.index[frame["player_id"] == player].to_numpy() for player in players}
        boot = []
        for _ in range(n_bootstrap):
            sampled = rng.choice(players, size=len(players), replace=True)
            idx = np.concatenate([groups[player] for player in sampled])
            boot.append(float(frame.loc[idx, "delta"].mean()))
        point = float(frame["delta"].mean())
        rows.append(
            {
                "split": split,
                "comparison": delta_name,
                "baseline_model": baseline_model,
                "comparator_model": comparator_model,
                "delta_mae": point,
                "delta_mae_ci_low": float(np.percentile(boot, 2.5)),
                "delta_mae_ci_high": float(np.percentile(boot, 97.5)),
            }
        )
    return pd.DataFrame.from_records(rows)
