# Scenario 02 — ProteinPeak Q2 2026 Launch Read

*"Is Cinnamon Crunch landing, or are we just shipping in?"*

**Status:** Active demo scenario, May 12, 2026 · Internal · Confidential

---

## Trigger

It is the week of **May 18, 2026**. **ProteinPeak Cinnamon Crunch (PP005)** and **ProteinPeak Cocoa Almond (PP006)** went on shelf in Q2 — the two flagship innovations of the Wellness Hero pillar. The FY26 plan requires ProteinPeak to grow from **$48M → $80M (+66.7%)**; the two new flavors are doing most of the heavy lifting in that forecast.

**Sage Park** (Brand Director, ProteinPeak) needs a credible **Week-4 read** by Friday May 22 for Audrey Vance. Whitfield will ask about it directly in the **May 26 business review**. Hugo Lin is sitting on a **$4.2M [sample] retail-media budget** that will get throttled up or down based on what the read says.

## The question Maya gets

At **4:47 PM Thursday May 14**, Nina Ortega forwards an email from Sage:

> *"Maya — can you get me a Week-4 read for the new SKUs by EOD Friday? I need to know (1) trial vs. plan, (2) repeat curve compared to Berry Crunch, (3) cannibalization of Original Vanilla Almond, and (4) whether the Target endcap is doing more or less than the Amazon push. Slide-ready. Whitfield meeting Tuesday."*

## Stakeholders

| Person | Role | What they want |
|---|---|---|
| Sage Park | Brand Director, ProteinPeak | Defend the launch trajectory; justify Q3 spend |
| Audrey Vance | CMO | Decide whether to greenlight the next two flavors in stage-gate |
| Hugo Lin | Director Performance Marketing | Read the creator/retail-media response curve |
| Helen Park-Choi | CFO | "Show me the elasticity, not the spend" |
| Gregory Whitfield | CEO | Validate his Wellness Hero bet for the board |
| Soo-jin Lee | NAM Target | Wants ammunition for the next Target review |
| Tasha Brooks | Performance Marketing (Pacvue ops) | Defends the $4.2M retail-media pace |
| Theo Mannering | Supply Planning (SAP / shipments owner) | "Tell me what to ship next" |

The political dynamic: **Sage is Whitfield's golden child.** If Maya's read is soft on the launch, it goes through three rounds of "are you sure" before anyone acts. If it's overly rosy and Whitfield commits more spend that doesn't pay out, Maya's name is on the slide.

## Data Maya needs to pull

The Acme synthetic dataset mirrors the real-world data Maya would touch. Each row here maps to where the signal lives in the parquet artifacts.

| Source | What Maya pulls | Friction today | Parquet anchor |
|---|---|---|---|
| Circana (IRI) Unify | Weekly POS by SKU × DMA × channel, distribution build | API → CSV reshape | `epos`, `syndicated_weekly` |
| NielsenIQ Connect | TDP, ACV%, share within protein-cereal subcategory | Different SKU keys than Circana | `syndicated_weekly`, `category_market_size` seed |
| Numerator panel | New-buyer %, source-of-volume, repeat rate week-over-week | Slow query interface | `household_transactions` (Switching_Flag) |
| Amazon Vendor Central (via Anil/Dev) | ASIN-level sales, search rank, share of voice | Different system | `epos` (Amazon), `search_trends` (Helium 10) |
| Target.com / Stackline | Velocity, content score, paid-search position | Separate UI; Maya lacks seat | `epos` (Target.com), `perfect_store` Target rows |
| Profitero | Digital-shelf content score, OOS rate, review velocity | Yet another login | `product_reviews`, `data_freshness_log` |
| Pacvue | Retail-media spend pacing, ROAS by SKU | Owned by Tasha Brooks | `marketing_spend` seed Q2 row, `promo_events` PP-E014 |
| Brandwatch | Creator-driven sentiment, organic mention volume | Mention-level data | `social_mentions`, `creator_posts` |
| Internal SAP (via Theo) | Shipments-to-retailer (sell-in) | 3 days behind Circana | `shipments` |

## Today: the nightmare

Maya gets the email at **4:47 PM Thursday May 14**. Friday May 15 is a wash on the LA decline write-up.

She spends **Monday May 18 and Tuesday May 19** stitching: pull Circana, reshape, join to Numerator export, manually reconcile Amazon ASIN-to-SKU, copy Stackline screenshots, ping Tasha Brooks for the Pacvue pull, ping Theo Mannering for shipments, screenshot Brandwatch dashboards.

