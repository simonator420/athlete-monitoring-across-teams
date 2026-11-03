# Multimodal Model Results

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

| split                               | model                                                     | n    | mae   | rmse  | bias   | r2     | within_1 | skill_vs_persistence |
| ----------------------------------- | --------------------------------------------------------- | ---- | ----- | ----- | ------ | ------ | -------- | -------------------- |
| cross_team_train_A_test_B           | M5_wellness_subjective_load_gps_external_load_catboost    | 2047 | 0.587 | 0.85  | -0.056 | 0.552  | 0.823    | 0.006                |
| cross_team_train_A_test_B           | M1_persistence                                            | 2047 | 0.591 | 1.139 | 0.273  | 0.196  | 0.875    | 0.0                  |
| cross_team_train_A_test_B           | M4_wellness_gps_external_load_elastic_net                 | 2047 | 0.623 | 0.882 | 0.006  | 0.518  | 0.822    | -0.055               |
| cross_team_train_A_test_B           | M3_wellness_subjective_load_catboost                      | 2047 | 0.646 | 0.912 | -0.121 | 0.484  | 0.791    | -0.093               |
| cross_team_train_A_test_B           | M5_wellness_subjective_load_gps_external_load_elastic_net | 2047 | 0.65  | 0.887 | -0.111 | 0.513  | 0.809    | -0.1                 |
| cross_team_train_A_test_B           | M2_wellness_elastic_net                                   | 2047 | 0.69  | 0.982 | -0.102 | 0.402  | 0.774    | -0.167               |
| cross_team_train_A_test_B           | M3_wellness_subjective_load_elastic_net                   | 2047 | 0.711 | 0.947 | -0.217 | 0.444  | 0.778    | -0.204               |
| cross_team_train_A_test_B           | M0_training_mean                                          | 2047 | 1.063 | 1.302 | -0.286 | -0.051 | 0.51     | -0.8                 |
| cross_team_train_B_test_A           | M5_wellness_subjective_load_gps_external_load_catboost    | 3425 | 0.713 | 1.011 | 0.088  | 0.416  | 0.758    | 0.209                |
| cross_team_train_B_test_A           | M3_wellness_subjective_load_catboost                      | 3425 | 0.744 | 1.045 | 0.082  | 0.376  | 0.751    | 0.176                |
| cross_team_train_B_test_A           | M5_wellness_subjective_load_gps_external_load_elastic_net | 3425 | 0.747 | 1.027 | 0.069  | 0.397  | 0.758    | 0.172                |
| cross_team_train_B_test_A           | M3_wellness_subjective_load_elastic_net                   | 3425 | 0.749 | 1.044 | 0.142  | 0.376  | 0.75     | 0.169                |
| cross_team_train_B_test_A           | M4_wellness_gps_external_load_elastic_net                 | 3425 | 0.76  | 1.04  | 0.031  | 0.381  | 0.745    | 0.158                |
| cross_team_train_B_test_A           | M2_wellness_elastic_net                                   | 3425 | 0.844 | 1.147 | 0.059  | 0.247  | 0.697    | 0.064                |
| cross_team_train_B_test_A           | M1_persistence                                            | 3425 | 0.902 | 1.411 | 0.311  | -0.139 | 0.813    | 0.0                  |
| cross_team_train_B_test_A           | M0_training_mean                                          | 3425 | 1.018 | 1.353 | 0.286  | -0.047 | 0.528    | -0.129               |
| random_observation_5fold            | M5_wellness_subjective_load_gps_external_load_catboost    | 5472 | 0.584 | 0.872 | 0.037  | 0.557  | 0.827    | 0.257                |
| random_observation_5fold            | M3_wellness_subjective_load_catboost                      | 5472 | 0.631 | 0.94  | 0.066  | 0.486  | 0.8      | 0.197                |
| random_observation_5fold            | M5_wellness_subjective_load_gps_external_load_elastic_net | 5472 | 0.656 | 0.925 | -0.0   | 0.501  | 0.808    | 0.165                |
| random_observation_5fold            | M4_wellness_gps_external_load_elastic_net                 | 5472 | 0.669 | 0.943 | -0.0   | 0.482  | 0.795    | 0.148                |
| random_observation_5fold            | M3_wellness_subjective_load_elastic_net                   | 5472 | 0.706 | 0.979 | 0.0    | 0.442  | 0.78     | 0.101                |
| random_observation_5fold            | M2_wellness_elastic_net                                   | 5472 | 0.772 | 1.078 | -0.0   | 0.324  | 0.734    | 0.017                |
| random_observation_5fold            | M1_persistence                                            | 5472 | 0.785 | 1.316 | 0.297  | -0.009 | 0.836    | 0.0                  |
| random_observation_5fold            | M0_training_mean                                          | 5472 | 1.023 | 1.311 | 0.0    | -0.0   | 0.537    | -0.303               |
| teamA_temporal_2020_train_2021_test | M5_wellness_subjective_load_gps_external_load_catboost    | 1991 | 0.646 | 0.894 | -0.057 | 0.506  | 0.808    | 0.236                |
| teamA_temporal_2020_train_2021_test | M3_wellness_subjective_load_catboost                      | 1991 | 0.656 | 0.917 | -0.016 | 0.48   | 0.797    | 0.223                |
| teamA_temporal_2020_train_2021_test | M5_wellness_subjective_load_gps_external_load_elastic_net | 1991 | 0.677 | 0.937 | -0.076 | 0.457  | 0.781    | 0.199                |
| teamA_temporal_2020_train_2021_test | M4_wellness_gps_external_load_elastic_net                 | 1991 | 0.679 | 0.945 | -0.011 | 0.447  | 0.79     | 0.197                |
| teamA_temporal_2020_train_2021_test | M3_wellness_subjective_load_elastic_net                   | 1991 | 0.718 | 0.977 | -0.084 | 0.409  | 0.763    | 0.15                 |
| teamA_temporal_2020_train_2021_test | M2_wellness_elastic_net                                   | 1991 | 0.81  | 1.1   | -0.027 | 0.252  | 0.711    | 0.041                |
| teamA_temporal_2020_train_2021_test | M1_persistence                                            | 1991 | 0.845 | 1.338 | 0.299  | -0.106 | 0.833    | 0.0                  |
| teamA_temporal_2020_train_2021_test | M0_training_mean                                          | 1991 | 1.017 | 1.277 | -0.11  | -0.008 | 0.559    | -0.204               |
| teamB_temporal_2020_train_2021_test | M5_wellness_subjective_load_gps_external_load_catboost    | 1255 | 0.547 | 0.848 | 0.102  | 0.515  | 0.829    | 0.084                |
| teamB_temporal_2020_train_2021_test | M3_wellness_subjective_load_catboost                      | 1255 | 0.585 | 0.914 | 0.113  | 0.437  | 0.81     | 0.02                 |
| teamB_temporal_2020_train_2021_test | M5_wellness_subjective_load_gps_external_load_elastic_net | 1255 | 0.591 | 0.842 | 0.014  | 0.522  | 0.837    | 0.01                 |
| teamB_temporal_2020_train_2021_test | M4_wellness_gps_external_load_elastic_net                 | 1255 | 0.592 | 0.849 | 0.012  | 0.514  | 0.84     | 0.008                |
| teamB_temporal_2020_train_2021_test | M1_persistence                                            | 1255 | 0.597 | 1.104 | 0.273  | 0.178  | 0.876    | 0.0                  |
| teamB_temporal_2020_train_2021_test | M3_wellness_subjective_load_elastic_net                   | 1255 | 0.624 | 0.889 | 0.046  | 0.468  | 0.812    | -0.046               |
| teamB_temporal_2020_train_2021_test | M2_wellness_elastic_net                                   | 1255 | 0.634 | 0.931 | 0.034  | 0.416  | 0.803    | -0.062               |
| teamB_temporal_2020_train_2021_test | M0_training_mean                                          | 1255 | 0.952 | 1.219 | 0.044  | -0.001 | 0.57     | -0.595               |
| temporal_2020_train_2021_test       | M5_wellness_subjective_load_gps_external_load_catboost    | 3246 | 0.587 | 0.846 | -0.005 | 0.547  | 0.825    | 0.216                |
| temporal_2020_train_2021_test       | M3_wellness_subjective_load_catboost                      | 3246 | 0.619 | 0.905 | 0.046  | 0.481  | 0.811    | 0.174                |
| temporal_2020_train_2021_test       | M5_wellness_subjective_load_gps_external_load_elastic_net | 3246 | 0.65  | 0.902 | -0.063 | 0.484  | 0.803    | 0.132                |
| temporal_2020_train_2021_test       | M4_wellness_gps_external_load_elastic_net                 | 3246 | 0.652 | 0.91  | -0.038 | 0.475  | 0.798    | 0.129                |
| temporal_2020_train_2021_test       | M3_wellness_subjective_load_elastic_net                   | 3246 | 0.689 | 0.949 | -0.038 | 0.43   | 0.783    | 0.08                 |
| temporal_2020_train_2021_test       | M2_wellness_elastic_net                                   | 3246 | 0.739 | 1.036 | -0.003 | 0.319  | 0.754    | 0.013                |
| temporal_2020_train_2021_test       | M1_persistence                                            | 3246 | 0.749 | 1.252 | 0.289  | 0.006  | 0.849    | 0.0                  |
| temporal_2020_train_2021_test       | M0_training_mean                                          | 3246 | 0.983 | 1.257 | -0.062 | -0.002 | 0.551    | -0.313               |
| temporal_org_train_A2020_test_B2021 | M1_persistence                                            | 1255 | 0.597 | 1.104 | 0.273  | 0.178  | 0.876    | 0.0                  |
| temporal_org_train_A2020_test_B2021 | M4_wellness_gps_external_load_elastic_net                 | 1255 | 0.65  | 0.883 | -0.087 | 0.474  | 0.81     | -0.089               |
| temporal_org_train_A2020_test_B2021 | M2_wellness_elastic_net                                   | 1255 | 0.662 | 0.939 | -0.085 | 0.405  | 0.79     | -0.11                |
| temporal_org_train_A2020_test_B2021 | M5_wellness_subjective_load_gps_external_load_elastic_net | 1255 | 0.712 | 0.935 | -0.26  | 0.411  | 0.764    | -0.192               |
| temporal_org_train_A2020_test_B2021 | M5_wellness_subjective_load_gps_external_load_catboost    | 1255 | 0.715 | 0.939 | -0.321 | 0.405  | 0.744    | -0.198               |
| temporal_org_train_A2020_test_B2021 | M3_wellness_subjective_load_catboost                      | 1255 | 0.717 | 0.96  | -0.253 | 0.379  | 0.739    | -0.202               |
| temporal_org_train_A2020_test_B2021 | M3_wellness_subjective_load_elastic_net                   | 1255 | 0.738 | 0.961 | -0.288 | 0.377  | 0.758    | -0.236               |
| temporal_org_train_A2020_test_B2021 | M0_training_mean                                          | 1255 | 1.03  | 1.262 | -0.333 | -0.075 | 0.54     | -0.726               |
| temporal_org_train_B2020_test_A2021 | M5_wellness_subjective_load_gps_external_load_catboost    | 1991 | 0.699 | 0.949 | 0.098  | 0.443  | 0.781    | 0.173                |
| temporal_org_train_B2020_test_A2021 | M3_wellness_subjective_load_catboost                      | 1991 | 0.709 | 0.98  | 0.127  | 0.406  | 0.771    | 0.161                |
| temporal_org_train_B2020_test_A2021 | M5_wellness_subjective_load_gps_external_load_elastic_net | 1991 | 0.71  | 0.993 | 0.05   | 0.391  | 0.776    | 0.16                 |
| temporal_org_train_B2020_test_A2021 | M3_wellness_subjective_load_elastic_net                   | 1991 | 0.718 | 1.015 | 0.253  | 0.363  | 0.765    | 0.15                 |
| temporal_org_train_B2020_test_A2021 | M4_wellness_gps_external_load_elastic_net                 | 1991 | 0.74  | 1.032 | 0.002  | 0.342  | 0.754    | 0.124                |
| temporal_org_train_B2020_test_A2021 | M2_wellness_elastic_net                                   | 1991 | 0.805 | 1.118 | 0.123  | 0.227  | 0.726    | 0.047                |
| temporal_org_train_B2020_test_A2021 | M1_persistence                                            | 1991 | 0.845 | 1.338 | 0.299  | -0.106 | 0.833    | 0.0                  |
| temporal_org_train_B2020_test_A2021 | M0_training_mean                                          | 1991 | 0.975 | 1.299 | 0.266  | -0.044 | 0.558    | -0.155               |
| unseen_player_grouped_5fold         | M5_wellness_subjective_load_gps_external_load_catboost    | 5472 | 0.634 | 0.911 | 0.051  | 0.517  | 0.807    | 0.192                |
| unseen_player_grouped_5fold         | M5_wellness_subjective_load_gps_external_load_elastic_net | 5472 | 0.667 | 0.935 | -0.003 | 0.491  | 0.8      | 0.15                 |
| unseen_player_grouped_5fold         | M4_wellness_gps_external_load_elastic_net                 | 5472 | 0.679 | 0.951 | -0.001 | 0.473  | 0.791    | 0.136                |
| unseen_player_grouped_5fold         | M3_wellness_subjective_load_catboost                      | 5472 | 0.68  | 0.974 | 0.053  | 0.448  | 0.783    | 0.134                |
| unseen_player_grouped_5fold         | M3_wellness_subjective_load_elastic_net                   | 5472 | 0.718 | 0.989 | 0.004  | 0.431  | 0.776    | 0.086                |
| unseen_player_grouped_5fold         | M2_wellness_elastic_net                                   | 5472 | 0.779 | 1.084 | 0.003  | 0.316  | 0.729    | 0.008                |
| unseen_player_grouped_5fold         | M1_persistence                                            | 5472 | 0.785 | 1.316 | 0.297  | -0.009 | 0.836    | 0.0                  |
| unseen_player_grouped_5fold         | M0_training_mean                                          | 5472 | 1.03  | 1.321 | -0.0   | -0.016 | 0.537    | -0.312               |

