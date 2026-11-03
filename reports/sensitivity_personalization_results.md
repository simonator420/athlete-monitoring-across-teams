# Sensitivity And Personalization Results

## Results

| split                                 | model                                                     | n    | mae   | rmse  | bias   | r2    | within_1 |
| ------------------------------------- | --------------------------------------------------------- | ---- | ----- | ----- | ------ | ----- | -------- |
| cross_team_train_A_test_B             | sensitivity_M5_plus_ACWR_ATL_CTL_monotony_strain          | 2047 | 0.65  | 0.887 | -0.111 | 0.513 | 0.809    |
| cross_team_train_A_test_B             | M5_wellness_subjective_load_gps_external_load_elastic_net | 2047 | 0.65  | 0.887 | -0.111 | 0.513 | 0.809    |
| cross_team_train_B_test_A             | sensitivity_M5_plus_ACWR_ATL_CTL_monotony_strain          | 3425 | 0.747 | 1.027 | 0.069  | 0.397 | 0.758    |
| cross_team_train_B_test_A             | M5_wellness_subjective_load_gps_external_load_elastic_net | 3425 | 0.747 | 1.027 | 0.069  | 0.397 | 0.758    |
| hr_available_cross_team_A_to_B        | M5_wellness_subjective_load_gps_external_load_elastic_net | 819  | 0.693 | 0.931 | -0.173 | 0.459 | 0.788    |
| hr_available_cross_team_A_to_B        | sensitivity_M5_plus_HR_available                          | 819  | 0.707 | 0.945 | -0.2   | 0.444 | 0.774    |
| hr_available_cross_team_B_to_A        | M5_wellness_subjective_load_gps_external_load_elastic_net | 1949 | 0.758 | 1.044 | 0.146  | 0.374 | 0.752    |
| hr_available_cross_team_B_to_A        | sensitivity_M5_plus_HR_available                          | 1949 | 0.758 | 1.044 | 0.146  | 0.374 | 0.752    |
| hr_available_temporal_2021_train_test | M5_wellness_subjective_load_gps_external_load_elastic_net | 1009 | 0.698 | 0.99  | 0.062  | 0.452 | 0.788    |
| hr_available_temporal_2021_train_test | sensitivity_M5_plus_HR_available                          | 1009 | 0.698 | 0.99  | 0.062  | 0.452 | 0.788    |
| temporal_2020_train_2021_test         | sensitivity_M5_plus_ACWR_ATL_CTL_monotony_strain          | 3246 | 0.649 | 0.902 | -0.048 | 0.484 | 0.803    |
| temporal_2020_train_2021_test         | M5_wellness_subjective_load_gps_external_load_elastic_net | 3246 | 0.65  | 0.902 | -0.063 | 0.484 | 0.803    |

## Results With Player-Cluster 95% CI

| split                                 | model                                                     | n    | mae   | rmse  | bias   | r2    | within_1 | mae_ci_low | mae_ci_high |
| ------------------------------------- | --------------------------------------------------------- | ---- | ----- | ----- | ------ | ----- | -------- | ---------- | ----------- |
| cross_team_train_A_test_B             | sensitivity_M5_plus_ACWR_ATL_CTL_monotony_strain          | 2047 | 0.65  | 0.887 | -0.111 | 0.513 | 0.809    | 0.567      | 0.762       |
| cross_team_train_A_test_B             | M5_wellness_subjective_load_gps_external_load_elastic_net | 2047 | 0.65  | 0.887 | -0.111 | 0.513 | 0.809    | 0.566      | 0.763       |
| cross_team_train_B_test_A             | sensitivity_M5_plus_ACWR_ATL_CTL_monotony_strain          | 3425 | 0.747 | 1.027 | 0.069  | 0.397 | 0.758    | 0.671      | 0.838       |
| cross_team_train_B_test_A             | M5_wellness_subjective_load_gps_external_load_elastic_net | 3425 | 0.747 | 1.027 | 0.069  | 0.397 | 0.758    | 0.671      | 0.847       |
| hr_available_cross_team_A_to_B        | M5_wellness_subjective_load_gps_external_load_elastic_net | 819  | 0.693 | 0.931 | -0.173 | 0.459 | 0.788    | 0.624      | 0.768       |
| hr_available_cross_team_A_to_B        | sensitivity_M5_plus_HR_available                          | 819  | 0.707 | 0.945 | -0.2   | 0.444 | 0.774    | 0.632      | 0.791       |
| hr_available_cross_team_B_to_A        | M5_wellness_subjective_load_gps_external_load_elastic_net | 1949 | 0.758 | 1.044 | 0.146  | 0.374 | 0.752    | 0.685      | 0.837       |
| hr_available_cross_team_B_to_A        | sensitivity_M5_plus_HR_available                          | 1949 | 0.758 | 1.044 | 0.146  | 0.374 | 0.752    | 0.683      | 0.839       |
| hr_available_temporal_2021_train_test | M5_wellness_subjective_load_gps_external_load_elastic_net | 1009 | 0.698 | 0.99  | 0.062  | 0.452 | 0.788    | 0.618      | 0.79        |
| hr_available_temporal_2021_train_test | sensitivity_M5_plus_HR_available                          | 1009 | 0.698 | 0.99  | 0.062  | 0.452 | 0.788    | 0.622      | 0.792       |
| temporal_2020_train_2021_test         | sensitivity_M5_plus_ACWR_ATL_CTL_monotony_strain          | 3246 | 0.649 | 0.902 | -0.048 | 0.484 | 0.803    | 0.594      | 0.712       |
| temporal_2020_train_2021_test         | M5_wellness_subjective_load_gps_external_load_elastic_net | 3246 | 0.65  | 0.902 | -0.063 | 0.484 | 0.803    | 0.598      | 0.71        |

