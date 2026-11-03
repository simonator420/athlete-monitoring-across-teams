# Additional robustness analyses

These analyses were added after the primary analysis plan was frozen. They are
therefore labelled post-hoc robustness or exploratory analyses. The frozen
Elastic Net predictions were reused without model refitting or retuning.

## GNSS selection and inverse-probability weighting

GNSS availability was modelled from current and historical wellness,
subjective-load variables, team and season using five-fold cross-fitted logistic
regression. Next-day readiness was not included. Stabilised inverse-probability
weights were clipped through propensity bounds of 0.02 and 0.98; the trimmed
analysis additionally winsorised weights at the first and 99th percentiles.

| team  | year | n_core | n_gnss | gnss_prevalence | propensity_auc_overall | propensity_min | propensity_max | trimmed_weight_min | trimmed_weight_max | effective_sample_size |
| ----- | ---- | ------ | ------ | --------------- | ---------------------- | -------------- | -------------- | ------------------ | ------------------ | --------------------- |
| TeamA | 2020 | 3819   | 1434   | 0.375           | 0.688                  | 0.006          | 0.964          | 0.471              | 3.04               | 1179.847              |
| TeamA | 2021 | 5903   | 1991   | 0.337           | 0.688                  | 0.011          | 0.923          | 0.471              | 3.04               | 1663.487              |
| TeamB | 2020 | 2412   | 792    | 0.328           | 0.688                  | 0.015          | 0.939          | 0.471              | 3.04               | 698.694               |
| TeamB | 2021 | 2497   | 1255   | 0.503           | 0.688                  | 0.026          | 0.928          | 0.471              | 3.04               | 1098.451              |

Across the covariates entered into the selection model, the maximum absolute
standardised difference before and after weighting was
0.326 and
0.195, respectively. Full balance
diagnostics are provided in `gnss_selection_balance.csv`.

| split                     | analysis         | n    | players | effective_sample_size | delta_mae_m5_minus_m3 | ci_low | ci_high |
| ------------------------- | ---------------- | ---- | ------- | --------------------- | --------------------- | ------ | ------- |
| cross_team_train_A_test_B | unweighted       | 2047 | 22      | 2047.0                | -0.061                | -0.095 | -0.028  |
| cross_team_train_A_test_B | ipw_untrimmed    | 2047 | 22      | 1769.98               | -0.051                | -0.091 | -0.016  |
| cross_team_train_A_test_B | ipw_trimmed_1_99 | 2047 | 22      | 1795.211              | -0.052                | -0.092 | -0.017  |
| cross_team_train_B_test_A | unweighted       | 3425 | 25      | 3425.0                | -0.002                | -0.026 | 0.028   |
| cross_team_train_B_test_A | ipw_untrimmed    | 3425 | 25      | 2588.344              | 0.014                 | -0.013 | 0.045   |
| cross_team_train_B_test_A | ipw_trimmed_1_99 | 3425 | 25      | 2832.993              | 0.014                 | -0.012 | 0.045   |

## Player-level heterogeneity

Negative values indicate lower absolute error for M5 than M3. The main model
comparison remains observation-weighted; the summaries below give each player
equal weight and should be interpreted as exploratory descriptions of
heterogeneity.

| split                     | players | player_weighted_mean_delta | player_weighted_mean_ci_low | player_weighted_mean_ci_high | median_player_delta | median_ci_low | median_ci_high | player_delta_q1 | player_delta_q3 | players_improved_n | players_improved_proportion | players_improved_ci_low | players_improved_ci_high |
| ------------------------- | ------- | -------------------------- | --------------------------- | ---------------------------- | ------------------- | ------------- | -------------- | --------------- | --------------- | ------------------ | --------------------------- | ----------------------- | ------------------------ |
| cross_team_train_A_test_B | 22      | -0.058                     | -0.082                      | -0.033                       | -0.055              | -0.088        | -0.019         | -0.099          | -0.016          | 18                 | 0.818                       | 0.636                   | 0.955                    |
| cross_team_train_B_test_A | 25      | -0.005                     | -0.032                      | 0.021                        | -0.014              | -0.031        | 0.02           | -0.034          | 0.035           | 16                 | 0.64                        | 0.44                    | 0.84                     |

## Calibration in external validation

Calibration intercepts and slopes use player-cluster bootstrap confidence
intervals. Ideal values are 0 and 1, respectively.

| split                     | model                                                     | n    | players | calibration_intercept | intercept_ci_low | intercept_ci_high | calibration_slope | slope_ci_low | slope_ci_high | mean_observed | mean_predicted | bias   |
| ------------------------- | --------------------------------------------------------- | ---- | ------- | --------------------- | ---------------- | ----------------- | ----------------- | ------------ | ------------- | ------------- | -------------- | ------ |
| cross_team_train_A_test_B | M1_persistence                                            | 2047 | 22      | 2.229                 | 1.203            | 3.922             | 0.659             | 0.42         | 0.804         | 7.058         | 7.331          | 0.273  |
| cross_team_train_A_test_B | M3_wellness_subjective_load_elastic_net                   | 2047 | 22      | -0.55                 | -1.156           | 0.399             | 1.112             | 0.971        | 1.194         | 7.058         | 6.841          | -0.217 |
| cross_team_train_A_test_B | M5_wellness_subjective_load_gps_external_load_elastic_net | 2047 | 22      | -0.607                | -1.451           | 0.531             | 1.103             | 0.934        | 1.218         | 7.058         | 6.946          | -0.111 |
| cross_team_train_B_test_A | M1_persistence                                            | 3425 | 25      | 3.581                 | 2.605            | 4.738             | 0.451             | 0.301        | 0.579         | 6.772         | 7.083          | 0.311  |
| cross_team_train_B_test_A | M3_wellness_subjective_load_elastic_net                   | 3425 | 25      | -0.557                | -1.108           | 0.25              | 1.06              | 0.949        | 1.137         | 6.772         | 6.914          | 0.142  |
| cross_team_train_B_test_A | M5_wellness_subjective_load_gps_external_load_elastic_net | 3425 | 25      | -0.94                 | -1.901           | 0.226             | 1.127             | 0.957        | 1.264         | 6.772         | 6.841          | 0.069  |

