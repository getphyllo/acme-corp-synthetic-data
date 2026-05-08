# Changelog

All notable changes to this dataset are tracked here. The repo follows [Semantic Versioning](https://semver.org/) — major bumps are breaking schema changes, minor bumps add tables/columns, patch bumps fix data without changing schema.

> **Current canonical version: `v0.4.0`** — 16 tables, 17 seed files, all gap-analysis-identified prompts answerable. See [`00-inbox/synthetic-data-gap-analysis-vs-mvp.md`](../00-inbox/synthetic-data-gap-analysis-vs-mvp.md) for the audit that drove v0.2 → v0.4.

## [v0.4.0] — 2026-05-08

### Added — Polish + edge cases (Tier 3 gaps from `00-inbox/synthetic-data-gap-analysis-vs-mvp.md`)

- **`data_freshness_log.parquet`** — weekly status of every Acme data feed (NielsenIQ / Numerator / SAP / Brandwatch / etc.); `Status` enum captures real-world drift
- **Seeds added:** `category_market_size.csv` (TAM), `sku_elasticity_estimates.csv` (pre-computed elasticities), `innovation_pipeline.csv` (Acme pipeline), `regional_brands.csv` (Cape Cod / Tony Chachere's / etc.), `macro_trends.csv` (30 consumer trends incl. GLP-1 / TikTok Shop / Hispanic formats), `social_topics.csv` (topic taxonomy)

## [v0.3.0] — 2026-05-08

### Added — Brand & Insights synthesis (Tier 2 gaps + T1.4)

The four Brand-Manager-side prompt families (social listening / creator activity / search momentum / product reviews) are now answerable. Adds the consumer-side context Priya Raman (Cat Manager) needs.

- **`competitor_launches.parquet`** — 30 hand-curated launch events, including Post Honey Bunches Almond (Sep 2025 — the LA stealth threat), GM Cheerios Oat Crunch (Jan 2026), Walmart Great Value PL expansion (LA H5), and Acme's own Crunchwell Cinnamon Twist underperformer
- **`social_mentions.parquet`** — 18,000 Brandwatch-shape mentions across TikTok / Instagram / Twitter / Reddit / YouTube; sentiment encoded with the LA Crunchwell dip + Honey Bunches viral wave + ProteinPeak athletic momentum
- **`creator_posts.parquet`** — 3,200 creator posts with 72hr attribution lift; sourced from a 50-creator master (`seeds/creators.csv`); encodes the Sage Park ProteinPeak athlete program
- **`search_trends.parquet`** — 2,400 monthly keyword × platform rows from Spate / Helium 10 / Google Trends; encodes high-protein cereal, oat milk barista, Cheerios Oat Crunch search peak
- **`product_reviews.parquet`** — 24,000 Bazaarvoice / PowerReviews-shape reviews with topic tags; Cinnamon Twist (CR006) low-rated; Crunchwell ratings dip during Hurricane Tonya OOS

### Encoded narrative facts (v0.3.0)

- Crunchwell sentiment in LA-DMA averages **−0.36** in Q4'25–Q1'26 vs +0.13 elsewhere
- Honey Bunches viral wave Q4 2025 (`Topic_Tags='viral;promo'`)
- ProteinPeak Sage Park athlete program drives top 5 attributed creator lifts
- "high-protein cereal" growing +18% MoM in search; "honey bunches almond" peaks at launch
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
- **`syndicated_weekly.parquet`** — 92,250 rows of DMA × category × channel × week panel data with full competitive share breakouts (Crunchwell, Post, General Mills, Kellanova, Private Label)
- **`brand_health.parquet`** — 15,000 survey responses with awareness funnel, 7-attribute battery, NPS, ethnicity, 10 competitor awareness flags
- **`households.parquet`** — 5,000-household master with demographics, loyalty segment, ethnicity
- **`household_transactions.parquet`** — 30,000 weekly HH purchases with `Switching_Flag` for the LA→Post switch
- **`acme.duckdb`** — single-file SQL DB with all six tables + seven seed tables loaded
- **Seeds**: SKU master (49), retailer master (26), geographies/DMAs (30), monthly POS, trade spend, marketing spend, Louisiana promo event log

### Encoded narrative facts

- Crunchwell LA share: ~6.0% (FY24) → ~3.9% (Q1 '26)
- Walmart Sept 2025 modular reset cuts Crunchwell Mega/Honey Nut Mega/Multigrain from 8 → 6 facings
- Hurricane Tonya (Nov 8, 2025) drops Crunchwell Mega OSA in LA from ~97% to ~67% for ~6 weeks
- Honey Bunches of Oats heavy promo at Rouses Q4 '25 → Q1 '26 (21% off, 6 weeks)
- LA Crunchwell-loyal HHs flagged switching to Honey Bunches starting Nov 2025

### Adapted from Kellogg ME reference set

- Geography: Middle East countries → US states + 30 DMAs
- Brands: Pringles/Corn Flakes → Acme's six brands + 8 competitors (Cheerios, Honey Bunches, Frosted Flakes, Quaker, Walmart Great Value PL, etc.)
- Calendar: Ramadan flag → BackToSchool / Holiday / Easter / SuperBowl seasonality enum
- Added: `Brand`, `Manufacturer`, `Ethnicity`, `Switching_Flag`, full competitor share breakouts on syndicated weekly
- Removed: Weetabix and Nestlé awareness (not US-relevant)