## Results With Player-Cluster 95% CI

| split                               | model                                                     | n    | mae   | rmse  | bias   | r2     | within_1 | mae_ci_low | mae_ci_high | skill_vs_persistence |
| ----------------------------------- | --------------------------------------------------------- | ---- | ----- | ----- | ------ | ------ | -------- | ---------- | ----------- | -------------------- |
| cross_team_train_A_test_B           | M5_wellness_subjective_load_gps_external_load_catboost    | 2047 | 0.587 | 0.85  | -0.056 | 0.552  | 0.823    | 0.47       | 0.714       | 0.006                |
| cross_team_train_A_test_B           | M1_persistence                                            | 2047 | 0.591 | 1.139 | 0.273  | 0.196  | 0.875    | 0.421      | 0.794       | 0.0                  |
| cross_team_train_A_test_B           | M4_wellness_gps_external_load_elastic_net                 | 2047 | 0.623 | 0.882 | 0.006  | 0.518  | 0.822    | 0.529      | 0.74        | -0.055               |
| cross_team_train_A_test_B           | M3_wellness_subjective_load_catboost                      | 2047 | 0.646 | 0.912 | -0.121 | 0.484  | 0.791    | 0.533      | 0.783       | -0.093               |
| cross_team_train_A_test_B           | M5_wellness_subjective_load_gps_external_load_elastic_net | 2047 | 0.65  | 0.887 | -0.111 | 0.513  | 0.809    | 0.57       | 0.762       | -0.1                 |
| cross_team_train_A_test_B           | M2_wellness_elastic_net                                   | 2047 | 0.69  | 0.982 | -0.102 | 0.402  | 0.774    | 0.565      | 0.844       | -0.167               |
| cross_team_train_A_test_B           | M3_wellness_subjective_load_elastic_net                   | 2047 | 0.711 | 0.947 | -0.217 | 0.444  | 0.778    | 0.617      | 0.837       | -0.204               |
| cross_team_train_A_test_B           | M0_training_mean                                          | 2047 | 1.063 | 1.302 | -0.286 | -0.051 | 0.51     | 0.885      | 1.269       | -0.8                 |
| cross_team_train_B_test_A           | M5_wellness_subjective_load_gps_external_load_catboost    | 3425 | 0.713 | 1.011 | 0.088  | 0.416  | 0.758    | 0.632      | 0.81        | 0.209                |
| cross_team_train_B_test_A           | M3_wellness_subjective_load_catboost                      | 3425 | 0.744 | 1.045 | 0.082  | 0.376  | 0.751    | 0.667      | 0.839       | 0.176                |
| cross_team_train_B_test_A           | M5_wellness_subjective_load_gps_external_load_elastic_net | 3425 | 0.747 | 1.027 | 0.069  | 0.397  | 0.758    | 0.672      | 0.836       | 0.172                |
| cross_team_train_B_test_A           | M3_wellness_subjective_load_elastic_net                   | 3425 | 0.749 | 1.044 | 0.142  | 0.376  | 0.75     | 0.674      | 0.851       | 0.169                |
| cross_team_train_B_test_A           | M4_wellness_gps_external_load_elastic_net                 | 3425 | 0.76  | 1.04  | 0.031  | 0.381  | 0.745    | 0.683      | 0.856       | 0.158                |
| cross_team_train_B_test_A           | M2_wellness_elastic_net                                   | 3425 | 0.844 | 1.147 | 0.059  | 0.247  | 0.697    | 0.749      | 0.959       | 0.064                |
| cross_team_train_B_test_A           | M1_persistence                                            | 3425 | 0.902 | 1.411 | 0.311  | -0.139 | 0.813    | 0.788      | 1.038       | 0.0                  |
| cross_team_train_B_test_A           | M0_training_mean                                          | 3425 | 1.018 | 1.353 | 0.286  | -0.047 | 0.528    | 0.883      | 1.185       | -0.129               |
| random_observation_5fold            | M5_wellness_subjective_load_gps_external_load_catboost    | 5472 | 0.584 | 0.872 | 0.037  | 0.557  | 0.827    | 0.512      | 0.654       | 0.257                |
| random_observation_5fold            | M3_wellness_subjective_load_catboost                      | 5472 | 0.631 | 0.94  | 0.066  | 0.486  | 0.8      | 0.561      | 0.708       | 0.197                |
| random_observation_5fold            | M5_wellness_subjective_load_gps_external_load_elastic_net | 5472 | 0.656 | 0.925 | -0.0   | 0.501  | 0.808    | 0.596      | 0.729       | 0.165                |
| random_observation_5fold            | M4_wellness_gps_external_load_elastic_net                 | 5472 | 0.669 | 0.943 | -0.0   | 0.482  | 0.795    | 0.602      | 0.746       | 0.148                |
| random_observation_5fold            | M3_wellness_subjective_load_elastic_net                   | 5472 | 0.706 | 0.979 | 0.0    | 0.442  | 0.78     | 0.644      | 0.778       | 0.101                |
| random_observation_5fold            | M2_wellness_elastic_net                                   | 5472 | 0.772 | 1.078 | -0.0   | 0.324  | 0.734    | 0.689      | 0.864       | 0.017                |
| random_observation_5fold            | M1_persistence                                            | 5472 | 0.785 | 1.316 | 0.297  | -0.009 | 0.836    | 0.677      | 0.899       | 0.0                  |
| random_observation_5fold            | M0_training_mean                                          | 5472 | 1.023 | 1.311 | 0.0    | -0.0   | 0.537    | 0.92       | 1.144       | -0.303               |
| teamA_temporal_2020_train_2021_test | M5_wellness_subjective_load_gps_external_load_catboost    | 1991 | 0.646 | 0.894 | -0.057 | 0.506  | 0.808    | 0.577      | 0.724       | 0.236                |
| teamA_temporal_2020_train_2021_test | M3_wellness_subjective_load_catboost                      | 1991 | 0.656 | 0.917 | -0.016 | 0.48   | 0.797    | 0.584      | 0.743       | 0.223                |
| teamA_temporal_2020_train_2021_test | M5_wellness_subjective_load_gps_external_load_elastic_net | 1991 | 0.677 | 0.937 | -0.076 | 0.457  | 0.781    | 0.606      | 0.769       | 0.199                |
| teamA_temporal_2020_train_2021_test | M4_wellness_gps_external_load_elastic_net                 | 1991 | 0.679 | 0.945 | -0.011 | 0.447  | 0.79     | 0.61       | 0.77        | 0.197                |
| teamA_temporal_2020_train_2021_test | M3_wellness_subjective_load_elastic_net                   | 1991 | 0.718 | 0.977 | -0.084 | 0.409  | 0.763    | 0.646      | 0.805       | 0.15                 |
| teamA_temporal_2020_train_2021_test | M2_wellness_elastic_net                                   | 1991 | 0.81  | 1.1   | -0.027 | 0.252  | 0.711    | 0.702      | 0.92        | 0.041                |
| teamA_temporal_2020_train_2021_test | M1_persistence                                            | 1991 | 0.845 | 1.338 | 0.299  | -0.106 | 0.833    | 0.717      | 0.982       | 0.0                  |
| teamA_temporal_2020_train_2021_test | M0_training_mean                                          | 1991 | 1.017 | 1.277 | -0.11  | -0.008 | 0.559    | 0.872      | 1.175       | -0.204               |
| teamB_temporal_2020_train_2021_test | M5_wellness_subjective_load_gps_external_load_catboost    | 1255 | 0.547 | 0.848 | 0.102  | 0.515  | 0.829    | 0.441      | 0.67        | 0.084                |
| teamB_temporal_2020_train_2021_test | M3_wellness_subjective_load_catboost                      | 1255 | 0.585 | 0.914 | 0.113  | 0.437  | 0.81     | 0.457      | 0.723       | 0.02                 |
| teamB_temporal_2020_train_2021_test | M5_wellness_subjective_load_gps_external_load_elastic_net | 1255 | 0.591 | 0.842 | 0.014  | 0.522  | 0.837    | 0.512      | 0.68        | 0.01                 |
| teamB_temporal_2020_train_2021_test | M4_wellness_gps_external_load_elastic_net                 | 1255 | 0.592 | 0.849 | 0.012  | 0.514  | 0.84     | 0.506      | 0.691       | 0.008                |
| teamB_temporal_2020_train_2021_test | M1_persistence                                            | 1255 | 0.597 | 1.104 | 0.273  | 0.178  | 0.876    | 0.446      | 0.769       | 0.0                  |
| teamB_temporal_2020_train_2021_test | M3_wellness_subjective_load_elastic_net                   | 1255 | 0.624 | 0.889 | 0.046  | 0.468  | 0.812    | 0.541      | 0.724       | -0.046               |
| teamB_temporal_2020_train_2021_test | M2_wellness_elastic_net                                   | 1255 | 0.634 | 0.931 | 0.034  | 0.416  | 0.803    | 0.522      | 0.76        | -0.062               |
| teamB_temporal_2020_train_2021_test | M0_training_mean                                          | 1255 | 0.952 | 1.219 | 0.044  | -0.001 | 0.57     | 0.788      | 1.108       | -0.595               |
| temporal_2020_train_2021_test       | M5_wellness_subjective_load_gps_external_load_catboost    | 3246 | 0.587 | 0.846 | -0.005 | 0.547  | 0.825    | 0.53       | 0.65        | 0.216                |
| temporal_2020_train_2021_test       | M3_wellness_subjective_load_catboost                      | 3246 | 0.619 | 0.905 | 0.046  | 0.481  | 0.811    | 0.555      | 0.691       | 0.174                |
| temporal_2020_train_2021_test       | M5_wellness_subjective_load_gps_external_load_elastic_net | 3246 | 0.65  | 0.902 | -0.063 | 0.484  | 0.803    | 0.596      | 0.71        | 0.132                |
| temporal_2020_train_2021_test       | M4_wellness_gps_external_load_elastic_net                 | 3246 | 0.652 | 0.91  | -0.038 | 0.475  | 0.798    | 0.601      | 0.712       | 0.129                |
| temporal_2020_train_2021_test       | M3_wellness_subjective_load_elastic_net                   | 3246 | 0.689 | 0.949 | -0.038 | 0.43   | 0.783    | 0.631      | 0.753       | 0.08                 |
| temporal_2020_train_2021_test       | M2_wellness_elastic_net                                   | 3246 | 0.739 | 1.036 | -0.003 | 0.319  | 0.754    | 0.653      | 0.826       | 0.013                |
| temporal_2020_train_2021_test       | M1_persistence                                            | 3246 | 0.749 | 1.252 | 0.289  | 0.006  | 0.849    | 0.643      | 0.864       | 0.0                  |
| temporal_2020_train_2021_test       | M0_training_mean                                          | 3246 | 0.983 | 1.257 | -0.062 | -0.002 | 0.551    | 0.867      | 1.109       | -0.313               |
| temporal_org_train_A2020_test_B2021 | M1_persistence                                            | 1255 | 0.597 | 1.104 | 0.273  | 0.178  | 0.876    | 0.443      | 0.764       | 0.0                  |
| temporal_org_train_A2020_test_B2021 | M4_wellness_gps_external_load_elastic_net                 | 1255 | 0.65  | 0.883 | -0.087 | 0.474  | 0.81     | 0.572      | 0.735       | -0.089               |
| temporal_org_train_A2020_test_B2021 | M2_wellness_elastic_net                                   | 1255 | 0.662 | 0.939 | -0.085 | 0.405  | 0.79     | 0.558      | 0.78        | -0.11                |
| temporal_org_train_A2020_test_B2021 | M5_wellness_subjective_load_gps_external_load_elastic_net | 1255 | 0.712 | 0.935 | -0.26  | 0.411  | 0.764    | 0.637      | 0.797       | -0.192               |
| temporal_org_train_A2020_test_B2021 | M5_wellness_subjective_load_gps_external_load_catboost    | 1255 | 0.715 | 0.939 | -0.321 | 0.405  | 0.744    | 0.604      | 0.838       | -0.198               |
| temporal_org_train_A2020_test_B2021 | M3_wellness_subjective_load_catboost                      | 1255 | 0.717 | 0.96  | -0.253 | 0.379  | 0.739    | 0.608      | 0.833       | -0.202               |
| temporal_org_train_A2020_test_B2021 | M3_wellness_subjective_load_elastic_net                   | 1255 | 0.738 | 0.961 | -0.288 | 0.377  | 0.758    | 0.663      | 0.823       | -0.236               |
| temporal_org_train_A2020_test_B2021 | M0_training_mean                                          | 1255 | 1.03  | 1.262 | -0.333 | -0.075 | 0.54     | 0.838      | 1.23        | -0.726               |
| temporal_org_train_B2020_test_A2021 | M5_wellness_subjective_load_gps_external_load_catboost    | 1991 | 0.699 | 0.949 | 0.098  | 0.443  | 0.781    | 0.638      | 0.764       | 0.173                |
| temporal_org_train_B2020_test_A2021 | M3_wellness_subjective_load_catboost                      | 1991 | 0.709 | 0.98  | 0.127  | 0.406  | 0.771    | 0.634      | 0.789       | 0.161                |
| temporal_org_train_B2020_test_A2021 | M5_wellness_subjective_load_gps_external_load_elastic_net | 1991 | 0.71  | 0.993 | 0.05   | 0.391  | 0.776    | 0.633      | 0.795       | 0.16                 |
| temporal_org_train_B2020_test_A2021 | M3_wellness_subjective_load_elastic_net                   | 1991 | 0.718 | 1.015 | 0.253  | 0.363  | 0.765    | 0.645      | 0.8         | 0.15                 |
| temporal_org_train_B2020_test_A2021 | M4_wellness_gps_external_load_elastic_net                 | 1991 | 0.74  | 1.032 | 0.002  | 0.342  | 0.754    | 0.662      | 0.83        | 0.124                |
| temporal_org_train_B2020_test_A2021 | M2_wellness_elastic_net                                   | 1991 | 0.805 | 1.118 | 0.123  | 0.227  | 0.726    | 0.708      | 0.914       | 0.047                |
| temporal_org_train_B2020_test_A2021 | M1_persistence                                            | 1991 | 0.845 | 1.338 | 0.299  | -0.106 | 0.833    | 0.72       | 0.986       | 0.0                  |
| temporal_org_train_B2020_test_A2021 | M0_training_mean                                          | 1991 | 0.975 | 1.299 | 0.266  | -0.044 | 0.558    | 0.833      | 1.16        | -0.155               |
| unseen_player_grouped_5fold         | M5_wellness_subjective_load_gps_external_load_catboost    | 5472 | 0.634 | 0.911 | 0.051  | 0.517  | 0.807    | 0.57       | 0.704       | 0.192                |
| unseen_player_grouped_5fold         | M5_wellness_subjective_load_gps_external_load_elastic_net | 5472 | 0.667 | 0.935 | -0.003 | 0.491  | 0.8      | 0.607      | 0.739       | 0.15                 |
| unseen_player_grouped_5fold         | M4_wellness_gps_external_load_elastic_net                 | 5472 | 0.679 | 0.951 | -0.001 | 0.473  | 0.791    | 0.614      | 0.756       | 0.136                |
| unseen_player_grouped_5fold         | M3_wellness_subjective_load_catboost                      | 5472 | 0.68  | 0.974 | 0.053  | 0.448  | 0.783    | 0.612      | 0.754       | 0.134                |
| unseen_player_grouped_5fold         | M3_wellness_subjective_load_elastic_net                   | 5472 | 0.718 | 0.989 | 0.004  | 0.431  | 0.776    | 0.66       | 0.792       | 0.086                |
| unseen_player_grouped_5fold         | M2_wellness_elastic_net                                   | 5472 | 0.779 | 1.084 | 0.003  | 0.316  | 0.729    | 0.697      | 0.871       | 0.008                |
| unseen_player_grouped_5fold         | M1_persistence                                            | 5472 | 0.785 | 1.316 | 0.297  | -0.009 | 0.836    | 0.669      | 0.906       | 0.0                  |
| unseen_player_grouped_5fold         | M0_training_mean                                          | 5472 | 1.03  | 1.321 | -0.0   | -0.016 | 0.537    | 0.924      | 1.153       | -0.312               |