## Performance by magnitude of next-day readiness change

These post-hoc strata describe unchanged readiness, a one-point change, and a
change of at least two points. They were not used for model selection.

| split                     | model                                                     | change_stratum | n    | players | mae   | mae_ci_low | mae_ci_high | bias   |
| ------------------------- | --------------------------------------------------------- | -------------- | ---- | ------- | ----- | ---------- | ----------- | ------ |
| cross_team_train_A_test_B | M1_persistence                                            | unchanged      | 1264 | 22      | 0.0   | 0.0        | 0.0         | 0.0    |
| cross_team_train_A_test_B | M1_persistence                                            | one_point      | 527  | 22      | 1.0   | 1.0        | 1.0         | 0.199  |
| cross_team_train_A_test_B | M1_persistence                                            | two_or_more    | 256  | 21      | 2.664 | 2.39       | 3.022       | 1.773  |
| cross_team_train_A_test_B | M3_wellness_subjective_load_elastic_net                   | unchanged      | 1264 | 22      | 0.568 | 0.464      | 0.689       | -0.401 |
| cross_team_train_A_test_B | M3_wellness_subjective_load_elastic_net                   | one_point      | 527  | 22      | 0.686 | 0.623      | 0.753       | -0.291 |
| cross_team_train_A_test_B | M3_wellness_subjective_load_elastic_net                   | two_or_more    | 256  | 21      | 1.468 | 1.258      | 1.703       | 0.846  |
| cross_team_train_A_test_B | M5_wellness_subjective_load_gps_external_load_elastic_net | unchanged      | 1264 | 22      | 0.484 | 0.417      | 0.57        | -0.273 |
| cross_team_train_A_test_B | M5_wellness_subjective_load_gps_external_load_elastic_net | one_point      | 527  | 22      | 0.654 | 0.611      | 0.719       | -0.193 |
| cross_team_train_A_test_B | M5_wellness_subjective_load_gps_external_load_elastic_net | two_or_more    | 256  | 21      | 1.461 | 1.249      | 1.7         | 0.852  |
| cross_team_train_B_test_A | M1_persistence                                            | unchanged      | 1459 | 25      | 0.0   | 0.0        | 0.0         | 0.0    |
| cross_team_train_B_test_A | M1_persistence                                            | one_point      | 1324 | 25      | 1.0   | 1.0        | 1.0         | -0.026 |
| cross_team_train_B_test_A | M1_persistence                                            | two_or_more    | 642  | 25      | 2.749 | 2.58       | 2.902       | 1.712  |
| cross_team_train_B_test_A | M3_wellness_subjective_load_elastic_net                   | unchanged      | 1459 | 25      | 0.41  | 0.364      | 0.466       | -0.063 |
| cross_team_train_B_test_A | M3_wellness_subjective_load_elastic_net                   | one_point      | 1324 | 25      | 0.689 | 0.651      | 0.736       | -0.035 |
| cross_team_train_B_test_A | M3_wellness_subjective_load_elastic_net                   | two_or_more    | 642  | 25      | 1.645 | 1.525      | 1.767       | 0.972  |
| cross_team_train_B_test_A | M5_wellness_subjective_load_gps_external_load_elastic_net | unchanged      | 1459 | 25      | 0.461 | 0.394      | 0.528       | -0.074 |
| cross_team_train_B_test_A | M5_wellness_subjective_load_gps_external_load_elastic_net | one_point      | 1324 | 25      | 0.717 | 0.663      | 0.778       | -0.09  |
| cross_team_train_B_test_A | M5_wellness_subjective_load_gps_external_load_elastic_net | two_or_more    | 642  | 25      | 1.46  | 1.287      | 1.671       | 0.723  |

## Hierarchical player-week bootstrap

This sensitivity analysis resamples players and, within sampled players,
calendar weeks. It supplements rather than replaces the prespecified
player-cluster bootstrap.

| split                     | n    | players | weeks | delta_mae_m5_minus_m3 | hierarchical_player_week_ci_low | hierarchical_player_week_ci_high |
| ------------------------- | ---- | ------- | ----- | --------------------- | ------------------------------- | -------------------------------- |
| cross_team_train_A_test_B | 2047 | 22      | 67    | -0.061                | -0.097                          | -0.026                           |
| cross_team_train_B_test_A | 3425 | 25      | 68    | -0.002                | -0.028                          | 0.03                             |
