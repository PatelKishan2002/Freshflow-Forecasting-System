# FreshFlow — Step Explanations (Plain English)

This file explains what happened in each step of the FreshFlow project, in simple language. Use this as your reference when you forget what a notebook did or need to remind yourself for an interview.

Each step has the same structure:
- **What we did** — the work in plain words
- **Why it matters** — the reason a senior DS would care
- **What we produced** — files saved or decisions locked in
- **Interview talking points** — sentences you can use when asked about this work

---

## Step 2A — dunnhumby Data Cleaning

**Notebook:** `notebooks/01_exploration/01_dunnhumby_deep_dive.ipynb`

**Date completed:** [fill in]

### The starting point

Raw dunnhumby Complete Journey dataset:
- 2.59 million transactions
- 711 days of data
- 2,500 households across 582 stores
- 92,353 products

The data was anonymized in two ways: real calendar dates were replaced with day numbers (1 to 711), and the retailer's identity was hidden. Our job was to clean, filter, and prepare it for forecasting.

### What we did

**1. Counted what we had.** Basic shape and scale checks before touching anything else.

**2. Built a perishable product filter.** The hard part. dunnhumby's DEPARTMENT labels were unreliable — true perishable dairy products (milk, cheese, yogurt) were misclassified into the GROCERY department. We built a two-level filter using both DEPARTMENT and COMMODITY_DESC to recover ~5,000 dairy SKUs hiding in GROCERY.

**3. Removed false positives.** Microwave popcorn was labeled PRODUCE but is shelf-stable. Frozen seafood was labeled SEAFOOD but has months of shelf life. We added a second filter pass to exclude these.

**4. Mapped DAY integers to real dates.** Used the community convention: Day 1 = Monday, January 6, 2014. This gave us a real calendar range of 2014-01-06 to 2015-12-17.

**5. Validated the date mapping.** Checked day-of-week patterns. Expected weekend peaks, found Thursday/Friday peaks instead. Investigated and confirmed this is a real retailer pattern (weekly ad cycles, biweekly Friday paydays in the US), not a data bug.

**6. Filtered transactions to perishables only.** Kept the 32% of transactions that involved perishable products. Dropped the rest.

**7. Quality checks.** Removed ~6K rows with zero quantity (data errors) or zero sales (free/coupon items). Confirmed no nulls anywhere.

**8. Discovered a ramp-up artifact.** Plotted daily transactions and saw all categories ramping from zero during the first 3 months. This was dunnhumby gradually enrolling households, not real demand growth. Dropped the first 90 days.

**9. Found extreme sparsity at SKU-store level.** 47% of SKU-store pairs have only 1 transaction over the entire period. This rules out SKU-store level forecasting — we will forecast at category-store level instead.

### Why it matters

Each finding above is a senior-DS judgment call that most portfolio projects skip. The cleaning isn't just busywork — it's the foundation that determines whether the forecasting model learns real patterns or garbage.

If we had skipped any of these steps:
- Bad department labels would have hidden dairy from the model
- Shelf-stable popcorn would have polluted our perishable signal
- The model would have learned "demand grows fast" from the ramp-up
- We would have tried to forecast at SKU-store level and failed silently

### What we produced

```
data/interim/
├── products_classified.parquet     # 92,353 products with IS_PERISHABLE flag
├── perishable_products.parquet     # 14,148 perishable SKUs only
└── transactions_perishable.parquet # 784,904 cleaned modeling transactions
```

### Final modeling dataset numbers

| Metric | Value |
|---|---|
| Transactions | 784,904 |
| Perishable SKUs | 13,546 |
| Stores | 458 |
| Households | 2,487 |
| Date range | 2014-04-06 to 2015-12-17 |
| Days | 621 |

**Category distribution:**
- DAIRY: 36.6%
- PRODUCE: 30.1%
- MEAT: 22.3%
- DELI: 8.7%
- BAKERY: 1.7%
- SEAFOOD: 0.7%

**Forecasting hierarchy decision:** Due to sparsity, we will forecast at category-store level (6 categories × 458 stores = 2,748 series), not SKU-store level.

### Interview talking points

Three sentences you can use in interviews. Pick whichever fits the question.

