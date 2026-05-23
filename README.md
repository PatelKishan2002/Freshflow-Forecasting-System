# FreshFlow — Perishable Waste & Markdown Intelligence

**A demand forecasting and decision-support system for grocery perishables, addressing the gap between sales prediction and operational waste reduction.**

Grocery retailers in Canada throw away an estimated $X billion of perishable food annually before it reaches a customer. Most demand forecasting work stops at "how many units will sell"; this project extends forecasting into a waste-aware decision layer that recommends when and how to mark down inventory to minimize spoilage while preserving margin.

## What this project does

- Forecasts demand for perishable categories (produce, dairy, meat, bakery) at SKU level using LightGBM and hierarchical reconciliation
- Simulates inventory flow and predicts category-level waste in dollars
- Recommends markdown timing and depth based on cost-aware optimization
- Serves predictions via a FastAPI backend with a Streamlit dashboard for non-technical users
- Deployed on Google Cloud Run

## Why this project exists

I work in receiving at a Canadian food distribution center. Every shift I see perishables move through the dock — produce, dairy, meat, deli. I see what arrives that the store will not sell in time. FreshFlow is my attempt to test whether Applied Data Science can model that waste, predict it, and recommend interventions — bridging operational ground-truth and analytical method.

## Data sources

| Source | Role in project | License |
|---|---|---|
| dunnhumby Complete Journey | Real grocery transactions (modeling layer) | Open for research |
| Statistics Canada Table 20-10-0056 | Canadian retail trade calibration | Open Government License |
| Statistics Canada Table 18-10-0004 | Canadian food CPI for price adjustment | Open Government License |
| Open Food Facts | Product attributes and category enrichment | Open Database License |
| ECCC "Taking Stock" + VCMI Avoidable Crisis 2024 | Canadian food waste benchmarks for impact extrapolation | Public reports |

### Obtaining raw data

Raw files are not in git (size and license). Place downloads under `data/raw/`:

| Source | How to obtain |
|--------|----------------|
| **dunnhumby** | [Kaggle: Complete Journey](https://www.kaggle.com/datasets/frtgn/complete-journey) — set `KAGGLE_USERNAME` and `KAGGLE_KEY` in `.env` |
| **Statistics Canada** | [StatCan tables](https://www150.statcan.gc.ca/) → `data/raw/statcan/` |
| **Open Food Facts** | [world.openfoodfacts.org](https://world.openfoodfacts.org/) → `data/raw/openfoodfacts/` |
| **Food waste reports** | Government PDFs → `data/raw/canada_food_waste_reports/` |

Run `notebooks/01_exploration/00_data_audit.ipynb` to validate schemas after download.

## Honest limitations

- No Canadian retailer publishes SKU-level transactions publicly, so the modeling layer uses US grocery data (dunnhumby) with Canadian context as a calibration overlay
- Waste is simulated from shelf-life assumptions, not measured directly — real waste data is proprietary to retailers
- This is a portfolio demonstration of methodology, not a production system; companies like Shelf Engine and Afresh have built commercial solutions in this space

## Setup

```bash
git clone https://github.com/PatelKishan2002/Freshflow-Forecasting-System.git
cd Freshflow-Forecasting-System
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
cp .env.example .env        # Add Kaggle credentials and DATA_DIR
make install
```

Paths and hyperparameters live in `configs/config.yaml`. Override `DATA_DIR` in `.env` if needed.

## Project structure

```
freshflow/
├── data/
│   ├── raw/                    # Immutable original downloads
│   │   ├── dunnhumby/
│   │   ├── statcan/
│   │   ├── openfoodfacts/
│   │   └── canada_food_waste_reports/
│   ├── interim/                # Cleaned per-source, not yet merged
│   ├── processed/              # Final modeling-ready tables
│   └── external/               # Any third-party reference data
├── notebooks/
│   ├── 01_exploration/         # EDA per data source
│   ├── 02_modeling/            # Model development
│   └── 03_reporting/           # Final analysis for writeup
├── src/
│   └── freshflow/
│       ├── __init__.py
│       ├── data/
│       │   ├── __init__.py
│       │   ├── load_dunnhumby.py
│       │   ├── load_statcan.py
│       │   └── load_openfoodfacts.py
│       ├── features/
│       │   ├── __init__.py
│       │   └── build_features.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── forecast.py
│       │   ├── waste.py
│       │   └── markdown.py
│       ├── evaluation/
│       │   ├── __init__.py
│       │   └── metrics.py
│       ├── visualization/
│       │   ├── __init__.py
│       │   └── plots.py
│       └── utils/
│           ├── __init__.py
│           └── io.py
├── tests/
│   └── __init__.py
├── configs/
│   └── config.yaml             # Paths, hyperparameters, constants
├── reports/
│   └── figures/                # Generated plots
├── app/                        # FastAPI + Streamlit deployment code (later)
├── docs/
├── .gitignore
├── .env.example
├── pyproject.toml
├── README.md
├── LICENSE
└── Makefile
```

## How to reproduce

1. **Download data** — Place raw files under `data/raw/` per source (see table above). Run exploration notebooks in `notebooks/01_exploration/` to validate schemas.
2. **Process** — (Future) pipelines in `src/freshflow/data/` write `data/interim/` and `data/processed/`.
3. **Train** — (Future) `notebooks/02_modeling/` or CLI using `src/freshflow/models/`.
4. **Evaluate** — (Future) metrics via `src/freshflow/evaluation/`; figures saved to `reports/figures/`.

```bash
make data    # Reminder to validate raw data via notebooks
make test    # Run tests once implemented
```

## Results

_TBD — forecast accuracy, waste reduction estimates, and markdown ROI will be documented here._

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE).
