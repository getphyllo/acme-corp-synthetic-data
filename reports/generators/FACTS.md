# Acme grounding facts — v0.7.0 dataset (for report authoring)

**Golden rule:** every headline number in a report must trace to this sheet, to
`acme.duckdb`, or to a `seeds/*.csv`. Where a number is a planning assumption
(a forward split, an FY27+ target), label it in-document as *"planning estimate"*
or *"target"*. Do NOT invent measured history.

Data window: history runs Jan 2024 → **31 May 2026** (Q2 FY26 is partial, through
~W22). "Today" for these docs is early **July 2026**. So:
- **Past two quarters** = Q1 FY26 (complete) + Q2 FY26 (actuals through May, launch read).
- **Next two quarters** = Q3 FY26 (Jul–Sep) + Q4 FY26 (Oct–Dec) — forward/plan.
- **3-year strategic** = FY27, FY28, FY29 — targets/commitments.

## Company
- FY25 net revenue **$812M** (+5.1% YoY). EBITDA margin **14.2%**, target **16% by FY28**.
- HQ Battle Creek MI; founded 1952; CEO Gregory Whitfield (since 2020). #4 US RTE cereal.
- Monthly plan FY26 = **$63.7M/mo** ($764M annualized run-rate at plan). Actuals:
  - 2026-01/02/03 ≈ $60.4/60.3/60.4M (**−5.2%**); 2026-04 $61.5M (−3.5%); 2026-05 $61.6M (−3.4%).
  - **Q1 FY26 total: $181.1M actual vs $191.2M plan = −5.3%.** Trajectory improving.

## Brands (FY25 revenue, from seeds/skus.csv)
| Brand | FY25 $M | SKUs | Units M | Note |
|---|---|---|---|---|
| Crunchwell | 312.0 | 8 | 65.2 | Flagship, Family Sweet; LA problem |
| TrailGrove | 152.0 | 10 | 24.4 | Granola/bars, healthy |
| MorningOats | 87–98 | 8 | 23.1 | Hot cereal/oats |
| HoneyNest | 94.0 | 12 | 20.7 | Kids sweet (declining segment) |
| RootDay | 62.0 | 8 | 12.3 | Oat milk (acq. 2023) |
| ProteinPeak | 48.0 | 6 | 6.1 | Wellness protein, +24.6%, launch engine |

## Brand plan-vs-actual, monthly FY26 (plan_vs_actual, $M/mo plan → var%)
- Crunchwell: plan $25.19M/mo, actual ~$23.7M, **−5.7 to −6.0%** every month.
- ProteinPeak: plan $5.80M/mo; Jan–Mar actual ~$4.33M (**−25.4%**, pre-launch); Apr–May ~$5.44M (**−6.1%**, post-launch).
- HoneyNest −1.1%; MorningOats −1.1%; RootDay −0.3%; TrailGrove −1.6%. (all "on track")

## Share (syndicated_weekly, RTE Cereal, value share %, quarterly avg)
National (ex-LA): Acme all-brand ~**7.86 → 8.09**; Crunchwell ~**6.0 flat**; Larksfield ~**14.0**; PL ~**10.0**.
Louisiana DMA: Acme 8.05 (25Q2) → **5.80 (26Q1)** → 6.31 (26Q2); Crunchwell 6.06 → **3.97 (26Q1)** → 4.16 (26Q2).
- Note: the **canonical LA headline** (docs/louisiana-decline.md, Mass/Grocery peak-to-trough) is **6.4% → 3.0%, −340 bps**. The value-weighted all-channel cut above is milder (~5.9→4.0) — same direction. Use −340 bps / 6.4%→3.0% as the headline, cite both.