**Wednesday May 20** she builds the cannibalization view by hand in a pivot table — ProteinPeak Vanilla Almond Original (PP001) velocity dipped **11% [sample]** the week the new flavors launched. Is that incremental cannibalization, or seasonal, or distribution mix? She can't tell cleanly without a baseline.

**Thursday May 21** the slide comes together: trial, repeat, cannibalization, channel split. By the time Sage sees it, it is a **Week-6 read** delivered as Week-4. The Whitfield meeting was last Tuesday. Sage filled the gap with vibes.

Total Maya-hours: **~22 hours over six business days** [sample]. Sage gets a slide. Maya gets the next email at 4:47 PM Thursday.

## With Clayface

A **Launch Tracker workspace** lights up Day 14 with:

1. **Trial vs. plan curve** (panel + POS triangulated) for each new SKU.
   - *Data joined:* `epos` × `plan_vs_actual` × `syndicated_weekly` for SKUs PP005/PP006, weeks 1–4.
2. **Repeat-curve overlay** against ProteinPeak Berry Crunch (PP003) and Original Vanilla Almond (PP001) at the same week-since-launch — auto-fetched from the historical archive.
   - *Data joined:* `household_transactions` grouped by `Product_SKU` and weeks-since-launch.
3. **Source-of-volume waterfall** showing % of buyers new to ProteinPeak vs. switching from Original — with a confidence band, not a single number.
   - *Data joined:* `household_transactions.Switching_Flag` distribution (`New_To_Brand` / `Cannibalization` / `Competitor_Switch`).
4. **Channel split** (Target endcap vs. Amazon vs. mass) with retail-media spend overlay from Pacvue.
   - *Data joined:* `epos` and `perfect_store` by `Banner`, overlaid with `marketing_spend.csv` Q2 ProteinPeak rows.
5. **Generated "so what" narrative**:
   > *"Trial is at 113% of plan in Target stores with endcap support, 78% of plan in Walmart-pilot. Repeat at Week 2 is tracking 1.2× Berry Crunch — strong. Cannibalization on Vanilla Almond Original is real but bounded at ~6% steady-state. Recommended action: hold spend on Amazon, lean in on Target endcap renewal."*

The tracker refreshes every Monday at 6 AM. Maya touches it only to validate; the slide is half-built when she opens it.

**Time-to-insight:** Day 14, not Day 42. **Maya-hours per refresh:** ~1 hour to review and add color [sample]. The Whitfield meeting now happens with a real read.

## Clayface surfaces involved

- **Insights Feed:** Week-4 anomaly card surfacing the cannibalization signal automatically.
- **Workspace ("ProteinPeak Q2 Launch"):** Persistent, Mission-anchored, with Chat + Activity defaults.
- **Analytics Canvas:** The trial/repeat/source-of-volume views with confidence overlays.
- **Drop-into-deck:** One-click export of the four key charts into a board-grade slide.
- **AI orchestration:** Generated narrative grounded in source-of-record data with provenance links.

## Why this scenario lands

This is the **innovation-launch reading** pattern — the single most common high-stakes question in a CPG insights team's quarter. Every brand launches things. Every launch needs a read at Week 4, Week 8, Week 13. Today, every read is a fire drill. Clayface turns it into a maintained surface.

It also dramatizes a specific Clayface differentiator: the *historical archive*. Comparing Cinnamon Crunch's repeat curve to Berry Crunch's at the same week is trivially valuable and almost no incumbent does it well, because the underlying datasets have changed schema versions and no one ever reconciles them. Clayface's semantic layer makes the comparison one-click.

## Suggested demo storyboard

1. **Cold open:** Maya gets Sage's 4:47 PM email. Show the email, show the nine tabs she'd open today.
2. **Cut to Monday:** Insights Feed already has a "ProteinPeak Cinnamon Crunch — Week 4 read available" card.
3. **Click in:** the Launch Tracker workspace opens with the four core views pre-rendered.
4. **The reveal:** the repeat curve overlay against Berry Crunch — *"this is the chart Maya would have spent six hours building"*.
5. **The action:** Maya types in chat *"draft a 4-slide read for Sage focused on cannibalization and channel split"* — drop-into-deck does the rest.
6. **The compounding loop:** every Monday at 6 AM, the workspace updates itself. Maya's first task on Monday is no longer "stitch" — it's "decide."

---

*Related: [`02-launch-data-model.md`](./02-launch-data-model.md) (encoding map) · [`03-hypothesis-tree.md`](./03-hypothesis-tree.md) (evidence) · [`05-personas-supplement.md`](./05-personas-supplement.md) (Sage/Hugo/Helen)*