## Heart-Rate Availability Sensitivity

The primary multimodal model is HR-free. These rows add HR only where HR is
available and compare the paired MAE change against the primary HR-free model.

| split                                 | comparison                         | baseline_model                                            | comparator_model                 | delta_mae | delta_mae_ci_low | delta_mae_ci_high |
| ------------------------------------- | ---------------------------------- | --------------------------------------------------------- | -------------------------------- | --------- | ---------------- | ----------------- |
| hr_available_cross_team_A_to_B        | HR_available_minus_primary_HR_free | M5_wellness_subjective_load_gps_external_load_elastic_net | sensitivity_M5_plus_HR_available | 0.014     | -0.007           | 0.03              |
| hr_available_cross_team_B_to_A        | HR_available_minus_primary_HR_free | M5_wellness_subjective_load_gps_external_load_elastic_net | sensitivity_M5_plus_HR_available | 0.0       | 0.0              | 0.0               |
| hr_available_temporal_2021_train_test | HR_available_minus_primary_HR_free | M5_wellness_subjective_load_gps_external_load_elastic_net | sensitivity_M5_plus_HR_available | 0.0       | 0.0              | 0.0               |

## Cold-Start Personalization

Each player is held out from population model fitting. The personalization
variant adds only a simple athlete-specific residual/intercept correction. For
each threshold, the population and personalized predictions are evaluated on
identical post-threshold observations.

| split                                      | model                                       | n    | mae   | rmse  | bias   | r2    | within_1 | mae_ci_low | mae_ci_high |
| ------------------------------------------ | ------------------------------------------- | ---- | ----- | ----- | ------ | ----- | -------- | ---------- | ----------- |
| leave_one_player_out_after_0_observations  | personalized_residual_after_0_observations  | 5472 | 0.671 | 0.939 | -0.002 | 0.487 | 0.799    | 0.61       | 0.74        |
| leave_one_player_out_after_0_observations  | population_prediction_after_0_observations  | 5472 | 0.671 | 0.939 | -0.002 | 0.487 | 0.799    | 0.613      | 0.737       |
| leave_one_player_out_after_14_observations | personalized_residual_after_14_observations | 4825 | 0.638 | 0.911 | -0.016 | 0.514 | 0.814    | 0.574      | 0.712       |
| leave_one_player_out_after_14_observations | population_prediction_after_14_observations | 4825 | 0.663 | 0.926 | -0.008 | 0.498 | 0.804    | 0.605      | 0.731       |
| leave_one_player_out_after_28_observations | personalized_residual_after_28_observations | 4223 | 0.615 | 0.871 | -0.019 | 0.539 | 0.827    | 0.557      | 0.683       |
| leave_one_player_out_after_28_observations | population_prediction_after_28_observations | 4223 | 0.64  | 0.888 | -0.015 | 0.521 | 0.816    | 0.585      | 0.699       |
| leave_one_player_out_after_7_observations  | personalized_residual_after_7_observations  | 5146 | 0.649 | 0.93  | -0.019 | 0.497 | 0.809    | 0.581      | 0.729       |
| leave_one_player_out_after_7_observations  | population_prediction_after_7_observations  | 5146 | 0.67  | 0.939 | -0.006 | 0.487 | 0.801    | 0.607      | 0.746       |

