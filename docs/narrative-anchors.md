# Narrative anchors — shared constants

The Acme synthetic data tells one coherent CPG story across **16 tables and 11 seed files**. A handful of constants are referenced in 5+ generators; if any of them changes, the others must change in lock-step or the narrative drifts.

If you're adding a new table, run `assert_consistency()` in `generator/generate.py` to confirm the LA decline narrative still reads correctly end-to-end.

---

## The five constants

| Constant | Value | Tables that depend on it |
|---|---|---|
| **Walmart cereal modular reset** | **2025-09-15** — Crunchwell Mega 8 → 6 facings; Cinnamon Twist deauthorized in some Walmart South stores | `perfect_store` (Facings), `sku_authorization` (Auth_Status for CR006), `competitor_launches` (LCH00007/08 — Great Value PL pickup) |
| **Hurricane Tonya landfall** | **2025-11-08** (recovery through 2025-12-15) | `perfect_store` (OSA_Pct), `shipments` (Fill_Rate_Pct, Cut_Reason='Storm'), `epos` (Honey Bunches substitution), `household_transactions` (Switching_Flag), `social_mentions` (supply-issue topic), `product_reviews` (lower ratings during OOS), `promo_events` (Recovery promo E006) |
| **Crunchwell LA share trajectory** | FY24 ~6.4% → Q1 2026 ~3.0% (-340 bps) | `syndicated_weekly` (Crunchwell_Value_Share), `plan_vs_actual` (Variance_Pct LA-DMA × Crunchwell), `brand_health` (LA wave taste/quality penalty), `social_mentions` (sentiment dip), `household_transactions` (Switching_Flag) |
| **Post Foods promo intensification at Rouses** | 2025-10-13 onward; 21% off Honey Bunches 14oz; 6 waves through Q1 2026 | `seeds/promo_events_louisiana.csv` (E001-E015 hand-curated), `epos` (LA Honey Bunches Yes/Yes promo), `perfect_store` (Honey Bunches at Rouses promo flag), `social_mentions` (Honey Bunches viral wave Q4 2025), `competitor_launches` (LCH00001 Honey Bunches Almond) |
| **Cinnamon Twist underperformer** | CR006, launched 2025-02-10 at 41% national ACV; lower review ratings; 39% authorization rate | `seeds/skus.csv` (status='Active-Underperform'), `perfect_store` (lower Facings at non-Walmart), `sku_authorization` (low Auth_Status), `product_reviews` (rating mean ~3.4 vs 4.3 for hero SKUs), `competitor_launches` (LCH00019 Acme launch tracker), `innovation_pipeline` (INV022 reformulation concept) |

---

## Cross-table assertions (run in `generator/generate.py`)

The generator runs three lightweight invariants before writing artifacts:

1. **LA Crunchwell Q1 2026 plan-vs-actual variance < -30%.** Confirms `plan_vs_actual` encodes the headline -45% shortfall.
2. **Hurricane Tonya storm-DC average fill rate < 75%.** Confirms `shipments` encodes the supply collapse.
3. **Cinnamon Twist (CR006) authorization rate between 30% and 55%.** Confirms `sku_authorization` encodes the void story.

Add new assertions when adding tables that depend on these anchors.

---

## What NOT to do

- **Do not "fix" the LA decline** by raising Crunchwell LA share in one table without raising it in all of them. The decline is a feature, not a bug — half the demo prompts depend on it.
- **Do not change the Hurricane Tonya date** without updating `docs/louisiana-decline.md` and `seeds/promo_events_louisiana.csv` (E005).
- **Do not delete or rename CR006.** The Cinnamon Twist underperformer story is hand-tuned across 5 tables.

---

## Provenance — which agency feeds which table

The new tables encode the data provenance Acme would actually have if these were real feeds. See `seeds/research_agencies.csv` for the full vendor master.

| Table | Primary "agency" / source |
|---|---|
| `epos` | Internal POS + NielsenIQ + IRI Circana |
| `perfect_store` | Walmart Luminate + Kroger 84.51 + internal store ops |
| `syndicated_weekly` | NielsenIQ syndicated POS |
| `brand_health` | Kantar Brand Tracker (bi-monthly waves) |
| `households` + `household_transactions` | Numerator HH panel |
| `plan_vs_actual` | SAP / Acme ERP (internal AOP and re-forecasts) |
| `sku_authorization` | SymphonyAI Retail + Walmart Luminate authorization audit |
| `shipments` | SAP outbound shipment + retailer DC receipt confirmations |
| `promo_events` | NielsenIQ promo lift modeling + retailer trade calendars |
| `competitor_launches` | Mintel GNPD + NielsenIQ Innovation Tracker + Walmart Luminate (PL) |
| `social_mentions` | Brandwatch (primary) + Sprout Social (owned-channel context) |
| `creator_posts` | Tribe Dynamics + CreatorIQ (paid activations) |
| `search_trends` | Spate (Google + TikTok) + Helium 10 (Amazon) + Google Trends free |
| `product_reviews` | Bazaarvoice (retailer.com) + PowerReviews (Walmart/Target) + Amazon Brand Analytics |
| `data_freshness_log` | Internal data ops monitoring |
