# Freshflow Forecasting System

Perishable waste forecasting and markdown optimization for grocery retailers.

## Problem statement

Grocery retailers lose billions annually to perishable spoilage and end-of-shelf markdowns. Freshflow combines transaction-level demand signals with category shelf-life assumptions and Canadian market calibration to forecast waste risk and inform markdown timing—reducing shrink while protecting margin on high-turnover departments.

## Data sources

| Source | What it provides | License | How to obtain |
|--------|------------------|---------|---------------|
| **dunnhumby Complete Journey** | Real US grocery transactions (baskets, products, departments) | [dunnhumby terms](https://www.dunnhumby.com/source-files/) | Kaggle: [Complete Journey](https://www.kaggle.com/datasets/frtgn/complete-journey) — set `KAGGLE_USERNAME` and `KAGGLE_KEY` in `.env` |
| **Statistics Canada** | Retail trade volumes, food CPI (Canadian macro calibration) | Open Government Licence – Canada | [StatCan tables](https://www150.statcan.gc.ca/) — download CSVs into `data/raw/statcan/` |
| **Open Food Facts** | Product attributes for Canadian SKUs (categories, labels) | [ODbL 1.0](https://opendatacommons.org/licenses/odbl/) | [world.openfoodfacts.org](https://world.openfoodfacts.org/) — export or API into `data/raw/openfoodfacts/` |
| **Canadian food waste reports** | National/contextual waste benchmarks (reference only) | Government of Canada publications | PDFs in `data/raw/canada_food_waste_reports/` (not used in modeling pipeline) |

### Data architecture (read this)

- **dunnhumby** is the **modeling layer**: real SKU- and basket-level US grocery transactions drive demand, waste, and markdown models.
- **Statistics Canada** provides **Canadian calibration** (macro retail and CPI trends), not SKU-level sales—no Canadian grocer publishes open transaction data at this granularity.
- **Open Food Facts** enriches product metadata where available; coverage for Canadian SKUs is incomplete.
- We are **transparent** about geography: models are trained on US transaction patterns and calibrated with Canadian macro indicators; results are illustrative for Canadian retail strategy, not a substitute for proprietary store data.

## Setup

```bash
git clone <repository-url>
cd freshflow
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

<!-- Placeholder: add key metrics, charts, and business impact after modeling -->

_TBD — forecast accuracy, waste reduction estimates, and markdown ROI will be documented here._

## Limitations and caveats

<!-- Placeholder: document geographic mismatch, shelf-life assumptions, data sparsity -->

_TBD — including US-trained models with Canadian calibration, assumed shelf lives by department, and lack of proprietary inventory/shrink data._

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE).
