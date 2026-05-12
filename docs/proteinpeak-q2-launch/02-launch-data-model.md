# Launch Data Model — How the Q2 ProteinPeak Launch Is Encoded

This is the engineering map for Scenario 2. Every signal the demo narrative depends on is encoded in one or more parquet/seed files. Use this file when you (1) need to verify the data is consistent, or (2) want to extend the scenario.

---

## Canonical SKUs

| SKU | Name | Status (post-launch) | Launch Date | Year-1 Plan (musd) |
|---|---|---|---|---|
| PP001 | ProteinPeak Vanilla Almond Original 12oz | Active (cannibalized) | 2021 | 30.0 |
| PP002 | ProteinPeak Chocolate Hazelnut 12oz | Active | 2022 | 13.0 |
| PP003 | ProteinPeak Berry Crunch 12oz | Active (historical compare anchor) | 2023 | 6.0 |
| PP004 | ProteinPeak Single-Serve Cups | Active | 2023 | 7.0 |
| **PP005** | **ProteinPeak Cinnamon Crunch 12oz** | **Active-Launch-Q2 (NEW)** | **2026-04-20** | **14.0** |
| **PP006** | **ProteinPeak Cocoa Almond 12oz** | **Active-Launch-Q2 (NEW)** | **2026-04-20** | **10.0** |

**Total ProteinPeak FY26 plan**: ~$80M (vs FY25 actuals $48M, +66.7%).

---

## Where each signal lives

### Trial vs plan (question 1)

**Encoded as a channel-split velocity gap.**

- `epos`: PP005/PP006 transactions on/after 2026-04-20. Target rows sell at the launch endcap; Walmart-pilot rows at lower velocity; Amazon coupon promo flag set.
- `perfect_store`: SKU = PP005/PP006 has dedicated launch-period rows (~1200) with:
  - Banner = Target: velocity ≈ 1.13 × baseline; OSA dip W0-W1; endcap promo flag.
  - Banner = Walmart: velocity ≈ 0.78 × baseline; pilot facings 3.
  - Banner = Amazon: velocity ≈ 1.04 × baseline; coupon depth 8%.
- `plan_vs_actual` (months 2026-04 and 2026-05):
  - ProteinPeak × Target → variance ≈ +8% to +18% (over plan)
  - ProteinPeak × Walmart → variance ≈ -17% to -27% (under plan)
- `category_market_size.csv` seed: Q2-FY2026-MTD Wellness Protein rows show channel-level trial gap (Target +21% growth, Walmart +12%).

### Repeat curve vs Berry Crunch (question 2)

**Encoded as HH repeat-purchase density.**

- `household_transactions`: Week-since-launch repeat purchases of PP005/PP006 by household. Berry Crunch (PP003) has 3 years of repeat history in the same table; the comparison joins on (`Household_ID`, `weeks_since_launch_bucket`). Repeat rate at Week 2 for PP005/PP006 sits ~1.2× Berry Crunch baseline.
- `product_reviews`: PP005/PP006 launch reviews (post-2026-04-20) skew higher rating (~4.6) than Berry Crunch's full-history (~4.4), reinforcing the repeat signal.

### Cannibalization of PP001 (question 3)

**Encoded as a velocity dip on PP001 in launch retailers + a HH switching flag.**

- `perfect_store`: PP001 rows on/after 2026-04-20 at Target/Amazon/WFM/Sprouts/Kroger have velocity multiplied by:
  - 0.89 in W0 (the -11% W1 dip from the scenario)
  - 0.94 in W1–W4 (the ~-6% steady-state)
- `household_transactions`: PP005/PP006 buys are tagged with `Switching_Flag = 'Cannibalization'` when SOV roll is 0.53–0.85.
- Aggregate distribution target: ~53% `New_To_Brand`, ~32% `Cannibalization`, ~15% `Competitor_Switch`.

### Channel split: Target endcap vs Amazon vs mass (question 4)

**Encoded in three places.**

