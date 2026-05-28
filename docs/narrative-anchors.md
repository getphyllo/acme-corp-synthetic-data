# Narrative anchors — shared constants

The Acme synthetic data tells **eleven coherent CPG stories** — five anchored to Sales / Category / Insights (Louisiana decline, ProteinPeak Q2 launch, Walmart Aug line review, Kroger JBR, Q1 retail-media effectiveness) and **six anchored to Marketing / Insights v2** (Crunchwell FY27 brand plan, ProteinPeak launch comms, Target back-to-school, Q3 SOTB, Chocolate Almond extension, LA-DMA diagnostic) — across **22 parquet tables and 31 seed files**. A handful of constants per scenario are referenced in 5+ generators; if any of them changes, the others must change in lock-step or the narrative drifts.

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

## Scenario 3 — Walmart August 2026 Line-Review Prep (Marcus-anchored)

| Constant | Value | Tables that depend on it |
|---|---|---|
| **Walmart August line review** | **2026-08-10** (line review date, ~12 weeks out from May 18, 2026 kickoff) | `seeds/walmart_endcap_audit_la.csv`, narrative folder `walmart-aug-line-review-story-v1/` |
| **Crunchwell South Division velocity-per-facing post-Sept-reset** | **+4%** (vs Sept 2025 baseline); facings down 25% (8 → 6 → 4 effective in LA); total category contribution down 22% | `perfect_store` (Facings × Sales_Units), `syndicated_weekly` (velocity decomposition) |
| **Larksfield 3-endcap pattern in LA Walmart Supercenters** | **23 of 41 LA Walmart Supercenters** have 3 Larksfield endcaps as of May 11, 2026 (Field & Honey 14oz, Field & Honey Almond, Harvest Hearth) | `seeds/walmart_endcap_audit_la.csv` (62 audit rows; 41 Supercenters; 23 with 3 endcaps) |
| **Marcus's August ask** | Recover **2 facings** on Crunchwell Mega and Honey Nut Mega at Walmart with a **$340K Q3 trade injection** to support the runway | `seeds/trade_promo_events_q1_2026.csv` (LA tactical injection precedent — TPE-Q1-011); `walmart-aug-line-review-story-v1/` |
| **Net expected impact** | **1.2 share points** of recovery in the South Division; **$612K** incremental revenue (per LA injection precedent) | `seeds/trade_promo_events_q1_2026.csv` TPE-Q1-011; `sku_elasticity_estimates` (CR002/CR004 Walmart) |
| **Related cross-flags from Insights tab** | Cinnamon Twist (CR006) delisting risk at H-E-B; Rouses Mega OOS at 8 doors; Larksfield endcap pattern across LA-DMA | `seeds/heb_cinnamon_twist_delist_risk.csv`, `seeds/rouses_oos_by_door.csv`, `seeds/walmart_endcap_audit_la.csv` |

---

## Scenario 4 — Kroger Q3 2026 JBR Pre-Read (Priya-anchored)

| Constant | Value | Tables that depend on it |
|---|---|---|
| **Kroger Q3 JBR** | **2026-07-08** (JBR date); pre-read due **2026-06-24**; shipped **2026-06-20** in the with-Clayface arc | `kroger-q3-jbr-story-v1/`, scenario narrative |
| **Larksfield Field & Honey at Kroger** | **+1.4 pts share nationally, +2.1 pts in the South** vs last JBR | `seeds/kroger_simple_truth_switching.csv` KST-LARK-NATIONAL / KST-LARK-SOUTH; `syndicated_weekly` (Larksfield_Value_Share × Kroger DMA cuts) |
| **Simple Truth (Kroger PL) gain** | **+0.8 pts** across the protein segment | `seeds/kroger_simple_truth_switching.csv` KST-ST-PROTEIN |
| **Crunchwell at Kroger** | **Flat** vs last JBR | `seeds/kroger_simple_truth_switching.csv` KST-CW-FLAT |
| **Segment shifts pulling from traditional family cereal** | **Protein-forward, Sugar-reduced, Ancient-grain** segments each pulling at **~2.3% per quarter** | `seeds/kroger_simple_truth_switching.csv` KST-SEGMENT-PF/SR/AG |
| **Crunchwell → Simple Truth switching study** | **14% of Crunchwell lapsed Kroger buyers** went to Simple Truth in Q1 2026 (national, all segments) | `seeds/kroger_simple_truth_switching.csv` KST-NATIONAL |
| **Pre-read deliverable** | **12-page** deck draft + recommendation framework (last 3 slides) | Narrative folder only |