## Calibration Summary

Calibration is summarized by regressing observed readiness on predicted
readiness within each validation split and model.

| split                               | model                                                     | n    | calibration_intercept | calibration_slope | mean_observed | mean_predicted |
| ----------------------------------- | --------------------------------------------------------- | ---- | --------------------- | ----------------- | ------------- | -------------- |
| cross_team_train_A_test_B           | M0_training_mean                                          | 2047 | 3.529                 | 0.521             | 7.058         | 6.772          |
| cross_team_train_A_test_B           | M1_persistence                                            | 2047 | 2.229                 | 0.659             | 7.058         | 7.331          |
| cross_team_train_A_test_B           | M2_wellness_elastic_net                                   | 2047 | -1.178                | 1.184             | 7.058         | 6.956          |
| cross_team_train_A_test_B           | M3_wellness_subjective_load_catboost                      | 2047 | -0.692                | 1.117             | 7.058         | 6.937          |
| cross_team_train_A_test_B           | M3_wellness_subjective_load_elastic_net                   | 2047 | -0.55                 | 1.112             | 7.058         | 6.841          |
| cross_team_train_A_test_B           | M4_wellness_gps_external_load_elastic_net                 | 2047 | -0.278                | 1.039             | 7.058         | 7.063          |
| cross_team_train_A_test_B           | M5_wellness_subjective_load_gps_external_load_catboost    | 2047 | -0.896                | 1.136             | 7.058         | 7.002          |
| cross_team_train_A_test_B           | M5_wellness_subjective_load_gps_external_load_elastic_net | 2047 | -0.607                | 1.103             | 7.058         | 6.946          |
| cross_team_train_B_test_A           | M0_training_mean                                          | 3425 | 3.386                 | 0.48              | 6.772         | 7.058          |
| cross_team_train_B_test_A           | M1_persistence                                            | 3425 | 3.581                 | 0.451             | 6.772         | 7.083          |
| cross_team_train_B_test_A           | M2_wellness_elastic_net                                   | 3425 | 0.543                 | 0.912             | 6.772         | 6.831          |
| cross_team_train_B_test_A           | M3_wellness_subjective_load_catboost                      | 3425 | -0.748                | 1.097             | 6.772         | 6.854          |
| cross_team_train_B_test_A           | M3_wellness_subjective_load_elastic_net                   | 3425 | -0.557                | 1.06              | 6.772         | 6.914          |
| cross_team_train_B_test_A           | M4_wellness_gps_external_load_elastic_net                 | 3425 | -0.517                | 1.071             | 6.772         | 6.803          |
| cross_team_train_B_test_A           | M5_wellness_subjective_load_gps_external_load_catboost    | 3425 | -0.744                | 1.096             | 6.772         | 6.86           |
| cross_team_train_B_test_A           | M5_wellness_subjective_load_gps_external_load_elastic_net | 3425 | -0.94                 | 1.127             | 6.772         | 6.841          |
| random_observation_5fold            | M0_training_mean                                          | 5472 | 34.389                | -3.999            | 6.879         | 6.879          |
| random_observation_5fold            | M1_persistence                                            | 5472 | 3.103                 | 0.526             | 6.879         | 7.176          |
| random_observation_5fold            | M2_wellness_elastic_net                                   | 5472 | -0.07                 | 1.01              | 6.879         | 6.879          |
| random_observation_5fold            | M3_wellness_subjective_load_catboost                      | 5472 | 0.071                 | 0.98              | 6.879         | 6.944          |
| random_observation_5fold            | M3_wellness_subjective_load_elastic_net                   | 5472 | -0.055                | 1.008             | 6.879         | 6.879          |
| random_observation_5fold            | M4_wellness_gps_external_load_elastic_net                 | 5472 | -0.141                | 1.021             | 6.879         | 6.878          |
| random_observation_5fold            | M5_wellness_subjective_load_gps_external_load_catboost    | 5472 | -0.097                | 1.009             | 6.879         | 6.916          |
| random_observation_5fold            | M5_wellness_subjective_load_gps_external_load_elastic_net | 5472 | -0.129                | 1.019             | 6.879         | 6.878          |
| teamA_temporal_2020_train_2021_test | M0_training_mean                                          | 1991 | 3.409                 | 0.508             | 6.818         | 6.708          |
| teamA_temporal_2020_train_2021_test | M1_persistence                                            | 1991 | 3.482                 | 0.469             | 6.818         | 7.118          |
| teamA_temporal_2020_train_2021_test | M2_wellness_elastic_net                                   | 1991 | 0.63                  | 0.911             | 6.818         | 6.791          |
| teamA_temporal_2020_train_2021_test | M3_wellness_subjective_load_catboost                      | 1991 | 0.184                 | 0.975             | 6.818         | 6.802          |
| teamA_temporal_2020_train_2021_test | M3_wellness_subjective_load_elastic_net                   | 1991 | 0.729                 | 0.904             | 6.818         | 6.734          |
| teamA_temporal_2020_train_2021_test | M4_wellness_gps_external_load_elastic_net                 | 1991 | 0.138                 | 0.981             | 6.818         | 6.807          |
| teamA_temporal_2020_train_2021_test | M5_wellness_subjective_load_gps_external_load_catboost    | 1991 | 0.461                 | 0.94              | 6.818         | 6.761          |
| teamA_temporal_2020_train_2021_test | M5_wellness_subjective_load_gps_external_load_elastic_net | 1991 | 0.702                 | 0.907             | 6.818         | 6.742          |
| teamB_temporal_2020_train_2021_test | M0_training_mean                                          | 1255 |                       |                   | 7.041         | 7.085          |
| teamB_temporal_2020_train_2021_test | M1_persistence                                            | 1255 | 2.306                 | 0.647             | 7.041         | 7.314          |
| teamB_temporal_2020_train_2021_test | M2_wellness_elastic_net                                   | 1255 | 0.112                 | 0.979             | 7.041         | 7.074          |
| teamB_temporal_2020_train_2021_test | M3_wellness_subjective_load_catboost                      | 1255 | 0.301                 | 0.942             | 7.041         | 7.154          |
| teamB_temporal_2020_train_2021_test | M3_wellness_subjective_load_elastic_net                   | 1255 | 0.112                 | 0.978             | 7.041         | 7.087          |
| teamB_temporal_2020_train_2021_test | M4_wellness_gps_external_load_elastic_net                 | 1255 | 0.368                 | 0.946             | 7.041         | 7.053          |
| teamB_temporal_2020_train_2021_test | M5_wellness_subjective_load_gps_external_load_catboost    | 1255 | 0.306                 | 0.943             | 7.041         | 7.143          |
| teamB_temporal_2020_train_2021_test | M5_wellness_subjective_load_gps_external_load_elastic_net | 1255 | 0.278                 | 0.959             | 7.041         | 7.055          |
| temporal_2020_train_2021_test       | M0_training_mean                                          | 3246 |                       |                   | 6.904         | 6.842          |
| temporal_2020_train_2021_test       | M1_persistence                                            | 3246 | 3.043                 | 0.537             | 6.904         | 7.193          |
| temporal_2020_train_2021_test       | M2_wellness_elastic_net                                   | 3246 | 0.371                 | 0.947             | 6.904         | 6.901          |
| temporal_2020_train_2021_test       | M3_wellness_subjective_load_catboost                      | 3246 | 0.344                 | 0.944             | 6.904         | 6.951          |
| temporal_2020_train_2021_test       | M3_wellness_subjective_load_elastic_net                   | 3246 | 0.706                 | 0.903             | 6.904         | 6.866          |
| temporal_2020_train_2021_test       | M4_wellness_gps_external_load_elastic_net                 | 3246 | 0.357                 | 0.954             | 6.904         | 6.866          |
| temporal_2020_train_2021_test       | M5_wellness_subjective_load_gps_external_load_catboost    | 3246 | 0.377                 | 0.946             | 6.904         | 6.899          |
| temporal_2020_train_2021_test       | M5_wellness_subjective_load_gps_external_load_elastic_net | 3246 | 0.669                 | 0.911             | 6.904         | 6.841          |
| temporal_org_train_A2020_test_B2021 | M0_training_mean                                          | 1255 | 3.52                  | 0.525             | 7.041         | 6.708          |
| temporal_org_train_A2020_test_B2021 | M1_persistence                                            | 1255 | 2.306                 | 0.647             | 7.041         | 7.314          |
| temporal_org_train_A2020_test_B2021 | M2_wellness_elastic_net                                   | 1255 | -0.369                | 1.065             | 7.041         | 6.956          |
| temporal_org_train_A2020_test_B2021 | M3_wellness_subjective_load_catboost                      | 1255 | 0.061                 | 1.028             | 7.041         | 6.787          |
| temporal_org_train_A2020_test_B2021 | M3_wellness_subjective_load_elastic_net                   | 1255 | 0.957                 | 0.901             | 7.041         | 6.753          |
| temporal_org_train_A2020_test_B2021 | M4_wellness_gps_external_load_elastic_net                 | 1255 | 0.291                 | 0.971             | 7.041         | 6.954          |
| temporal_org_train_A2020_test_B2021 | M5_wellness_subjective_load_gps_external_load_catboost    | 1255 | -0.063                | 1.057             | 7.041         | 6.72           |
| temporal_org_train_A2020_test_B2021 | M5_wellness_subjective_load_gps_external_load_elastic_net | 1255 | 0.973                 | 0.895             | 7.041         | 6.78           |
| temporal_org_train_B2020_test_A2021 | M0_training_mean                                          | 1991 |                       |                   | 6.818         | 7.085          |
| temporal_org_train_B2020_test_A2021 | M1_persistence                                            | 1991 | 3.482                 | 0.469             | 6.818         | 7.118          |
| temporal_org_train_B2020_test_A2021 | M2_wellness_elastic_net                                   | 1991 | 0.903                 | 0.852             | 6.818         | 6.941          |
| temporal_org_train_B2020_test_A2021 | M3_wellness_subjective_load_catboost                      | 1991 | -0.803                | 1.097             | 6.818         | 6.945          |
| temporal_org_train_B2020_test_A2021 | M3_wellness_subjective_load_elastic_net                   | 1991 | 0.361                 | 0.913             | 6.818         | 7.071          |
| temporal_org_train_B2020_test_A2021 | M4_wellness_gps_external_load_elastic_net                 | 1991 | 0.64                  | 0.906             | 6.818         | 6.82           |
| temporal_org_train_B2020_test_A2021 | M5_wellness_subjective_load_gps_external_load_catboost    | 1991 | 0.053                 | 0.978             | 6.818         | 6.916          |
| temporal_org_train_B2020_test_A2021 | M5_wellness_subjective_load_gps_external_load_elastic_net | 1991 | 0.367                 | 0.939             | 6.818         | 6.868          |
| unseen_player_grouped_5fold         | M0_training_mean                                          | 5472 | 34.459                | -4.009            | 6.879         | 6.879          |
| unseen_player_grouped_5fold         | M1_persistence                                            | 5472 | 3.103                 | 0.526             | 6.879         | 7.176          |
| unseen_player_grouped_5fold         | M2_wellness_elastic_net                                   | 5472 | -0.219                | 1.031             | 6.879         | 6.882          |
| unseen_player_grouped_5fold         | M3_wellness_subjective_load_catboost                      | 5472 | -0.216                | 1.024             | 6.879         | 6.932          |
| unseen_player_grouped_5fold         | M3_wellness_subjective_load_elastic_net                   | 5472 | -0.311                | 1.045             | 6.879         | 6.883          |
| unseen_player_grouped_5fold         | M4_wellness_gps_external_load_elastic_net                 | 5472 | -0.294                | 1.043             | 6.879         | 6.878          |
| unseen_player_grouped_5fold         | M5_wellness_subjective_load_gps_external_load_catboost    | 5472 | -0.385                | 1.048             | 6.879         | 6.93           |
| unseen_player_grouped_5fold         | M5_wellness_subjective_load_gps_external_load_elastic_net | 5472 | -0.168                | 1.025             | 6.879         | 6.876          |

