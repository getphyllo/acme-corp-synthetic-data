# Acme Corp — Synthetic Data

A canonical, internally-consistent fictional CPG dataset for prototype building, design discussions, and demo storytelling. Built around **Acme Corp**, a $812M cereal-and-adjacencies company headquartered in Battle Creek, Michigan, currently fighting a **Q1 2026 share decline in the Louisiana DMA** (the data tells the story).

> Single source of truth. Use this version (`v0.4.0`) as the anchor for any prototype that needs CPG-shape data. If you need to evolve the schema, tag a new version — don't edit in place.

## What's in here

```
acme-corp-synthetic-data/
├── data/                              ← parquet (commit-tracked, ready to query)
│   ├── epos.parquet                       30,000 rows · transaction-level POS · v0.1
│   ├── perfect_store.parquet              50,000 rows · store-day-SKU panel w/ OSA, facings · v0.1
│   ├── syndicated_weekly.parquet          92,250 rows · DMA × cat × channel × week (NielsenIQ-shape) · v0.1
│   ├── brand_health.parquet               15,000 rows · survey panel w/ awareness, NPS, attrs (Kantar-shape) · v0.1
│   ├── households.parquet                  5,000 rows · HH master w/ demographics, loyalty (Numerator-shape) · v0.1
│   ├── household_transactions.parquet     30,000 rows · weekly HH purchases w/ switching flag · v0.1
│   ├── plan_vs_actual.parquet             ~99,000 rows · monthly plan-vs-actual w/ AOP / FCST_REV · v0.2
│   ├── sku_authorization.parquet          ~60,000 rows · store × SKU auth + distribution snapshot · v0.2
│   ├── shipments.parquet                  ~48,000 rows · weekly Acme plant → Retailer DC fill rate · v0.2
│   ├── promo_events.parquet                  720 rows · all-retailer promo log w/ mechanic + ROI · v0.2
│   ├── competitor_launches.parquet            30 rows · hand-curated launch events · v0.3
│   ├── social_mentions.parquet            18,000 rows · Brandwatch-shape social listening · v0.3
│   ├── creator_posts.parquet               3,200 rows · Tribe Dynamics-shape creator posts · v0.3
│   ├── search_trends.parquet               2,400 rows · Spate / Helium 10-shape keyword volume · v0.3
│   ├── product_reviews.parquet            24,000 rows · Bazaarvoice / PowerReviews-shape reviews · v0.3
│   └── data_freshness_log.parquet            450 rows · weekly feed status metadata · v0.4
├── samples/                           ← 100-row CSV slices for previewing in any tool
├── seeds/                             ← small, hand-curated reference CSVs
│   ├── skus.csv · retailers.csv · geographies.csv (v0.1 masters)
│   ├── retailer_divisions.csv (v0.2 — 46 banner divisions)
│   ├── competitor_launches.csv · research_agencies.csv (v0.2)
│   ├── creators.csv (v0.3 — 50 creator master)
│   ├── regional_brands.csv · innovation_pipeline.csv · category_market_size.csv ·
│   │   sku_elasticity_estimates.csv · macro_trends.csv · social_topics.csv (v0.4)
│   ├── monthly_pos_fy25_q12026.csv · trade_spend_fy25.csv · marketing_spend.csv
│   └── promo_events_louisiana.csv (canonical LA event log)
├── acme.duckdb                        ← single-file SQL DB with all 16 tables + 17 seed tables loaded
├── generator/                         ← deterministic generator (seed=42)
├── docs/
│   ├── louisiana-decline.md           ← the canonical demo scenario
│   ├── narrative-anchors.md           ← shared constants across tables (v0.2+)
│   ├── personas/                      ← Maya · Marcus · Diane · Priya
│   └── schema/
│       ├── column-mapping.md          ← v0.1 Kellogg-fork mapping
│       └── new-tables.md              ← v0.2 / v0.3 / v0.4 schema reference
├── notebooks/                         ← starter exploration
├── CHANGELOG.md
└── LICENSE
```

## Quick start (60 seconds)

### Option A — DuckDB (fastest)

```bash
brew install duckdb            # or: pip install duckdb && python -m duckdb
duckdb acme.duckdb
```

```sql
-- The headline question Acme leadership is asking right now:
SELECT SUBSTR(Week,1,4) AS yr,
       ROUND(AVG(Crunchwell_Value_Share)*100, 2) AS la_share_pct
FROM syndicated_weekly
WHERE DMA = 'LA-DMA' AND Category = 'RTE Cereal'
GROUP BY 1 ORDER BY 1;
```

### Option B — Python / pandas

```python
import pandas as pd
epos = pd.read_parquet("data/epos.parquet")
perfect_store = pd.read_parquet("data/perfect_store.parquet")
# ... 30 seconds and you're querying.
```

### Option C — eyeball it in Excel/Numbers

Open anything in `samples/`. Each file is 100 rows of the corresponding parquet, plain CSV, opens anywhere.

### Option D — DuckDB-WASM (browser)

