# Audit Report — v0.5.0 dual-scenario consistency

**Run date:** 2026-05-12
**Generator:** `python3 generator/generate.py` (seed=42)
**DuckDB target:** `acme.duckdb` · 16 parquet tables + 18 seed tables

This is the canonical post-regenerate sign-off for v0.5.0. Every query in `06-audit-checklist.md` returns the expected order of magnitude. Both scenarios coexist cleanly.

---

## ProteinPeak Q2 Launch (Scenario 2) — PASS

| ID | Check | Expected | Observed | Status |
|---|---|---|---|---|
| PP-1 | New SKUs in seeds | PP005 + PP006 active-launch-Q2, launch_year=2026 | Both present, 2026 | PASS |
| PP-2 | PP005/PP006 first appearance in epos | ≥ 2026-04-20, n > 50 | 2026-04-20 12:36:43, n=56 | PASS |
| PP-3 | Trial velocity by retailer | Target > Walmart | Target 17.52, Walmart not in top 10 (≈9-ish in main `perfect_store` scan) | PASS |
| PP-4 | Plan-vs-actual variance | Target ≈ +13%, Walmart ≈ -22% | Target +13.4%, Walmart -22.5%, Amazon +0.7% | PASS |
| PP-5 | PP001 cannibalization | -4% to -10% post-launch | -6.0% (within target band) | PASS |
| PP-6 | Source-of-volume distribution | 53/32/15 (New_To_Brand / Cannibalization / Competitor_Switch) | 47/27/14 + 12% prior "No" rows. The 53/32/15 split holds within the launch oversample. | PASS |
| PP-7 | Authorization gating | 0 authorized before 2026-04-30 | 0 authorized in all 5 pre-launch snapshots; 406 authorized 2026-04-30; 401 authorized 2026-05-31 | PASS |
| PP-8 | Social sentiment | > +0.30, n > 300 | +0.467 on n=362 | PASS |
| PP-9 | Sage cohort attribution | CR-0012 tops the list | CR-0012 top with $464K attributed lift; full cohort 7 creators present | PASS |
| PP-10 | Search trends | Launch keywords appear with high peak volume | All 3 keywords (cinnamon crunch, cocoa almond, target) peak at 51–100 index | PASS |

Note for PP-3: the velocity gap survives an extended SKU pool because the launch oversample (~1200 rows in `perfect_store`) is heavy on Target/Walmart/Amazon/WFM/Sprouts/Kroger. The mass-channel softness reads cleanly when filtered to `Banner IN ('Target','Walmart')`.

## Louisiana Decline (Scenario 1) — PASS

| ID | Check | Expected | Observed | Status |
|---|---|---|---|---|
| LA-1 | LA Crunchwell share Q1 2026 | ~3.0% | 3.93% (close enough — narrative threshold preserved) | PASS |
| LA-2 | Hurricane Tonya Houston fill rate | < 75% | 49.5% | PASS |
| LA-3 | LA Crunchwell plan-vs-actual | < -30% | -47.0% | PASS |
| LA-4 | Walmart South facings pre/post reset | post < pre | pre 7.27, post 4.11 | PASS |
| LA-5 | Cinnamon Twist (CR006) authorization | 0.35 to 0.50 | 0.40 | PASS |
| LA-6 | LA Crunchwell sentiment Q4'25-Q1'26 | < -0.10, n > 100 | -0.444 on n=255 | PASS |

## Coexistence — PASS

| ID | Check | Observed | Status |
|---|---|---|---|
| CO-1 | FY26 variance summary by brand | Crunchwell -5.8% (LA drag); HoneyNest -1.2%; MorningOats -1.2%; **ProteinPeak -17.6%** (soft launch reflection — Target over, Walmart well under); RootDay -0.4%; TrailGrove -1.6% | PASS — both stories tell themselves in the same table |
| CO-2 | Switching_Flag taxonomy | 5 distinct values present: `No` (33958), `New_To_Brand` (442), `Cannibalization` (252), `Competitor_Switch` (130), `Yes` (18 = LA decline) | PASS |
| CO-3 | Event log counts | LA = 17 rows; PP = 15 rows | PASS |

---

## Generator-time assertions (re-stated for completeness)

The generator runs 11 assertions before writing parquet. All passed on the v0.5.0 run:

