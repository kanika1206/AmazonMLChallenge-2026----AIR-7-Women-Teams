# Amazon ML Challenge: Business Entity Resolution

This portfolio edition presents selected engineering and ML components from Team Agastaya's business entity resolution project. It includes reusable utilities and tests, not the complete production solution or submission outputs.

## Problem

Given noisy business records from three sources, identify which records describe the same business. Source 1 is the reference source. Names and addresses vary in spelling, formatting, language, and completeness. The task includes entities with no matching records and a test country absent from training.

## Approach

The full project used a candidate-generation stage, string-based pair features, gradient-boosted classification, a second learning stage, and precision-oriented decision processing. Production candidate generation, tuned features, model configurations, orchestration, and final decision rules are withheld.

The public code retains TSV loading and ID mapping, basic text normalization, ordinary name/address similarities, generic LightGBM training and prediction wrappers, macro F0.5 evaluation, geographic parsing, and output-format utilities. Model parameters and training rounds must be supplied by the caller. There is no production training or submission command.

## Technologies and engineering

Python, Polars, NumPy, RapidFuzz, Unidecode, LightGBM, and pytest. The project involved controlling candidate growth, limiting memory use, processing text in parallel, handling missing fields, validating record identifiers, and evaluating precision/recall trade-offs.

The public normalization is deliberately simplified. `normalize_name` keeps its tuple return shape, with an empty second field because production legal-form extraction is withheld. `add_normalized_columns` returns basic core-name, address, and number columns; production phonetic and legal columns are absent. `match_features` retains only standard string similarities. The `postprocess` directory contains generic utilities and no production rule runner.

## Results and lineage

| Result | Status |
|---|---|
| Historical FinalV2 public leaderboard macro F0.5: 0.987026 | Reported team competition result; not a result of this public edition |
| Private rebuilt pipeline out-of-fold macro F0.5: 0.9792 | Reported development result; production components are withheld |
| Public utility edition | No model benchmark claimed |
| Ensemble experiment | Proposed; no achieved score claimed |

The original leaderboard model's full run settings were not retained. The private rebuilt pipeline was not identical to the historical submission. No final predictions, candidate lists, weights, or experimental probability dumps are distributed here.

## Run the public checks

Use Python 3.12 or newer with the retained dependency pins.

From this directory:

```bash
python -m venv .venv
```

Activate the environment for your platform, then:

```bash
python -m pip install -r requirements.txt pytest==8.4.2
python -m pytest
```

Tests use small fabricated records and exercise the retained utilities. These instructions do not train the withheld production system. Dependency pins are retained from the original project environment.

All seven utility tests passed on Windows with Python 3.12.4. A separate smoke check verified imports, data loading, normalization, similarities, and output round-tripping. Native LightGBM training raised an access violation in that environment with both the original and unchanged public training wrappers. The wrappers remain unchanged; model training needs verification in the intended execution environment.

## Data and project context

The public challenge data and public training labels are retained in the cleaned local `../../dataset.zip`; its macOS metadata has been removed. The archive's validator is retained with its executable logic unchanged and code comments/docstrings removed. The archive is excluded from ordinary Git tracking because of its size; obtain the public challenge data from its original distribution or a separately hosted copy. `../../PS.pdf` describes the task and evaluation.

## Team attribution

Team Agastaya: Kanika, Kiran Sehrawat, and Mahee Agarwal. This edition preserves the original team attribution. Individual responsibilities are not asserted because the supplied material does not identify them.

See `../../Documentation_template.md` for the portfolio case study. Public code demonstrates selected components; complete production behavior and competition results cannot be regenerated from this edition.
