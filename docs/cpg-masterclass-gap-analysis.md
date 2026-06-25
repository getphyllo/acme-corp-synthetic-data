# CPG Masterclass — Coverage Gap vs. ACME Scenarios

*Cross-walk between Amit Singh's "CPG Fundamentals Masterclass" (May 11, 2026; uploaded May 28, 2026) and the canonical Acme synthetic-data scenarios — what the dataset covers today, what is partially covered, and what new scenarios / seeds / personas should be added to make the dataset capable of exercising every concept in the masterclass.*

**Status:** Draft for review, 2026-05-28 · Authored against shipped `v0.6.0` artifacts (Louisiana + ProteinPeak + Walmart Aug + Kroger Q3 + Tasha CFO). The README declares an in-flight `v0.7.0` adding six additional scenarios (Cory Whitman annual brand plan · Renee Alvarez PP launch comms · Wes Okafor Target back-to-school · Nina Ortega category state-of-the-business · Maya Chen PP Chocolate Almond concept test · Jordan Hsu LA leading-indicator diagnostic) but the underlying scenario docs, persona files, CHANGELOG entry, and narrative-anchors rows are not yet shipped. This analysis is calibrated to what is **queryable today**; the v0.7.0 intent is noted inline where it changes a recommendation.
**Audience:** Anyone using the Acme dataset to fixture a Clayface prototype, PRD, or design surface against a real CPG workflow.

---

## 1. How "v1" and "v2" of the Acme dataset map onto the masterclass

The dataset has shipped in two scenario waves:

| Wave | Scenarios | Anchor persona | Decision pattern |
|---|---|---|---|
| **v1** (v0.1.0 → v0.5.0) | **S1 Louisiana Cereal Decline** · **S2 ProteinPeak Q2 Launch Read** | Maya Chen (Senior Insights Analyst) | Defensive root-cause synthesis + offensive Week-4 launch read |
| **v2** (v0.6.0, May 16, 2026) | **S3 Walmart Aug Line-Review Prep** · **S4 Kroger Q3 JBR Pre-Read** · **S5 Q1 Retail-Media & Trade-Promo Effectiveness CFO Read** | Marcus Boudreaux (Sales) · Priya Raman (Category) · Tasha Brooks (eCommerce/RM) | Retailer-facing JBP/JBR prep + Finance-facing spend defense |

Read together, the five scenarios cover Maya's defensive and offensive insights work (v1), the retailer-facing commercial work (v2 — Marcus/Priya), and the trade-spend/retail-media defense in front of Finance (v2 — Tasha). That is genuinely broader than most synthetic CPG datasets in circulation.

The masterclass, however, frames CPG around **seven decision moments**, **six functions**, **five metric levels**, **six data types**, **three buyer archetypes** (consumer/shopper/customer), and a **money waterfall** anchored on NSV. Mapped against that surface area, the Acme dataset covers about **60–65%** of the concepts deeply, **20–25%** partially, and leaves **15–20%** uncovered.

---

## 2. Concept-by-concept coverage matrix

Legend: ✅ Covered · ⚠️ Partial / implicit · ❌ Not covered.

### 2.1 The seven decision moments Clayface should own (slide 27)

| Decision moment | Covered by | Status | Gap |
|---|---|---|---|
| 1. Plugged into consumer sentiment | `brand_health`, `social_mentions`, `product_reviews` across S1/S2 | ✅ | None on data. Scenario-level "consumer-sentiment-led" story is implicit, not headlined. |
| 2. Ongoing MBR / QBR | Implicit in S2 (Whitfield May 26 review) and S1 (May 28 board read) | ⚠️ | No scenario explicitly framed as a recurring monthly business review with a hero SKU under forecast. |
| 3. Promo / Launch / Campaign post-mortem | S2 (PP launch Week-4 read); S5 (retail-media effectiveness, Q1 trade-promo) | ✅ | Strong on launch + retail-media. **No campaign post-mortem** — e.g., "the Crunchwell Honey Nut TV burst in October — did it work?" |
| 4. Competitor response / campaign analysis | Larksfield is antagonist throughout S1, S3, S4 | ⚠️ | No dedicated scenario where Acme is **responding** to a specific live competitor campaign (e.g., "Field & Honey just dropped a 4-week TikTok campaign — counter it"). |
| 5. JBP / JBR preparation | S3 Walmart Aug line review; S4 Kroger Q3 JBR | ✅ | Coverage is strong but **misses the JBP season itself (Oct-Dec)** — the actual annual negotiation, locked listings and promo calendars. |
| 6. Innovation Gate Review | `innovation_pipeline.csv` seed; PP005/PP006 sit post-Stage-6 | ❌ | No pre-launch stage-gate scenario. **No BASES / HUT / concept-test / pack-test / copy-test data**. The hardest single gap in the dataset for the masterclass. |
| 7. Category Growth Opportunity Scan | `category_market_size.csv`, `macro_trends.csv`, `social_topics.csv` | ❌ | Seeds exist; **no scenario assembles them into a "where is the category going, where should we play?" scan**. |