## Category (seed_category_market_size, NielsenIQ-shape)
- RTE Cereal total US: FY24 $8.24B (+0.9%) → FY25 $8.35B (+1.3%). Acme share **5.7%**.
- **Wellness Protein**: $710M FY24 → $840M FY25 (**+18.3%**), Q2FY26 MTD +18.6%. Acme share 7.1→**7.6→8.4%**. Fastest pocket.
- Family Sweet (Crunchwell's home): $2.86B, +1.4%. Kids Sweet: $1.41B, **−2.8%** (declining).
- Family Oat +2.4%; Oat milk (Plant-Based) $1.64B **+18.8%**; Granola $1.88B +3.3%; Hot Cereal ~flat/decline, single-serve cups +9.8%.
- Louisiana RTE total $38M/qtr, **−2.8%** (category itself shrinking locally).
- Target Wellness Protein Acme share **18.4%** vs Walmart **5.2%** (Target over-indexes for ProteinPeak).

## Retail media Q1 2026 (seed_retail_media_spend_q1_2026)
Total ~**$4.2M** → **$2.73M incremental ($0.65 per $1)**.
| Platform | Spend | Incremental | Modeled incr. ratio |
|---|---|---|---|
| Amazon Ads | $2.4M | $0.98M | **0.40** (drag) |
| Walmart Connect | $1.0M | $1.21M | **1.20** (best) |
| Kroger Precision | $0.4M | $0.32M | 0.77 |
| Target Roundel | $0.4M | $0.22M | 0.50 |
Proposed H2: reallocate ~$700K out of Amazon into Walmart/Kroger + LA (2.2× ROI).

## Trade promotion (trade_promo_events_q1_2026 + trade_spend_fy25)
- Q1 FY26: **43 events, $11.6M spend, $10.9M incremental, avg lift 14.3%, incrementality index 0.52.**
- FY25 trade by brand ($K, depth%, incr): Crunchwell $92.4M/24.4%/0.57; HoneyNest $21.7M/24.2%/0.51; TrailGrove $10.8M/13.5%/0.52; MorningOats $10.2M/17.8%/0.59; ProteinPeak $6.9M/11.5%/0.45; RootDay $4.7M/9.5%/0.43. Total ~$146M.
- Crunchwell trade rate ~25.6% of gross (heavy); ProteinPeak ~12.9% (lean).

## Marketing / A&P spend (seed_marketing_spend, $K)
- By period: 25Q1 $24.5M, 25Q2 $11.9M, 25Q3 $10.2M, 25Q4 $5.9M, 26Q1 $10.9M, 26Q2 $11.7M.
- Crunchwell ~$48.7M/yr (Linear TV $24M, Retail Media $12.2M, CTV $6.3M, Paid Social $3.3M...). TV-heavy, traditional.
- ProteinPeak ~$22.2M (Paid Social $7.8M, Retail Media $6.55M, CTV $4.7M, Influencer $2.86M...). Digital/creator-led.
- HoneyNest/MorningOats tiny (<$1.1M). TrailGrove/RootDay small, social-led.

## Brand equity (brand_equity_quarterly, Crunchwell US-NAT, Top-2-box %; Kantar-shape)
FY25Q1 → FY26Q2:
- **Relevance 68.6 → 62.7 (−5.9 pp)** — the lead diagnostic, declining.
- Trust 72.3 → 72.9 (holds). Taste 74.4 → 73.2. Quality 69.3 → 70.3 (holds). Modernity 51.0 → 48.8 (soft).
- Diagnosis: "Relevance, not Trust" — Crunchwell is trusted but drifting from cultural relevance.
- brand_health: NPS ~6.5 flat; aided awareness ~82%; taste score ~3.6/5.

## Supply chain (shipments; Fill_Rate_Pct is a fraction, 0.95 = 95%)
- Normal fill ~**95%**, OTIF ~90%. Hurricane Tonya (Nov 2025) storm cuts: fill **51.6%** (Storm), Production_Lag 83%, Quality_Hold 83%. Houston/Thibodaux/Tyler DCs hit.
- Recovered to ~95% by Q1/Q2 FY26.

## Innovation pipeline (seeds/innovation_pipeline.csv)
- **Live Q2 FY26**: ProteinPeak Cinnamon Crunch (PP005, $14M yr1, conf 0.74), Cocoa Almond (PP006, $10M, 0.68). Launched **2026-04-20**.
- **Stage-5 Launch Prep**: Crunchwell Pack Refresh — Hero SKUs ($28M yr1, conf 0.82, launch **2026-08-15**). Biggest near-term bet.
- **Stage-4 Pre-Launch**: HoneyNest Birthday Cake LTO ($2.4M, Q4), MorningOats Cup Pumpkin Spice LTO ($1.8M, Q3).
- **Stage-3 Prototype**: Crunchwell Mega Family Pack 36oz ($8.5M, 2027-Q1), Cinnamon Twist Reformulation (recovery), MorningOats Overnight Banana, RootDay Single-Serve Carton (On-Hold).
- **Stage-2 Concept**: Crunchwell Hispanic "Maiz Crunch" ($12M, 2027-Q1, conf 0.46), RootDay Coffee Creamer, TrailGrove Bites Yogurt-Coated, others.
- **Stage-1 Idea**: ProteinPeak Bars 12g ($8M, 2028-Q2), RootDay Yogurt Smoothie ($6M), Crunchwell High-Fiber ($5M), HoneyNest Plus Whole Grain ($4M).
- **Discontinue (Q3 FY26)**: RootDay Coconut Blend, HoneyNest Granola Crunch, HoneyNest Cookie Dough.

## Chocolate Almond concept test (seed_concept_test_chocolate_almond; ProteinPeak Q3)
- n=1000, **64% top-2-box** (clears 55% action standard); +6pp vs launch-SKU pretest; +11pp vs innovation benchmark.
- Protein-curious cohort 71% TTB (intent 3.06/5); lapsed-cereal 66%; current-Crunchwell 52%.
- Cannibalization vs ProteinPeak launch SKUs: 22% overlap, 14pp additive, **8pp substitutional < 12pp SteerCo gate → PASSES**.
- Cannibalization vs Crunchwell: 6% overlap, 2pp substitutional (negligible).
- Field of 2026-06-22 → 2026-07-11. Chocolate breakfast preference +14pp in protein-curious (U&A Apr 2026).

## ProteinPeak launch (Scenario 2, past-quarter facts)
- Launched PP005+PP006 on 2026-04-20. Trial 110–113% of plan at Target, 77–78% at Walmart-pilot. Target velocity ~17.5 vs Walmart ~9.2 u/store/wk.
- **Source of volume** (household_transactions PP005/PP006, of "real" switches): New-to-brand **53%** (431), Cannibalization **32%** (260), Competitor switch **15%** (125).
- Repeat W2 ≈ 1.2× Berry Crunch (PP003). Social sentiment **+0.44** on ~496 mentions 2026.
- Q2 retail-media budget $4.2M (Hugo Lin). Launch comms envelope $6.4M (Renee Alvarez).

## Competitive (seed_competitor_launches, recent)
- **Field & Honey (Larksfield)** = the aggressor: Almond launch 2025-09-08 (LA stealth); **14g-protein line ext LCH00032 launched 2026-05-12** (escalates protein + LA fronts); spring lemon LTO.
- Cheerios (GM): Choco Crunch (2026-01-15), Peanut Butter (2026-04-06). Great Value PL Honey Almond/Nut (2025-08, high ACV 84-86%). Magic Spoon, RXBAR, Catalina Crunch (protein/keto challengers).
- Crunchwell CR009 Pack Refresh proposed 2026-08-15 (= the innovation Pack Refresh).

## Shopper panel / cohorts
- Kantar cohorts (penetration %, FY25Q1→FY26Q2): loyal-family 46.1→**44.7 (eroding)**; protein-returner 11.0→**12.7 (growing)**; cereal-skipper 18.7→**21.0 (growing, bad)**; price-shopper 24.0→24.7.
- Social sentiment 2026: ProteinPeak +0.44; Crunchwell **−0.11** (316 mentions); MorningOats +0.10; Oatly +0.20.

## Geography (seed_geographies, Crunchwell share FY25→Q1FY26)
- Home turf: Chicago 7.8→7.7, Midwest 7.4→7.2, PNW 6.8→6.6, Houston 6.7→6.5 (strong).
- **Battlefields**: Louisiana DMA 6.4→**3.0**, New Orleans 5.1→**3.0**, Baton Rouge 5.8→**4.2**.
- **Leading-indicator watch** (early F&H spread): Birmingham 5.7→5.4, Memphis 5.4→5.1.
- Under-indexed: Northeast 3.8→3.7, NYC 3.4.

## Macro trends (seed_macro_trends, strength 0-1)
High-protein cereal 0.92 (Up); TikTok Shop grocery 0.86; oat-milk barista 0.84; cinnamon renaissance 0.81; **GLP-1/Ozempic appetite shift 0.81 (Down volume)**; sustainable packaging 0.74; LTO acceleration 0.74; low-sugar pressure 0.72; kid-cereal mom-guilt 0.68 (Down kids).

## Retailers (seed_retailers, Acme FY25 $M)
Walmart $184M (21.4% ACV, Tier1), Kroger $93M, Target $68M, Albertsons $52M, Costco $52M (Club), Amazon $44M, H-E-B $32M, Publix $29M, Sam's $28M, Meijer $21M, Aldi $15M.

## Personas (use as owners/authors)
Maya Chen (Sr Insights Analyst, Cereals); Marcus Boudreaux (Dir Sales, South); Diane Halverson (VP Sales NA); Priya Raman (Category Mgr); Tasha Brooks (eComm/retail media); Sage Park (ProteinPeak brand); Cory Whitman (Crunchwell brand); Renee Alvarez (comms); Hugo Lin (media); Nina Ortega (category insights); Jordan Hsu (LA diagnostic); Wes Okafor (shopper mktg/BTS); Gregory Whitfield (CEO); + a CFO (unnamed) and CMO.