- `perfect_store` `Banner` column with launch-period oversample (~1200 rows).
- `promo_events`: dedicated rows for each PP005/PP006 launch-retailer event (PP-E001 through PP-E014 in `seeds/proteinpeak_q2_launch.csv`, merged into `promo_events.parquet`).
- `marketing_spend.csv` seed: 2026-Q2 ProteinPeak rows for Retail Media (Roundel Target $1.8M + Amazon Ads $1.4M + Walmart Connect $500K + Sprouts $250K) + Connected TV ($2.2M) + Paid Social TikTok ($2.6M) + Influencer Macro ($1.2M).
  - These spend rows sum to ~$11.0M [sample] Q2 ProteinPeak total media; the $4.2M number Hugo Lin is "sitting on" maps to **net-incremental retail-media** (Target Roundel + Amazon Ads + Walmart Connect + Sprouts) less Q1 baseline run-rate.

---

## Date windows extended for the launch

The synthetic dataset's primary windows now extend to **2026-05-31** for every table that has a date column. This is so:

- The Week-4 read window (May 15–22, 2026) has data behind it.
- The Whitfield business review (May 26, 2026) has weeks of post-launch data to reference.
- The repeat-curve comparison vs Berry Crunch has at least 4 weeks of post-launch HH purchases.

| Table | Old end date | New end date |
|---|---|---|
| `epos` | 2026-03-31 | 2026-05-31 |
| `perfect_store` | 2026-03-31 | 2026-05-31 |
| `syndicated_weekly` | 2026-05-04 | 2026-05-25 (W21) |
| `brand_health` (waves) | 2026Q1 | 2026Q1 + **2026Q2** |
| `household_transactions` | 2026-03-31 | 2026-05-31 |
| `plan_vs_actual` (months) | 2026-03 | 2026-05 |
| `sku_authorization` snapshots | 2026-03-31 | + **2026-04-30, 2026-05-31** |
| `shipments` | 2026-03-31 | 2026-05-31 |
| `promo_events` | 2026-03-31 | 2026-05-31 |
| `social_mentions` | 2026-03-31 | 2026-05-31 |
| `creator_posts` | 2026-03-31 | 2026-05-31 |
| `search_trends` (months) | 2026-03 | 2026-05 |
| `product_reviews` | 2026-03-31 | 2026-05-31 |
| `data_freshness_log` | 2026-05-04 | 2026-05-25 |

The Louisiana decline (Scenario 1) is unaffected — all of its anchor dates (Sept 2025 reset, Nov 2025 hurricane, Q1 2026 share) sit inside both old and new windows.

---

## Switching_Flag taxonomy (extended)

The `household_transactions.Switching_Flag` column now carries the following values:

| Value | Meaning | Scenario |
|---|---|---|
| `No` | Default — no switching event detected | Both |
| `Yes` | LA Crunchwell-loyal household switched to Field & Honey (Q4'25-Q1'26) | LA decline |
| `New_To_Brand` | Household purchased PP005 or PP006 with no prior ProteinPeak history | PP Q2 launch |
| `Cannibalization` | Household purchased PP005/PP006 having previously been a PP001 buyer | PP Q2 launch |
| `Competitor_Switch` | Household purchased PP005/PP006 having previously been a Magic Spoon / Three Wishes / Catalina buyer | PP Q2 launch |

Backward compatibility: existing prototypes that filter `Switching_Flag = 'Yes'` for the LA story continue to work unchanged. New prototypes can filter on the new values.

---

## Curated event log

The full launch event timeline lives at [`seeds/proteinpeak_q2_launch.csv`](../../seeds/proteinpeak_q2_launch.csv). This is the canonical analog of `seeds/promo_events_louisiana.csv` and is also re-emitted into `promo_events.parquet` for query.

| Event | Date | What |
|---|---|---|
| PP-E001 / PP-E002 | 2026-04-20 | Target launch + endcap, PP005 + PP006 |
| PP-E003 / PP-E004 | 2026-04-20 → 2026-05-17 | 4-wk Target endcap window |
| PP-E005 / PP-E006 | 2026-04-20 → 2026-05-31 | Amazon launch coupon |
| PP-E007–PP-E010 | 2026-04-20 → 2026-05-31 | WFM + Sprouts new-item TPR |
| PP-E011 | 2026-04-27 → 2026-05-24 | Walmart-pilot SKU test (soft trial) |
| PP-E012 | 2026-04-27 → 2026-05-24 | Kroger Cocoa Almond new-item |
| PP-E013 | 2026-04-20 | Sage Park #ProteinDrop creator launch (CR-0012 anchor) |
| PP-E014 | 2026-04-20 → 2026-05-31 | $4.2M Q2 retail-media (Pacvue) |
| PP-E015 | 2026-05-25 | Maya's Week-4 read deck milestone |
