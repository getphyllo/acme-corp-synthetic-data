# Narrative anchors — shared constants

The Acme synthetic data tells two coherent CPG stories — the **Louisiana Cereal Decline (Q1 2026)** and the **ProteinPeak Q2 2026 Launch Read** — across **16 tables and 13 seed files**. A handful of constants per scenario are referenced in 5+ generators; if any of them changes, the others must change in lock-step or the narrative drifts.

If you're adding a new table, run `assert_consistency()` in `generator/generate.py` to confirm both scenarios still read correctly end-to-end.

---

## Scenario 1 — Louisiana Cereal Decline (Q1 2026)

| Constant | Value | Tables that depend on it |
|---|---|---|
| **Walmart cereal modular reset** | **2025-09-15** — Crunchwell Mega 8 → 6 facings; Cinnamon Twist deauthorized in some Walmart South stores | `perfect_store` (Facings), `sku_authorization` (Auth_Status for CR006), `competitor_launches` (LCH00007/08 — Great Value PL pickup) |
| **Hurricane Tonya landfall** | **2025-11-08** (recovery through 2025-12-15) | `perfect_store` (OSA_Pct), `shipments` (Fill_Rate_Pct, Cut_Reason='Storm'), `epos` (Field & Honey substitution), `household_transactions` (Switching_Flag='Yes'), `social_mentions` (supply-issue topic), `product_reviews` (lower ratings during OOS), `promo_events` (Recovery promo E006) |
| **Crunchwell LA share trajectory** | FY24 ~6.4% → Q1 2026 ~3.0% (-340 bps) | `syndicated_weekly` (Crunchwell_Value_Share), `plan_vs_actual` (Variance_Pct LA-DMA × Crunchwell), `brand_health` (LA wave taste/quality penalty), `social_mentions` (sentiment dip), `household_transactions` (Switching_Flag) |
| **Larksfield Foods promo intensification at Rouses** | 2025-10-13 onward; 21% off Field & Honey 14oz; 6 waves through Q1 2026 | `seeds/promo_events_louisiana.csv` (E001-E017 hand-curated), `epos` (LA Field & Honey Yes/Yes promo), `perfect_store` (Field & Honey at Rouses promo flag), `social_mentions` (Field & Honey viral wave Q4 2025), `competitor_launches` (LCH00001 Field & Honey Almond) |
| **Cinnamon Twist underperformer** | CR006, launched 2025-02-10 at 41% national ACV; lower review ratings; 39% authorization rate | `seeds/skus.csv` (status='Active-Underperform'), `perfect_store` (lower Facings at non-Walmart), `sku_authorization` (low Auth_Status), `product_reviews` (rating mean ~3.4 vs 4.3 for hero SKUs), `competitor_launches` (LCH00019 Acme launch tracker), `innovation_pipeline` (INV022 reformulation concept) |

---

## Scenario 2 — ProteinPeak Q2 2026 Launch Read

