# Descriptive Tables

## Cohort Summary

| team  | year | core_rows | players | gps_rows | gps_players | gps_share_pct |
| ----- | ---- | --------- | ------- | -------- | ----------- | ------------- |
| TeamA | 2020 | 3819      | 23      | 1434     | 22          | 37.5          |
| TeamA | 2021 | 5903      | 27      | 1991     | 24          | 33.7          |
| TeamB | 2020 | 2412      | 14      | 792      | 12          | 32.8          |
| TeamB | 2021 | 2497      | 23      | 1255     | 22          | 50.3          |

## Objective Coverage And Training Characteristics

| team  | year | objective_player_days | objective_players | median_distance_m | median_duration_min | median_hr_coverage |
| ----- | ---- | --------------------- | ----------------- | ----------------- | ------------------- | ------------------ |
| TeamA | 2020 | 2325                  | 28                | 4865.723          | 98.973              | 0.0                |
| TeamA | 2021 | 2960                  | 31                | 4710.734          | 97.278              | 0.929              |
| TeamB | 2020 | 1837                  | 20                | 4041.748          | 92.478              | 0.0                |
| TeamB | 2021 | 2872                  | 33                | 4814.308          | 105.346             | 0.482              |

## GPS Selection SMD

| comparison            | variable                      | n_positive | n_reference | mean_positive | mean_reference | smd    | abs_smd |
| --------------------- | ----------------------------- | ---------- | ----------- | ------------- | -------------- | ------ | ------- |
| has_gps_True_vs_other | readiness                     | 5472       | 9159        | 7.176         | 6.579          | 0.429  | 0.429   |
| has_gps_True_vs_other | session_srpe_sum              | 5022       | 5950        | 539.766       | 458.184        | 0.309  | 0.309   |
| has_gps_True_vs_other | session_rpe_mean              | 5022       | 5950        | 5.944         | 5.418          | 0.287  | 0.287   |
| has_gps_True_vs_other | session_duration_sum          | 5022       | 5950        | 88.452        | 80.922         | 0.229  | 0.229   |
| has_gps_True_vs_other | session_srpe_sum_past_28d_sum | 5455       | 9088        | 9752.575      | 9190.89        | 0.167  | 0.167   |
| has_gps_True_vs_other | readiness_past_7d_mean        | 5436       | 9064        | 6.924         | 6.748          | 0.152  | 0.152   |
| has_gps_True_vs_other | fatigue                       | 5470       | 9154        | 3.082         | 2.995          | 0.145  | 0.145   |
| has_gps_True_vs_other | soreness_t_plus_1             | 5469       | 9158        | 2.723         | 2.819          | -0.133 | 0.133   |
| has_gps_True_vs_other | readiness_past_3d_mean        | 5380       | 8971        | 6.911         | 6.752          | 0.128  | 0.128   |
| has_gps_True_vs_other | stress                        | 5472       | 9152        | 3.164         | 3.231          | -0.107 | 0.107   |
| has_gps_True_vs_other | fatigue_t_plus_1              | 5470       | 9151        | 2.987         | 3.045          | -0.096 | 0.096   |
| has_gps_True_vs_other | readiness_t_plus_1            | 5472       | 9159        | 6.879         | 6.745          | 0.094  | 0.094   |
| has_gps_True_vs_other | sleep_quality                 | 5468       | 9152        | 3.232         | 3.283          | -0.073 | 0.073   |
| has_gps_True_vs_other | mood                          | 5471       | 9155        | 3.35          | 3.388          | -0.062 | 0.062   |
| has_gps_True_vs_other | sleep_duration                | 5468       | 9142        | 8.181         | 8.148          | 0.034  | 0.034   |
| has_gps_True_vs_other | soreness                      | 5470       | 9157        | 2.806         | 2.783          | 0.032  | 0.032   |
| has_gps_True_vs_other | session_srpe_sum_past_7d_sum  | 5391       | 8940        | 2517.971      | 2492.478       | 0.027  | 0.027   |
| has_gps_True_vs_other | session_count                 | 5022       | 5950        | 1.145         | 1.151          | -0.017 | 0.017   |

