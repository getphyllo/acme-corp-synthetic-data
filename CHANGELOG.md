# Changelog

All notable changes to this dataset are tracked here. The repo follows [Semantic Versioning](https://semver.org/) — major bumps are breaking schema changes, minor bumps add tables/columns, patch bumps fix data without changing schema.

> **Current canonical version: `v0.5.0`** — Adds the **ProteinPeak Q2 2026 Launch Read** as Scenario 2 alongside the existing Louisiana decline (Scenario 1). Extends the data window to 2026-05-31. Adds SKUs PP005 (Cinnamon Crunch) + PP006 (Cocoa Almond). Renames PP001 to "ProteinPeak Vanilla Almond Original". Adds 6 new audit assertions; 13 seed files (was 11); 7-snapshot `sku_authorization` (was 5). All v0.4.1 row queries continue to work; row counts are larger but distributions are preserved.

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