## Incremental GPS Comparison

Negative delta means the HR-free GPS external-load block improved MAE over the
wellness plus subjective-load model on the same split.

| split                               | mae_subjective_load | mae_subjective_load_gps | mae_delta_gps_minus_subjective_load |
| ----------------------------------- | ------------------- | ----------------------- | ----------------------------------- |
| cross_team_train_A_test_B           | 0.711               | 0.65                    | -0.061                              |
| cross_team_train_B_test_A           | 0.749               | 0.747                   | -0.002                              |
| random_observation_5fold            | 0.706               | 0.656                   | -0.05                               |
| teamA_temporal_2020_train_2021_test | 0.718               | 0.677                   | -0.041                              |
| teamB_temporal_2020_train_2021_test | 0.624               | 0.591                   | -0.033                              |
| temporal_2020_train_2021_test       | 0.689               | 0.65                    | -0.038                              |
| temporal_org_train_A2020_test_B2021 | 0.738               | 0.712                   | -0.026                              |
| temporal_org_train_B2020_test_A2021 | 0.718               | 0.71                    | -0.008                              |
| unseen_player_grouped_5fold         | 0.718               | 0.667                   | -0.05                               |

## Paired Delta MAE With Player-Cluster 95% CI

| split                               | comparison                         | baseline_model                          | comparator_model                                          | delta_mae | delta_mae_ci_low | delta_mae_ci_high |
| ----------------------------------- | ---------------------------------- | --------------------------------------- | --------------------------------------------------------- | --------- | ---------------- | ----------------- |
| random_observation_5fold            | M5_minus_M3_primary_gps_increment  | M3_wellness_subjective_load_elastic_net | M5_wellness_subjective_load_gps_external_load_elastic_net | -0.05     | -0.065           | -0.035            |
| unseen_player_grouped_5fold         | M5_minus_M3_primary_gps_increment  | M3_wellness_subjective_load_elastic_net | M5_wellness_subjective_load_gps_external_load_elastic_net | -0.05     | -0.066           | -0.033            |
| temporal_2020_train_2021_test       | M5_minus_M3_primary_gps_increment  | M3_wellness_subjective_load_elastic_net | M5_wellness_subjective_load_gps_external_load_elastic_net | -0.038    | -0.056           | -0.02             |
| teamA_temporal_2020_train_2021_test | M5_minus_M3_primary_gps_increment  | M3_wellness_subjective_load_elastic_net | M5_wellness_subjective_load_gps_external_load_elastic_net | -0.041    | -0.06            | -0.023            |
| teamB_temporal_2020_train_2021_test | M5_minus_M3_primary_gps_increment  | M3_wellness_subjective_load_elastic_net | M5_wellness_subjective_load_gps_external_load_elastic_net | -0.033    | -0.066           | -0.003            |
| cross_team_train_A_test_B           | M5_minus_M3_primary_gps_increment  | M3_wellness_subjective_load_elastic_net | M5_wellness_subjective_load_gps_external_load_elastic_net | -0.061    | -0.097           | -0.03             |
| cross_team_train_B_test_A           | M5_minus_M3_primary_gps_increment  | M3_wellness_subjective_load_elastic_net | M5_wellness_subjective_load_gps_external_load_elastic_net | -0.002    | -0.025           | 0.028             |
| temporal_org_train_A2020_test_B2021 | M5_minus_M3_primary_gps_increment  | M3_wellness_subjective_load_elastic_net | M5_wellness_subjective_load_gps_external_load_elastic_net | -0.026    | -0.063           | 0.011             |
| temporal_org_train_B2020_test_A2021 | M5_minus_M3_primary_gps_increment  | M3_wellness_subjective_load_elastic_net | M5_wellness_subjective_load_gps_external_load_elastic_net | -0.008    | -0.037           | 0.021             |
| random_observation_5fold            | CatBoost_M5_minus_M3_gps_increment | M3_wellness_subjective_load_catboost    | M5_wellness_subjective_load_gps_external_load_catboost    | -0.047    | -0.064           | -0.033            |
| unseen_player_grouped_5fold         | CatBoost_M5_minus_M3_gps_increment | M3_wellness_subjective_load_catboost    | M5_wellness_subjective_load_gps_external_load_catboost    | -0.046    | -0.059           | -0.032            |
| temporal_2020_train_2021_test       | CatBoost_M5_minus_M3_gps_increment | M3_wellness_subjective_load_catboost    | M5_wellness_subjective_load_gps_external_load_catboost    | -0.032    | -0.05            | -0.017            |
| teamA_temporal_2020_train_2021_test | CatBoost_M5_minus_M3_gps_increment | M3_wellness_subjective_load_catboost    | M5_wellness_subjective_load_gps_external_load_catboost    | -0.01     | -0.031           | 0.008             |
| teamB_temporal_2020_train_2021_test | CatBoost_M5_minus_M3_gps_increment | M3_wellness_subjective_load_catboost    | M5_wellness_subjective_load_gps_external_load_catboost    | -0.038    | -0.064           | -0.013            |
| cross_team_train_A_test_B           | CatBoost_M5_minus_M3_gps_increment | M3_wellness_subjective_load_catboost    | M5_wellness_subjective_load_gps_external_load_catboost    | -0.059    | -0.088           | -0.03             |
| cross_team_train_B_test_A           | CatBoost_M5_minus_M3_gps_increment | M3_wellness_subjective_load_catboost    | M5_wellness_subjective_load_gps_external_load_catboost    | -0.03     | -0.053           | -0.009            |
| temporal_org_train_A2020_test_B2021 | CatBoost_M5_minus_M3_gps_increment | M3_wellness_subjective_load_catboost    | M5_wellness_subjective_load_gps_external_load_catboost    | -0.002    | -0.031           | 0.021             |
| temporal_org_train_B2020_test_A2021 | CatBoost_M5_minus_M3_gps_increment | M3_wellness_subjective_load_catboost    | M5_wellness_subjective_load_gps_external_load_catboost    | -0.01     | -0.042           | 0.019             |
| random_observation_5fold            | M5_minus_persistence               | M1_persistence                          | M5_wellness_subjective_load_gps_external_load_elastic_net | -0.129    | -0.2             | -0.058            |
| unseen_player_grouped_5fold         | M5_minus_persistence               | M1_persistence                          | M5_wellness_subjective_load_gps_external_load_elastic_net | -0.118    | -0.192           | -0.049            |
| temporal_2020_train_2021_test       | M5_minus_persistence               | M1_persistence                          | M5_wellness_subjective_load_gps_external_load_elastic_net | -0.099    | -0.181           | -0.02             |
| teamA_temporal_2020_train_2021_test | M5_minus_persistence               | M1_persistence                          | M5_wellness_subjective_load_gps_external_load_elastic_net | -0.168    | -0.273           | -0.069            |
| teamB_temporal_2020_train_2021_test | M5_minus_persistence               | M1_persistence                          | M5_wellness_subjective_load_gps_external_load_elastic_net | -0.006    | -0.101           | 0.079             |
| cross_team_train_A_test_B           | M5_minus_persistence               | M1_persistence                          | M5_wellness_subjective_load_gps_external_load_elastic_net | 0.059     | -0.059           | 0.163             |
| cross_team_train_B_test_A           | M5_minus_persistence               | M1_persistence                          | M5_wellness_subjective_load_gps_external_load_elastic_net | -0.155    | -0.227           | -0.085            |
| temporal_org_train_A2020_test_B2021 | M5_minus_persistence               | M1_persistence                          | M5_wellness_subjective_load_gps_external_load_elastic_net | 0.115     | -0.009           | 0.247             |
| temporal_org_train_B2020_test_A2021 | M5_minus_persistence               | M1_persistence                          | M5_wellness_subjective_load_gps_external_load_elastic_net | -0.135    | -0.241           | -0.04             |

