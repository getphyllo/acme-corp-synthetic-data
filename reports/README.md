# Acme Corp — Report Pack

A set of **10 realistic business documents** (PPTX / PDF / DOCX / XLSX) generated on top of the Acme
synthetic dataset. They exist so the Clayface demo and any document-ingestion / RAG / training pipelines
have **format-diverse, internally-consistent source material** to test against — the kind of files a CPG
insights team actually produces, every figure traceable to a table in this repo.

- **Focus:** Crunchwell (Louisiana Q1 2026 decline) and ProteinPeak (Q2 2026 launch).
- **Coverage:** strategy, planning, last-QBR numbers, and sales data.
- **Grounding:** every headline number is pulled from the parquet/seed tables or the canonical scenario
  docs. Nothing is invented. A verification script confirmed 13/13 anchor checks against `acme.duckdb`.
- **Generated:** 2026-06-25.

> All documents are marked **Internal · Confidential — Acme Corp synthetic demo data**. The data and the
> people in it are fictional.

---

## The 10 reports

| # | File | Format | Persona / owner | Type | Scenario |
|---|------|--------|-----------------|------|----------|
| 01 | `01-crunchwell-louisiana-q1-2026-business-review.pptx` | PPTX | Maya Chen → Diane Halverson | **Last QBR** | LA decline |
| 02 | `02-proteinpeak-q2-launch-week4-read.pptx` | PPTX | Maya Chen → Sage Park | **Last QBR / launch read** | PP launch |
| 03 | `03-kroger-q3-2026-jbr-pre-read.pptx` | PPTX | Priya Raman | **Planning / QBR** | Kroger JBR |
| 04 | `04-crunchwell-fy27-annual-brand-plan.pdf` | PDF | Cory Whitman | **Strategy** | Crunchwell FY27 |
| 05 | `05-q1-2026-retail-media-trade-effectiveness-cfo-read.pdf` | PDF | Tasha Brooks → CFO | **Strategy / finance** | Q1 spend read |
| 06 | `06-proteinpeak-q3-chocolate-almond-concept-test.pdf` | PDF | Maya Chen | **Planning / research** | Choc-Almond test |
| 07 | `07-proteinpeak-q2-launch-comms-creator-plan.docx` | DOCX | Renee Alvarez | **Planning** | PP launch comms |
| 08 | `08-walmart-august-2026-line-review-pre-read.docx` | DOCX | Marcus Boudreaux | **Planning** | Walmart line review |
| 09 | `09-crunchwell-louisiana-sales-data-pack.xlsx` | XLSX | Maya / Marcus | **Sales data** | LA decline |
| 10 | `10-proteinpeak-q2-launch-sales-data-pack.xlsx` | XLSX | Maya / Sage | **Sales data** | PP launch |

`charts/` holds the chart PNGs embedded in the decks and PDFs (kept as reusable image assets).

---

## What each report says (and where the numbers come from)

**01 · Crunchwell Louisiana Q1 2026 Business Review** — the defensive QBR. Crunchwell LA share −340 bps
(Q4'24 6.4% → Q1'26 3.0%), five-hypothesis attribution (Walmart reset ~55%, Larksfield ~20%, Hurricane
Tonya ~12%, Walmart PL ~8%, Hispanic shift ~5%), and the three-leg recovery plan.
*Source:* `syndicated_weekly`, `perfect_store`, `shipments`, `docs/louisiana-decline.md`.

**02 · ProteinPeak Q2 Week-4 Read** — trial vs plan (Target 110, Walmart-pilot 77), repeat 1.2× Berry
Crunch, source-of-volume 53/32/15, channel/retail-media GO-HOLD-PAUSE actions.
*Source:* `plan_vs_actual`, `perfect_store`, `household_transactions`, `proteinpeak_q2_launch`.

**03 · Kroger Q3 2026 JBR Pre-Read** — Larksfield +1.4 pts national / +2.1 pts South, Simple Truth +0.8
pts in protein, Crunchwell flat, 14.3% Crunchwell→Simple Truth switch, segment shifts at 2.3 pts/qtr.
*Source:* `kroger_simple_truth_switching`, `syndicated_weekly`.

