# Week-4 Read Deck — Outline (Maya → Sage → Audrey → Whitfield)

The deck Maya would have spent ~22 hours building by hand. Clayface produces it in ~1 hour of human-in-the-loop review. This file is the canonical structure both versions converge on.

**Audience:** Sage Park (primary) → Audrey Vance, Hugo Lin, Helen Park-Choi, Gregory Whitfield (Tuesday May 26 business review).

**Length:** 4 slides + appendix. Maya's classic "one chart per question" discipline.

**Delivery format:** PPTX, Acme template. Maya's name on slide 0. Sourced from `epos`, `perfect_store`, `household_transactions`, `plan_vs_actual`, `social_mentions`, `creator_posts`, `marketing_spend.csv`, `promo_events`.

---

## Slide 0 — Title + executive summary

**Title:** *ProteinPeak Q2 Launch — Week-4 Read (May 18, 2026)*

**One-line so-what:** *Cinnamon Crunch and Cocoa Almond are landing — strong at Target, soft at Walmart-pilot, cannibalization bounded. Recommended action: hold Amazon spend, lean into Target endcap renewal, deprioritize Walmart-pilot expansion.*

**Key numbers (top-right card):**
- Trial: **+13% over plan** at Target / **-22% under plan** at Walmart-pilot
- Repeat (W2): **1.2× Berry Crunch** at the same week-since-launch
- Cannibalization of PP001: **~6% steady-state** (bounded)
- $$ retail-media (Hugo): **$1.2M of $4.2M spent through Week 4** — pacing on plan

---

## Slide 1 — Trial vs plan, by channel

**Chart:** Vertical bar chart, x-axis = retailer (Target, Walmart, Amazon, Whole Foods, Sprouts, Kroger), y-axis = trial index (100 = plan). Reference line at 100. Color: green ≥ 100, amber 80–99, red < 80.

**Data:** `plan_vs_actual` × `perfect_store`, post-2026-04-20, PP005 + PP006 combined.

**Caption:**
> *"Target endcap is the engine. The launch is on plan in Amazon and slightly above in WFM/Sprouts. The Walmart-pilot is well below plan — premium-protein cereal needs an endcap signal at Walmart to land, and the pilot didn't include endcap support."*

**Confidence band:** ±4% on Target (4 weeks of data, n=270 store-weeks); ±9% on Walmart (smaller pilot footprint, n=110 store-weeks).

---

## Slide 2 — Repeat curve vs Berry Crunch

**Chart:** Two-line overlay. X-axis = weeks-since-launch (0, 1, 2, 3, 4). Y-axis = cumulative repeat rate (% of W1 buyers who buy again within the window). Lines: PP005 Cinnamon Crunch (Acme accent), PP003 Berry Crunch (gray reference at same weeks-since-launch in 2023).

**Data:** `household_transactions` HH-level repeat-buyer logic; see SQL in `03-hypothesis-tree.md::H2`.

**Caption:**
> *"At Week 2, Cinnamon Crunch repeat sits at 1.2× Berry Crunch. Cocoa Almond is tracking slightly below (1.05×) but still positive. The historical archive comparison is the unlock — Berry Crunch's W2 number was buried in three quarters of Numerator exports nobody had stitched."*

**Confidence overlay:** Lighter shaded band shows ±1 SD on each line.

---

## Slide 3 — Source-of-volume waterfall + PP001 cannibalization

**Chart:** Horizontal waterfall. Starting bar = PP005 + PP006 incremental household buys. Decomposition: New-To-Brand (53%) → Cannibalization (32% from PP001) → Competitor Switch (15% from Magic Spoon / Three Wishes / Catalina). Below: PP001 velocity dip = -11% W1, -6% W2-4.

**Data:** `household_transactions.Switching_Flag` + `perfect_store` PP001 velocity.

**Caption:**
> *"~53% of buyers are net-new to ProteinPeak — the launch is doing what it should. The 32% from PP001 is bounded at ~6% steady-state cannibalization, which is ~$1.5M of pulled-forward demand on a $25M franchise SKU. Net of cannibalization, the launch is +$22M incremental on plan for FY26 — well above the $14M + $10M = $24M plan."*

**Risk note:** *"If cannibalization widens to 12%+ by Week 8 (the historical pattern for protein launches that lack flavor differentiation), revisit the stage-gate decision on the next two flavors."*

---

## Slide 4 — Channel mix + retail-media response

**Chart:** Bubble chart. X-axis = Q2 retail-media spend ($M). Y-axis = trial index (=plan). Bubble size = weeks-of-supply remaining. One bubble per retailer.

**Data:** `marketing_spend.csv` Q2 ProteinPeak rows + `plan_vs_actual` + `shipments` weeks-of-supply.

**Annotations:**
- Target Roundel: $1.8M spent, trial 113%, 6 wks supply — **GO** (recommend endcap renewal)
- Amazon Ads: $1.4M spent, trial 102%, 4 wks supply — **HOLD** (already at plan)
- Walmart Connect: $500K spent, trial 78%, 9 wks supply — **PAUSE** (allocate elsewhere)
- Sprouts Brand+: $250K spent, trial 108%, 5 wks supply — **GO** (small spend, high ROAS)

**Caption:**
> *"$1.2M of the $4.2M Q2 retail-media budget is committed; recommended re-allocation reroutes the $700K Walmart Connect plan toward Target Roundel renewal and a small Whole Foods endcap test. Sage cohort creator-driven sentiment is +0.47 (Brandwatch). Hugo to confirm Tasha Brooks' Pacvue pacing supports the re-route."*

---

## Appendix slides (Maya keeps for back-pocket questions)

- **A1 — SKU-level trial-vs-plan**: PP005 vs PP006 individually (PP005 stronger; PP006 needs Q3 push).
- **A2 — Geographic concentration**: PP005/PP006 trial by DMA (NYC, LAX, CHI, BOS lead; Southeast trails — opportunity for Q3 Target endcap renewal in Southeast cluster).
- **A3 — Brandwatch / creator detail**: Sage Park anchor creator (CR-0012 @sage_park_athlete) drives top attributed lift, followed by CR-0007 @gymrat.miles.
- **A4 — Confidence interval methodology**: Why the Week-4 read is a Week-4 read and not a Week-2 read (statistical power on the repeat curve).
- **A5 — Sell-in vs sell-through**: Shipments outpaced sell-through in Walmart Week 1 (allocation pull; weeks-of-supply ballooned to 9 weeks); on track everywhere else.

---

## Cross-references

- Data is sourced from the parquet files in `data/`. See [`02-launch-data-model.md`](./02-launch-data-model.md) for the encoding map.
- Hypothesis evidence and SQL queries: [`03-hypothesis-tree.md`](./03-hypothesis-tree.md).
- Audit queries to verify the data is consistent before the deck goes out: [`06-audit-checklist.md`](./06-audit-checklist.md).