## CatBoost Block Permutation Importance

Positive values mean MAE became worse when the held-out block was permuted.

| split                         | model                                                  | block                   | baseline_mae | permuted_mae_delta | permuted_mae_delta_sd |
| ----------------------------- | ------------------------------------------------------ | ----------------------- | ------------ | ------------------ | --------------------- |
| cross_team_train_A_test_B     | M5_wellness_subjective_load_gps_external_load_catboost | wellness_history        | 0.587        | 0.531              | 0.014                 |
| cross_team_train_A_test_B     | M5_wellness_subjective_load_gps_external_load_catboost | gps_external_load       | 0.587        | 0.087              | 0.005                 |
| cross_team_train_A_test_B     | M5_wellness_subjective_load_gps_external_load_catboost | subjective_load_history | 0.587        | 0.041              | 0.006                 |
| cross_team_train_B_test_A     | M5_wellness_subjective_load_gps_external_load_catboost | wellness_history        | 0.713        | 0.411              | 0.008                 |
| cross_team_train_B_test_A     | M5_wellness_subjective_load_gps_external_load_catboost | gps_external_load       | 0.713        | 0.128              | 0.005                 |
| cross_team_train_B_test_A     | M5_wellness_subjective_load_gps_external_load_catboost | subjective_load_history | 0.713        | 0.037              | 0.002                 |
| temporal_2020_train_2021_test | M5_wellness_subjective_load_gps_external_load_catboost | wellness_history        | 0.587        | 0.511              | 0.011                 |
| temporal_2020_train_2021_test | M5_wellness_subjective_load_gps_external_load_catboost | gps_external_load       | 0.587        | 0.17               | 0.007                 |
| temporal_2020_train_2021_test | M5_wellness_subjective_load_gps_external_load_catboost | subjective_load_history | 0.587        | 0.039              | 0.003                 |