1. **On data quality work:**
   > "I discovered the department labels in dunnhumby were unreliable for perishable classification. I built a two-level filter using both department and commodity description, which recovered over 5,000 dairy products misclassified into the GROCERY department."

2. **On exploratory analysis:**
   > "When I plotted daily transactions over time, I noticed the first 90 days showed a ramp-up pattern across all categories. This wasn't real demand growth — it was dunnhumby gradually enrolling households. I excluded this period from training to prevent the model from learning spurious trends."

3. **On honest investigation:**
   > "I found Thursday-Friday demand peaks instead of the typical weekend peaks I expected. Rather than assume my date mapping was wrong, I tested it with holiday-adjusted comparisons. The pattern persisted, which told me it's a real characteristic of this retailer — likely driven by weekly ad cycles and biweekly Friday paydays. I documented the finding rather than forcing textbook assumptions onto the data."

### Honest limitations to mention

When asked about weaknesses or limitations of this step:

- **dunnhumby is US data, not Canadian.** No Canadian retailer publishes SKU-level data publicly. The methodology transfers; the specific patterns might not.
- **Day-to-date mapping uses a community convention, not an official source.** dunnhumby anonymized this on purpose. The convention is widely used in research papers, but it isn't 100% confirmed.
- **47% of SKU-store pairs have only 1 transaction.** This is real data sparsity, and it constrains us to category-level forecasting.

---

## Step 2B — Open Food Facts Canadian Filtering

**Notebook:** `notebooks/01_exploration/02_openfoodfacts_canada.ipynb`

### What we did

Streamed the 1.27 GB Open Food Facts global product database in chunks (200K rows at a time) and filtered to Canadian products. Then kept only products with a name, category, and barcode. Ended up with ~29K usable Canadian products.

### Why it matters

Provides a real Canadian product reference layer for the README and storytelling. Demonstrates we used a Canadian open data source even though no Canadian retailer publishes SKU-level transactions.

### Honest limitation

Open Food Facts is community-maintained, so coverage is uneven. Many Canadian products in OFF have sparse category fields before the quality filter; after filtering, every row has `categories_tags`, but keyword-based perishable counts overlap (one product can match multiple categories). This is **not** a feature source for the forecasting model — it's a Canadian context layer for descriptive purposes only. dunnhumby products (US) and OFF Canadian products are different SKUs and cannot be joined directly.

### What we produced

`data/interim/openfoodfacts_canada.parquet` — 28,752 Canadian products with name, brand, category, barcode.

**README context (keyword matches on `categories_en`, overlapping):** DAIRY 3,640; PRODUCE 2,412; MEAT 2,062; BAKERY 1,673; DELI 810; SEAFOOD 568 — sum of matches 11,165 (not unique SKUs).

### Interview talking point

> "I filtered Open Food Facts to 29K Canadian products as a context layer for the project. I want to be clear about its role though — it's not a direct feature input, since dunnhumby products and OFF Canadian products are different SKUs. It's there for descriptive grounding and to show the project uses Canadian open data alongside the US modeling data."

That last sentence is what senior interviewers want to hear. Honest about what the data does and doesn't do.

---

## Step 2C — Statistics Canada Seasonality and CPI

**Notebook:** `notebooks/01_exploration/03_statcan_seasonality.ipynb`

### What we did

Loaded two Canadian government datasets:
1. **StatCan Table 20-10-0056** (Retail trade by industry) — filtered to Food & beverage retailers (NAICS 445), aggregated 4 provinces (Quebec, Ontario, Alberta, BC) into a Canada total, computed monthly seasonality index from 2017–2025.
2. **StatCan Table 18-10-0004** (Consumer Price Index) — filtered to 4 perishable categories (Meat, Dairy, Bakery, Fresh produce).

### Key findings

**Canadian food retail seasonality (2017–2025 average):**

| Month | Index | Interpretation |
|---|---|---|
| Jan | 0.90 | -10% below average |
| **Feb** | **0.86** | **lowest month** |
| Mar | 0.98 | slightly below |
| Apr | 0.96 | below |
| May | 1.04 | +4% above |
| Jun | 1.04 | +4% above |
| Jul | 1.05 | summer peak |
| Aug | 1.04 | +4% above |
| Sep | 0.99 | average |
| Oct | 1.01 | average |
| Nov | 0.99 | slightly below |
| **Dec** | **1.14** | **+14% — Christmas peak** |