### 2.2 The six CPG functions (slide 10)

| Function | Persona in Acme | Status | Notes |
|---|---|---|---|
| Marketing / Brand | Audrey Vance (CMO), Sage Park (Brand Dir), Hugo Lin (Performance) | ⚠️ | Named in S2 dialogue; **none have a dedicated persona file** in `docs/personas/`. |
| Sales / Commercial | Marcus Boudreaux ✅; Diane Halverson ✅; Tom Reilly (NAM Walmart) ⚠️ | ✅ | Marcus + Diane have full persona files; Tom is a name in S3 only. |
| Insights / CMI | Maya Chen ✅; Nina Ortega (Director, Maya's boss) ⚠️ | ⚠️ | Maya is fully formed; **Nina (Maya's manager — and a likely economic buyer per the masterclass) has no persona file**. |
| Category / Shopper / RGM | Priya Raman ✅; Marian Holt (RGM) ⚠️ | ⚠️ | Priya is fully formed; **Marian (the trade-depth/elasticity gatekeeper named in S1 and S5) has no persona file**. |
| Finance | Helen Park-Choi (CFO) ⚠️ | ❌ | Named in S2 + S5 but **no persona file**. Finance is the function that kills budget — under-modeled. |
| Supply Chain / Ops | Theo Mannering (Supply Planning); Devraj (Houston DC) | ❌ | Named only as dialogue refs; **no persona, no scenario where Supply is the protagonist** (e.g., a forward-looking supply scare or a SKU rationalization). |

### 2.3 The five metric levels (slide 15)

| Level | Acme tables that move it | Status |
|---|---|---|
| Enterprise (revenue, profit, margin, market share, cash conversion) | `plan_vs_actual`, `syndicated_weekly` | ⚠️ — revenue + share covered; **margin / EBITDA / cash conversion not in data model**. |
| Brand/Category (penetration, salience, equity, repeat, awareness, consideration) | `brand_health`, `household_transactions` | ✅ |
| Commercial (distribution, share of shelf, rate of sale, promo ROI, sell-out) | `perfect_store`, `sku_authorization`, `promo_events`, `shipments` | ✅ |
| Innovation (launch sales, incrementality, cannibalization, pipeline strength) | S2 scenario + `innovation_pipeline.csv` | ⚠️ — post-launch covered; pre-launch pipeline is a seed only. |
| Execution (availability, forecast accuracy, service level, speed to market) | `perfect_store.OSA_Pct`, `shipments.Fill_Rate_Pct`, `data_freshness_log` | ✅ |

### 2.4 The six data types in CPG insights (slide 16)

| Data type | Acme analog | Status |
|---|---|---|
| 1. Continuous syndicated (NielsenIQ / Kantar Worldpanel / Circana) | `syndicated_weekly`, `epos` | ✅ |
| 2. Brand & comms tracking (Kantar MillwardBrown / Ipsos) | `brand_health` (per-wave) | ⚠️ — **no campaign tracker / copy-test recall / equity index over time**. |
| 3. State of the Nation (annual bespoke qual + quant) | none | ❌ — **no annual category deep-dive artifact**. |
| 4. Focused deep dives (segmentation, pricing, lapsed-buyer) | S1 LA decline is the output; no underlying segmentation study | ⚠️ — output exists; **upstream segmentation / pricing-study artifacts don't**. |
| 5. Innovation & launch testing (BASES, HUT, pack test, copy test) | none | ❌ — **single biggest data-type gap**. |
| 6. Qualitative research (focus groups, ethnographies, IDIs) | none | ❌ — **no qual transcripts, themes, or "consumer voice" sample**. |