## Feature Blocks

Wellness: readiness, fatigue, soreness, mood, stress, sleep_quality, sleep_duration, readiness_past_3d_mean, readiness_past_7d_mean, fatigue_past_3d_mean, fatigue_past_7d_mean, soreness_past_3d_mean, soreness_past_7d_mean, sleep_quality_past_3d_mean, sleep_quality_past_7d_mean, sleep_duration_past_3d_mean, sleep_duration_past_7d_mean

Subjective load/history: session_count, session_srpe_sum, session_duration_sum, session_rpe_mean, session_rpe_max, session_srpe_sum_past_3d_sum, session_srpe_sum_past_7d_sum, session_srpe_sum_past_28d_sum

GPS external load: objective_duration_min, objective_distance_m, objective_distance_m_per_min, objective_hsr_distance_m, objective_hsr_m_per_min, objective_sprint_distance_m, objective_sprint_m_per_min, objective_speed_max, objective_accel_distance_m, objective_decel_distance_m

HR sensitivity candidates: objective_heart_rate_mean, objective_heart_rate_max, objective_heart_rate_coverage

GPS QC variables excluded from primary model: objective_gps_tick_count, objective_valid_speed_tick_count, objective_raw_row_count, objective_hacc_mean, objective_hdop_mean, objective_signal_quality_mean, objective_num_satellites_mean, objective_num_satellites_min, objective_num_satellites_max, objective_implausible_speed_tick_rate, objective_implausible_heart_rate_tick_rate
