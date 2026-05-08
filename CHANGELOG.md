# Changelog

All notable changes to this dataset are tracked here. The repo follows [Semantic Versioning](https://semver.org/) — major bumps are breaking schema changes, minor bumps add tables/columns, patch bumps fix data without changing schema.

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