| Constant | Value | Tables that depend on it |
|---|---|---|
| **ProteinPeak Cinnamon Crunch launch** | **PP005 launched 2026-04-20** at 38% ACV (Target+WFM+Sprouts+Amazon+Walmart-pilot+Kroger) | `seeds/skus.csv`, `competitor_launches` (LCH00021), `epos`, `perfect_store` (launch oversample), `sku_authorization` (2026-04-30 snapshot), `shipments`, `social_mentions`, `creator_posts`, `search_trends`, `product_reviews`, `household_transactions`, `plan_vs_actual` |
| **ProteinPeak Cocoa Almond co-launch** | **PP006 launched 2026-04-20** (Target+WFM+Sprouts+Amazon+Kroger) | Same as PP005; `competitor_launches` LCH00031 |
| **Target endcap channel performance** | Trial 113% of plan at Target; 78% at Walmart-pilot; ~100% Amazon; ~108% WFM/Sprouts | `perfect_store` (Sales_Units by Banner), `epos`, `plan_vs_actual` (variance by Retailer × Period 2026-04/05), `seeds/proteinpeak_q2_launch.csv` (PP-E003/E004 Target endcap events) |
| **Repeat curve vs Berry Crunch** | Week-2 repeat for PP005 ≈ **1.2× PP003 Berry Crunch** at same week-since-launch | `household_transactions` (repeat-purchase density by Product_SKU × weeks-since-launch), `product_reviews` (rating ≈ 4.6 vs PP003 ≈ 4.4) |
| **Cannibalization of PP001 Vanilla Almond Original** | PP001 velocity -11% W1, -6% steady-state W2-4 at launch retailers | `perfect_store` (PP001 velocity multiplier at Target/Amazon/WFM/Sprouts/Kroger post-2026-04-20), `household_transactions` (Switching_Flag='Cannibalization' ~32% of PP005/PP006 buys) |
| **Source-of-volume distribution** | ~53% New_To_Brand, ~32% Cannibalization, ~15% Competitor_Switch | `household_transactions.Switching_Flag` extended taxonomy; dedicated launch oversample of ~800 rows |
| **$4.2M Q2 retail-media budget (Hugo Lin)** | Pacvue-orchestrated; allocated Target Roundel + Amazon Ads + Walmart Connect + Sprouts Brand+ | `seeds/marketing_spend.csv` (2026-Q2 ProteinPeak rows), `seeds/proteinpeak_q2_launch.csv` PP-E014, `seeds/trade_spend_fy25.csv` |
| **Sage Park athlete cohort** | Anchor CR-0012 + cohort 2 (CR-0007 / CR-0021 / CR-0040 / CR-0042 / CR-0013 / CR-0027) | `seeds/creators.csv` (Active-Q2-2026 status), `creator_posts` (boosted attribution + ProteinPeak-skewed brand selection post-launch), `social_mentions` (creator-drop topic) |
| **Week-4 read milestone** | Friday 2026-05-22 (deck due) / Tuesday 2026-05-26 (Whitfield business review) | `seeds/proteinpeak_q2_launch.csv` PP-E015, `docs/proteinpeak-q2-launch/04-week4-read-deck-outline.md` |

---

## Cross-table assertions (run in `generator/generate.py`)

The generator runs ten lightweight invariants before writing artifacts:

**Louisiana decline (Scenario 1)**
1. LA Crunchwell Q1 2026 plan-vs-actual variance < -30%. Confirms `plan_vs_actual` encodes the headline -45% shortfall.
2. Hurricane Tonya storm-DC average fill rate < 75%. Confirms `shipments` encodes the supply collapse.
3. Cinnamon Twist (CR006) authorization rate between 30% and 55%. Confirms `sku_authorization` encodes the void story.
4. LA Crunchwell social sentiment Q4'25-Q1'26 < -0.10. Confirms `social_mentions` encodes the sentiment dip.
5. Cinnamon Twist (CR006) average review rating < hero SKUs by ≥ 0.5. Confirms `product_reviews` encodes the underperformer signal.

**ProteinPeak Q2 launch (Scenario 2)**
6. PP005/PP006 Target velocity > Walmart velocity (perfect_store post-2026-04-20). Confirms the channel-split story.
7. PP001 post-launch velocity ≤ pre-launch × 1.02. Confirms cannibalization.
8. PP005/PP006 authorization = 0 before 2026-04-30 snapshot. Confirms launch gating.
9. ProteinPeak Target variance > Walmart variance (plan_vs_actual 2026-04/05). Confirms over/under-trial split.
10. ProteinPeak post-launch social sentiment > +0.10 with > 50 mentions. Confirms positive launch buzz.
11. `Switching_Flag = 'New_To_Brand'` count exceeds `'Cannibalization'` count among PP005/PP006 buys. Confirms source-of-volume waterfall.

Add new assertions when adding tables that depend on either set of anchors.

---

## What NOT to do

- **Do not "fix" the LA decline** by raising Crunchwell LA share in one table without raising it in all of them. The decline is a feature, not a bug — half the demo prompts depend on it.
- **Do not change the Hurricane Tonya date** without updating `docs/louisiana-decline.md` and `seeds/promo_events_louisiana.csv` (E005).
- **Do not delete or rename CR006.** The Cinnamon Twist underperformer story is hand-tuned across 5 tables.
- **Do not change the ProteinPeak Q2 launch date** without updating `docs/proteinpeak-q2-launch/`, `seeds/proteinpeak_q2_launch.csv`, `seeds/competitor_launches.csv` (LCH00021/LCH00031), `seeds/skus.csv`, and `seeds/innovation_pipeline.csv` (INV003/INV004).
- **Do not delete or rename PP005/PP006.** Both launch SKUs are hand-tuned across 12 tables and the assertion suite will fail if either disappears.
- **Do not rename PP001 back to "ProteinPeak Original" without renaming it everywhere.** The cannibalization narrative reads "ProteinPeak Vanilla Almond Original" because the Q2 launch scenario calls it that explicitly.

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