## Cold-Start Paired Delta MAE

| split                                      | comparison                             | baseline_model                              | comparator_model                            | delta_mae | delta_mae_ci_low | delta_mae_ci_high |
| ------------------------------------------ | -------------------------------------- | ------------------------------------------- | ------------------------------------------- | --------- | ---------------- | ----------------- |
| leave_one_player_out_after_7_observations  | personalized_minus_population_after_7  | population_prediction_after_7_observations  | personalized_residual_after_7_observations  | -0.021    | -0.043           | -0.002            |
| leave_one_player_out_after_14_observations | personalized_minus_population_after_14 | population_prediction_after_14_observations | personalized_residual_after_14_observations | -0.024    | -0.047           | -0.006            |
| leave_one_player_out_after_28_observations | personalized_minus_population_after_28 | population_prediction_after_28_observations | personalized_residual_after_28_observations | -0.025    | -0.049           | -0.005            |

## Target-Team Recalibration

The model is fit on the source-team 2020 data. Target-team 2020 data are used
only to estimate a calibration intercept/slope, then evaluation is performed on
the target-team 2021 observations.

| split                                   | model                                       | n    | mae   | rmse  | bias   | r2    | within_1 |
| --------------------------------------- | ------------------------------------------- | ---- | ----- | ----- | ------ | ----- | -------- |
| source_A2020_calibrate_B2020_test_B2021 | target_team_intercept_slope_recalibrated_M5 | 1255 | 0.686 | 0.926 | -0.157 | 0.421 | 0.783    |
| source_A2020_calibrate_B2020_test_B2021 | zero_shot_source_team_M5                    | 1255 | 0.712 | 0.935 | -0.26  | 0.411 | 0.764    |
| source_B2020_calibrate_A2020_test_A2021 | zero_shot_source_team_M5                    | 1991 | 0.71  | 0.993 | 0.05   | 0.391 | 0.776    |
| source_B2020_calibrate_A2020_test_A2021 | target_team_intercept_slope_recalibrated_M5 | 1991 | 0.718 | 0.99  | -0.031 | 0.394 | 0.768    |

## Target-Team Recalibration Paired Delta MAE

| split                                   | comparison                          | baseline_model           | comparator_model                            | delta_mae | delta_mae_ci_low | delta_mae_ci_high |
| --------------------------------------- | ----------------------------------- | ------------------------ | ------------------------------------------- | --------- | ---------------- | ----------------- |
| source_A2020_calibrate_B2020_test_B2021 | target_recalibrated_minus_zero_shot | zero_shot_source_team_M5 | target_team_intercept_slope_recalibrated_M5 | -0.025    | -0.055           | 0.002             |
| source_B2020_calibrate_A2020_test_A2021 | target_recalibrated_minus_zero_shot | zero_shot_source_team_M5 | target_team_intercept_slope_recalibrated_M5 | 0.007     | -0.005           | 0.021             |

## Focused Sensitivity Analyses

Match-day sensitivity was not run because session/activity type metadata were not available for defensible match classification.