---

## Scenario 5 — Q1 2026 Retail-Media & Trade-Promo Effectiveness Read (Tasha-anchored)

| Constant | Value | Tables that depend on it |
|---|---|---|
| **CFO half-day session** | **2026-06-04** (Helen Park-Choi); attendees Helen, Nathan, Marian, Audrey, Tasha, Marcus Yu, Robert Kim | `q1-spend-effectiveness-story-v1/` |
| **Q1 2026 retail-media envelope** | **$4.2M total** across four platforms | `seeds/retail_media_spend_q1_2026.csv` (24 rows; sums to $4,200K) |
| **Q1 2026 trade-promo envelope** | **$11.6M total** across all retailers; includes Marcus's LA tactical injection | `seeds/trade_promo_events_q1_2026.csv` (43 rows; sums to $11,600K) |
| **Q1 retail-media incrementality decomposition** | **$2.7M incremental revenue / $1.1M cannibalization / $0.4M undetermined** within confidence band | `seeds/retail_media_spend_q1_2026.csv` (sum of incremental_revenue_kusd / cannibalized_base_kusd / undetermined_kusd) |
| **Blended incrementality ratio** | **$0.64** of incremental revenue per $1 spent | `seeds/retail_media_spend_q1_2026.csv` (sum incr / sum spend) |
| **Per-platform incrementality ratios** | **Walmart Connect $1.20** / **Amazon Ads $0.41** / **Kroger Precision Marketing $0.79** / **Target Roundel $0.55** | `seeds/retail_media_spend_q1_2026.csv` (modeled_incrementality_ratio × spend per platform) |
| **LA tactical injection** | **$280K spend → 1.1 pts share recovery** (vs 1.2-pt model expectation) → **$612K incremental revenue** → 2.2× incremental ROI | `seeds/trade_promo_events_q1_2026.csv` TPE-Q1-011 |
| **H2 reallocation recommendation** | **Pull $700K from Amazon Ads, push into Walmart Connect + Kroger Precision** | `seeds/retail_media_spend_q1_2026.csv` (Amazon Ads ratio $0.41 vs the two stronger platforms) |
| **Value-destroying trade-promo cluster** | **3 Mountain West events in Q1** with negative incrementality (TPE-Q1-018/019/020) | `seeds/trade_promo_events_q1_2026.csv` (dma_focus='Mountain West' rows) |
| **ProteinPeak vs Crunchwell retail-media outperformance** | **2.3× at the SKU level** (PP003 Berry Crunch vs CR002 Original Mega on Amazon Ads at compatible bid CPCs) | `seeds/retail_media_spend_q1_2026.csv` (ProteinPeak Amazon Ads $0.44 ratio vs Crunchwell Amazon Ads $0.41 ratio at portfolio level; the 2.3× is the per-SKU pair efficiency, documented in scenario narrative) |
| **Marian's elasticity model** | Last refreshed **2026-04-15**; used as the gate for Tasha's incrementality numbers in the CFO read | `seeds/sku_elasticity_estimates.csv` (last_recalibrated=2026-04-15); `data_freshness_log.parquet` |

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

**Walmart August line-review prep (Scenario 3)**

12. `seeds/walmart_endcap_audit_la.csv` has **≥23 LA Walmart Supercenters with `larksfield_endcap_count >= 3`** as of audit_date='2026-05-11'. Confirms the "23 of 41" anchor in Marcus's pre-read.
13. `seeds/walmart_endcap_audit_la.csv` has **0 rows with `acme_endcap_count >= 1`** as of audit_date='2026-05-11' (zero Acme endcaps captured in the May field walk). Confirms the "we are losing real estate" narrative.

**Kroger Q3 JBR pre-read (Scenario 4)**

14. `seeds/kroger_simple_truth_switching.csv` KST-NATIONAL row has `switch_rate_pct = 14.3` (within ±0.5pp of 14%). Confirms the Crunchwell-lapsed → Simple Truth headline in Priya's pre-read.
15. `seeds/kroger_simple_truth_switching.csv` KST-LARK-NATIONAL row has `share_pt_shift = 1.40` AND KST-LARK-SOUTH has `share_pt_shift = 2.10`. Confirms the +1.4 / +2.1 anchor.
16. `seeds/kroger_simple_truth_switching.csv` has three segment-shift rows (KST-SEGMENT-PF, KST-SEGMENT-SR, KST-SEGMENT-AG), each with `share_pt_shift = 2.30`. Confirms the 2.3%/quarter segment anchor.

**Q1 retail-media & trade-promo effectiveness (Scenario 5)**