### 2.5 The consumer / shopper / customer trichotomy (slide 8)

| Lens | Acme data | Status |
|---|---|---|
| **Consumer** (uses it) | `brand_health`, `social_mentions`, `product_reviews`, `household_transactions` (consumption side) | ✅ |
| **Shopper** (buys it) | `household_transactions` (Switching_Flag, Promotion_Type), `epos` (Promotion_Flag) | ✅ |
| **Customer** (retailer) | `sku_authorization`, `perfect_store` (facings/OSA), `shipments` (DC fill), `retailer_divisions`, `walmart_endcap_audit_la.csv` | ✅ |

Strong across the board — but **the trichotomy isn't named** in any scenario doc. Adding one paragraph per scenario calling out "the consumer story is X, the shopper story is Y, the customer story is Z" would make this an explicit teaching surface for designers.

### 2.6 The money waterfall (slide 7)

| Layer | Acme analog | Status |
|---|---|---|
| Gross Revenue | `plan_vs_actual.Plan_Revenue_USD / Actual_Revenue_USD`; `monthly_pos_fy25_q12026.csv` | ✅ |
| − Trade spend (15–25%) | `trade_spend_fy25.csv`, `promo_events`, `trade_promo_events_q1_2026.csv` | ✅ (excellent in S5) |
| **= NSV (net sales value)** | not computed as a field anywhere | ❌ — **NSV is the only number Finance cares about per the masterclass; it should be a derived field or a column**. |
| − COGS | not modeled | ❌ |
| − A&P (media + agencies + research) | `marketing_spend.csv`, `retail_media_spend_q1_2026.csv` | ⚠️ — media + retail-media covered; **agency fees and research budget line not separable**. |
| = Brand contribution | not computed | ❌ |

**Recommendation:** Add a `nsv_waterfall.csv` seed (brand × period × layer) that lets a scenario explicitly traverse the waterfall and answer "what's the NSV implication?" — that single addition unlocks finance-conversation muscle the dataset currently lacks.

### 2.7 The buying committee for an AI tool sold to CPG (slide 14)

| Masterclass role | Acme persona | Status |
|---|---|---|
| Likely buyer — **CMI / Insights Director** | Nina Ortega (named only) | ❌ No persona file |
| Likely buyer — **Analytics Head** | Robert Kim (named in S1 + S5 context) | ❌ No persona file |
| Likely buyer — **RGM / Category Director** | Priya Raman (Category Manager — not Director) | ⚠️ Title gap |
| Sponsor — **CMO** | Audrey Vance (named only) | ❌ No persona file |
| Spend approval — **Finance** | Helen Park-Choi (CFO, named only) | ❌ No persona file |
| Spend approval — **Procurement** | none | ❌ |
| Can kill — **IT / CIO** | Robert Kim (loosely) | ❌ |
| Can kill — **Legal / Data Privacy / InfoSec** | none | ❌ |
| User, not buyer — **Brand Manager** | Sage Park (Director, not Sr BM); no Sr Brand Manager persona | ⚠️ — **Rachel analog missing**. The masterclass's hero user persona — Sr Brand Manager — doesn't exist in Acme. |

**This is the highest-leverage persona gap in the dataset.** The masterclass is unambiguous that brand managers are users not buyers; that the buying-committee chain is CMI Director → Analytics Head → CMO sponsor with Finance/Procurement/IT/Legal as kill-gates. Acme's `docs/personas/` has the four operational personas (Maya, Marcus, Diane, Priya) but **none of the buying-committee personas**. Every Clayface PRD that claims a buyer is currently pointing at thin air.

### 2.8 The CPG calendar (slide 19)