| split                         | model                                                    | n    | mae   | rmse  | bias   | r2     | within_1 | mae_ci_low | mae_ci_high |
| ----------------------------- | -------------------------------------------------------- | ---- | ----- | ----- | ------ | ------ | -------- | ---------- | ----------- |
| cross_team_train_A_test_B     | sensitivity_complete_case_M5                             | 1690 | 0.643 | 0.877 | -0.092 | 0.531  | 0.822    | 0.561      | 0.758       |
| cross_team_train_A_test_B     | sensitivity_delta_readiness_without_current_readiness    | 2047 | 0.67  | 0.964 | -0.053 | 0.24   | 0.782    | 0.567      | 0.796       |
| cross_team_train_A_test_B     | sensitivity_imputed_M5_on_complete_case_rows             | 1690 | 0.644 | 0.876 | -0.098 | 0.531  | 0.815    | 0.564      | 0.756       |
| cross_team_train_A_test_B     | sensitivity_next_day_fatigue                             | 2047 | 0.276 | 0.441 | 0.031  | 0.211  | 0.96     | 0.204      | 0.36        |
| cross_team_train_A_test_B     | sensitivity_next_day_readiness_without_current_readiness | 2047 | 0.686 | 0.924 | -0.134 | 0.471  | 0.794    | 0.595      | 0.802       |
| cross_team_train_A_test_B     | sensitivity_next_day_soreness                            | 2046 | 0.36  | 0.468 | -0.033 | 0.37   | 0.962    | 0.296      | 0.428       |
| cross_team_train_B_test_A     | sensitivity_complete_case_M5                             | 3119 | 0.723 | 0.981 | 0.053  | 0.426  | 0.768    | 0.654      | 0.813       |
| cross_team_train_B_test_A     | sensitivity_delta_readiness_without_current_readiness    | 3425 | 0.854 | 1.201 | -0.001 | 0.239  | 0.691    | 0.763      | 0.973       |
| cross_team_train_B_test_A     | sensitivity_imputed_M5_on_complete_case_rows             | 3119 | 0.727 | 0.986 | 0.049  | 0.42   | 0.765    | 0.656      | 0.816       |
| cross_team_train_B_test_A     | sensitivity_next_day_fatigue                             | 3423 | 0.396 | 0.542 | -0.027 | 0.259  | 0.939    | 0.323      | 0.478       |
| cross_team_train_B_test_A     | sensitivity_next_day_readiness_without_current_readiness | 3425 | 0.763 | 1.046 | 0.073  | 0.374  | 0.744    | 0.688      | 0.857       |
| cross_team_train_B_test_A     | sensitivity_next_day_soreness                            | 3423 | 0.452 | 0.567 | 0.037  | 0.411  | 0.93     | 0.416      | 0.494       |
| temporal_2020_train_2021_test | sensitivity_complete_case_M5                             | 2720 | 0.635 | 0.859 | -0.075 | 0.522  | 0.805    | 0.589      | 0.689       |
| temporal_2020_train_2021_test | sensitivity_delta_readiness_without_current_readiness    | 3246 | 0.729 | 1.011 | -0.063 | 0.312  | 0.754    | 0.669      | 0.79        |
| temporal_2020_train_2021_test | sensitivity_imputed_M5_on_complete_case_rows             | 2720 | 0.63  | 0.854 | -0.066 | 0.528  | 0.811    | 0.583      | 0.687       |
| temporal_2020_train_2021_test | sensitivity_next_day_fatigue                             | 3244 | 0.334 | 0.59  | 0.032  | -0.003 | 0.824    | 0.254      | 0.422       |
| temporal_2020_train_2021_test | sensitivity_next_day_readiness_without_current_readiness | 3246 | 0.671 | 0.929 | -0.06  | 0.453  | 0.795    | 0.617      | 0.73        |
| temporal_2020_train_2021_test | sensitivity_next_day_soreness                            | 3243 | 0.406 | 0.526 | -0.012 | 0.437  | 0.938    | 0.364      | 0.447       |

## Feature Blocks

Primary model features: readiness, fatigue, soreness, mood, stress, sleep_quality, sleep_duration, readiness_past_3d_mean, readiness_past_7d_mean, fatigue_past_3d_mean, fatigue_past_7d_mean, soreness_past_3d_mean, soreness_past_7d_mean, sleep_quality_past_3d_mean, sleep_quality_past_7d_mean, sleep_duration_past_3d_mean, sleep_duration_past_7d_mean, session_count, session_srpe_sum, session_duration_sum, session_rpe_mean, session_rpe_max, session_srpe_sum_past_3d_sum, session_srpe_sum_past_7d_sum, session_srpe_sum_past_28d_sum, objective_duration_min, objective_distance_m, objective_distance_m_per_min, objective_hsr_distance_m, objective_hsr_m_per_min, objective_sprint_distance_m, objective_sprint_m_per_min, objective_speed_max, objective_accel_distance_m, objective_decel_distance_m

Derived-load sensitivity features: daily_load, weekly_load, atl, ctl28, ctl42, acwr, monotony, strain

HR sensitivity features: objective_heart_rate_mean, objective_heart_rate_max, objective_heart_rate_coverage