17. `seeds/retail_media_spend_q1_2026.csv` total `spend_kusd` = **$4,200K ± 1%** (the $4.2M envelope). Confirms the envelope anchor.
18. `seeds/retail_media_spend_q1_2026.csv` total `incremental_revenue_kusd` between **$2,650K and $2,750K** (the $2.7M anchor). Confirms the blended incrementality story.
19. `seeds/retail_media_spend_q1_2026.csv` per-platform incrementality ratios: **Walmart Connect = 1.20 ± 0.02**, **Amazon Ads = 0.41 ± 0.02**, **Kroger Precision = 0.79 ± 0.02**, **Target Roundel = 0.55 ± 0.02**. Confirms the per-platform anchors.
20. `seeds/trade_promo_events_q1_2026.csv` total `spend_kusd` = **$11,600K ± 1%** (the $11.6M trade-promo envelope). Confirms Tasha's CFO deck anchor.
21. `seeds/trade_promo_events_q1_2026.csv` row TPE-Q1-011 has `spend_kusd = 280` AND `incremental_revenue_kusd = 612` (LA tactical injection landed close to plan). Confirms Marcus's recovery story.
22. `seeds/trade_promo_events_q1_2026.csv` has **exactly 3 rows** with `dma_focus = 'Mountain West'` AND negative `modeled_incrementality_index`. Confirms Tasha's value-destroying cluster.

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

---

## Scenarios 6–11 — Marketing & Insights v2 (added v0.7.0)

Six new scenarios anchored to the **Marketing & Insights persona pack** (`clayface-workspace/03-research/acme/11-scenarios/v2/`). Each one runs on the v2 cohort frame plus the new Kantar / Ipsos / Numerator tables.

### Shared v2 cohort frame (used across S6–S11)

The four-cohort frame from the April 2026 U&A becomes the **canonical Insights-wide cohort definition** in v0.7.0:

| Cohort | What it is | n in U&A | Headline |
|---|---|---:|---|
| `cereal-skipper` | Households skipping cereal 3+ mornings/wk; swap-out behavior | 672 | Out of the category; recoverable with protein offer |
| `protein-returner` | Swap-out households who came back via protein cereal | 540 | Driving the +11.4% protein-segment growth |
| `loyal-family` | The steady core; slightly declining frequency | 768 | Slight price sensitivity but steady |
| `price-shopper` | Moving to private label; concentrated South + Mountain West | 420 | The Great Value / Simple Truth pickup |

**Hard rule:** the cereal-skipper cell-size limit is n=672 — segment-level reads OK, regional DMA cuts NOT OK. Workspace tiles must expose this constraint.

### Scenario 6 — Crunchwell FY27 annual brand plan (Cory Whitman)