| Cycle | Acme scenario coverage | Status |
|---|---|---|
| **JBP season Oct–Dec** (annual retailer negotiation; listings + promo calendar locked) | S3 (Aug line review — adjacent, but the JBP itself is Oct-Dec) | ⚠️ |
| **AOP lock December** | `plan_vs_actual` extends to 2026-05 with AOP / FCST_REV; AOP-locking moment not scenarized | ⚠️ |
| **LRP / PSP Feb–Apr** (3-year strategic planning) | none | ❌ |
| **Q1 / Q2 / Q3 / Q4 QBR** | S2 (May 26 Whitfield); S5 (June 4 CFO half-day); S1 (May 28 board) | ✅ |
| **MBR (monthly)** | none | ❌ — **no scenario starts with "it's the first Monday of the month, MBR is in 3 days"**. |
| **Weekly / daily fires** (retailer threats, performance dips, escalations) | S3 references; S1 Hurricane Tonya | ⚠️ — covered in past tense; no current weekly fire as a scenario. |

### 2.9 The four breakout scenarios in the masterclass (slide 20 — "9:12am Wednesday")

These are the masterclass's own scenario primitives. They are the closest the masterclass comes to prescribing what a CPG-AI tool must handle. Mapping them onto Acme:

| Masterclass breakout | Closest Acme scenario | Status |
|---|---|---|
| **Retailer Threat** — biggest customer cutting display support for hero SKU | S3 Walmart facings (recovery, not active threat) | ⚠️ — adjacent, but not "Walmart just sent the email today" |
| **Performance Dip** — hero SKU 18% under forecast for the month, Sales asking why | S1 LA decline (quarterly, multi-source) | ⚠️ — quarterly view; **no single-month "hero SKU −18% MTD" trigger** |
| **Supply Issue** — factory warns of a 3-week shortfall if there's a demand spike | S1 Hurricane Tonya (past tense, recovered) | ❌ — **no forward-looking supply scare** |
| **Leadership Ask** — VP wants a revised innovation deck by Friday, no brief yet | S2 Sage email (close — but to Maya, not a brand manager, and a launch-read, not an innovation deck) | ⚠️ |

Acme has 0 / 4 of the masterclass's own scenarios encoded cleanly. Each one is small enough to add as a v0.7.0 scenario.

### 2.10 The CPG graveyard (slide 23)

The masterclass leans heavily on the graveyard — Crystal Pepsi, New Coke, EZ Squirt, Bud Light 2023, Colgate Frozen Lasagne, Cosmopolitan Yoghurt. Failed launches with great decks and no shopper logic.

Acme has **Cinnamon Twist (CR006)** as a single underperformer (~41% authorization, ~3.3 review rating, in `competitor_launches` as LCH00019). That is the closest thing to a graveyard artifact. **Adding a richer pipeline-of-failure** — e.g., one stage-gated concept that failed BASES, one launched product that died at Week 13 — would let Clayface demonstrate the "fewer expensive mistakes" pitch the masterclass closes on.

### 2.11 The five permanent tensions (slide 13)

The masterclass frames CPG decisions as resolutions of five tensions: long-term brand vs short-term sales, global vs local, desirability vs margin, innovation gamble vs hero defence, data richness vs decision speed.

S1 LA is implicitly a "short-term tactical (Rouses injection) vs long-term brand (pack refresh + media)" trade-off. S5 Tasha is explicitly a "incrementality (margin reality) vs platform-reported ROAS (story)" trade-off. None of the others surface a tension by name.

**Recommendation:** Each scenario doc should end with a one-line "the tension Maya / Marcus / Priya / Tasha is being asked to resolve" — that is the bridge between data and the masterclass's framing.

---

## 3. What the dataset is missing — proposed new scenarios and seeds

These are ranked by leverage against the masterclass and against likely Clayface PRD work. Each is sized to be a single scenario bundle, added to `docs/`, with 1–2 seed files, no parquet schema changes.

### Tier A — must-add to be masterclass-fluent (next dataset version)