Standard deviations are 1.4–3.9%, meaning the pattern is highly consistent across 9 years.

**Canadian food CPI (April 2026, base 2002 = 100):**
- Meat: 235.4 (up 135%)
- Bakery: 216.5 (up 117%)
- Produce: 198.9 (up 99%)
- Dairy: 178.3 (up 78%)

### Why it matters

Two purposes:

1. **Validation benchmark.** When the forecasting model runs on dunnhumby data, the seasonal pattern it produces should resemble this Canadian seasonality — adjusting for the US-vs-Canada holiday calendar shift (US Thanksgiving in November, Canadian Thanksgiving in October).
2. **Honest Canadian framing.** Real numbers from a real government source. Defensible in any interview question about Canadian retail patterns.

### What we produced

```
data/interim/
├── canada_seasonality.parquet
├── canada_food_cpi.parquet
└── canada_retail_food.parquet
```

### Interview talking points

1. **On validation:**
   > "I pulled monthly Canadian food retail seasonality from Statistics Canada Table 20-10-0056 to use as a calibration benchmark. Canadian grocery shows a 14% December peak and a 14% February trough, very consistent across 2017–2025. After training on US data, the model's seasonal output should reproduce this shape, with adjustments for US-Canada holiday calendar differences."

2. **On the data layering approach:**
   > "I treat the project as a layered architecture: dunnhumby provides the modeling layer because no Canadian retailer publishes SKU-level data, and Statistics Canada provides the calibration layer to validate that the methodology's assumptions align with Canadian patterns. Each source does one job, and they're not merged into one table."

### Honest limitations

- The retail trade data only includes 4 provinces (Quebec, Ontario, Alberta, BC). Statistics Canada doesn't publish a Canada-wide total in this table at the level we need. We computed it as a sum of these provinces, which covers ~85% of Canadian retail.
- CPI data starts at 2021, not earlier. Fine for current inflation context, but doesn't go back to dunnhumby's 2014–2015 period.
- StatCan retail trade is reported in nominal CAD. We don't deflate it because we're using it for seasonality (within-year patterns), not multi-year growth analysis.

---

## Step 2D — Canadian Food Waste Numbers Extracted

**File:** `data/raw/canada_food_waste_reports/key_numbers.txt`

### What we did

Read the VCMI/Second Harvest 2024 Avoidable Crisis Update (technical report + roadmap) and the ECCC Taking Stock report. Extracted headline numbers, methodology revisions between 2019 and 2024, and category-level breakdowns.

### Key numbers locked in

**Headline:**
- 8.83 million tonnes of avoidable food waste annually in Canada (2024)
- $58 billion estimated value (CPI-adjusted)
- 13% of avoidable waste occurs at retail = 1.14 million tonnes

**By category (all avoidable waste):**
- Produce: 38.4% | Dairy: 14.6% | Meat: 4.3% | Seafood: 0.8%
- Field crops including bakery: 38.5%

**By category (BBD-driven avoidable waste only — the subset FreshFlow targets):**
- Bakery: 45.5% | Dairy: 32.5% | Produce: 12.2%

### Why it matters

These numbers anchor every Canadian-impact claim in the README. Without them, FreshFlow would be a generic forecasting project. With them, it has a defensible business framing tied to real Canadian government and industry research.

### Strategic implication

The BBD-driven waste numbers identified Bakery, Dairy, and Produce as the three categories where markdown timing intervention is most impactful. This shapes the project framing going forward.

### Interview talking point

> "I anchored the project's impact framing in the 2024 Second Harvest / VCMI Avoidable Crisis report — the most-cited Canadian food waste reference. Within retail, 1.14 million tonnes of avoidable waste happen annually. The interesting finding was that best-before-date driven waste — the slice that markdown timing can actually address — concentrates in three categories: bakery at 45.5%, dairy at 32.5%, and produce at 12.2%. That shaped how I scoped the project."

---

## Step 2E — Mixed-grain forecasting grids

**Notebook:** `notebooks/02_modeling/01_feature_engineering.ipynb`

### Architectural decision: mixed-grain forecasting

After EDA on activity rates, the project uses two parallel data grids:

- **Store-level grid:** DAIRY, PRODUCE, MEAT, DELI — filtered to stores with ≥75% category activity (417 series)
- **Chain-level grid:** BAKERY, SEAFOOD — aggregated across all stores (2 series)

**Reason:** dunnhumby's sample has dense data for some categories at store level but sparse data for others. Forcing uniform grain would either lose signal (over-aggregating dense categories) or train on noise (under-aggregating sparse categories). Real production retail systems use the same mixed-grain pattern.

### What we did

1. Built a complete store × category × week grid for dense categories and filled zero-sales weeks.
2. Audited activity rate per (store, category) series — many series were inactive most weeks (~46% zero-sales before filtering).
3. Kept only store-level series at ≥75% activity; moved SEAFOOD to chain-week (no store sold it consistently).
4. Aggregated BAKERY and SEAFOOD to chain-week (~90 weeks each).

### What we produced

```
data/interim/
├── dense_store_category_weekly.parquet   # store-level: DAIRY, PRODUCE, MEAT, DELI
└── chain_weekly.parquet                  # chain-level: BAKERY, SEAFOOD
```

### Interview talking point

> "I didn't force one forecasting grain for every category. Activity-rate EDA showed dairy and produce are dense at store level, but bakery and seafood aren't — so I run store×category models for the dense four and chain-week models for the sparse two. That's how real retail forecasting stacks are built."

---

## Step 3 — Feature Engineering

**Notebooks:** `notebooks/02_modeling/01_feature_engineering.ipynb` and `02_promotion_features.ipynb`

### What we did

Built five families of features on top of the cleaned weekly aggregated data:

1. **Lag features** (5): units_lag_1, _2, _4, _8, _52 — past weekly sales with shift(1) to prevent leakage
2. **Rolling features** (4): 4-week and 12-week rolling mean and std of past sales
3. **Calendar features** (5): MONTH, WEEK_OF_YEAR, QUARTER, IS_HOLIDAY_WEEK, WEEKS_TO_YEAR_END
4. **Category encoding** (4): one-hot encoded perishable categories
5. **Promotion features** (3): pct_skus_on_display, pct_skus_on_mailer, pct_skus_front_page — built from dunnhumby causal_data (8M filtered rows)

All features built separately for the dense (store-category-week) and chain (category-week) grids.

### Key findings

**On data architecture (activity filter):**

The initial cartesian grid (every store × every category × every week) had 67.4% zero-sales weeks — mostly because dunnhumby includes stores that don't actually sell some categories. Applied an activity filter (≥75% non-zero weeks per series) which dropped the zero rate to 2.4% and produced 413 clean store-category series for DAIRY, PRODUCE, MEAT, DELI.

SEAFOOD was moved to chain-level (joining BAKERY) because no individual store sells seafood consistently enough for store-level forecasting.

**On promotion features:**

Counter to my expectation, the strongest promotion signal was front-page mailer placement (correlation 0.275), not display intensity (0.142). General mailer presence had weak signal (0.093) because 96% of weeks have some mailer activity — the variance is in WHERE promotions appear, not WHETHER they appear.

### Why it matters

The data architecture decisions (mixed-grain forecasting, activity filtering) reflect real production-retail practice. The promotion feature discovery shows the value of correlation analysis before model training — knowing front-page is the strongest signal helps validate the trained model later.

### What we produced

```
data/interim/
├── features_dense.parquet     # 15,694 rows × 30 columns
└── features_chain.parquet     # 76 rows × 30 columns
```

### Interview talking points

1. **On feature engineering discipline:**
   > "I built lag and rolling features with explicit shift(1) operations so the model only sees data it would actually have at prediction time. This prevents the most common time-series leakage mistake."

2. **On the promotion finding:**
   > "Through correlation analysis I found that 96% of weeks have some promotional activity at this retailer, so 'is there a promotion' had weak signal. The discriminating feature was front-page mailer placement — the most expensive ad spot — which had 0.275 correlation with weekly sales. That insight came from EDA before any model training and was later validated by the model's feature importance ranking."

3. **On data-driven architecture:**
   > "I didn't force a single forecasting grain. Dairy, produce, meat, and deli are dense enough for store-level forecasting at 413 active series. Bakery and seafood are too sparse — they're modeled at chain level. This mixed-grain approach is what real production retail systems use, and the activity rate distribution made the decision data-driven, not arbitrary."