| Constant | Value | Tables that depend on it |
|---|---|---|
| **Crunchwell category share loss** | -2.1 points over six quarters (FY25Q1 → FY26Q2) | `brand_equity_quarterly` (Relevance and Modernity trends), `syndicated_weekly` (national share trend), `kantar_worldpanel_cohort` |
| **Loss decomposition** | -1.3 Field & Honey / -0.6 private label / -0.2 other branded | `competitor_launches` (LF-FHA-14, PL-GVHA-14, etc.) |
| **Trust ~flat over 6 quarters** | 72.3 → 72.9 at US-NAT for Crunchwell | `brand_equity_quarterly` |
| **Relevance down 6pp** | 68.6 → 62.7 at US-NAT for Crunchwell | `brand_equity_quarterly` (the lead diagnostic for Cory's platform) |
| **Crunchwell vs Field & Honey price gap** | 8% (FY24Q4) → 14% (FY26Q2) on a per-ounce basis at Walmart Mega | `epos`, `perfect_store` |

### Scenario 7 — ProteinPeak launch comms & creator plan (Renee Alvarez)

| Constant | Value | Tables that depend on it |
|---|---|---|
| **Launch envelope** | $6.4M across creator, paid social, retail media, sampling, PR | `seeds/proteinpeak_q2_launch.csv`, `creator_posts`, `marketing_spend` |
| **Field & Honey 14g protein extension launch** | **LCH00032 / 2026-05-12** at 612 stores; narrows ProteinPeak protein delta from 11g → 6g | `competitor_launches` (new row), `concept_tests` (CL1 competitive flag) |
| **Three claims tested** | "20g protein, less sugar" / "Clean fuel, real grains, no fillers" / "Eat like you mean it" | `concept_tests` (Test_ID=CT_LAUNCH_CLAIMS_2026Q2) |
| **Sampling cohort** | 280K Numerator HHs — protein-segment buyers, never-Crunchwell | derivable from `households` × `household_transactions` |
| **Retail media flight** | 58% to Walmart Connect + Amazon, 42% to Kroger Precision + Target Roundel | `marketing_spend`, `retail_media_spend_q1_2026` |

### Scenario 8 — Target back-to-school 2026 (Wes Okafor)

| Constant | Value | Tables that depend on it |
|---|---|---|
| **2025 Target BTS incremental** | **$14.2M category dollars** (table shows $14.4M, within ±1.5%) | `numerator_bts_occasion` |
| **Mechanic decomposition** | Endcap 62% / Circular 21% / Roundel 12% / Cartwheel 5% | (qualitative anchor in CHANGELOG) |
| **Velocity per door** | Crunchwell Mega 1.42× baseline through 2025 program window | `perfect_store` Target stores |
| **Target × ProteinPeak cohort overlap** | **64.7% — highest of any major retailer** | `numerator_bts_occasion` (Protein_Curious_Cohort_Overlap) |
| **Target Circle overlay** | ~70% of Target BTS shoppers are Target Circle members | `numerator_bts_occasion` (Target_Circle_Membership_Overlap) |
| **2026 velocity-per-door commits** | ProteinPeak 1.38× baseline, Crunchwell Mega 1.45× baseline | Cross-referenced with `sku_elasticity_estimates` |
| **Cinnamon Twist Cartwheel** | Destroyed value in 2025 — do not repeat in 2026 | Internal v0.7.0 narrative; surfaced as anti-pattern |

### Scenario 9 — Q3 SOTB read (Nina Ortega)

| Constant | Value | Tables that depend on it |
|---|---|---|
| **NielsenIQ — cereal category** | +2.1% dollars, units flat, price-mix +2.0%, protein segment +11.4%, family cereal -1.2% | `syndicated_weekly` |
| **Kantar — household penetration** | -60bps overall; protein vs family-cereal buyer 38% overlap | `kantar_worldpanel_cohort` |
| **U&A — breakfast fragmentation** | **28% of HHs skip cereal 3+ mornings/wk**; 64% cite protein as swap driver | `ua_study_responses`, `ua_qual_pointers` |
| **Data-hierarchy ordering** | Behavior leads (U&A) → Panel follows (Kantar) → Till trails (Nielsen) | Workspace canvas enforces — not a table-level rule |

### Scenario 10 — ProteinPeak Q3 Chocolate Almond concept test (Maya Chen)

| Constant | Value | Tables that depend on it |
|---|---|---|
| **Field period** | 2026-06-22 to 2026-07-11; n=1,000 | `concept_tests` (Test_ID=CT_CHOC_ALMOND_2026Q3) |
| **Top-two-box purchase intent** | **64%** (clears 55% action standard; +6pp over launch SKU pre-test) | `concept_tests` |
| **Cohort breakouts** | protein-curious 71%, lapsed-cereal 66%, current-Crunchwell 52% | `concept_tests` |
| **Cannibalization gate** | 22% overlap → 14pp additive + 8pp substitutional; **clears 12pp steerco threshold** | `concept_tests` |
| **U&A overlay** | Chocolate-as-breakfast-flavor preference +14pp above category avg in protein-curious cohort | `ua_study_responses` (Chocolate_Breakfast_Pref by Cohort) |
| **F&H competitive flag** | Field & Honey Chocolate Crunch trademark filed 2026-04-22 → likely Q4 launch | `competitor_launches` LCH00032 notes |

### Scenario 11 — LA-DMA share decline diagnostic (Jordan Hsu)

| Constant | Value | Tables that depend on it |
|---|---|---|
| **Share loss** | -3.1 points of cereal category share in LA-DMA over 8 weeks vs flat national | `syndicated_weekly` |
| **Decomposition** | -1.4 velocity / -0.9 facings / -0.6 price gap / -0.2 mix | `perfect_store`, `epos`, `syndicated_weekly` |
| **Cohort losses** | Baton Rouge families with kids 5–14 -19% frequency (71% went to Field & Honey); protein-curious -26% frequency (out of category) | `kantar_worldpanel_cohort`, `household_transactions` |
| **Leading-indicator DMAs** | **BIR-DMA + MEM-DMA** — both showing early-stage LA pattern | `syndicated_weekly`, `geographies.csv` (new rows) |
| **Response plan invest** | $740K total → 1.8 points of recovery over 12 weeks (modeled) | Cross-referenced with `sku_elasticity_estimates` |