*Note: the README declares an in-flight v0.7.0 that includes a ProteinPeak Q3 Chocolate Almond concept-test scenario (Maya-anchored, masterclass decision moment #6) and a category state-of-the-business scenario (Nina-anchored, masterclass decision moment #7). When those ship as full docs + seeds, A1 and parts of B3 below convert from "must-add" to "verify". Until the docs ship, they are intent, not coverage.*

**A1. S6 — Innovation Stage-Gate Review (Q3 2026 — Lillian Park-anchored)**

*Trigger:* Lillian Park (Innovation Director) needs Maya and Sage to defend INV-006 (a working title: "Crunchwell High-Fiber") at the Stage-4 gate review on August 18, 2026. BASES concept test ran at 67 (below the 72 hero threshold); HUT scored 4.1/5 (above pass); pack test had 22% choice penalty vs. control. Should we kill, iterate, or proceed to Stage-5?

*New seeds:* `concept_tests.csv` (BASES + HUT + pack + copy scores per concept × wave); `stage_gate_decisions.csv` (gate review history with go/kill/iterate + rationale).

*Why this is the most important addition:* It puts decision moment #6 on the board, fills the data-type #5 hole, and gives Clayface a "fewer expensive mistakes" story that survives Amit's pitch test. It also gives the dataset its first "concept that didn't survive" — the closest thing to a graveyard slide.

**A2. S7 — October JBP Season Negotiation (Walmart 2027 Annual JBP)**

*Trigger:* It is the week of October 13, 2026. Diane and Tom Reilly are six weeks out from the Walmart 2027 annual JBP signing. Walmart's category buyer (Rachel Esposito, fictional) has signalled she will demand a 3% trade-depth increase across Acme's cereal portfolio and listing fees for the Hispanic-format flanker (the H4 demographic opportunity from S1). Diane needs to walk in with a counter that defends NSV, holds 6 hero SKUs, and gives ground on tail SKUs.

*New seeds:* `jbp_2027_walmart_proposals.csv` (line-by-line proposal grid: each Walmart ask, Acme counter, NSV impact, share impact, fallback). `trade_calendar_2027_draft.csv`.

*Why this matters:* It hits decision moment #5 (JBP prep) at the **actual moment of the year** the masterclass calls out (slide 12, 19). S3/S4 are JBR/line-review-adjacent; this is the JBP itself.

**A3. S8 — September MBR with a Hero SKU −18% MTD (Crunchwell Original Family at H-E-B)**

*Trigger:* It is Monday September 7, 2026. The August close shows Crunchwell Original Family at H-E-B is −18% vs plan MTD. Marcus's South region MBR is Wednesday September 9. Audrey wants a 1-page brief by Tuesday EOD: is this a noise blip, a demand softening, an H-E-B-specific issue, or the early signal of something bigger?

*New seeds:* extends `plan_vs_actual` to September; no new file needed if window extends. Add `mbr_calendar_2026.csv` (each region's MBR cadence + attendees + standing agenda).

*Why this matters:* It hits the masterclass's "Performance Dip" breakout cleanly, and is the **first MBR-anchored scenario** in the dataset.

**A4. S9 — Tuesday Retailer Threat (Walmart "we're delisting CR006 in 6 weeks")**

*Trigger:* Tuesday May 19, 2026 — 9:12am. Tom Reilly forwards an email from Rachel Esposito (Walmart category buyer): "Cinnamon Twist is on the Walmart Spring 2026 SKU rationalization list. We'll be delisting in 6 weeks unless you can show velocity-per-facing recovery and a defensible reason for keeping it." Marcus and Priya have a Friday counter-proposal due.

*New seeds:* `walmart_skurat_spring_2026.csv` (Walmart's rationalization candidate list with current velocity, decision date, Acme defense plan / kill decision).

*Why this matters:* Exact masterclass breakout #1. Cinnamon Twist (CR006) is already the dataset's underperformer; this gives the underperformer story a current-day decision moment, not a historical reference.

### Tier B — high-leverage but lower urgency

**B1. S10 — Forward-Looking Supply Scare (Spring 2026 Atlanta DC capacity warning)**

Theo Mannering sends a memo: Atlanta DC will run at 80% capacity through Q3 due to a packaging-line retrofit, exactly during the back-to-school Crunchwell push. Pre-positioning options, SKU-rationalization options, lost-sales modelling. Decision: do we accept the constraint, build inventory ahead, or shift volume to Houston?

*New seeds:* `dc_capacity_2026.csv`; uses existing `shipments`.

**B2. S11 — Q3 Campaign Post-Mortem (Crunchwell Pack Refresh + Media Burst)**

A 6-week post-launch read of the Crunchwell pack refresh media + creator burst (Hugo Lin's $1.4M LA-targeted spend referenced in the S1 recovery plan). Did the spend land incremental volume vs. baseline? How did the creator cohort perform vs. paid social?

*New seeds:* `creator_campaign_pp_refresh.csv`; uses existing `social_mentions`, `creator_posts`, `marketing_spend`.

**B3. S12 — Annual Category Growth Opportunity Scan (FY27 LRP input)**

It is March 2026. Diane and Audrey are starting LRP/PSP work for FY27. Maya is asked to deliver a 20-page category-opportunity scan: where is the cereal category growing (high-protein, sugar-reduced, ancient-grain, Hispanic formats, kids), where is it shrinking, and where should Acme bet over the next 3 years?

*New seeds:* `category_segments_5yr.csv` (growth-rate decomposition by segment × channel × geography); uses existing `category_market_size`, `macro_trends`, `social_topics`.

**B4. S13 — Competitor Response — "Field & Honey Just Dropped a 4-Week TikTok Push"**

Brandwatch alerts a sudden spike in Field & Honey mentions on TikTok (April 2026). Within 48 hours, Audrey needs Sage's team to assess: is this an emerging Crunchwell-equivalent threat? What's the counter-play (creator drop, paid social, retail-media, ignore)?

*New seeds:* extends `social_mentions` and `creator_posts`; no new file required.

### Tier C — atmospheric / depth additions

- **C1. Qualitative research artifacts** — 1-2 anonymized focus-group transcripts + a small "themes" table tied to the LA decline. Adds data-type #6.
- **C2. Brand & comms tracker** — quarterly equity index per brand × campaign × wave with diagnostic attributes; adds data-type #2.
- **C3. State-of-the-Nation FY26 cereal report** — single 20-slide PDF + summary CSV referencing the macro trends + segmentation. Adds data-type #3.
- **C4. NSV waterfall seed** — `nsv_waterfall.csv` (brand × period × layer with Gross → Trade → NSV → COGS → A&P → Brand Contribution rows). Makes the masterclass's money slide queryable.
- **C5. Buying-committee personas** — six new persona files in `docs/personas/`: Nina Ortega (CMI Director), Robert Kim (VP Analytics), Audrey Vance (CMO), Helen Park-Choi (CFO), Lillian Park (Innovation Director), Veda Hollow (Data Governance / AI Risk).
- **C6. A canonical "Rachel" Sr Brand Manager persona** — closest analog is a fictional persona between Sage (Director) and Maya (Analyst). Anchor on the masterclass's Rachel-Tuesday schedule directly.

---

## 4. Per-scenario annotations — what each existing scenario already teaches against the masterclass

These are sticky-note additions for the existing scenario docs. None require schema changes.

### S1 — Louisiana Cereal Decline (v1)

| Masterclass concept it teaches | Where it lands in the scenario doc |
|---|---|
| The Chain (Data → Insight → Implication → Decision → Brief → Execution) | "Recovery plan" + "Recommendation to the board" sections — strong on Decision and Brief, weak on Execution loop-back. |
| Consumer / Shopper / Customer trichotomy | All three present (brand health = consumer; switching = shopper; Walmart facings = customer). Not named. |
| 5 metric levels | Hits Enterprise (revenue + share), Commercial (facings, OSA), Execution (DC fill). Misses Innovation. |
| Permanent tension | Short-term tactical (Rouses injection) vs long-term brand (pack refresh + media). Not named. |
| 5 failure modes for AI tools | "What would have caught this earlier" section is a direct hit on failure mode #5 ("adds a place to check, not a decision to land"). |

*Add a "Masterclass tags" footer to `docs/louisiana-decline.md`.*

### S2 — ProteinPeak Q2 Launch Read (v1)

| Masterclass concept it teaches | Where it lands |
|---|---|
| Decision moment #3 — Promo / Launch post-mortem | Full Week-4 read with trial, repeat, source-of-volume, cannibalization, channel split. |
| Innovation metric level | Trial × Repeat × Cannibalization × Incrementality. |
| AGM "Is the growth real or did we promo our way here?" | Source-of-volume waterfall directly answers this. |
| Buying committee | Sage (user), Audrey (sponsor), Helen Park-Choi (CFO challenge), Whitfield (board). Closest the dataset comes to mapping the chain. |

### S3 — Walmart Aug Line Review (v2 — Marcus)

| Masterclass concept it teaches | Where it lands |
|---|---|
| Decision moment #5 — JBP / JBR prep | Direct hit on Walmart line-review prep. |
| Customer (retailer) layer — what the retailer holds | Walmart's facing allocation, endcap monopoly by Larksfield (23 of 41 stores), delisting threat language. |
| Permanent tension — global consistency vs local relevance | Walmart South Division's regional sweetened-cereal index vs national reset. |
| 5 metric levels — Commercial | Velocity-per-facing, share of shelf, facing audit. |

### S4 — Kroger Q3 JBR (v2 — Priya)

| Masterclass concept it teaches | Where it lands |
|---|---|
| Decision moment #5 — JBP / JBR prep | Aisle-level pre-read with consumer-demand cuts. |
| Permanent tension — innovation gamble vs hero defence | Protein-forward + sugar-reduced + ancient-grain segments each pulling 2.3% / quarter from traditional family cereal. |
| Buying committee — Category Captain dynamic | Priya speaking on behalf of the category, not just Crunchwell, to Kroger. The "category insight is the gift they didn't ask for but need" line. |

### S5 — Tasha CFO Read (v2 — Retail Media + Trade Promo Effectiveness)

| Masterclass concept it teaches | Where it lands |
|---|---|
| The money waterfall (slide 7) | Best in the dataset — separates platform-reported ROAS from modeled incrementality. |
| AGM "Did margin hold against costs, retailers and inflation?" | Direct hit. The blended $0.64 incrementality ratio is the answer. |
| 5 metric levels — Enterprise + Commercial | $4.2M envelope, per-platform decomposition, $2.7M incremental. |
| Permanent tension — data richness vs decision speed | Marian's elasticity model `last_recalibrated=2026-04-15` as the gate. |

---

## 5. Recommended next-version plan

A pragmatic sequence that yields visible masterclass coverage with minimal schema churn:

| Version | Scope | Effort |
|---|---|---|
| **v0.7.0** (target: 2026-06-13) | Add S6 (Innovation Stage-Gate) + S9 (Walmart CR006 delisting threat) + C5 (six buying-committee personas) + C6 (Rachel Sr Brand Manager persona) + per-scenario masterclass-tags footers | 1 week |
| **v0.7.1** | Add S8 (September MBR Performance Dip) + C4 (NSV waterfall seed) | 3 days |
| **v0.8.0** | Add S7 (October JBP Walmart 2027) + S10 (forward supply scare) | 1 week |
| **v0.9.0** | Add S12 (annual category growth opportunity scan) + S11 (Q3 campaign post-mortem) + C1/C2/C3 (atmospheric data-type fills) | 1 week |

After v0.7.0, the dataset can fixture every concept in the masterclass to a queryable artifact. After v0.8.0, every one of the seven decision moments and all four breakout scenarios are scenarized. After v0.9.0, all six data types are present.

---

## 6. The single sentence to put on the README

*"The Acme synthetic dataset encodes the seven CPG decision moments (consumer sentiment, MBR/QBR, launch + campaign post-mortems, competitor response, JBP/JBR prep, innovation stage-gate, category growth scan) across the six CPG functions and the full money waterfall — so that any Clayface prototype, PRD, or demo can be fixtured against a real workflow, not an imagined one."*

That sentence is true after v0.9.0, not before. The work above is the path to making it true.

---

*Last updated: 2026-05-28 · Cross-walked against `CPG Fundamentals Masterclass` by Amit Singh (May 11, 2026 · 28 slides).*
