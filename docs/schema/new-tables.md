# New tables — schema reference (v0.2.0 + v0.3.0 + v0.4.0 + v0.7.0)

These tables are additive on top of the v0.1.0 core six. They close the gaps identified in `00-inbox/synthetic-data-gap-analysis-vs-mvp.md` and unblock the Brand Manager / Category Manager / VP Sales prompt set in the persona playbook. The **v0.7.0 expansion** adds six Marketing & Insights tables anchored to the Marketing & Insights persona pack (`clayface-workspace/03-research/acme/11-scenarios/v2/`).

> Every table joins back to one of the existing entity sets — SKUs (`seeds/skus.csv`), retailers (`seeds/retailers.csv`), DMAs (`seeds/geographies.csv`), or stores (`Store_ID` from `perfect_store`).

---

## v0.2.0 — Sales-side completeness

### `plan_vs_actual` — monthly grain

Brand × Retailer × DMA × Period actuals vs. AOP / re-forecast.

| Column | Type | Notes |
|---|---|---|
| `Period` | YYYY-MM | Monthly grain |
| `Brand` | enum(6) | Crunchwell / HoneyNest / ProteinPeak / MorningOats / TrailGrove / RootDay |
| `Retailer` | enum | Joins to `seeds/retailers.csv` |
| `DMA` | enum | Joins to `seeds/geographies.csv` |
| `Plan_Revenue_USD` | float | Monthly revenue plan |
| `Plan_Units` | int | Monthly unit plan |
| `Actual_Revenue_USD` | float | Realized revenue |
| `Actual_Units` | int | Realized units |
| `Variance_USD` | float | actual − plan |
| `Variance_Pct` | float | (actual − plan) / plan |
| `Variance_Status` | enum | On-Track / Soft / Red / Over |
| `Plan_Source` | enum | "AOP" or "FCST_REV" (re-forecast) |

**Narrative encoded:** Crunchwell LA-DMA Q1 2026 averages **−47% vs plan** (Red status across Jan/Feb/Mar). ProteinPeak FY26 plan was +67% vs +24% actual (slowing).

**Headline prompt unblocked:** "How are top SKUs performing at Kroger vs. plan?"

---

### `sku_authorization` — store × SKU × month

Authorization vs. distribution snapshot. Captures the gap between "the SKU is approved at this store" and "the SKU is actually on the shelf this week."

| Column | Type | Notes |
|---|---|---|
| `Snapshot_Date` | YYYY-MM-DD | Month-end snapshot (5 snapshots Nov 2025 → Mar 2026) |
| `Store_ID` | str | Joins to `perfect_store.Store_ID` |
| `Banner` | str | Retailer chain |
| `Banner_Division` | str | New v0.2.0 column |
| `Banner_Region` | str | New v0.2.0 column |
| `DMA` | str | |
| `State` | str | |
| `Size_Tier` | enum | S / M / L |
| `SKU` | str | Acme SKU id |
| `Brand` | str | |
| `Auth_Status` | enum | Authorized / Not_Authorized |
| `Distribution_Status` | enum | Distributed / Authorized_Not_Distributed / Out_Of_Distribution |
| `Ranged_Since` | YYYY-MM-DD | When SKU was first authorized at store |
| `ACV_Weight_Pct` | float | Store's share of national ACV |
| `Why_Not_Distributed` | enum | OOS / store_choice / supply_chain / new_listing_pending / discontinued |

**Narrative encoded:** Cinnamon Twist (CR006) at 39% national authorization, 67% distributed-of-authorized at Walmart — explicit distribution void. RootDay 12% authorized at Walmart (test only). H-E-B ProteinPeak 38% — expansion headroom.

**Headline prompts unblocked:** "Top distribution void opportunities at Target — SKUs authorized but <80% ACV." "If we gained authorization at the 500 Albertsons stores where we're not currently distributed, what's the estimated annual revenue opportunity?"

---

### `shipments` — weekly DC × SKU

Acme plant → Retailer DC fill rate and on-time data.