## Team Shift SMD

| comparison          | variable                      | n_positive | n_reference | mean_positive | mean_reference | smd    | abs_smd | sample                 |
| ------------------- | ----------------------------- | ---------- | ----------- | ------------- | -------------- | ------ | ------- | ---------------------- |
| team_TeamA_vs_other | mood                          | 9721       | 4905        | 3.467         | 3.19           | 0.484  | 0.484   | core_subjective_cohort |
| team_TeamA_vs_other | sleep_quality                 | 9714       | 4906        | 3.367         | 3.06           | 0.456  | 0.456   | core_subjective_cohort |
| team_TeamA_vs_other | session_rpe_mean              | 7538       | 3434        | 5.461         | 6.092          | -0.356 | 0.356   | core_subjective_cohort |
| team_TeamA_vs_other | readiness_past_7d_mean        | 9664       | 4836        | 6.684         | 7.073          | -0.329 | 0.329   | core_subjective_cohort |
| team_TeamA_vs_other | readiness_past_3d_mean        | 9571       | 4780        | 6.68          | 7.075          | -0.31  | 0.31    | core_subjective_cohort |
| team_TeamA_vs_other | sleep_duration                | 9705       | 4905        | 8.257         | 7.969          | 0.299  | 0.299   | core_subjective_cohort |
| team_TeamA_vs_other | stress                        | 9719       | 4905        | 3.264         | 3.09           | 0.298  | 0.298   | core_subjective_cohort |
| team_TeamA_vs_other | readiness                     | 9722       | 4909        | 6.672         | 7.059          | -0.269 | 0.269   | core_subjective_cohort |
| team_TeamA_vs_other | readiness_t_plus_1            | 9722       | 4909        | 6.668         | 7.046          | -0.264 | 0.264   | core_subjective_cohort |
| team_TeamA_vs_other | fatigue_t_plus_1              | 9718       | 4903        | 3.062         | 2.946          | 0.196  | 0.196   | core_subjective_cohort |
| team_TeamA_vs_other | session_srpe_sum              | 7538       | 3434        | 479.447       | 530.817        | -0.195 | 0.195   | core_subjective_cohort |
| team_TeamA_vs_other | fatigue                       | 9719       | 4905        | 3.066         | 2.951          | 0.191  | 0.191   | core_subjective_cohort |
| team_TeamA_vs_other | session_srpe_sum_past_28d_sum | 9688       | 4855        | 9579.382      | 9046.766       | 0.154  | 0.154   | core_subjective_cohort |
| team_TeamA_vs_other | soreness_t_plus_1             | 9719       | 4908        | 2.805         | 2.74           | 0.091  | 0.091   | core_subjective_cohort |
| team_TeamA_vs_other | soreness                      | 9720       | 4907        | 2.812         | 2.75           | 0.087  | 0.087   | core_subjective_cohort |
| team_TeamA_vs_other | session_srpe_sum_past_7d_sum  | 9569       | 4762        | 2520.143      | 2465.747       | 0.057  | 0.057   | core_subjective_cohort |
| team_TeamA_vs_other | session_count                 | 7538       | 3434        | 1.153         | 1.139          | 0.037  | 0.037   | core_subjective_cohort |
| team_TeamA_vs_other | session_duration_sum          | 7538       | 3434        | 84.105        | 84.946         | -0.026 | 0.026   | core_subjective_cohort |
| team_TeamA_vs_other | mood                          | 3425       | 2046        | 3.477         | 3.138          | 0.634  | 0.634   | gps_matched_cohort     |
| team_TeamA_vs_other | sleep_quality                 | 3421       | 2047        | 3.351         | 3.031          | 0.503  | 0.503   | gps_matched_cohort     |
