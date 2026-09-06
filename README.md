# Do Athlete Monitoring Across Teams?
### Subjective Wellness, External Load, and Next-Day Readiness Across Teams

---

## Repository Structure

```
athlete-monitoring-across-teams/
├── data/
│   └── processed_release/
│       ├── subjective_player_day.csv       # Daily subjective monitoring data
│       └── objective_session_features.csv   # Session-level objective features
├── scripts/
│   ├── 04_build_linkage_and_core_cohort.py
│   ├── 05_run_subjective_baselines.py
│   ├── 06_merge_objective_player_day_features.py
│   ├── 07_run_multimodal_models.py
│   ├── 08_make_descriptive_tables.py
│   └── 09_run_sensitivity_and_personalization.py
├── src/soccermon/
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Reproducing the Results

The statistical analyses can be reproduced from the processed input files
included in this repository without access to the original raw exports.

1. Install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Set the processed-data directory:
   ```bash
   export SOCCERMON_PROCESSED_DIR=data/processed_release
   ```
3. Run the analysis scripts in order:
   ```bash
   python scripts/04_build_linkage_and_core_cohort.py
   python scripts/05_run_subjective_baselines.py
   python scripts/06_merge_objective_player_day_features.py
   python scripts/07_run_multimodal_models.py
   python scripts/08_make_descriptive_tables.py
   python scripts/09_run_sensitivity_and_personalization.py
   ```

The scripts cover cohort construction, subjective baselines, objective-feature
linkage, multimodal models, descriptive tables, and sensitivity and
personalization analyses. Intermediate and final CSV outputs are regenerated
in `data/processed_release/`; Markdown summaries are written to `reports/`.

---

## Notes on the Data

`subjective_player_day.csv` contains the daily subjective monitoring records
used to construct the core cohort and calculate the longitudinal wellness and
subjective-load features. `objective_session_features.csv` contains the
session-level GPS, heart-rate, and signal-quality summaries used for the
objective-feature linkage and multimodal analyses.

The raw SoccerMon exports and the earlier extraction steps are not included.
The included processed inputs are the analysis-ready files required by the
reproduction pipeline.

---

## Citation

> *Will be updated upon publication.*

---

## License

Code released under the [MIT License](LICENSE).