| Column | Type | Notes |
|---|---|---|
| `Shipment_ID` | str | SHP######## |
| `Week_Start` | YYYY-MM-DD | Monday week start |
| `Brand` | str | Acme brand |
| `SKU` | str | |
| `Retailer` | str | |
| `Retailer_DC` | str | "Walmart Houston DC" etc. |
| `Origin_Acme_Plant` | enum | Battle Creek / Lancaster / Houston / Modesto |
| `Ordered_Units` | int | Retailer PO |
| `Shipped_Units` | int | Acme shipped |
| `Delivered_Units` | int | Received OK at DC |
| `Fill_Rate_Pct` | float | delivered / ordered |
| `On_Time_Pct` | int | 0 or 1 |
| `Cut_Reason` | enum | None / OOS / Production_Lag / Quality_Hold / Truck_Capacity / Storm |

**Narrative encoded:** Hurricane Tonya — Houston-region DCs (Walmart Houston DC, Rouses Thibodaux DC, Brookshire's Tyler DC, H-E-B Houston DC, Kroger Memphis DC) collapse to ~58% fill rate Nov 8 – Dec 15, 2025 with `Cut_Reason='Storm'`. Crunchwell Mega specifically pushed below 50%.

**Headline prompt unblocked:** "Show me our fill rate by retailer for the last 4 weeks. Flag any retailer below 95%."

---

### `promo_events` — event-level

All-retailer promo log with mechanic taxonomy and ROI math.

| Column | Type | Notes |
|---|---|---|
| `Event_ID` | str | PE##### |
| `Start_Date` / `End_Date` | YYYY-MM-DD | |
| `Brand` / `Manufacturer` / `SKU` | str | |
| `Retailer` / `Banner_Division` / `Banner_Region` | str | |
| `DMA` | str | |
| `Mechanic` | enum | TPR / BOGO / Multi-Buy / Display / Feature / Feature+Display / Bundle / Coupon |
| `Promo_Depth_Pct` | int | 0–50 |
| `Display_Type` | enum | Endcap / In-Aisle / Lobby / None |
| `Feature_Type` | enum | Retailer_Circular / Digital_Coupon / Email / None |
| `Trade_Spend_USD` | float | Event-level cost |
| `Pre_Promo_Baseline_Units` | int | 4-week lookback |
| `Promo_Units` | int | During-event |
| `Lift_Pct` | float | (promo − baseline) / baseline |
| `Incremental_Units` | int | promo − baseline |
| `Forward_Buy_Pct` | float | Share of incremental that's pull-forward |
| `True_Incremental_Units` | int | incremental × (1 − forward_buy) |
| `ROI` | float | (gross_margin × true_incremental) / trade_spend |

**Narrative encoded:** Industry-typical mix per retailer (Walmart Feature+Display heavy, Kroger Multi-Buy heavy, Costco Bundle heavy). Median ROI ~1.2x. The hand-curated LA Field & Honey sequence remains in `seeds/promo_events_louisiana.csv` — it's still the canonical record for that story.

**Headline prompts unblocked:** "Summarize ROI of every promotion we ran at Walmart in Q1." "Which promo mechanics deliver the best lift for our top 10 SKUs at Kroger?" "How much of our promotional volume is true incrementality vs. forward-buy?"

---

### `competitor_launches` — event-level

Hand-curated competitor + Acme launch event log. Sourced from `seeds/competitor_launches.csv`.

| Column | Type | Notes |
|---|---|---|
| `launch_id` | str | LCH##### |
| `brand` / `manufacturer` | str | |
| `sku_new` | str | |
| `product_description` | str | |
| `launch_date` | YYYY-MM-DD | |
| `launch_retailers` | str | semicolon-list |
| `launch_dmas` | str | "ALL" or DMA list |
| `pack_oz` / `launch_price_usd` | float | |
| `claim_headline` | str | |
| `trade_support` | str | |
| `buzz_index_day30` | float | 0.0–1.0 |
| `acv_at_launch_pct` / `acv_day_90_pct` / `acv_day_180_pct` | float | |
| `year1_velocity_units_per_store_per_wk` | float | |
| `status` | enum | Live / Withdrawn / Limited Release / Pre-Launch / Active-Underperform |
| `intel_source` | str | NielsenIQ Innovation Tracker / Mintel GNPD / Walmart Luminate / etc. |
| `notes` | str | |

**Narrative encoded:** ~31 launches anchored on real CPG launch tempo, including Larksfield "Field & Honey Almond" Sept 2025 (LA stealth threat), GM "Cheerios Oat Crunch" Jan 2026, Walmart Great Value Honey Toasted Oats expansion (took Crunchwell's facings — LA H5), Acme's own Crunchwell Cinnamon Twist (the underperformer), and ProteinPeak's Q2 2026 Cinnamon Crunch (LCH00021 — PP005) + Cocoa Almond (LCH00031 — PP006) co-launch on April 20, 2026 (Scenario 2 anchor).

**Headline prompts unblocked:** "Did any competitors launch new products in the last 7 days?" "Which new items launched in our category in the last 6 months are gaining traction?" "Generate a competitive response brief: [Competitor] just launched 4 new SKUs at Walmart..."

---

## v0.3.0 — Brand & Insights synthesis

### `social_mentions` — Brandwatch-shape

Per-mention social listening data across TikTok, Instagram, Twitter/X, Reddit, YouTube, Facebook.

| Column | Type | Notes |
|---|---|---|
| `Mention_ID` | str | |
| `Date` | YYYY-MM-DD | |
| `Platform` | enum | |
| `Brand_Mentioned` / `Manufacturer` | str | |
| `Author_Type` | enum | Consumer / Creator / Press / Brand |
| `Reach` / `Engagement` | int | |
| `Sentiment_-1to1` | float | |
| `Sentiment_Bucket` | enum | Positive / Neutral / Negative |
| `Topic_Tags` | str | semicolon-list (joins to `seeds/social_topics.csv`) |
| `Has_Video` | int | 0/1 |
| `DMA_Region` | str | DMA id or 'UNKNOWN' (~45% UNKNOWN, realistic for social geo-inference) |
| `Source` | str | "Brandwatch" |

**Narrative encoded:** Crunchwell sentiment dip in LA Q4 2025–Q1 2026 (avg around −0.36 vs +0.13 elsewhere). Field & Honey viral wave with `Topic_Tags='viral;promo'`. ProteinPeak athletic-momentum lift Q1 2026.

**Headline prompts unblocked:** "How has consumer sentiment about our brand changed?" "What's driving negative sentiment?" "Social momentum vs. competition?"

---

### `creator_posts` — Tribe Dynamics-shape

Influencer / creator post-level activity with 72-hour attribution lift. Joins to `seeds/creators.csv` (50 hand-curated creators across tiers and niches).

| Column | Type | Notes |
|---|---|---|
| `Post_ID` | str | |
| `Creator_ID` | str | Joins to `creators.csv` |
| `Handle` | str | |
| `Platform` | enum | |
| `Date` | YYYY-MM-DD | |
| `Brand_Mentioned` | str | |
| `Disclosed_Partnership` | enum | Yes / No |
| `Followers_Snapshot` | int | |
| `Reach` / `Engagement` | int | |
| `Engagement_Rate` | float | |
| `Attributed_Sales_Lift_72hr_USD` | float | 0 if not disclosed |
| `Niche` / `Tier` | str | |
| `Source` | str | "Tribe Dynamics" |

**Narrative encoded:** Sage Park ProteinPeak athlete program (5 anchor creators in Q1–Q2 2026). RootDay barista creator program. Crunchwell Pack Refresh creator outreach in pipeline.

**Headline prompts unblocked:** "Which creators posted about products in our category?" "Did we see lift within 72 hours of their posts?"

---

### `search_trends` — Spate / Helium 10-shape

Monthly keyword search volume across Google, Amazon, TikTok.

| Column | Type | Notes |
|---|---|---|
| `Date` | YYYY-MM-01 | First-of-month |
| `Platform` | enum | Google / Amazon / TikTok |
| `Keyword` | str | |
| `Category` | enum | RTE Cereal / Hot Cereal / Granola / Plant-Based Milk / Bar |
| `Volume_Index_0to100` | float | |
| `Brand_Relevance` | str | Crunchwell / ProteinPeak / category / etc. |
| `MoM_Growth_Pct` | float | |
| `Source` | str | "Spate" or "Helium 10" |

**Narrative encoded:** "high-protein cereal" growing +18% MoM, "oat milk barista" +16%, "field & honey almond" peaks at launch (Sept 2025), "cheerios oat crunch" peaks at launch (Jan 2026). "crunchwell review" slightly negative drift.

**Headline prompts unblocked:** "Fastest-growing search terms in our category we don't rank for." "Top trending topics on TikTok." Innovation white-space prompts.

---

### `product_reviews` — Bazaarvoice / PowerReviews-shape

Per-review data across Amazon / Walmart.com / Target.com / Kroger.com / Instacart / DTC.

| Column | Type | Notes |
|---|---|---|
| `Review_ID` | str | |
| `SKU` / `Brand` / `Category` | str | |
| `Retailer` | enum | Amazon / Walmart.com / Target.com / Kroger.com / Instacart / DTC |
| `Date` | YYYY-MM-DD | |
| `Rating_1to5` | int | |
| `Verified_Purchase` | enum | Yes / No |
| `Topic_Tags` | str | semicolon-list (positive: taste/value/health/...; negative: stale/pack-damage/too-sweet/oos/...) |
| `Sentiment_-1to1` | float | |
| `Review_Length_Chars` | int | |
| `Helpful_Votes` | int | |
| `Source` | str | "Bazaarvoice" / "PowerReviews" / "Amazon Brand Analytics" |

**Narrative encoded:** Cinnamon Twist (CR006) average rating ~3.4 vs hero SKU ~4.3. Crunchwell ratings dip during Hurricane Tonya OOS (Nov 2025–Jan 2026) tagged with `oos` / `supply-issue`. Premium SKUs (ProteinPeak, TrailGrove, RootDay) average 4.4.

**Headline prompts unblocked:** "Top 3 unmet consumer needs based on negative review themes." "Competitor products gaining the most review momentum."

---

## v0.4.0 — Polish + edge cases

### `data_freshness_log` — weekly metadata

Per-week status of each data feed (NielsenIQ, Numerator, SAP, Brandwatch, etc.).

| Column | Type | Notes |
|---|---|---|
| `Week_Start` | YYYY-MM-DD | |
| `Feed_Name` | str | Joins informally to `seeds/research_agencies.csv` |
| `Cadence` | enum | Real-time / Hourly / Daily / Weekly / Monthly / Quarterly / Annual / On-Demand / Bi-monthly |
| `Last_Refreshed` | timestamp | |
| `Lag_Hours` | int | |
| `Status` | enum | On-Track / Lagging / Stale / Outage |
| `Owner_Team` | enum | Insights / E-Comm / Marketing / Innovation / IT / External |

**Narrative encoded:** Most feeds On-Track. Kroger 84.51 occasionally Lagging. SAP shipments outage Feb 16, 2026. Helium 10 occasionally Lagging.

**Headline prompts unblocked:** "Any data gaps in our feeds this week?"

---

## Reference seeds (also new)

| File | Rows | Purpose |
|---|---:|---|
| `seeds/retailer_divisions.csv` | 46 | Banner-division master — ground truth for `Banner_Division` / `Banner_Region` columns |
| `seeds/competitor_launches.csv` | 30 | Hand-curated launch events |
| `seeds/research_agencies.csv` | 27 | Vendor master — which agency feeds which table |
| `seeds/creators.csv` | 50 | Influencer master |
| `seeds/regional_brands.csv` | 12 | Regional / private-label competitive set |
| `seeds/innovation_pipeline.csv` | 25 | Acme pipeline concept master |
| `seeds/category_market_size.csv` | 33 | TAM by category × subcategory × period |
| `seeds/sku_elasticity_estimates.csv` | 36 | Pre-computed elasticity per SKU × retailer |
| `seeds/macro_trends.csv` | 30 | Macro consumer trend feed |
| `seeds/social_topics.csv` | 20 | Social topic taxonomy |

---

## v0.7.0 — Marketing & Insights (six new tables)

Anchored to the **Marketing & Insights persona pack** (`clayface-workspace/00-inbox/00-drop-zone/2026-05-28-marketing-insights-personas.md` → promoted to `11-scenarios/v2/`). Six personas, six scenarios, six new tables. The five scenarios this set unblocks:

- **S6** — Cory Whitman / Crunchwell FY27 annual brand plan (`brand_equity_quarterly`)
- **S7** — Renee Alvarez / ProteinPeak launch comms (`concept_tests` claims test + `competitor_launches` F&H 14g row)
- **S8** — Wes Okafor / Target back-to-school 2026 (`numerator_bts_occasion`)
- **S9** — Nina Ortega / Q3 SOTB (`ua_study_responses` + `ua_qual_pointers` + `kantar_worldpanel_cohort`)
- **S10** — Maya Chen / ProteinPeak Q3 Chocolate Almond concept test (`concept_tests`)
- **S11** — Jordan Hsu / LA-DMA share decline diagnostic (uses existing tables + new BIR-DMA / MEM-DMA leading-indicator DMAs)

### `brand_equity_quarterly` — Kantar Brand Equity Tracker

Brand × DMA × Quarter × Attribute. Adds **Relevance** and **Modernity** on top of the v0.1.0 brand-health 5pt battery (taste/quality/health/value/family_friendly/innovation/trust).

| Column | Type | Notes |
|---|---|---|
| `Brand` | enum | Crunchwell / ProteinPeak / HoneyNest / MorningOats / Field & Honey / Cheerios / Simple Truth PL |
| `DMA` | enum | US-NAT / LA-DMA / US-MW / US-SE / US-NE (5 geographies; coarser grain than `brand_health`) |
| `Wave` | enum | FY25Q1 – FY26Q2 (six quarters) |
| `Wave_Close_Date` | date | Quarter-close survey date |
| `Attribute` | enum | Trust / Relevance / Quality / Taste / Modernity |
| `Top_Two_Box_Pct` | float | 0–100 |
| `N_Respondents` | int | Cell-level sample size (typically 180–320) |
| `Source` | str | "Kantar Brand Equity Tracker" |
| `Methodology_Note` | str | Per-attribute methodology footnote |

**Narrative encoded:** Crunchwell **Trust ~flat over 6 quarters** (72.3 → 72.9 at US-NAT), **Relevance down 5.9pp** (68.6 → 62.7). LA-DMA Crunchwell softens more than national, especially Q1 2026 onwards. Field & Honey gaining on Relevance + Modernity. ProteinPeak only present FY25Q4+ (pre-launch concept-test era and Q2 launch).

**Headline prompts unblocked:** "Which Crunchwell attribute has declined most over six quarters and against which competitor?" "Show me the Trust vs Relevance trajectory at LA-DMA."

### `ua_study_responses` — April 2026 U&A Behavioral Study (n=2,400, Ipsos)

Per-respondent U&A behavioral data — the **leading-indicator** layer in the Insights data hierarchy (behavior leads, panel follows, till trails).

| Column | Type | Notes |
|---|---|---|
| `Response_ID` | str | UA_NNNNNN |
| `Field_Date` | date | 2026-04-08 (single fielding) |
| `Wave` | enum | 2026Q2 |
| `Cohort` | enum | cereal-skipper / protein-returner / loyal-family / price-shopper (the canonical v2 four-cohort frame) |
| `DMA` | enum | 32 DMAs weighted to volume |
| `State` | str | Two-letter |
| `Primary_Occasion` | enum | weekday-am / weekend-am / post-workout / afternoon-snack / evening |
| `Skip_Cereal_3plus_Mornings` | bool | The defining behavior of the cereal-skipper cohort |
| `Cite_Protein_As_Swap_Driver` | bool | "Why do you swap out of cereal?" |
| `Intent_Add_Protein_Morning_0to10` | float | Stated-intent |
| `Skip_Frequency_Mornings_Per_Wk` | float | 0–7 |
| `Chocolate_Breakfast_Pref` | bool | Used by Maya's Chocolate Almond concept-test U&A overlay |
| `GLP1_Adjacent` | bool | Self-reported GLP-1 use / adjacent |
| `HOH_Age_Band`, `Income_Band`, `Presence_Of_Kids_5_14` | enum/bool | Standard demos |
| `Vendor` | str | "Ipsos" |
| `Respondent_Weight` | float | Projection weight (0.6–1.4) |

**Narrative encoded:** **28% of households skip cereal 3+ mornings/week** (672/2,400, exactly the cell-size limit Nina enforces). **62% of skippers cite protein as the swap driver** (v2 canon: 64%). Cereal-skipper cell n=672 is large enough for segment-level reads but **not for regional DMA cuts** — workspace tiles should expose this constraint.

**Headline prompts unblocked:** "What changed in consumer behavior YoY?" "Reconcile the Nielsen till read with the Kantar panel and our U&A — what's the consumer story?" "Does the Chocolate Almond extension have behavioral evidence?"

### `ua_qual_pointers` — 36 In-Home Interview Index

Pointer table for the qual leg of the April U&A. One row per in-home.

| Column | Type | Notes |
|---|---|---|
| `Interview_ID` | str | UA-IH-NN |
| `Cohort`, `DMA`, `HOH_Age_Band`, `N_Kids`, `Income_Band` | various | Household profile |
| `Themes` | str | Semicolon-list (3 themes per interview) |
| `Chocolate_Mention_Flag` | bool | Used by Maya's Chocolate Almond U&A overlay |
| `Chocolate_Unprompted_Flag` | bool | Stronger signal — respondent mentioned chocolate without being asked |
| `Duration_Min` | int | 48–92 min |
| `Transcript_Path` | str | `_qual/2026-04-ua/in-home-NN-cohort-dma.txt` (synthetic path) |
| `Notes` | str | Plain-English summary |
| `Wave`, `Field_Date`, `Vendor` | various | Constant across all 36 |

**Narrative encoded:** Among the 36 in-homes, ~3 protein-curious respondents mention chocolate as a breakfast flavor preference, with 1–2 unprompted. Maya cites these in the Chocolate Almond steerco brief.

### `kantar_worldpanel_cohort` — Household-Cohort Frame

Cohort × DMA × Quarter household penetration + frequency from the Kantar Worldpanel. The **panel** layer in the data hierarchy.

| Column | Type | Notes |
|---|---|---|
| `Cohort` | enum | Four-cohort frame |
| `DMA` | enum | US-NAT / LA-DMA / US-MW / US-SE / US-NE |
| `Quarter` | enum | FY25Q1 – FY26Q2 |
| `Wave_Close_Date` | date | |
| `HH_Penetration_Pct` | float | % of households |
| `Purchases_Per_Buyer_Per_Qtr` | float | Frequency among the remaining buyers |
| `N_Panel_HH` | int | Sample size |
| `Source` | str | "Kantar Worldpanel" |

**Narrative encoded:** Cereal-skipper cohort **growing** (penetration up over six quarters). Loyal-family declining slowly. Frequency among loyal-family buyers grows (the "remaining buyers buy more" effect). LA-DMA loyal-family frequency drops sharply in 2026Q1–Q2 (the Crunchwell loss).

### `numerator_bts_occasion` — Back-to-School Occasion (2025 benchmark)

Retailer × ISO-week 2025 back-to-school occasion data, with the **Target Circle membership overlay** and the **protein-curious cohort overlap**.

| Column | Type | Notes |
|---|---|---|
| `Retailer` | enum | Target / Walmart / Kroger / Albertsons / Costco |
| `ISO_Week` | str | 2025-W28 through 2025-W34 (the BTS window) |
| `Week_Start_Date` | date | |
| `HH_Kids_5_14_Buying_Cereal_Share` | float | 0–1 |
| `Protein_Curious_Cohort_Overlap` | float | Highest at Target (64%) |
| `Target_Circle_Membership_Overlap` | float | Target only; ~70% |
| `Incremental_Category_Dollars_KUSD` | float | The 2025 BTS benchmark — sums to **$14.2M at Target** |
| `Program_Year`, `Source`, `Definition` | various | |

**Narrative encoded:** **Target 2025 BTS = $14.4M incremental category dollars** (v2 canon $14.2M, within tolerance). Peaks weeks 2–3 of August (W32–W33). Target × protein-curious overlap = 64.7% (canon 64%, the highest of any major retailer).

**Headline prompts unblocked:** "What did the 2025 Target BTS program deliver?" "Which retailer has the highest protein-curious cohort overlap for the ProteinPeak launch?"

### `concept_tests` — Concept Test Results (long-form)

Long-form (one-row-per-metric) concept-test results table combining Maya's Chocolate Almond test (n=1,000) and Renee's April launch claims test (n=1,200), both with cohort cuts using the **Acme four-cohort segmentation** (not Ipsos defaults).

| Column | Type | Notes |
|---|---|---|
| `Test_ID` | str | CT_CHOC_ALMOND_2026Q3 / CT_LAUNCH_CLAIMS_2026Q2 |
| `Test_Name` | str | Human-readable |
| `Vendor` | str | Ipsos (Chocolate Almond) / Kantar (Launch Claims) |
| `Section` | enum | topline / cohort / cannibalization / validation / overlay / competitive / meta / CL1 / CL2 / CL3 |
| `Metric` | str | top_two_box_pct / n_in_cohort / substitutional_overlap_pp / etc. |
| `Value` | mixed | float / int / date / bool |
| `Unit` | enum | pct / pp / n / bool / score / date / g |
| `Scope` | str | Cohort name or scope qualifier |
| `Acme_Segmentation_Used` | bool | Always 1 — the v2 rule |
| `Cannibalization_Threshold_Pp` | int | 12pp for Chocolate Almond steerco; null for launch-claims |
| `Notes` | str | |

**Narrative encoded:** Chocolate Almond clears at **64% top-two-box** (+6pp over launch SKU, +11pp over benchmark). Cannibalization: 22% overlap → 14pp additive, 8pp substitutional → **clears 12pp gate**. Launch claim CL1 ("20g protein, less sugar") strongest at 78% with protein-curious; competitive flag for Field & Honey 14g narrows protein delta 11g → 6g.

**Headline prompts unblocked:** "Does Chocolate Almond clear the cannibalization gate?" "Which launch claim should lead with the protein-curious cohort?" "Did the Field & Honey 14g launch change our claim ranking?"

---

## v0.7.0 — Reference seeds (also new)

| File | Rows | Purpose |
|---|---:|---|
| `seeds/brand_equity_tracker_quarterly.csv` | 975 | Source seed for `brand_equity_quarterly` parquet |
| `seeds/ua_study_2026q2_reference.csv` | 28 | Cohort × occasion reference grain (expanded into 2,400 per-respondent rows) |
| `seeds/ua_qual_pointers_2026q2.csv` | 36 | One row per in-home interview |
| `seeds/kantar_worldpanel_cohort_frame.csv` | 120 | Source seed for `kantar_worldpanel_cohort` parquet |
| `seeds/numerator_bts_occasion_2025.csv` | 35 | Source seed for `numerator_bts_occasion` parquet |
| `seeds/concept_test_chocolate_almond.csv` | 25 | Chocolate Almond test (n=1,000) |
| `seeds/concept_test_launch_claims_2026q2.csv` | 35 | April Kantar launch-claims test (n=1,200) |

**Plus two merges:**

- `seeds/competitor_launches.csv` — appended Field & Honey 14g protein extension (LCH00032, May 12 2026 launch) to support Renee's competitive-shift narrative in v2 Scenario 02.
- `seeds/geographies.csv` — appended Birmingham-Tuscaloosa-Anniston DMA (BIR-DMA) + Memphis DMA (MEM-DMA) as the leading-indicator DMAs Jordan flags in v2 Scenario 06.