**04 · Crunchwell FY27 Annual Brand Plan** — strategy. −2.1 pts category share over 6 quarters; relevance
down 5.9 pp (68.6 → 62.7) is the lead diagnostic while trust holds; price gap to Field & Honey 8% → 14%;
three-pillar plan.
*Source:* `brand_equity_quarterly`, `syndicated_weekly`, `skus.csv`, `competitor_launches`.

**05 · Q1 2026 Retail-Media & Trade-Promo Effectiveness (CFO read)** — $4.2M RM envelope returning $2.73M
incremental ($0.65 per $1); Amazon Ads drag (0.41 vs Walmart Connect 1.21); $11.6M trade envelope; LA
injection 2.2× ROI; H2 reallocation of $700K.
*Source:* `retail_media_spend_q1_2026`, `trade_promo_events_q1_2026`, `sku_elasticity_estimates`.

**06 · ProteinPeak Q3 Chocolate Almond Concept Test** — 64% top-two-box (clears the 55% standard);
cohort breakouts (protein-curious 71%); cannibalization gate passes (8 pp substitutional < 12 pp); F&H
chocolate competitive flag.
*Source:* `concept_test_chocolate_almond`, `ua_study_responses`, `competitor_launches` (LCH00032).

**07 · ProteinPeak Launch Comms & Creator Plan** — $6.4M envelope across creator / paid social / retail
media / sampling / PR; three tested claims; Sage Park creator cohort; 280K-HH sampling; 58/42 RM flight.
*Source:* `proteinpeak_q2_launch`, `concept_test_launch_claims_2026q2`, `creators.csv`, `marketing_spend`.

**08 · Walmart August 2026 Line-Review Pre-Read** — Marcus's ask for +2 facings + $340K Q3 injection;
velocity-per-facing +4%; the May 11 field walk (23 of 41 Supercenters with 3 Larksfield endcaps, 0 Acme);
projected +1.2 pts / $612K recovery.
*Source:* `walmart_endcap_audit_la`, `perfect_store`, `trade_promo_events_q1_2026` (TPE-Q1-011).

**09 · Crunchwell Louisiana Sales Data Pack** — 8 tabs: weekly LA share, the 340 bps decomposition,
EPOS by brand, perfect-store OSA/facings, the Houston-DC storm fill-rate collapse (to ~42%), the LA promo
calendar, and the Walmart endcap audit.
*Source:* `syndicated_weekly`, `epos`, `perfect_store`, `shipments`, `promo_events_louisiana`, `walmart_endcap_audit_la`.

**10 · ProteinPeak Q2 Launch Sales Data Pack** — 7 tabs: trial vs plan by retailer, velocity by banner,
source of volume, repeat curve, the launch calendar, and the retail-media plan + Q1 benchmarks.
*Source:* `plan_vs_actual`, `perfect_store`, `household_transactions`, `proteinpeak_q2_launch`, `retail_media_spend_q1_2026`.

---

## Notes on grounding

- Headline LA share figures (Q4'24 **6.4%** → Q1'26 **3.0%**) follow `docs/louisiana-decline.md`, which
  measures the Mass/Grocery peak-to-trough. The value-weighted all-channel cut in `syndicated_weekly` is
  milder (≈5.9% → ≈4.0%) but moves in the same direction — both are shown so the narrative and the raw
  table reconcile.
- A few planning-level splits (e.g. the $6.4M launch envelope by lever) are flagged as planning estimates
  in-document; the committed totals and all measured figures are table-grounded.
- Personas referenced: **Maya Chen** (analyst), **Marcus Boudreaux** (sales, South), **Diane Halverson**
  (VP Sales NA), **Priya Raman** (category), **Tasha Brooks** (eComm/retail media), plus secondary
  stakeholders Sage Park, Cory Whitman, Renee Alvarez, Hugo Lin, Helen Park-Choi and Tom Reilly.
