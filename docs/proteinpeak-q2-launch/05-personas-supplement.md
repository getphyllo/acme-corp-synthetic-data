# Persona Supplement — Q2 ProteinPeak Launch Cast

The four core personas live in `docs/personas/`. This supplement adds the launch-specific stakeholders the scenario depends on and overlays Maya's calendar for the Week-4 read window. Where a person already exists in the canonical persona files, only the launch-specific behavior is captured here.

---

## Sage Park — Brand Director, ProteinPeak

**Role:** Brand Director of the ProteinPeak franchise. Reports to Cory Whitman (VP Brand, Wellness & Snacks); Cory reports to Audrey Vance (CMO).

**Background:** Former pro track & field athlete; founded a small wellness-snack brand before Acme acquired it in 2023 and made her Brand Director. She is **Whitfield's "golden child"** — the visible face of Acme's Wellness Hero pillar bet for the board.

**What she wants from the Week-4 read:**
- Defensible numbers she can use to justify $4.2M+ of Q3 retail-media (Hugo Lin's budget).
- A green light from Audrey on the next two flavors (Stage-Gate for Q4 2026).
- Slide-ready material for the Whitfield May 26 business review.

**How she treats Maya:** Sage assumes Maya works for ProteinPeak. Maya does not. The political friction is the source of Maya's "ProteinPeak-Crunchwell tension" pain point (see `docs/personas/01-maya-chen-analyst.md` line 111).

**What she'd say in a meeting:**
- *"Don't bury the channel signal in the appendix — Audrey only reads slide 1."*
- *"If repeat is above 1.0× Berry Crunch I want that as the headline."*
- *"Tell Hugo to keep the Roundel hot through July."*

**Active creator partnerships (her cohort):**
- **CR-0012 @sage_park_athlete** — signature anchor (her own old training partner)
- **CR-0007 @gymrat.miles** — cohort 1, ProteinPeak ambassador
- **CR-0021 @runnerwithprotein** — cohort 2
- **CR-0040 @runfastfueled** — cohort 2
- **CR-0042 @quickprotein** — cohort 2 (Sage Park alumni)
- **CR-0013 @nick_wellbeing** — newly-activated Q2 2026

---

## Hugo Lin — Director, Performance Marketing

**Role:** Owns Acme's retail-media and paid-social practice across all brands. Reports to Audrey Vance.

**Background:** Came from a digital agency (Wpromote). Built Acme's first Retail Media Center of Excellence in 2024. Operationally close to Tasha Brooks (his Pacvue ops lead).

**What he wants from the Week-4 read:**
- ROAS by SKU × channel so he can decide where to push the remaining $3M of Q2 retail-media.
- Creator-driven attribution evidence to defend the Sage cohort investment to Helen Park-Choi (CFO).

**How he treats Maya:** Hugo respects Maya. He sends CSVs in his own schema (a Maya pain point from Monday May 11). He is not a fast Slack responder but always answers within 24 hours.

**Key view he opens first:** Pacvue ROAS by retailer × SKU for the prior 7 days.

---

## Helen Park-Choi — CFO

**Role:** Chief Financial Officer, Acme Corp. Reports to Whitfield. New to Acme — joined Q4 2025.

**Background:** Came from PepsiCo Frito-Lay finance. Brings a "show me elasticity, not spend" discipline that the previous CFO didn't.

**What she wants from the Week-4 read:**
- Net incremental revenue from PP005+PP006 *after* cannibalization of PP001, expressed in $M not %.
- The elasticity number (already provisional in `seeds/sku_elasticity_estimates.csv` — -1.18 at Target).
- A defensible base-case forecast for FY26 ProteinPeak vs the $80M plan.

**What she'd say:** *"Trial is a vanity metric. Show me what fraction of the $24M plan we're locked into based on first 4 weeks of repeat data."*

**She is also the Hugo Lin restraint** — she will challenge Hugo's recommendation to lean Q3 spend into Target Roundel unless the marginal-ROAS math is clean.

---

## Tasha Brooks — Performance Marketing Operations (Pacvue lead)

**Role:** Reports to Hugo Lin. Runs the day-to-day operations of Acme's Pacvue seat. Owns retail-media spend pacing and ROAS reporting.

**Background:** Internal Acme employee, came up through Crunchwell brand operations before moving to Performance Marketing. Operational, not strategic.

**What she wants from the Week-4 read:**
- A simple "GO / HOLD / PAUSE" call on each retail-media line item so she can adjust Pacvue pacing on Monday morning.

**Maya's interaction with her:** Maya pings Tasha on Mondays to pull Pacvue spend export. Tasha typically returns the file within 2 hours but in a different schema than Maya's reports use — another stitch-time loss.

---

## Theo Mannering — Director, Supply Planning

**Role:** Owns the SAP outbound shipment feed and runs allocation planning for new launches. Reports to Devraj Patel (E-Comm + Supply); Devraj reports to Robert Kim (VP IT) on a dotted line.

**Background:** 15-year supply chain veteran; came from Kraft Heinz. Conservative on allocation; runs hot on hurricane-season scenarios after the Hurricane Tonya fallout.

**What he wants from the Week-4 read:**
- Sell-through vs sell-in by retailer for PP005 + PP006 so he can adjust the next 8 weeks of Battle Creek production allocation.
- Early warning on weeks-of-supply outliers (Walmart-pilot is at 9 weeks — too high; Target is at 5 weeks — about right).

**Operational reality:** Theo's SAP shipment data is **3 days behind** Circana POS. The lag is the source of the "is the read a Week-4 or a Week-6 read" tension in the scenario.

---

## Soo-jin Lee — NAM Target (existing in retailers.csv)

The Q2 launch is the **single most important read** for Soo-jin's August Target line review. If Cinnamon Crunch + Cocoa Almond hold trial at 113% through Week 8, she can ask for two more facings and a Q4 endcap renewal. If trial falls below 100% by Week 6, she has to defend the existing facings.

She does not have direct access to Stackline (Acme's Target.com data tool) — Maya runs that query for her.

---

## Maya Chen — Calendar overlay for the Week-4 read week (May 18–22, 2026)

This is the week immediately after the Louisiana decline board read (May 28 is the next big day on her LA calendar). Sage's email at 4:47 PM Thursday May 14 forces a context switch.

### Monday May 18 (in-office, Battle Creek)
- **6:00 AM** — Up, run 5 miles (taper week).
- **8:30 AM** — Arrives Battle Creek. Three new Slack messages.
- **9:00 AM** — Pulls Circana POS for PP005/PP006 — has to manually reconcile ASIN-to-SKU for Amazon (Anil Mehra hasn't standardized the mapping).
- **10:00 AM** — Insights team standup. Nina: "How long for the Sage read?" Maya: "EOD Friday is tight if I'm also closing the LA recovery one-pager."
- **11:00 AM** — Slack DM to Tasha Brooks: *"Can you pull Pacvue ROAS by SKU × retailer for the Sage read?"*
- **2:00 PM** — Builds initial trial-vs-plan chart in Tableau. Realizes the FY26 plan-by-month wasn't fully encoded in `plan_vs_actual` for the launch SKUs — has to ping the Sales Finance team.

### Tuesday May 19 (WFH)
- **7:30 AM** — Standup with Priya on the LA recovery deck for Diane.
- **9:00 AM** — Switches to ProteinPeak. Builds the repeat-curve overlay vs Berry Crunch. **This is the four-hour chart** — has to query Numerator HH transactions, roll up week-since-launch, join PP003 historical data, validate against `product_reviews`.
- **2:00 PM** — Tasha responds with the Pacvue export. Different schema. Maya re-shapes for 40 minutes.
- **4:00 PM** — Sketches the source-of-volume waterfall. Realizes she needs to talk to Hugo to confirm the attribution methodology for "competitor switch" — does it count anyone who bought Magic Spoon in the prior 12 weeks, or 4 weeks?

### Wednesday May 20 (in-office)
- Builds the channel-mix bubble chart. Theo Mannering returns the SAP weeks-of-supply data at 3 PM. Walmart-pilot is at 9 weeks of supply — that's the chart's biggest visual.
- 5 PM: Drafts the deck outline. Sends to Nina at 6:30 PM.

### Thursday May 21 (in-office)
- Nina's edits land at 7 AM. Two rounds with Sage.
- 11 AM: Sage calls Maya directly. *"Can you lead the slide-1 talk-through with Whitfield? I want you in the room."*
- 4 PM: Final deck. Sends to Sage, Audrey, Hugo, Helen, Soo-jin, Theo cc'd.

### Friday May 22 (WFH)
- The deck is the read. Maya gets two thumbs-up replies and one terse Helen Park-Choi reply: *"Slide 3 — what's the elasticity at 12% cannibalization?"* — which is the **appendix question Maya already prepared for** (A4).
- 5 PM: Logs off. Tries to read a novel.

### Tuesday May 26 — the meeting
- Maya stands at the back. Sage presents. Whitfield's only question lands on slide 4 — *"Why is Walmart-pilot soft if Cinnamon is a Walmart-shopper flavor?"* — and Sage defers to Maya. Maya answers in 90 seconds. Whitfield: *"OK. Lean into Target."*

This is the loop Clayface is built to compress.
