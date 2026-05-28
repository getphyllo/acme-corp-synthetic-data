# Changelog

All notable changes to this dataset are tracked here. The repo follows [Semantic Versioning](https://semver.org/) — major bumps are breaking schema changes, minor bumps add tables/columns, patch bumps fix data without changing schema.

> **Current canonical version: `v0.7.0`** — Adds **six Marketing & Insights v2 scenarios** (Cory's Crunchwell FY27 brand plan, Renee's ProteinPeak launch comms, Wes's Target back-to-school 2026, Nina's Q3 SOTB, Maya's Chocolate Almond concept test, Jordan's LA-DMA share decline diagnostic) on top of the existing S1–S5 stories. Adds **6 new parquet tables** (22 total, was 16), **7 new seed files** (31 total, was 24), **9 new cross-table assertions** (31 total, was 22), and **2 new leading-indicator DMAs** (BIR-DMA, MEM-DMA). Appends the **Field & Honey 14g protein extension** (LCH00032) to `competitor_launches`. v0.7.0 *does* add parquet schema (six new tables); all v0.6.0 queries on the previous 16 tables continue to work unchanged.

## [v0.7.0] — 2026-05-28

### Added — Six Marketing & Insights v2 scenarios (S6–S11)

Six new scenarios anchored to the **v2 Marketing & Insights persona pack** (`clayface-workspace/00-inbox/00-drop-zone/2026-05-28-marketing-insights-personas.md` → promoted to `11-scenarios/v2/`):

**Scenario 6 — Crunchwell FY27 Annual Brand Plan** (Cory Whitman, Brand Director Crunchwell)

- Trigger: Wednesday 2026-06-03; FY27 plan due to Devon + Helen by 2026-07-15
- Cory's ask: defensible **diagnosis + creative platform + media envelope** in six weeks
- Anchors: Crunchwell -2.1 share points over 6 quarters (-1.3 F&H / -0.6 PL / -0.2 other); **Trust ~flat, Relevance -6pp** (the lead diagnostic); price gap to F&H widened 8% → 14%; protein-curious cohort first-purchase F&H 38% of the time
- Decision: "Modern Relevance, Heritage Trust" platform; trade-to-media reallocation defended on incrementality

**Scenario 7 — ProteinPeak Launch Comms & Creator Plan** (Renee Alvarez, Sr Brand Manager ProteinPeak)

- Trigger: Monday 2026-05-18; launch ships 2026-07-01, on-shelf 2026-07-08; recommendation due 2026-06-06
- Renee's ask: $6.4M envelope allocation across creator, paid social, retail media, sampling, PR; **claim ranking holds against Field & Honey 14g shift**
- Anchors: Three claims clearing 55% action standard (CL1 "20g protein, less sugar" wins protein-curious + GLP-1-adjacent; CL2 "Clean fuel, real grains, no fillers" wins lapsed; CL3 "Eat like you mean it" = platform line); F&H 14g narrows protein delta 11g → 6g (sugar leg still wins); **280K-household Numerator sampling cohort** (never-Crunchwell); creator-overlap analysis flags 4 names with F&H paid posts in last 12 months; retail-media flight 58% Walmart Connect + Amazon, 42% Kroger Precision + Target Roundel

**Scenario 8 — Target Back-to-School 2026 Program** (Wes Okafor, Sr Mgr Shopper Marketing)

- Trigger: Tuesday 2026-05-26; Christina Reyes (Target buyer) needs proposal by 2026-06-12; window runs 2026-07-13 → 2026-08-23
- Wes's ask: buyer-ready proposal covering Crunchwell Mega endcap (800 doors), ProteinPeak circular feature (4 weeks), Cinnamon Twist mechanic redesign
- Anchors: **2025 BTS = $14.4M incremental category dollars** (mechanic decomp endcap 62% / circular 21% / Roundel 12% / Cartwheel 5%); 2025 velocity per door Crunchwell Mega 1.42× baseline; **Target × ProteinPeak cohort overlap 64.7%** (highest of any major retailer); 2026 velocity commits PP 1.38×, CR Mega 1.45×; **Cinnamon Twist Cartwheel destroyed value in 2025** → do not repeat
- Net: $2.8M Acme investment / $1.2M Target Roundel co-invest

**Scenario 9 — Q3 Category State-of-the-Business Read** (Nina Ortega, VP Consumer Insights)

- Trigger: Monday 2026-06-01; read happens 2026-07-22 to Helen + Devon + exec committee
- Nina's ask: **reconcile NielsenIQ + Kantar Worldpanel + April U&A** into a single consumer story
- Anchors: NielsenIQ category +2.1% (protein segment +11.4%, family cereal -1.2%); Kantar HH penetration -60bps but frequency up; **U&A: 28% of HHs skip cereal 3+ mornings/wk; 64% cite protein as swap driver**; data hierarchy: behavior leads → panel follows → till trails; **cereal-skipper cell n=672** (segment-level OK, regional DMA cuts not OK); Numerator triangulates the U&A swap-out pattern

**Scenario 10 — ProteinPeak Q3 Chocolate Almond Concept Test** (Maya Chen, Sr Insights Analyst, Innovation & Foresight)

- Trigger: Wednesday 2026-06-10; field 2026-06-22 → 2026-07-11 (n=1,000); steerco brief due 2026-07-25
- Maya's ask: decision-support brief with **topline + cohort breakouts (Acme segmentation, not Ipsos) + cannibalization gate on same screen**
- Anchors: **Top-two-box 64%** (clears 55% standard, +6pp over launch SKU pre-test, +11pp over cereal innovation benchmark); cohort cuts protein-curious 71% / lapsed-cereal 66% / current-Crunchwell 52%; **cannibalization: 22% overlap → 14pp additive, 8pp substitutional → clears 12pp steerco threshold**; U&A overlay: chocolate-as-breakfast preference +14pp above category avg in protein-curious cohort; F&H Chocolate Crunch trademark filed 2026-04-22

**Scenario 11 — LA-DMA Share Decline Diagnostic** (Jordan Hsu, Manager Category & Shopper Insights)

- Trigger: Tuesday 2026-05-19; diagnostic due 2026-05-23 for Marcus (Walmart Aug prep) + Priya (Kroger JBR pre-read)
- Jordan's ask: decompose 3.1-point share loss in LA-DMA over 8 weeks; identify lost cohort + destination + leading-indicator DMAs
- Anchors: Decomposition -1.4 velocity / -0.9 facings / -0.6 price gap / -0.2 mix; Baton Rouge families with kids 5-14 down 19% frequency (71% → F&H); protein-curious cohort down 26% frequency (out of category); **leading-indicator DMAs: BIR-DMA + MEM-DMA** (early-stage LA pattern); response plan $740K → 1.8 share points recovery over 12 weeks

**New parquet tables (6) — 22 total (was 16):**

| Table | Rows | Purpose |
|---|---:|---|
| `brand_equity_quarterly` | 975 | Kantar tracker w/ Relevance + Modernity added on top of v0.1.0 brand-health 5pt battery. Anchors Cory's diagnosis. |
| `ua_study_responses` | 2,400 | April 2026 Ipsos U&A behavioral study at per-respondent grain. Anchors Nina's SOTB and Maya's concept-test U&A overlay. |
| `ua_qual_pointers` | 36 | In-home interview index with chocolate-mention flags. Used in Maya's steerco brief. |
| `kantar_worldpanel_cohort` | 120 | HH penetration + frequency by cohort × DMA × quarter. The panel layer in the data hierarchy. |
| `numerator_bts_occasion` | 35 | Target 2025 back-to-school benchmark with Target Circle + protein-curious overlays. Anchors Wes's 2026 program. |
| `concept_tests` | 60 | Long-form (one-row-per-metric) results for Chocolate Almond + April launch claims. Acme-segmentation cuts. |

**New seed files (7) — 31 total (was 24):**

| File | Rows | Purpose |
|---|---:|---|
| `seeds/brand_equity_tracker_quarterly.csv` | 975 | Source seed for `brand_equity_quarterly` parquet |
| `seeds/ua_study_2026q2_reference.csv` | 28 | Cohort × occasion reference grain (expanded into 2,400 per-respondent rows) |
| `seeds/ua_qual_pointers_2026q2.csv` | 36 | One row per in-home interview |
| `seeds/kantar_worldpanel_cohort_frame.csv` | 120 | Source seed for `kantar_worldpanel_cohort` parquet |
| `seeds/numerator_bts_occasion_2025.csv` | 35 | Source seed for `numerator_bts_occasion` parquet |
| `seeds/concept_test_chocolate_almond.csv` | 25 | Chocolate Almond test (n=1,000) |
| `seeds/concept_test_launch_claims_2026q2.csv` | 35 | April Kantar launch-claims test (n=1,200) |

**Seed merges (2):**

- `seeds/competitor_launches.csv` — appended **Field & Honey 14g protein extension (LCH00032, 2026-05-12 launch, 612 stores)** to support Renee's competitive-shift narrative in S7.
- `seeds/geographies.csv` — appended **Birmingham-Tuscaloosa-Anniston DMA (BIR-DMA) + Memphis DMA (MEM-DMA)** as Jordan's leading-indicator DMAs in S11.

**Generator changes:**

- Added 6 new `gen_*` functions: `gen_brand_equity_quarterly`, `gen_ua_study_responses`, `gen_ua_qual_pointers`, `gen_kantar_worldpanel_cohort`, `gen_numerator_bts_occasion`, `gen_concept_tests`.
- Extended `DMAS`, `DMA_CITIES`, and `DMA_STATE` constants with BIR-DMA + MEM-DMA. Both new DMAs ripple through all transactional tables (`epos`, `perfect_store`, `syndicated_weekly`, `brand_health`, `household_transactions`, `plan_vs_actual`, `sku_authorization`) at low-weight volumes since they're watch-list, not full-volume.
- Updated `main()` from 16-step to 22-step pipeline.

**New cross-table assertions (9 — bringing total from 22 → 31):**

23. Crunchwell US-NAT Trust drift FY25Q1 → FY26Q2 < 3pp absolute (roughly flat).
24. Crunchwell US-NAT Relevance drift FY25Q1 → FY26Q2 ≤ -3pp (v2 canon ~-6pp).
25. U&A `Skip_Cereal_3plus_Mornings` rate ∈ [24%, 32%] (v2 canon 28%).
26. U&A cereal-skipper cohort n == exactly 672 (the cell-size constraint Nina enforces).
27. U&A `Cite_Protein_As_Swap_Driver` rate among skippers ∈ [58%, 70%] (canon 64%).
28. Kantar cereal-skipper cohort penetration grows FY25Q1 → FY26Q2 at US-NAT.
29. Numerator BTS Target 2025 incremental total ∈ [$13M, $15.4M] (v2 canon $14.2M).
30. Numerator BTS Target × protein-curious overlap > Walmart's, and ∈ [60%, 68%] (canon 64%).
31. Concept test Chocolate Almond top-two-box ≥ 55% (clears action standard) AND substitutional cannibalization < 12pp (clears steerco gate). BIR-DMA + MEM-DMA both present in `syndicated_weekly`.

**Notes for prototype maintainers:**

- v0.7.0 *does* introduce parquet schema change (6 new tables). All v0.6.0 queries on the previous 16 tables continue to work unchanged.
- The v2 four-cohort frame (cereal-skipper / protein-returner / loyal-family / price-shopper) is **canonical** going forward. Workspace tiles should use these cohort names; the 2024 Acme segmentation in older personas is being phased out over FY27.
- `ua_study_responses.Cohort` is the canonical foreign key — `kantar_worldpanel_cohort.Cohort` uses the same values. Joining the two reconciles the behavior layer with the panel layer.
- The U&A cereal-skipper n=672 limit is a hard rule. Any workspace tile that tries to filter the cohort to a single DMA must surface the cell-size constraint or the read goes wrong.
- The 12pp substitutional cannibalization threshold on `concept_tests` is the Acme steerco standard. If a future scenario changes it (e.g., lowers to 10pp for line extensions vs full launches), the assertion must be updated.

## [v0.6.0] — 2026-05-16

### Added — Three commercial-persona scenarios (S3, S4, S5)

Three new scenarios ride alongside the existing Louisiana decline (S1) and ProteinPeak Q2 launch (S2), anchored to the **V2 commercial-personas brief** (`/clayface-workspace/00-inbox/30-personas-research/2026-05-16-commercial-personas-v2/`):

**Scenario 3 — Walmart August 2026 Line-Review Prep** (Marcus Boudreaux, Director Sales South)

- Trigger: Monday 2026-05-18; line review 12 weeks out (~Aug 10, 2026)
- Marcus's ask: recover **2 facings on Crunchwell Mega + Honey Nut Mega** at Walmart South Division
- Anchor: velocity-per-facing **+4%** since Sept 2025 cut despite **25% facing reduction** → category contribution down 22%; Larksfield 3-endcap pattern across **23 of 41** LA Walmart Supercenters
- Net expected impact (Q3 tactical): **1.2 share points** of recovery, **$612K** incremental revenue, against **$340K** trade investment
- Related cross-flags surfaced in narrative: Cinnamon Twist (CR006) H-E-B delisting risk; Rouses Mega OOS at 8 doors

**Scenario 4 — Kroger Q3 2026 JBR Pre-Read** (Priya Raman, Category Manager — Kroger Category Captain)

- Trigger: Tuesday 2026-05-19; JBR Tuesday 2026-07-08; pre-read due 2026-06-24 (shipped 2026-06-20 in the with-Clayface arc)
- Priya's ask: deliver an aisle-level pre-read with consumer-demand and rebalance recommendation
- Anchors: Larksfield Field & Honey **+1.4 pts** at Kroger nationally / **+2.1 pts** in the South; Simple Truth **+0.8 pts** across the protein segment; Crunchwell flat at Kroger; three segment shifts (protein-forward, sugar-reduced, ancient-grain) each pulling **2.3% per quarter** from traditional family cereal
- Switching insight surfaced: **14% of Crunchwell lapsed Kroger buyers** went to Simple Truth in Q1 2026

**Scenario 5 — Q1 2026 Retail-Media & Trade-Promo Effectiveness Read** (Tasha Brooks, Director eCommerce & Retail Media)

- Trigger: Thursday 2026-05-21; CFO half-day session Thursday 2026-06-04 (called by Helen Park-Choi)
- Tasha's ask: defend the retail-media envelope; deliver true incrementality (not platform-reported ROAS) by channel × retailer × SKU
- Anchors: **$4.2M** Q1 retail-media envelope; **$11.6M** Q1 trade-promo spend; decomposition = **$2.7M incremental / $1.1M cannibalization / $0.4M undetermined**; blended ratio **$0.64**; per-platform ratios **WMT Connect $1.20 / Amazon $0.41 / Kroger Precision $0.79 / Target Roundel $0.55**
- LA tactical injection (Marcus, late March): **$280K** spend → **1.1 share points** vs 1.2 model expectation → **$612K** incremental revenue → **2.2× incremental ROI**
- H2 reallocation recommendation: **pull $700K from Amazon Ads** → push into Walmart Connect + Kroger Precision
- Surfaced insight: **3 value-destroying trade-promo events** in Mountain West Q1 (negative incrementality)
- ProteinPeak/Crunchwell retail-media SKU-level outperformance: **2.3×** on Amazon (PP003 Berry Crunch vs CR002 Original Mega)

**New seed files (5):**

| File | Rows | Purpose |
|---|---:|---|
| `seeds/retail_media_spend_q1_2026.csv` | 24 | Q1 2026 retail-media spend by platform × brand × month with platform-reported ROAS, modeled incrementality ratio, incremental revenue, cannibalization, undetermined. Sums to $4.2M spend / $2.7M incremental. |
| `seeds/trade_promo_events_q1_2026.csv` | 43 | Q1 2026 trade-promo event log across all retailers ($11.6M total). Anchors Marcus's LA tactical injection (TPE-Q1-011) and Tasha's Mountain West value-destroying cluster (TPE-Q1-018/019/020). |
| `seeds/walmart_endcap_audit_la.csv` | 62 | Walmart Supercenter endcap snapshot for Louisiana, Sept 2025 → May 2026. Anchors the 23-of-41 Larksfield 3-endcap pattern. |
| `seeds/kroger_simple_truth_switching.csv` | 21 | Crunchwell-lapsed → Simple Truth (Kroger PL) switching study by Kroger division. Anchors 14% national switch rate and three segment-level 2.3%/qtr shifts. |
| `seeds/heb_cinnamon_twist_delist_risk.csv` | 9 | H-E-B Cinnamon Twist (CR006) authorization risk by region. Anchors Marcus's cross-flag for the Walmart pre-read. |
| `seeds/rouses_oos_by_door.csv` | 15 | Rouses Mega (CR002) OOS audit door-by-door as of 2026-05-12. Anchors the "8 doors OOS" reference in Marcus's pre-read. |

(That's 6 net new seeds, taking the total from 13 → 18.)

**New cross-table assertions (11 — bringing total from 11 → 22):**

12. Walmart endcap audit has ≥23 LA Supercenters with `larksfield_endcap_count >= 3` on 2026-05-11.
13. Walmart endcap audit has 0 LA stores with `acme_endcap_count >= 1` on 2026-05-11.
14. Kroger Simple Truth switching national rate ≈ 14% (±0.5pp).
15. Kroger Larksfield gain = +1.40 pts national, +2.10 pts South.
16. Three Kroger segment shifts (protein-forward / sugar-reduced / ancient-grain) each at +2.30 pts/quarter.
17. Q1 retail-media total spend = $4.2M (±1%).
18. Q1 retail-media total incremental revenue = $2.70M (±$50K).
19. Per-platform incrementality ratios: WMT Connect 1.20 / Amazon 0.41 / Kroger Precision 0.79 / Target Roundel 0.55 (±0.02).
20. Q1 trade-promo total spend = $11.6M (±1%).
21. LA tactical injection (TPE-Q1-011) spend=$280K, incr=$612K.
22. Exactly 3 Mountain West trade-promo events with negative incrementality.

**Notes for prototype maintainers:**

- v0.6.0 is **seeds-only** — no parquet-table schema changes. All v0.5.0 queries continue to work unchanged.
- The new scenarios cross-reference existing parquet tables: `perfect_store` (facings, OSA), `syndicated_weekly` (Crunchwell_Value_Share by Kroger DMA), `sku_elasticity_estimates` (LA injection model), `data_freshness_log` (model refresh dates).
- Marian's elasticity model `last_recalibrated` field is the gate Tasha leans on in the CFO read. Don't change `2026-04-15` without updating the scenario narrative.
- Marcus's LA tactical injection economics (2.2× incremental ROI) flow from the existing `sku_elasticity_estimates.csv` Rouses CR002 row (elasticity -2.12, confidence 0.66) — that's the model that produced the 1.2 prediction; the 1.1 landed result is the synthetic outcome.

## [v0.5.0] — 2026-05-12

### Added — ProteinPeak Q2 2026 Launch Read (Scenario 2)

A second scenario rides on top of the existing Louisiana decline dataset. Both stories are now queryable from the same 16 parquet tables and the same DuckDB file. See [`docs/proteinpeak-q2-launch/`](./docs/proteinpeak-q2-launch/) for the full playbook.

**New SKUs:**

| SKU | Name | Launch Date | Year-1 Plan |
|---|---|---|---|
| **PP005** | ProteinPeak Cinnamon Crunch 12oz | 2026-04-20 | $14M |
| **PP006** | ProteinPeak Cocoa Almond 12oz | 2026-04-20 | $10M |

**Renamed SKU (non-breaking — same SKU ID, more descriptive name):**

| SKU | Was | Now |
|---|---|---|
| PP001 | ProteinPeak Original | **ProteinPeak Vanilla Almond Original** |

**New seed file:** `seeds/proteinpeak_q2_launch.csv` — 15-event canonical launch timeline (PP-E001–PP-E015) covering Target endcap, Amazon coupon, WFM/Sprouts new-item TPR, Walmart-pilot, Sage Park creator drop, and the $4.2M Pacvue retail-media line item. Mirrors `seeds/promo_events_louisiana.csv`.

**Data window extension:** all 16 tables now extend to **2026-05-31** (previously 2026-03-31 for most). The Q1 LA decline anchors and Q1 plan-vs-actual values are unchanged.

**Extended Switching_Flag taxonomy** (`household_transactions`):

| Value | Meaning |
|---|---|
| `No` | Default — no switching event |
| `Yes` | LA decline — Crunchwell-loyal HH switched to Field & Honey (unchanged) |
| `New_To_Brand` | NEW — HH bought PP005/PP006 with no prior ProteinPeak history |
| `Cannibalization` | NEW — HH bought PP005/PP006 having previously bought PP001 |
| `Competitor_Switch` | NEW — HH bought PP005/PP006 having previously bought Magic Spoon/Three Wishes/Catalina |

**New brand_health wave:** `2026Q2` — adds awareness lift for ProteinPeak post-launch.

**Authorization snapshots added:** `2026-04-30` and `2026-05-31` (alongside the existing 5 snapshots).

**Six new cross-table assertions** in `assert_consistency()`:

6. PP005/PP006 Target velocity > Walmart velocity
7. PP001 post-launch velocity ≤ pre-launch × 1.02 (cannibalization)
8. PP005/PP006 authorization = 0 before 2026-04-30
9. ProteinPeak Target plan-variance > Walmart plan-variance (Q2 2026)
10. PP launch social sentiment > +0.10 with ≥ 50 mentions
11. `New_To_Brand` count > `Cannibalization` count among PP005/PP006 HH buys

**Seed updates:**

- `seeds/skus.csv` — PP001 renamed; PP005 + PP006 added
- `seeds/innovation_pipeline.csv` — INV003/INV004 promoted Stage-5 → Stage-6 In-Market
- `seeds/competitor_launches.csv` — LCH00021 promoted Pre-Launch → Live; LCH00031 added (Cocoa Almond)
- `seeds/marketing_spend.csv` — 2026-Q2 ProteinPeak Q2 launch rows added (~$11M total media; $4.2M retail-media net incremental)
- `seeds/trade_spend_fy25.csv` — 3 ProteinPeak retailer rows added (WFM, Sprouts, Kroger)
- `seeds/sku_elasticity_estimates.csv` — 8 provisional elasticity rows for PP005/PP006 (Target/Amazon/Walmart/WFM)
- `seeds/macro_trends.csv` — MT004 cinnamon updated; MT031 cocoa-protein + MT032 Wellness-Hero pillar added
- `seeds/social_topics.csv` — 5 new launch-related topics (new-launch, cinnamon, cocoa-chocolate, target-endcap, creator-drop)
- `seeds/creators.csv` — CR-0013 promoted Pitched → Active for Q2 cohort
- `seeds/monthly_pos_fy25_q12026.csv` — added ProteinPeak 2025-04, 2025-Q4, 2026-Q1, 2026-04, 2026-05 rows (with PP005/PP006 SKU-level breakdown)
- `seeds/category_market_size.csv` — added Q2-FY2026-MTD Wellness Protein rows (national + Target + Walmart)

**Docs:**

- New folder `docs/proteinpeak-q2-launch/` with 6 reference files (overview, data model, hypothesis tree, deck outline, persona supplement, audit checklist)
- `docs/narrative-anchors.md` — restructured for dual-scenario; new ProteinPeak constants table; 6 new assertions documented; new "do not" rules
- `README.md` — second narrative table for Scenario 2; tree updated; version bumped

**Notes for prototype maintainers:**

- All v0.4.1 queries continue to work — same column names, same primary keys, same retailer / DMA / brand vocabularies.
- The seed `random.seed(42)` is preserved. Re-running the generator on the same code yields the same rows.
- Total row count grew ~12-15% across most tables because of window extension + launch oversamples. If a prototype relies on hard-coded row counts (it shouldn't), update.

## [v0.4.1] — 2026-05-10

### Changed — Fictionalize the #3 cereal competitor

The #3 US cereal manufacturer in the Acme universe — previously identified by the real-world brand "Post Foods" and its flagship SKUs "Honey Bunches of Oats" and "Great Grains" — is renamed to a fully fictional competitor. This is a world-consistency fix: every other brand around Acme (Crunchwell, HoneyNest, ProteinPeak, TrailGrove, RootDay) was already fictional; Post was the last real-world name leaking in. Upstream Clayface vault made the same rename in `03-research/acme/` before this commit.

| Was | Now |
|---|---|
| Post Foods (manufacturer) | **Larksfield Foods** |
| Honey Bunches of Oats (SKU + brand) | **Field & Honey** |
| Great Grains (SKU + brand) | **Harvest Hearth** |

### Schema changes

Two column renames in regenerated parquets:

| Table | Was | Now |
|---|---|---|
| `syndicated_weekly` | `Post_Value_Share` | **`Larksfield_Value_Share`** |
| `brand_health` | `aided_aw_honey_bunches` | **`aided_aw_field_honey`** |

### What did *not* change

- **All row counts.** Every table preserves its v0.4.0 row count exactly (verified against pre-regen snapshot). `seed=42` determinism holds.
- **All column counts.** Every table preserves its v0.4.0 column count (the two renames swap one column for another, no adds/drops).
- **All dollar amounts, dates, transaction IDs, sentiment scores, switching flags, fill rates, ROI calculations.** The randomness draws are byte-stable; only the brand/manufacturer string labels swap.
- **SKU IDs `PF001` and `PF002`.** Retained as opaque historical join keys. The "PF" prefix is now a documented historical artifact — real-world CPG SKU codes routinely carry legacy prefixes from acquired or rebranded entities. Renaming these IDs would force a foreign-key migration across 6+ tables for no analytical benefit.

### Files touched in this rename

- **Seeds (8):** `competitor_launches.csv`, `creators.csv`, `geographies.csv`, `macro_trends.csv`, `promo_events_louisiana.csv`, `retailer_divisions.csv`, `retailers.csv`, `social_topics.csv`, `trade_spend_fy25.csv`
- **Generator (1):** `generator/generate.py` — 18 string literals + 2 emitted column names
- **Docs (9):** `docs/louisiana-decline.md`, `docs/narrative-anchors.md`, 4× `docs/personas/*.md`, 4× `docs/schema/*.md`
- **Top-level (2):** `README.md`, `CHANGELOG.md`
- **Regenerated:** 11 of 16 `data/*.parquet` files, 10 of 16 `samples/*_sample.csv` files, `acme.duckdb` (the 5 unchanged tables — `data_freshness_log`, `households`, `plan_vs_actual`, `shipments`, `sku_authorization` — have no competitor brand references in their schemas)

### What's still real-world

This pass intentionally left **General Mills / Cheerios / Honey Nut Cheerios / Kellanova / Frosted Flakes / Walmart Great Value** unchanged. Those are still real-world names in the dataset. Renaming them is on the table as a v0.5.0 follow-up; bundling them into this commit would balloon the diff and make review harder. Surface them only if needed.

## [v0.4.0] — 2026-05-08

### Added — Polish + edge cases (Tier 3 gaps from `00-inbox/synthetic-data-gap-analysis-vs-mvp.md`)

- **`data_freshness_log.parquet`** — weekly status of every Acme data feed (NielsenIQ / Numerator / SAP / Brandwatch / etc.); `Status` enum captures real-world drift
- **Seeds added:** `category_market_size.csv` (TAM), `sku_elasticity_estimates.csv` (pre-computed elasticities), `innovation_pipeline.csv` (Acme pipeline), `regional_brands.csv` (Cape Cod / Tony Chachere's / etc.), `macro_trends.csv` (30 consumer trends incl. GLP-1 / TikTok Shop / Hispanic formats), `social_topics.csv` (topic taxonomy)

## [v0.3.0] — 2026-05-08

### Added — Brand & Insights synthesis (Tier 2 gaps + T1.4)

The four Brand-Manager-side prompt families (social listening / creator activity / search momentum / product reviews) are now answerable. Adds the consumer-side context Priya Raman (Cat Manager) needs.

- **`competitor_launches.parquet`** — 30 hand-curated launch events, including Larksfield Field & Honey Almond (Sep 2025 — the LA stealth threat), GM Cheerios Oat Crunch (Jan 2026), Walmart Great Value PL expansion (LA H5), and Acme's own Crunchwell Cinnamon Twist underperformer
- **`social_mentions.parquet`** — 18,000 Brandwatch-shape mentions across TikTok / Instagram / Twitter / Reddit / YouTube; sentiment encoded with the LA Crunchwell dip + Field & Honey viral wave + ProteinPeak athletic momentum
- **`creator_posts.parquet`** — 3,200 creator posts with 72hr attribution lift; sourced from a 50-creator master (`seeds/creators.csv`); encodes the Sage Park ProteinPeak athlete program
- **`search_trends.parquet`** — 2,400 monthly keyword × platform rows from Spate / Helium 10 / Google Trends; encodes high-protein cereal, oat milk barista, Cheerios Oat Crunch search peak
- **`product_reviews.parquet`** — 24,000 Bazaarvoice / PowerReviews-shape reviews with topic tags; Cinnamon Twist (CR006) low-rated; Crunchwell ratings dip during Hurricane Tonya OOS

### Encoded narrative facts (v0.3.0)

- Crunchwell sentiment in LA-DMA averages **−0.36** in Q4'25–Q1'26 vs +0.13 elsewhere
- Field & Honey viral wave Q4 2025 (`Topic_Tags='viral;promo'`)
- ProteinPeak Sage Park athlete program drives top 5 attributed creator lifts
- "high-protein cereal" growing +18% MoM in search; "field & honey almond" peaks at launch
- Cinnamon Twist (CR006) average rating ~3.4 vs hero SKU ~4.3; negative themes: stale / pack-damage / too-sweet / oos

## [v0.2.0] — 2026-05-08

### Added — Sales-side completeness (Tier 1 gaps from `00-inbox/synthetic-data-gap-analysis-vs-mvp.md`)

The four Sales-side personas (Maya / Marcus / Diane) can now answer their core retail-side prompts end-to-end. Coverage of the persona playbook moves from ~62% to ~85% of in-scope prompts.

- **`plan_vs_actual.parquet`** — ~99,000 rows · monthly Brand × Retailer × DMA plan vs. actual with `Variance_Status` + `Plan_Source` (AOP vs FCST_REV); encodes the FY26 Acme operating plan (LA Crunchwell -47% vs +1.5% plan)
- **`sku_authorization.parquet`** — ~60,000 rows · per-store × Acme-SKU monthly snapshot of `Auth_Status` + `Distribution_Status`; encodes Cinnamon Twist 39% authorization, Walmart RootDay 12% test-only, H-E-B ProteinPeak 38% headroom
- **`shipments.parquet`** — ~48,000 rows · weekly DC × SKU fill rate from `seeds/research_agencies.csv` SAP feed; encodes Hurricane Tonya storm-DC collapse to ~58% Nov 8 – Dec 15 with `Cut_Reason='Storm'`
- **`promo_events.parquet`** — 720 rows · all-retailer promo log with mechanic taxonomy (TPR / BOGO / Multi-Buy / Display / Feature / Feature+Display / Bundle / Coupon), Trade_Spend, Lift, Forward_Buy, ROI; `seeds/promo_events_louisiana.csv` remains the canonical hand-curated LA subset

### Schema additions to existing v0.1.0 tables

- **`epos`** — added `Banner_Division` + `Banner_Region` columns
- **`perfect_store`** — added `Banner_Division` + `Banner_Region` columns
- **`household_transactions`** — added `Banner_Division` + `Banner_Region` columns

These two columns make divisional rollups possible (Walmart South / Kroger Cincinnati / Walmart West / etc.) and reveal that the Sept 2025 reset hit Walmart South hardest.

### Generator hardening

- Added `assert_consistency()` cross-table invariants — LA Crunchwell variance, Hurricane Tonya fill rate, Cinnamon Twist authorization rate
- Added `docs/narrative-anchors.md` — the five constants that 5+ tables depend on; reference before changing any of them

### Seeds added

- `seeds/retailer_divisions.csv` — 46 banner divisions (Walmart 5 / Kroger 14 / Target 3 / Albertsons 5 / H-E-B 5 / Publix 3 / Rouses 4 / Costco 5)
- `seeds/competitor_launches.csv` — 30 launch events
- `seeds/research_agencies.csv` — 27 data-vendor master records (NielsenIQ / Numerator / Kantar / Brandwatch / Tribe Dynamics / Mintel / Spate / Helium 10 / Bazaarvoice / SAP / etc.)

## [v0.1.0] — 2026-05-08

### Initial release

Six core tables + seven hand-curated seed tables, the four primary personas, the Louisiana decline scenario, and a reproducible generator.

- **`epos.parquet`** — 30,000 transaction-level rows (Kellogg ME EPOS-shape, US-anchored)
- **`perfect_store.parquet`** — 50,000 store-day-SKU rows with inventory, OSA, planogram compliance, facings
- **`syndicated_weekly.parquet`** — 92,250 rows of DMA × category × channel × week panel data with full competitive share breakouts (Crunchwell, Larksfield, General Mills, Kellanova, Private Label)
- **`brand_health.parquet`** — 15,000 survey responses with awareness funnel, 7-attribute battery, NPS, ethnicity, 10 competitor awareness flags
- **`households.parquet`** — 5,000-household master with demographics, loyalty segment, ethnicity
- **`household_transactions.parquet`** — 30,000 weekly HH purchases with `Switching_Flag` for the LA→Larksfield switch
- **`acme.duckdb`** — single-file SQL DB with all six tables + seven seed tables loaded
- **Seeds**: SKU master (49), retailer master (26), geographies/DMAs (30), monthly POS, trade spend, marketing spend, Louisiana promo event log

### Encoded narrative facts

- Crunchwell LA share: ~6.0% (FY24) → ~3.9% (Q1 '26)
- Walmart Sept 2025 modular reset cuts Crunchwell Mega/Honey Nut Mega/Multigrain from 8 → 6 facings
- Hurricane Tonya (Nov 8, 2025) drops Crunchwell Mega OSA in LA from ~97% to ~67% for ~6 weeks
- Field & Honey heavy promo at Rouses Q4 '25 → Q1 '26 (21% off, 6 weeks)
- LA Crunchwell-loyal HHs flagged switching to Field & Honey starting Nov 2025

### Adapted from Kellogg ME reference set

- Geography: Middle East countries → US states + 30 DMAs
- Brands: Pringles/Corn Flakes → Acme's six brands + 8 competitors (Cheerios, Field & Honey, Frosted Flakes, Quaker, Walmart Great Value PL, etc.)
- Calendar: Ramadan flag → BackToSchool / Holiday / Easter / SuperBowl seasonality enum
- Added: `Brand`, `Manufacturer`, `Ethnicity`, `Switching_Flag`, full competitor share breakouts on syndicated weekly
- Removed: Weetabix and Nestlé awareness (not US-relevant)
