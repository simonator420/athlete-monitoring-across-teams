# Analysis Plan V2

Timestamp: 2026-09-05

This plan freezes the strengthened analysis after the initial feasibility/QC
run. The earlier analysis is treated as data audit and pipeline validation; the
version below defines the final primary outcome, model ladder, validation
hierarchy, sensitivity analyses, and reporting emphasis.

## Primary Outcome

The primary outcome is next-day readiness (`readiness_t_plus_1`) among
player-days with a strict one-day follow-up and an objectively monitored
football exposure for multimodal analyses.

## Primary Predictors

Current wellness predictors are readiness, fatigue, soreness, mood, stress,
sleep quality, and sleep duration. Transparent subjective load predictors are
current session count, duration, RPE, sRPE, and preceding 3-, 7-, and 28-day
sRPE history, plus preceding 3- and 7-day wellness history. Historical features
are calculated on the full subjective longitudinal player-day dataset before
outcome filtering and before GPS matching.

The primary GPS block is HR-free and restricted to interpretable external-load
features: duration, total distance, distance per minute, high-speed-running
distance, HSR per minute, sprint distance, sprint per minute, maximum speed,
acceleration distance, and deceleration distance.

Heart-rate and GPS signal-quality variables are not primary physiological
predictors. HR is reserved for an available-HR sensitivity analysis; tick
counts, satellite count, HDOP, HACC, signal quality, raw row counts, and
implausible-tick rates are QC descriptors.

## GPS Feature Definitions

Raw SoccerMon objective files contain 100 Hz inertial rows with repeated 10 Hz
GPS values. GPS summaries are therefore first collapsed to one GPS observation
per file/time point before distance, duration, and acceleration are calculated.
Distances are computed from valid speed ticks only. Speeds greater than 12 m/s
are counted as implausible and excluded from distance, HSR, sprint, and
intensity calculations. HSR is speed >4.44 m/s. Sprinting is speed >5.55 m/s.
Acceleration/deceleration distance uses +/-2.26 m/s2 sustained for at least
three consecutive 10 Hz ticks, with qualifying efforts followed until
acceleration/deceleration returns to 0 m/s2.

Daily means are weighted by relevant tick counts rather than unweighted means
of session-level means.

## Model Ladder

All models are evaluated on identical GPS-matched observations.

- M0: training-set mean.
- M1: persistence, current readiness.
- M2: wellness plus recent wellness history.
- M3: wellness plus transparent subjective load/history.
- M4: wellness plus GPS external load.
- M5: wellness plus subjective load/history plus GPS external load.

The primary incremental-value comparison is M5 versus M3. M4 versus M2
describes GPS value without subjective load. M3 versus M2 describes subjective
load value beyond wellness.

## Validation Hierarchy

Elastic Net is the primary inferential/prediction model. CatBoost is the
secondary nonlinear benchmark. The final model set includes the two simple
baselines, tuned Elastic Net, and CatBoost. CatBoost is evaluated for M3 and M5
using the same feature blocks as Elastic Net so that GPS increment is not
confounded with algorithm choice.

Hyperparameter tuning uses inner resampling that matches the outer validation
scenario: ordinary K-fold for the random-observation experiment, GroupKFold by
player for unseen-player validation, and expanding-window forward
date-blocked validation for temporal, cross-team, team-specific temporal, and
temporal-organisational deployment splits. The forward inner validation uses
four chronological date blocks for three inner folds: block 1 validates block
2, blocks 1+2 validate block 3, and blocks 1+2+3 validate block 4.
Preprocessing, model selection, and evaluation therefore respect the structure
of each validation scenario.

The validation hierarchy includes random observation-level 5-fold CV, grouped
player-independent 5-fold CV for unseen athletes, temporal 2020 to 2021
validation, team-specific temporal validation, cross-team A to B and B to A
validation, and stringent temporal-organisational A2020 to B2021 and B2020 to
A2021 comparisons.

The prespecified primary external-validation contrast is cross-team deployment
from Team A to Team B (`cross_team_train_A_test_B`). The reverse direction and
temporal-organisational contrasts are reported as secondary transportability
checks.

## Sensitivity Analyses

Focused sensitivity analyses include derived load metrics
(ACWR/ATL/CTL/monotony/strain) added to the primary model, HR added only on
available-HR rows, team direction reversed, team-specific temporal validation,
next-day readiness without current readiness as a predictor, next-day fatigue,
next-day soreness, delta readiness with current readiness excluded, complete-case
analysis, and cold-start personalization using simple player-specific
residual/intercept correction after 0, 7, 14, and 28 previous valid observations.
Alternative-outcome prediction bounds are target-specific: readiness is bounded
to 1-10, fatigue and soreness to 1-5, and delta readiness to -9 to 9.

Cold-start personalization is evaluated against the unpersonalized population
prediction on the same post-threshold observations for each threshold. Match-day
exclusion is performed only if session/activity metadata permit defensible match
classification; otherwise the metadata limitation is documented.

Target-team recalibration is evaluated by fitting on A2020, estimating only an
intercept/slope calibration on B2020, and evaluating on B2021, then reversing the
team direction. CatBoost is not retrained on target-team data for this analysis.

Distribution-shift and GPS-selection audits compare GPS-matched versus non-GPS
core observations and Team A versus Team B using standardised mean differences
and player-date availability heatmaps.

## Uncertainty And Reporting

Important performance results are reported as effect magnitudes with
player-cluster bootstrap 95% confidence intervals. The main table reports MAE,
RMSE, R2, bias, and the proportion of predictions within +/-1 readiness point.
Paired player-cluster bootstrap intervals are reported for delta MAE, especially
M5 minus M3 and M5 minus persistence.

Interpretation is based on magnitude, precision, and transportability rather
than p-values.