For prototypes built with v0/Lovable/Bolt or any frontend tool, the parquet files can be queried directly in-browser via [DuckDB-WASM](https://shell.duckdb.org/) — no server. Drop a parquet URL in.

## The narrative encoded in the data

The point of this dataset is that it tells a coherent CPG story without any joins to external context. Acme's **Crunchwell** flagship (#4 US RTE cereal at 5.8% share) is leaking 340 bps of share in **Louisiana** over Q1 2026. The data has these facts baked in — query them and they show up:

| Fact | Where to find it |
|---|---|
| Crunchwell LA share drops from ~6.0% (FY24) → ~3.9% (Q1 '26) | `syndicated_weekly` filter `DMA='LA-DMA' AND Category='RTE Cereal'` |
| Walmart Sept 2025 modular reset (Crunchwell Mega 8 → 6 facings) | `perfect_store` where `SKU IN ('CR002','CR004','CR005') AND Banner='Walmart' AND Date >= '2025-09-15'` — also `Banner_Region='Walmart South'` lowest avg facings |
| Hurricane Tonya OSA collapse Nov 2025 (97% → 67%) | `perfect_store` where `DMA='LA-DMA' AND SKU IN ('CR002','CR004','CR005') AND Date BETWEEN '2025-11-08' AND '2025-12-15'` |
| Hurricane Tonya supply collapse — Houston DC fill rate ~58% | `shipments` where `Retailer_DC LIKE '%Houston%' OR LIKE '%Thibodaux%' OR LIKE '%Tyler%' AND Cut_Reason='Storm'` |
| LA Crunchwell -47% vs plan in Q1 2026 | `plan_vs_actual` where `Brand='Crunchwell' AND DMA='LA-DMA' AND Period >= '2026-01'` |
| Larksfield Foods promo intensification at Rouses (21% off, weekly) | `perfect_store` filter `Banner='Rouses' AND Brand='Field & Honey'` + canonical event log `seeds/promo_events_louisiana.csv` |
| Field & Honey Almond launch (LA stealth threat) | `competitor_launches WHERE brand='Field & Honey' AND launch_date='2025-09-08'` |
| Field & Honey viral wave Q4 2025 | `social_mentions WHERE Brand_Mentioned='Field & Honey' AND DMA_Region='LA-DMA' AND Topic_Tags LIKE '%viral%'` |
| LA Crunchwell-loyal HHs switching to Field & Honey | `household_transactions WHERE Switching_Flag='Yes' AND DMA='LA-DMA'` |
| Crunchwell perception softening in LA Q4'25 + Q1'26 | `brand_health WHERE dma='LA-DMA' AND wave IN ('2025Q4','2026Q1')` — `taste`/`quality` ~0.4 lower |
| Crunchwell sentiment dip in LA on social | `social_mentions WHERE Brand_Mentioned='Crunchwell' AND DMA_Region='LA-DMA'` — avg sentiment ~−0.36 |
| Cinnamon Twist (CR006) underperformer story | `sku_authorization WHERE SKU='CR006'` (39% authorized) + `product_reviews WHERE SKU='CR006'` (avg ~3.4) + `competitor_launches WHERE launch_id='LCH00019'` |

Full root-cause walkthrough: [`docs/louisiana-decline.md`](./docs/louisiana-decline.md).

## Who this dataset is for

| You're a… | Use it for… | Start at |
|---|---|---|
| **Engineer** building a Clayface prototype | A real CPG-shape backend without spinning up a warehouse | `acme.duckdb` or `data/*.parquet` |
| **Designer** mocking up a screen | A live, queryable seed for charts and cards in v0/Lovable | `samples/*.csv` or DuckDB-WASM |
| **PM** framing a feature | A canonical demo story (the LA decline) and persona reactions | `docs/louisiana-decline.md` + `docs/personas/` |
| **Data scientist** building MMM or panel | A pre-shaped weekly dataset with the LA outlier baked in | `data/syndicated_weekly.parquet` + `docs/schema/mmm-schema.md` |

## Acme at a glance

- **HQ:** Battle Creek, MI · **Founded:** 1952 · **CEO:** Gregory Whitfield (since 2020)
- **FY25 net revenue:** $812M (+5.1% YoY) · **EBITDA margin:** 14.2% (target 16% by FY28)
- **Brands:** Crunchwell ($312M flagship), HoneyNest ($94M, kids), ProteinPeak ($48M, +24.6%), MorningOats ($98M), TrailGrove ($152M), RootDay ($62M oat milk, acquired 2023)
- **#4 US RTE cereal player** behind General Mills, Kellanova, Larksfield Foods

## The four primary personas

| Persona | Name | Role |
|---|---|---|
| 1 — End user | [Maya Chen](./docs/personas/01-maya-chen-analyst.md) | Senior Insights Analyst, Cereals · 32 |
| 2 — Stakeholder | [Marcus Boudreaux](./docs/personas/02-marcus-boudreaux-sales-director.md) | Director Sales, South Region · 45 |
| 3 — Economic buyer | [Diane Halverson](./docs/personas/03-diane-halverson-vp-sales.md) | VP Sales North America · 52 |
| 4 — Cat manager | [Priya Raman](./docs/personas/04-priya-raman-category-manager.md) | Category Manager, Cereals & Adjacent · 38 |

## Schema overview (one screen)

| Table | Grain | Key columns | Mirrors |
|---|---|---|---|
| `epos` | per-transaction | `Transaction_ID, Date_Time, DMA, Banner_Division, Brand, Manufacturer, Promotion_Flag` | Kellogg ME EPOS shape |
| `perfect_store` | store × day × SKU | `Date, Store_ID, DMA, Banner, Banner_Division, OSA_Pct, Facings` | Kellogg ME Perfect Store |
| `syndicated_weekly` | DMA × category × channel × week | `Crunchwell_Value_Share, Larksfield_Value_Share, Promo_Share, ACV_Distribution_Pct` | NielsenIQ-style |
| `brand_health` | per-respondent (survey) | `wave, dma, ethnicity, aided_aw_*, nps_0to10, taste/quality/health/value/...` | Kantar/Suzy-style |
| `households` | per-household (panel master) | `DMA, Income_Bracket, Ethnicity, Brand_Loyalty_Segment` | Numerator-style |
| `household_transactions` | HH × week × purchase | `Brand, Banner_Division, Switching_Flag, Promotion_Type` | Numerator transaction log |
| `plan_vs_actual` | brand × retailer × DMA × month | `Plan_Revenue_USD, Actual_Revenue_USD, Variance_Pct, Plan_Source` | SAP / Acme ERP |
| `sku_authorization` | store × SKU × month | `Auth_Status, Distribution_Status, Why_Not_Distributed, ACV_Weight_Pct` | SymphonyAI / Walmart Luminate |
| `shipments` | week × SKU × DC | `Ordered_Units, Fill_Rate_Pct, On_Time_Pct, Cut_Reason, Origin_Acme_Plant` | SAP outbound + DC receipts |
| `promo_events` | per-event | `Mechanic, Promo_Depth_Pct, Lift_Pct, Forward_Buy_Pct, ROI` | NielsenIQ promo lift |
| `competitor_launches` | per-launch | `launch_date, claim_headline, acv_at_launch_pct, year1_velocity, intel_source` | Mintel GNPD + NIQ Innovation |
| `social_mentions` | per-mention | `Platform, Brand_Mentioned, Sentiment, Topic_Tags, Reach, Engagement` | Brandwatch |
| `creator_posts` | per-post | `Creator_ID, Brand_Mentioned, Disclosed_Partnership, Attributed_Sales_Lift_72hr_USD` | Tribe Dynamics |
| `search_trends` | keyword × platform × month | `Volume_Index_0to100, MoM_Growth_Pct, Brand_Relevance` | Spate / Helium 10 / Google Trends |
| `product_reviews` | per-review | `Rating_1to5, Topic_Tags, Sentiment, Verified_Purchase, Helpful_Votes` | Bazaarvoice / PowerReviews |
| `data_freshness_log` | feed × week | `Last_Refreshed, Lag_Hours, Status, Cadence, Owner_Team` | internal data ops |

Full column-by-column mapping for v0.1.0: [`docs/schema/column-mapping.md`](./docs/schema/column-mapping.md). New-tables schema (v0.2.0+): [`docs/schema/new-tables.md`](./docs/schema/new-tables.md). Shared narrative anchors: [`docs/narrative-anchors.md`](./docs/narrative-anchors.md).

## Versioning

- **v0.1.0** — initial public seed. See [`CHANGELOG.md`](./CHANGELOG.md).
- Breaking schema changes bump the minor version. Adding a new column/table is a patch.
- The deterministic generator means *the same version always produces the same data*. Don't edit `data/*.parquet` by hand — change the generator and bump.

## Regenerating from scratch

```bash
pip install -r generator/requirements.txt
python generator/generate.py
```

`random.seed(42)` makes runs reproducible. Output overwrites `data/`, `samples/`, and `acme.duckdb` in place. To experiment with a different sample, change the seed at the top of `generator/generate.py`.

## Contributing

- **Adding a column:** edit `generator/generate.py`, regenerate, update `docs/schema/column-mapping.md`, bump patch version, PR.
- **Adding a table:** edit generator + add a section to this README and to `docs/schema/`. Bump minor.
- **Changing the narrative:** propose in an issue first — the LA decline is calibrated across 6 tables and many people's prototypes will pin to it.
- **Don't commit one-off CSVs.** If it's worth keeping, add it to the generator.

## License

MIT. See [`LICENSE`](./LICENSE).

## A note on realism

This is fictional data, but it's calibrated to look like a real CPG company's data shape. Pricing, share %, ACV, OSA, facings, switching rates, panel demographics — all in plausible ranges for the actual cereal category. Use it for design and prototyping; do **not** use it for any real CPG decision-making, benchmarking, or competitive intelligence. Any resemblance to a real company's KPIs is coincidence — the underlying model is intentionally derived from public CPG industry literature, not from any single firm.