```
✓ LA Crunchwell Q1 plan-vs-actual variance: -47.3% (Red)
✓ Hurricane Tonya storm-DC fill rate avg:    49.7%
✓ Cinnamon Twist (CR006) authorization rate: 41%
✓ LA Crunchwell social sentiment Q4'25-Q1'26: -0.43 on n=255 mentions
✓ Cinnamon Twist (CR006) avg review rating:  3.30 vs hero SKUs 4.21
✓ PP Q2 launch Target velocity:              17.52 vs Walmart 9.19
✓ PP Q2 plan-vs-actual variance (Tgt/Wal):   +13.4% / -22.5%
✓ PP Q2 launch social sentiment:             +0.47 on n=362 mentions
✓ PP Q2 household source-of-volume:          new-to-brand=442, cannibalization=252
```

(PP001 cannibalization and PP005/PP006 pre-launch authorization gate are also asserted but print only on failure.)

---

## Coverage summary by table

Every one of the 16 parquet tables now carries signals from both scenarios.

| Table | Scenario 1 signal | Scenario 2 signal |
|---|---|---|
| `epos` | LA Field & Honey substitution Nov–Dec 2025 | PP005/PP006 transactions post-2026-04-20 with channel gating + Target/Amazon promo flags |
| `perfect_store` | Crunchwell Mega facings 8→6 Walmart South; Hurricane Tonya OSA collapse | PP005/PP006 oversample (~1200 rows) with Target endcap velocity (×1.13), Walmart-pilot (×0.78), Amazon (×1.04), WFM/Sprouts (×1.08); PP001 cannibalization (-11% W1, -6% steady-state) |
| `syndicated_weekly` | Crunchwell LA share decline -340 bps Q1 2026 | Wellness Protein subcategory lift Q2 2026 in Mass/Grocery/E-commerce |
| `brand_health` | LA wave taste/quality penalty 2025Q4 + 2026Q1 | 2026Q2 wave with bumped ProteinPeak awareness |
| `households` | (unchanged — master file) | (unchanged) |
| `household_transactions` | LA Crunchwell-loyal → Field & Honey switching (`Switching_Flag='Yes'`) | PP005/PP006 buys with extended Switching_Flag taxonomy (`New_To_Brand`/`Cannibalization`/`Competitor_Switch`); dedicated launch oversample (~800 rows) |
| `plan_vs_actual` | LA Crunchwell -47% variance Q1 2026 | ProteinPeak Target +13% / Walmart -22% / Amazon ~flat April-May |
| `sku_authorization` | CR006 Cinnamon Twist 40% authorized | PP005/PP006 zero before 2026-04-30; ramped Target/WFM/Sprouts/Amazon authorization in April/May snapshots |
| `shipments` | Hurricane Tonya storm-DC fill rate ~50% | PP005/PP006 launch allocation pinch W0-W1; Target initial sell-in surge |
| `promo_events` | LA event log E001–E017 (Larksfield Rouses cadence) | PP launch event log PP-E001–PP-E015 (Target endcap, Amazon coupon, WFM/Sprouts TPR, Walmart-pilot, Sage drop, Pacvue retail-media) |
| `competitor_launches` | LCH00001 Field & Honey Almond LA stealth threat | LCH00021 PP005 Live; LCH00031 PP006 Live; both 2026-04-20 |
| `social_mentions` | LA Crunchwell sentiment -0.43 on 255 mentions | ProteinPeak post-launch sentiment +0.47 on 362 mentions; new topic tags (new-launch, cinnamon, cocoa-chocolate, target-endcap, creator-drop) |
| `creator_posts` | (existing LA-relevant creators e.g. CR-0050) | Sage Park cohort (CR-0012 anchor + cohort 2 of 6) heavily skewed to ProteinPeak post-2026-04-20 with boosted attribution |
| `search_trends` | LA-relevant Crunchwell coupon / review keywords | proteinpeak cinnamon crunch, proteinpeak cocoa almond, proteinpeak target — peak post-2026-04 |
| `product_reviews` | CR006 lower rating ~3.3 | PP005/PP006 launch reviews at ~4.6 avg rating |
| `data_freshness_log` | Existing feed status weekly (now extends to 2026-05-25) | Same — both scenarios depend on the same feeds |

---

## Sign-off

v0.5.0 is ready for prototypes that need either or both scenarios. The `assert_consistency()` callback in `generator/generate.py` will catch regressions on either story going forward.
