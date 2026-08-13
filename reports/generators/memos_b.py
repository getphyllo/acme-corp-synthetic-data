"""DOCX documents 71-80 — functional memos, minutes, briefs and playbooks.
Run: python generators/memos_b.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import (money, chart_line, chart_bar, chart_grouped, chart_stacked,
                 chart_waterfall, chart_donut)
from docx_lib import Memo
import qlib as q


# ============================================ 71 · Trade reallocation defence ==
def r71_trade_reallocation_defence():
    m = Memo("71-h2-2026-trade-spend-reallocation-memo-to-cfo.docx",
             kicker="FUNDING MEMORANDUM",
             title="H2 FY2026 Trade Spend Reallocation — The Case",
             subtitle="Why we are moving $2.4M a quarter inside the trade budget rather than "
                      "asking for more of it",
             byline="RGM Lead with Trade Finance",
             meta=["To: CFO · cc VP Sales NA", "Period: Q3–Q4 FY2026",
                   "Companion documents: Reports 54 and 64", "Version: v1 · July 2026"],
             short="Trade reallocation",
             doc_type="Internal funding memorandum")

    ev = q.trade_events_raw()
    bymech = q.trade_events("mechanic")
    byret = q.trade_events("retailer")
    tb = q.trade_brand()
    el = q.elasticity()

    tot_sp = ev.spend_kusd.sum() / 1000
    tot_inc = ev.incremental_revenue_kusd.sum() / 1000
    idx = ev.modeled_incrementality_index.mean()

    m.at_a_glance([(f"${tot_sp:.1f}M", "Q1 trade spend"), (f"{idx:.2f}", "incrementality index"),
                   ("$2.4M", "quarterly reallocation"), ("$0", "incremental budget requested")])

    m.h1("THE ASK", "1 · What we are asking you to approve")
    m.lede("No new money. A different mix, with a floor under event quality and a cap over depth.")
    m.body(
        f"In Q1 FY2026 we ran {len(ev)} promoted events costing ${tot_sp:.1f}M and generating "
        f"${tot_inc:.1f}M of modelled incremental revenue — an incrementality index of {idx:.2f}. "
        "Applying a 0.45 index floor to that calendar would have removed the lowest-returning "
        "mechanics and freed roughly $2.4M a quarter for feature-and-display weight, which indexes "
        "higher on every brand we run it on. We are asking for approval of the reallocation and the "
        "guardrails, not for additional trade budget.")

    m.h1("THE EVIDENCE", "2 · Where the money currently goes to die")
    bymech8 = q.roll_up(bymech, "mechanic", 8, sum_cols=("events", "spend", "inc"),
                        mean_cols=("lift", "idx"), other="All other mechanics")
    mrows = [[r.mechanic, f"{int(r.events)}", money(r.spend / 1000, dp=1), f"{r.lift:.1f}%",
              f"{r.idx:.2f}", "Keep" if r.idx >= 0.45 else "Stop"] for r in bymech8.itertuples()]
    m.table(["Mechanic", "Events", "Spend", "Avg modelled lift", "Index", "Call"], mrows,
            widths=[0.28, 0.11, 0.15, 0.19, 0.12, 0.15], size=9.0,
            note="Source: seed_trade_promo_events_q1_2026, grouped by mechanic.")
    ch = chart_bar("r71_mech.png", [str(x)[:16] for x in bymech8.mechanic],
                   [float(x) for x in bymech8.idx],
                   title="Modelled incrementality index by mechanic, Q1 FY26",
                   colors_list=["#2E7D75" if v >= 0.55 else ("#B98A2E" if v >= 0.45 else "#B24A2E")
                                for v in bymech8.idx])
    m.image(ch, "The spread between mechanics is wide enough that mix, not budget, is the lever.")

    m.h1("THE MECHANISM", "3 · Why depth is the wrong instrument for our packs")
    m.body(
        f"Our most promoted packs are also our most elastic. {el.sku_name.iloc[0]} at "
        f"{el.retailer.iloc[0]} carries an elasticity of {el.elast.iloc[0]:.2f}, and the next four "
        "most elastic points in the portfolio are all Crunchwell Mega and Multigrain packs at Rouses "
        "and Walmart — the two banners where Larksfield has been most aggressive on endcaps in "
        "Louisiana. Deep discounting on those packs buys volume at a permanent cost to the reference "
        "price, which is a mechanism in the Louisiana base erosion rather than a defence against it.")
    erows = [[r.sku_name[:34], r.retailer, f"{r.elast:.2f}", f"${r.price:.2f}", f"{r.conf:.2f}"]
             for r in el.head(8).itertuples()]
    m.table(["SKU", "Retailer", "Elasticity", "Baseline price", "Model confidence"], erows,
            widths=[0.34, 0.18, 0.16, 0.16, 0.16], size=9.0,
            note="Source: seed_sku_elasticity_estimates.")

    m.h1("THE MOVE", "4 · Where the $2.4M goes")
    m.table(["From", "$M/quarter", "To", "$M/quarter", "Expected index"],
            [["Sub-0.45 mechanics across all brands", "−2.4", "Feature-and-display weight, "
              "top-5 retailers", "+1.5", "0.62"],
             ["", "", "Louisiana recovery trade at capped depth", "+0.6", "0.58"],
             ["", "", "ProteinPeak display support (no depth)", "+0.3", "0.70"],
             ["Net", "−2.4", "", "+2.4", "Portfolio 0.52 → 0.60"]],
            widths=[0.30, 0.13, 0.30, 0.13, 0.14], total_row=True, align_right_from=1, size=9.0,
            note="Planning estimate. Index expectations from comparable Q1 mechanics in "
                 "seed_trade_promo_events_q1_2026.")
    m.callout("What this is worth",
              "Moving the portfolio index from 0.52 to 0.60 on a $146M annual trade base is worth "
              "approximately 60 basis points of EBITDA — the largest single margin lever in the FY27 "
              "plan that does not touch A&P, headcount or list price.", "win")

    m.h1("OBJECTIONS", "5 · The three arguments against, answered")
    m.bullets([
        "**\"Cutting depth loses volume.\"** It loses some promoted volume and keeps base volume. The "
        "index is precisely the measure of how much of the promoted volume was incremental — at 0.52, "
        "about half of what we lose was never ours to gain.",
        "**\"Retailers will not accept it.\"** Feature and display are what retailers actually want in "
        "a category with declining units; both build category dollars. We are taking that case into "
        "the August Walmart line review (Report 77) as a joint growth argument.",
        "**\"We need the depth to defend Louisiana.\"** Louisiana lost 340 basis points primarily "
        "because we lost facings, not because we lost price competitiveness. The recovery plan leads "
        "with shelf, not with depth (Report 76).",
    ])

    trows = [[r.brand, money(r.spend_m), f"{r.depth:.1f}%", f"{r.incr:.2f}",
              "≤20%" if r.brand == "Crunchwell" else ("≤10%" if r.brand == "ProteinPeak" else "≤15%")]
             for r in tb.itertuples()]
    m.h1("BASELINE", "6 · Where each brand starts")
    m.table(["Brand", "FY25 trade spend", "Average depth", "Index", "FY27 cap"], trows,
            widths=[0.24, 0.22, 0.18, 0.14, 0.22],
            note="Source: seed_trade_spend_fy25.")

    m.recommendations([
        ("Approve the $2.4M/quarter reallocation inside the existing trade budget", "CFO", "By Aug 1"),
        ("Approve the 0.45 index floor and the depth caps as policy (Report 64)", "CFO", "Aug 1 2026"),
        ("Rebuild the Q3 and Q4 calendars against the floor", "NAM team / Trade Finance", "By Aug 15"),
        ("Report portfolio and brand index monthly alongside spend", "Trade Finance", "From August"),
    ])
    m.signoff([("CFO", "the reallocation and the guardrails"),
               ("Diane Halverson, VP Sales NA", "customer-facing execution of the caps")])
    return m.build()


# ==================================================== 72 · S&OP minutes ========
def r72_sop_minutes():
    m = Memo("72-q2-2026-sop-ibp-cycle-minutes-decision-log.docx",
             kicker="MEETING MINUTES & DECISION LOG",
             title="Q2 FY2026 S&OP / IBP Executive Cycle",
             subtitle="Consensus number, constraints, decisions taken and actions carried forward",
             byline="S&OP Lead (chair) · minuted by Demand Planning",
             meta=["Meeting: July 2026 executive S&OP review",
                   "Attendees: CFO, VP Supply Chain, VP Sales NA, VP Brand, Demand Planning, FP&A",
                   "Companion deck: Report 52"],
             short="Q2 FY26 S&OP minutes",
             doc_type="Internal meeting record")

    pm = q.pva_month()
    p2, a2, v2 = q.pva_total(q.Q2)
    fill = q.fill_month("2025-09-01")
    cuts = q.cut_reasons("2025-10-01")
    pipe = q.pipeline()

    m.at_a_glance([("$379M", "consensus H2 number"), (f"{v2:+.1f}%", "Q2 QTD vs plan"),
                   (f"{float(fill.fill.iloc[-1]):.1f}%", "fill rate"), ("5", "decisions taken")])

    m.h1("ATTENDANCE & PURPOSE", "1 · Cycle summary")
    m.body(
        "The July cycle reconciled the demand, supply and financial plans for Q3 and Q4 FY2026 and "
        "agreed a single consensus number. Two constraints were tabled and both were resolved within "
        "the cycle. No items were escalated beyond this meeting.")
    m.table(["Review step", "Owner", "Outcome"],
            [["Demand review", "Demand Planning", "Unconstrained forecast $384M for H2"],
             ["Supply review", "VP Supply Chain",
              "Service fully recovered; changeover capacity flagged as the binding constraint"],
             ["Product / innovation review", "VP Brand",
              "Three launches inside the horizon; Pack Refresh confirmed for Aug 15"],
             ["Reconciliation", "S&OP Lead", "Consensus $379M; $3M gap held as management risk"],
             ["Management review", "CFO", "Consensus accepted; five decisions taken"]],
            widths=[0.26, 0.22, 0.52], align_right_from=9, size=9.0)

    m.h1("DEMAND", "2 · Demand review")
    m.body(
        f"Q2 through May delivered {money(a2)} against {money(p2)} of plan ({v2:+.1f}%), with the "
        f"monthly gap narrowing from {float(pm['var'].min()):+.1f}% in February to "
        f"{float(pm['var'].iloc[-1]):+.1f}% in May. Demand Planning presented an unconstrained H2 "
        "forecast of $384M built off the May run-rate plus the Pack Refresh and full-quarter "
        "ProteinPeak distribution.")
    ch = chart_line("r72_month.png", list(pm.Period),
                    {"Plan ($M)": [float(x) for x in pm.plan],
                     "Actual ($M)": [float(x) for x in pm.act]},
                    title="FY2026 monthly revenue, plan versus actual ($M)")
    m.image(ch, "The basis for the H2 build: May's actual held flat, not the original plan.")
    m.body(
        "**Challenge from Finance:** whether the forecast assumes Louisiana recovery. **Response:** "
        "it does not — no recovery beyond the ~35 basis points already measured in Q2 is built in. "
        "**Accepted.**")

    m.h1("SUPPLY", "3 · Supply review")
    m.body(
        f"Fill rate stands at {float(fill.fill.iloc[-1]):.1f}% and OTIF at "
        f"{float(fill.otif.iloc[-1]):.1f}%, fully recovered from the November 2025 storm trough. The "
        "binding constraint for H2 is the Pack Refresh changeover in weeks 33 to 35, which consumes "
        "Battle Creek line capacity and will depress base-SKU fill for approximately two weeks.")
    crows = [[r.reason, f"{r.cut_k:,.1f}K", f"{r.fill:.1f}%", f"{int(r.lines):,}"]
             for r in cuts.itertuples()]
    m.table(["Cut reason", "Units cut", "Fill on those lines", "Order lines"], crows,
            widths=[0.34, 0.22, 0.26, 0.18], size=9.0,
            note="Source: shipments, order lines since October 2025.")
    m.callout("Point raised by VP Sales NA",
              "Launch_Allocation cuts are a deliberate choice to protect launch fill, but they "
              "currently surface to customers as a service miss. Agreed action: make them a visible "
              "line in the demand plan from the next cycle.", "action")

    m.h1("PRODUCT", "4 · Innovation review")
    prows = [[r.concept_name[:38], r.brand, r.stage_gate, str(r.planned_launch_date),
              q.musd(r.projected_revenue_year1_musd)]
             for r in pipe[pipe.stage_gate.isin(["Stage-6 In-Market", "Stage-5 Launch Prep",
                                                 "Stage-4 Pre-Launch"])].itertuples()]
    m.table(["Concept", "Brand", "Stage", "Planned launch", "Year-1"], prows,
            widths=[0.34, 0.16, 0.20, 0.16, 0.14], align_right_from=3, size=9.0,
            note="Source: seeds/innovation_pipeline.csv.")

    m.h1("RECONCILIATION", "5 · From $384M to $379M")
    m.table(["Step", "H2 $M", "Raised by"],
            [["Unconstrained demand forecast", "384.0", "Demand Planning"],
             ["Less: Pack Refresh changeover phasing", "−2.5", "VP Supply Chain"],
             ["Less: ProteinPeak allocation at Walmart", "−1.5", "VP Supply Chain"],
             ["Less: HoneyNest and RootDay discontinuations", "−1.6", "VP Brand"],
             ["Plus: retail-media reallocation upside", "+0.6", "CFO"],
             ["Consensus H2 number", "379.0", "S&OP Lead"]],
            widths=[0.50, 0.18, 0.32], total_row=True, align_right_from=1, size=9.0)

    m.decisions([["Adopt $379M as the H2 consensus number; hold the $3M gap as management risk",
                  "CFO", "Jul 2026", "Action"],
                 ["Protect Pack Refresh changeover capacity ahead of base-SKU fill in weeks 33–35",
                  "VP Supply Chain", "Aug 1", "Action"],
                 ["Pre-agree the ProteinPeak allocation rule if Walmart authorises early",
                  "Supply Chain / Sage Park", "Aug 15", "Action"],
                 ["Make Launch_Allocation cuts a visible demand-plan line", "Demand Planning",
                  "Next cycle", "Action"],
                 ["Release the $700K retail-media reallocation", "CFO / Tasha Brooks", "Aug 1",
                  "Action"]])

    m.h1("ACTIONS", "6 · Carried forward to the August cycle")
    m.table(["#", "Action", "Owner", "Due"],
            [["1", "Pre-build Pack Refresh hero SKUs in weeks 31–32", "VP Supply Chain", "Jul 31"],
             ["2", "Communicate changeover fill impact to top-10 customers", "Customer Logistics",
              "Aug 1"],
             ["3", "Publish the allocation rule for ProteinPeak", "Supply Chain", "Aug 15"],
             ["4", "Add Launch_Allocation to the demand-plan template", "Demand Planning",
              "Next cycle"],
             ["5", "Report reallocation in-flight incrementality at week 8", "Hugo Lin", "Oct 2026"]],
            widths=[0.06, 0.54, 0.24, 0.16], align_right_from=3, size=9.5)
    return m.build()


# ================================================ 73 · Supply after-action =====
def r73_storm_after_action():
    m = Memo("73-hurricane-tonya-supply-after-action-review.docx",
             kicker="AFTER-ACTION REVIEW",
             title="Hurricane Tonya — Supply Disruption After-Action Review",
             subtitle="What happened, what it cost us in share, what we did well and the five "
                      "things we will do differently",
             byline="VP Supply Chain with Customer Logistics and Category Insights",
             meta=["Event: November 2025 · Review completed July 2026",
                   "Scope: Houston, Thibodaux and Tyler DCs; Louisiana and Texas DMAs",
                   "Companion deck: Report 53"],
             short="Tonya after-action",
             doc_type="Internal after-action review")

    fill = q.fill_month("2025-08-01")
    cuts = q.cut_reasons("2025-10-01")
    dc = q.fill_dc("2025-10-01")
    rouses = q.rouses_oos()
    la = q.share_quarter(la=True)

    trough = fill.loc[fill.fill.idxmin()]

    m.at_a_glance([(f"{float(trough.fill):.1f}%", f"fill trough ({trough.mo})"),
                   ("2 quarters", "time to full recovery"),
                   ("≈12%", "share of the LA decline attributed"),
                   ("5", "changes committed")])

    m.h1("SUMMARY", "1 · What happened")
    m.lede("A two-week weather event produced a two-quarter service recovery and a permanent share "
           "loss. The recovery speed, not the event, is what we are reviewing.")
    m.body(
        f"Hurricane Tonya made landfall in November 2025. Fill rate across the affected network fell "
        f"to {float(trough.fill):.1f}% in {trough.mo}, driven by storm cuts at the Houston, "
        "Thibodaux and Tyler DCs, with production lag and quality-hold cuts compounding it over the "
        "following weeks. Service returned to normal levels — approximately 95% fill and 90% OTIF — "
        f"by Q1 and Q2 FY2026, a recovery of roughly two quarters.")
    m.body(
        f"Over the same window, Crunchwell's Louisiana share fell from {la.cw.iloc[1]:.2f}% to a "
        f"trough of {la.cw.min():.2f}%. Root-cause attribution assigns approximately 12% of the "
        "340 basis point decline to the supply event, behind the Walmart facing reset (≈55%) and "
        "Larksfield promotional intensity (≈20%). The supply event was not the largest cause, but it "
        "was the one entirely within our control.")

    ch = chart_line("r73_fill.png", list(fill.mo),
                    {"Fill rate (%)": [float(x) for x in fill.fill],
                     "OTIF (%)": [float(x) for x in fill.otif]},
                    title="Fill rate and OTIF by month (%) — through the event and recovery",
                    pct=True)
    m.image(ch, "The trough is sharp; the recovery is slow. The slope on the right-hand side is what "
                "this review is about.")

    m.h1("THE COST", "2 · What it cost")
    m.table(["Consequence", "Measure", "Source"],
            [["Fill-rate trough", f"{float(trough.fill):.1f}% in {trough.mo}", "shipments"],
             ["Storm-cut units", f"{float(cuts[cuts.reason=='Storm'].cut_k.iloc[0]):,.1f}K",
              "shipments, Cut_Reason = Storm"],
             ["Compounding cut reasons", "Production_Lag and Quality_Hold both elevated post-event",
              "shipments"],
             ["Share attributed to supply", "≈12% of the 340 bps Louisiana decline",
              "Root-cause attribution (Report 58)"],
             ["Residual door-level effect",
              f"{len(rouses[rouses.osa < 70])} audited Rouses doors still below 70% OSA in 2026",
              "seed_rouses_oos_by_door"]],
            widths=[0.28, 0.44, 0.28], align_right_from=9, size=9.0)
    m.callout("The finding that matters most",
              "Warehouse fill recovered months before store shelves did. Fourteen audited Louisiana "
              "doors were still below 70% on-shelf availability well into 2026, every one of them "
              "next to a Larksfield endcap. We measured our recovery at the DC and declared victory "
              "before the shelf agreed.", "risk")

    drows = [[r.dc, f"{r.fill:.1f}%", f"{r.otif:.1f}%", f"{int(r.lines):,}"]
             for r in dc.itertuples()]
    m.h1("BY DC", "3 · Where the damage concentrated")
    m.table(["Retailer DC", "Fill", "OTIF", "Order lines"], drows,
            widths=[0.46, 0.18, 0.18, 0.18], size=9.0,
            note="Source: shipments, October 2025 onward, ranked by fill ascending.")

    m.h1("WHAT WENT WELL", "4 · Three things worth keeping")
    m.bullets([
        "**Allocation discipline held.** When capacity was short we protected the hero SKUs and the "
        "top-volume accounts rather than spreading the shortfall evenly. That was the right call and "
        "it is now the documented default.",
        "**Cut-reason coding stayed clean throughout.** Storm, Production_Lag and Quality_Hold were "
        "coded distinctly, which is the only reason this review can attribute anything at all.",
        "**Cross-functional escalation worked in week one.** Supply, Sales and Brand were in the same "
        "room within 48 hours of landfall.",
    ])

    m.h1("WHAT DID NOT", "5 · Four things that failed")
    m.bullets([
        "**We measured recovery at the wrong level.** DC fill returned to normal while store OSA did "
        "not, and nothing in our reporting surfaced the gap.",
        "**Store-level recovery had no owner.** Once fill recovered, the event was closed at the "
        "supply end and nobody owned the shelf.",
        "**We did not contest the competitive response.** Larksfield took endcap space during the "
        "outage and kept it. There was no plan for winning it back.",
        "**No pre-positioning plan existed.** The Houston and Tyler DCs serve a hurricane-exposed "
        "region and held no seasonal buffer.",
    ])

    rrows = [[r.sku_name[:30], r.city, f"{r.osa:.0f}%", f"{int(r.oos_days)}", str(r.lf_endcap)]
             for r in rouses.head(9).itertuples()]
    m.h1("EVIDENCE", "6 · The door-level residue, months later")
    m.table(["SKU", "City", "OSA", "Q1 2026 OOS days", "Larksfield endcap"], rrows,
            widths=[0.32, 0.20, 0.14, 0.20, 0.14], size=9.0,
            note="Source: seed_rouses_oos_by_door.")

    m.h1("CHANGES", "7 · The five commitments")
    m.table(["#", "Change", "Owner", "In place by"],
            [["1", "Pre-position seasonal inventory at Houston and Tyler from week 32 each year",
              "VP Supply Chain", "Aug 15 2026"],
             ["2", "Recovery is measured at store OSA, not DC fill; both reported until OSA recovers",
              "Customer Logistics", "Sep 1 2026"],
             ["3", "Named store-recovery owner appointed at the start of any service event, "
              "separate from the supply owner", "VP Supply Chain / VP Sales NA", "Immediate"],
             ["4", "Competitive shelf-response plan is part of the service-event playbook",
              "Marcus Boudreaux", "Sep 1 2026"],
             ["5", "Alternate DC routing pre-agreed with the top five Southern customers",
              "Customer Logistics", "Oct 1 2026"]],
            widths=[0.06, 0.52, 0.24, 0.18], align_right_from=3, size=9.0)

    m.recommendations([
        ("Adopt the five changes as standing supply-chain policy", "VP Supply Chain", "By Sep 1"),
        ("Fund third-party merchandising in the 14 worst Louisiana doors for 12 weeks",
         "Customer Logistics", "From Aug 1"),
        ("Add store-level OSA to the monthly service scorecard for the top-100 volume stores",
         "Customer Logistics", "By Sep 1"),
        ("Re-run this review against the 2026 hurricane season", "VP Supply Chain", "January 2027"),
    ])
    m.signoff([("VP Supply Chain", "the findings and the five changes"),
               ("Diane Halverson, VP Sales NA", "the store-recovery ownership model")])
    return m.build()


# ================================================== 74 · MMM readout memo ======
def r74_mmm_readout():
    m = Memo("74-h1-2026-media-effectiveness-readout-h2-reallocation.docx",
             kicker="MEASUREMENT READOUT",
             title="H1 FY2026 Media Effectiveness and the H2 Reallocation",
             subtitle="What modelled incrementality says about each platform, and the $700K we are "
                      "moving because of it",
             byline="Hugo Lin, Director — Performance Marketing, with Tasha Brooks",
             meta=["Period: Q1 FY2026 measured; H2 FY2026 recommended",
                   "Companion deck: Report 55 · Governance: Report 75",
                   "Version: v1 · July 2026"],
             short="H1 FY26 MMM readout",
             doc_type="Internal measurement readout")

    rm = q.retail_media()
    rmb = q.retail_media_brand()
    per = q.mkt_by_period()
    cw = q.mkt_spend("Crunchwell")
    pp = q.mkt_spend("ProteinPeak")
    ratio = rm.inc_m.sum() / rm.spend_m.sum()
    amz = rm[rm.platform == "Amazon Ads"].iloc[0]
    wmt = rm[rm.platform == "Walmart Connect"].iloc[0]

    m.at_a_glance([(f"${ratio:.2f}", "blended incremental per $1"),
                   (f"{wmt.ratio:.2f}", "best platform ratio"),
                   (f"{amz.ratio:.2f}", "worst platform ratio"),
                   ("$700K", "recommended move")])

    m.h1("THE READ", "1 · The average hides the decision")
    m.lede(f"${ratio:.2f} of modelled incremental revenue per dollar is an acceptable blended number "
           "produced by two platforms subsidising two others.")
    m.body(
        f"Q1 FY2026 retail media spent ${rm.spend_m.sum():.1f}M and returned "
        f"${rm.inc_m.sum():.2f}M of modelled incremental revenue. Inside that, Walmart Connect "
        f"returned {wmt.ratio:.2f} per dollar on ${wmt.spend_m:.1f}M, while Amazon Ads returned "
        f"{amz.ratio:.2f} per dollar on ${amz.spend_m:.1f}M — more than twice the spend at less than "
        "a third of the return. This is the largest single efficiency leak in the marketing plan.")
    rows = [[r.platform, money(r.spend_m), money(r.inc_m, dp=2), f"{r.rroas:.2f}", f"{r.ratio:.2f}",
             "Reinvest" if r.ratio >= 1 else "Reallocate"] for r in rm.itertuples()]
    rows.append(["Total", money(rm.spend_m.sum()), money(rm.inc_m.sum(), dp=2),
                 f"{rm.rroas.mean():.2f}", f"{ratio:.2f}", "Rebalance"])
    m.table(["Platform", "Spend", "Modelled incremental", "Reported ROAS", "Modelled ratio", "Call"],
            rows, widths=[0.26, 0.13, 0.20, 0.15, 0.15, 0.11], total_row=True, status_col=5,
            size=9.0,
            note="Source: seed_retail_media_spend_q1_2026. Modelled incrementality governs budget "
                 "decisions; platform-reported ROAS is shown for contrast only.")

    ch = chart_grouped("r74_gap.png", list(rm.platform),
                       {"Platform-reported ROAS": [float(x) for x in rm.rroas],
                        "Modelled incrementality": [float(x) for x in rm.ratio]},
                       title="Reported ROAS versus modelled incrementality, by platform")
    m.image(ch, "Every platform reports better than the model. The size of the gap is the useful "
                "signal.")

    m.h1("WHY THE GAP", "2 · Reported ROAS and modelled incrementality are different questions")
    m.body(
        "Platform-reported ROAS answers \"how much revenue is associated with exposure to this ad?\" "
        "Modelled incrementality answers \"how much of that revenue would not have happened "
        "otherwise?\" The second question is the one a budget decision needs. Amazon shows the widest "
        f"gap — reported {amz.rroas:.2f} against modelled {amz.ratio:.2f} — largely because a "
        "substantial share of exposed purchases are base purchases from customers who were already "
        "buying. Walmart Connect shows the narrowest gap and is the only platform above 1.0 on the "
        "modelled measure.")
    m.callout("The governance point",
              "This is not an accusation that platform numbers are wrong. They measure what they say "
              "they measure. The discipline we are adopting is that budget allocation uses modelled "
              "incrementality and platform dashboards are used for in-flight optimisation "
              "only (Report 75).", "info")

    brows = [[r.brand, money(r.spend / 1000, dp=2), money(r.inc / 1000, dp=2), f"{r.ratio:.2f}"]
             for r in rmb.itertuples()]
    m.h1("BY BRAND", "3 · Which brands are getting value")
    m.table(["Brand", "Spend", "Modelled incremental", "Ratio"], brows,
            widths=[0.34, 0.22, 0.26, 0.18],
            note="Source: seed_retail_media_spend_q1_2026, grouped by brand.")

    m.h1("MIX", "4 · Two brands, two philosophies")
    chc = chart_donut("r74_cw.png", [c[:18] for c in cw.channel.head(6)],
                      [float(x) for x in cw.spend_m.head(6)], title="Crunchwell A&P mix ($M)")
    m.image(chc, f"Crunchwell: ${cw.spend_m.sum():.1f}M, linear-TV-led.")
    chp = chart_donut("r74_pp.png", [c[:18] for c in pp.channel.head(6)],
                      [float(x) for x in pp.spend_m.head(6)], title="ProteinPeak A&P mix ($M)")
    m.image(chp, f"ProteinPeak: ${pp.spend_m.sum():.1f}M, paid-social and creator-led.")
    m.body(
        "The brand growing fastest runs the mix weighted to creator, paid social and retail media. "
        "The brand that has been flat for six quarters runs the mix weighted to linear television. "
        "That is not proof of causation, but combined with the sentiment gap (+0.44 versus −0.11) it "
        "is enough to justify moving a third of Crunchwell's TV line into CTV, creator and retail "
        "media in FY2027.")

    m.h1("THE MOVE", "5 · The H2 reallocation, platform by platform")
    m.table(["Platform", "Q1 spend", "H2 change", "Rationale"],
            [["Amazon Ads", money(float(amz.spend_m)), "−$700K",
              f"Modelled ratio {amz.ratio:.2f}; the largest leak in the plan"],
             ["Walmart Connect", money(float(wmt.spend_m)), "+$350K",
              f"Modelled ratio {wmt.ratio:.2f}; the only platform above 1.0"],
             ["Kroger Precision Marketing",
              money(float(rm[rm.platform == 'Kroger Precision Marketing'].spend_m.iloc[0])), "+$200K",
              "Ratio 0.77 and improving; strong grocery overlap"],
             ["Louisiana injection (cross-platform)", "—", "+$150K",
              "2.2x portfolio ROI on the recovery leg"],
             ["Net", money(rm.spend_m.sum()), "$0", "Reallocation, not incremental budget"]],
            widths=[0.26, 0.14, 0.16, 0.44], total_row=True, align_right_from=9, size=9.0,
            note="H2 figures are the recommended plan; Q1 spend from "
                 "seed_retail_media_spend_q1_2026.")

    prows = [[r.period, money(r.spend_m)] for r in per.itertuples()]
    m.h1("PHASING", "6 · A secondary finding worth acting on")
    m.table(["Period", "A&P spend"], prows, widths=[0.6, 0.4],
            note="Source: seed_marketing_spend by period.")
    m.body(
        "Total A&P is lumpy — the quarterly range is wide in a category bought weekly. Smoothing "
        "phasing to match purchase behaviour is a free efficiency gain and is recommended for the "
        "FY2027 plan.")

    m.recommendations([
        ("Approve the $700K reallocation out of Amazon Ads", "CFO / Tasha Brooks", "By Aug 1"),
        ("Adopt modelled incrementality as the single budget-governing metric", "Hugo Lin",
         "From Aug 1"),
        ("Move a third of Crunchwell's linear TV line into CTV, creator and retail media in FY27",
         "CMO / Cory Whitman", "FY27 planning"),
        ("Smooth A&P phasing against weekly purchase behaviour", "Hugo Lin", "FY27 planning"),
        ("Re-read incrementality at week 8 and week 13 post-reallocation", "Hugo Lin", "Q4 FY26"),
    ])
    return m.build()


# ============================================== 75 · Retail media governance ===
def r75_retail_media_governance():
    m = Memo("75-retail-media-measurement-governance-standard.docx",
             kicker="STANDARD · MEASUREMENT & GOVERNANCE",
             title="Retail Media Measurement and Governance Standard",
             subtitle="Which number governs which decision, who owns each one, and what we stop "
                      "reporting",
             byline="Tasha Brooks, Director — eCommerce & Retail Media, with Hugo Lin",
             meta=["Effective: August 1 2026", "Applies to: all retail-media platforms and agencies",
                   "Companion documents: Reports 55 and 74", "Version: v1 · July 2026"],
             short="Retail media standard",
             doc_type="Internal measurement standard")

    rm = q.retail_media()
    rmb = q.retail_media_brand()
    ratio = rm.inc_m.sum() / rm.spend_m.sum()

    m.at_a_glance([("Modelled incrementality", "the governing metric"),
                   (f"${ratio:.2f}", "current blended ratio"),
                   ("1.00", "FY29 target ratio"), ("4", "platforms in scope")])

    m.h1("PURPOSE", "1 · Why this standard exists")
    m.body(
        "We run four retail-media platforms that each report a different number using a different "
        "attribution window, and we make budget decisions across all four. Without one governing "
        "metric, the platform with the most generous attribution wins the budget — which is precisely "
        f"what has been happening. Q1 FY2026 shows Amazon Ads reporting "
        f"{float(rm[rm.platform=='Amazon Ads'].rroas.iloc[0]):.2f} ROAS on a modelled incrementality "
        f"of {float(rm[rm.platform=='Amazon Ads'].ratio.iloc[0]):.2f}, against Walmart Connect at "
        f"{float(rm[rm.platform=='Walmart Connect'].rroas.iloc[0]):.2f} reported and "
        f"{float(rm[rm.platform=='Walmart Connect'].ratio.iloc[0]):.2f} modelled.")

    m.h1("THE RULE", "2 · One metric governs budget")
    m.bullets([
        "**Budget allocation across platforms uses modelled incrementality ratio only.** No exceptions.",
        "**Platform-reported ROAS is used for in-flight optimisation** — creative, bidding, keyword "
        "and audience decisions inside an already-approved budget.",
        "**Cannibalised and undetermined revenue are reported explicitly**, not netted into the "
        "incremental figure.",
        "**Every platform is re-measured quarterly.** A platform's ratio is a current estimate, not a "
        "standing property.",
        "**Agencies are briefed on modelled incrementality**, and their performance is assessed "
        "against it rather than against platform dashboards.",
    ])
    m.table(["Decision", "Governing metric", "Owner", "Cadence"],
            [["Budget split across platforms", "Modelled incrementality ratio", "Tasha Brooks",
              "Quarterly"],
             ["Budget split across brands", "Modelled incremental revenue by brand", "Hugo Lin",
              "Quarterly"],
             ["Creative, bidding, audience", "Platform-reported metrics", "Agency", "Weekly"],
             ["Total retail-media envelope", "Blended ratio versus target", "CMO / CFO",
              "Annual planning"],
             ["Platform continuation", "Two consecutive quarters below 0.50 ratio", "Tasha Brooks",
              "Quarterly"]],
            widths=[0.28, 0.30, 0.22, 0.20], align_right_from=9, size=9.0)

    ch = chart_bar("r75_ratio.png", list(rm.platform), [float(x) for x in rm.ratio],
                   title="Modelled incrementality ratio by platform, Q1 FY2026",
                   colors_list=["#B24A2E" if v < 0.55 else ("#B98A2E" if v < 1.0 else "#2E7D75")
                                for v in rm.ratio])
    m.image(ch, "The current baseline. A platform below 0.50 for two consecutive quarters comes up "
                "for a continuation decision.")

    m.h1("DEFINITIONS", "3 · What each number means")
    m.table(["Term", "Definition", "Source"],
            [["Spend", "Gross media spend committed to the platform in the period",
              "Platform invoice"],
             ["Platform-reported ROAS", "Revenue attributed by the platform ÷ spend, on the "
              "platform's own attribution window", "Platform dashboard"],
             ["Modelled incremental revenue",
              "Revenue the model attributes to the exposure that would not otherwise have occurred",
              "Acme mix model"],
             ["Cannibalised base", "Exposed revenue the model attributes to already-planned purchase",
              "Acme mix model"],
             ["Undetermined", "Exposed revenue the model cannot confidently classify",
              "Acme mix model"],
             ["Modelled incrementality ratio", "Modelled incremental revenue ÷ spend",
              "Derived"]],
            widths=[0.24, 0.52, 0.24], align_right_from=9, size=9.0,
            note="Field names match seed_retail_media_spend_q1_2026 so the standard and the data "
                 "stay in step.")

    m.h1("REPORTING", "4 · What we start and stop reporting")
    m.h2("4.1 · Starts")
    m.bullets([
        "Monthly modelled incrementality ratio by platform and by brand, in the commercial review.",
        "Explicit cannibalised and undetermined lines alongside incremental revenue.",
        "A named confidence level on each platform's modelled figure.",
        "Louisiana and other priority-DMA cuts where spend is geo-weighted.",
    ])
    m.h2("4.2 · Stops")
    m.bullets([
        "Platform-reported ROAS as a headline in any budget document.",
        "Blended ROAS across platforms — it averages incompatible attribution windows.",
        "Any comparison of one platform's reported number to another's.",
    ])
    m.callout("The practical consequence",
              "Under this standard, the Q1 FY2026 allocation would not have been approved. Amazon "
              "Ads at a 0.40 ratio would have been capped, and the H2 reallocation (Report 74) is the "
              "correction. The standard exists so the correction does not have to happen again "
              "annually.", "action")

    brows = [[r.brand, money(r.spend / 1000, dp=2), money(r.inc / 1000, dp=2), f"{r.ratio:.2f}"]
             for r in rmb.itertuples()]
    m.h1("BASELINE", "5 · Where each brand starts")
    m.table(["Brand", "Q1 spend", "Modelled incremental", "Ratio"], brows,
            widths=[0.34, 0.22, 0.26, 0.18],
            note="Source: seed_retail_media_spend_q1_2026.")

    m.recommendations([
        ("Adopt the standard with effect from August 1 2026", "CMO / CFO", "Aug 1 2026"),
        ("Re-brief all retail-media agencies against modelled incrementality", "Tasha Brooks",
         "By Aug 15"),
        ("Add the monthly incrementality report to the commercial review pack", "Hugo Lin",
         "From August"),
        ("Set the FY27 target blended ratio at 0.85 and the FY29 target at 1.00", "CMO",
         "FY27 planning"),
        ("Review platform continuation for any platform below 0.50 for two quarters",
         "Tasha Brooks", "Quarterly"),
    ])
    m.signoff([("CMO", "the standard and the governing metric"),
               ("CFO", "the budget-decision rule"),
               ("Tasha Brooks", "platform-level application and agency briefing")])
    return m.build()


# ================================================= 76 · Louisiana action plan ==
def r76_louisiana_action_plan():
    m = Memo("76-louisiana-90-day-recovery-action-plan.docx",
             kicker="ACTION PLAN · 90 DAYS",
             title="Louisiana Recovery — 90-Day Action Plan",
             subtitle="Three legs, fourteen doors, one line review, and the measures we will be "
                      "judged on in twelve weeks",
             byline="Marcus Boudreaux, Director Sales South, with Jordan Hsu (diagnostic)",
             meta=["Period: August–October 2026", "Diagnostic: Report 58 · Brand plan: Report 66",
                   "Version: v1 · July 2026"],
             short="LA 90-day plan",
             doc_type="Internal action plan")

    la = q.share_quarter(la=True)
    end = q.endcap_la()
    rouses = q.rouses_oos()
    geo = q.geos()
    pos = q.pos("Crunchwell", "LA-DMA")

    m.at_a_glance([("−340 bps", "peak-to-trough share"),
                   (f"{la.cw.iloc[-1]:.2f}%", "share today"),
                   ("4.0%", "12-week target"), ("14", "focus doors")])

    m.h1("THE PLAN", "1 · Three legs, in order")
    m.lede("Shelf first, availability second, demand third. Media into an empty shelf is wasted money.")
    m.body(
        f"Crunchwell's Louisiana share fell approximately 340 basis points from the Mass/Grocery peak "
        f"to 3.0% in Q1 FY2026 and has recovered to {la.cw.iloc[-1]:.2f}% on the all-channel "
        "value-weighted measure. Root-cause attribution puts roughly 55% of the decline on the "
        "September 2025 Walmart modular reset, 20% on Larksfield promotional intensity at Rouses, "
        "12% on the Hurricane Tonya supply event, and the balance on private label and shopper-mix "
        "shift. The sequence of this plan follows that attribution.")
    m.table(["Leg", "What we do", "Investment", "Owner", "12-week measure"],
            [["1 · Shelf", "Restore Crunchwell Mega to 8 facings in the Walmart LA modular; win one "
              "endcap per supercenter", "Line-review ask", "Marcus Boudreaux",
              "Average facings ≥7.5; at least one endcap"],
             ["2 · Availability", "Third-party merchandising in the 14 worst doors; Rouses OSA "
              "recovery programme", "≈$0.4M", "Customer Logistics", "OSA ≥90% in audited doors"],
             ["3 · Demand", "Louisiana retail-media injection plus targeted Rouses trade at capped "
              "depth", "≈$1.1M", "Tasha Brooks / NAM", "LA Crunchwell share ≥4.0%"]],
            widths=[0.12, 0.34, 0.13, 0.19, 0.22], align_right_from=9, size=9.0,
            note="Investment figures are the funded amounts; media leg ROI is 2.2x portfolio average "
                 "per seed_retail_media_spend_q1_2026.")

    ch = chart_line("r76_share.png", list(la.q),
                    {"Crunchwell Louisiana": [float(x) for x in la.cw],
                     "Larksfield Louisiana": [float(x) for x in la.lf],
                     "Private label Louisiana": [float(x) for x in la.pl]},
                    title="Louisiana DMA value share (%)", pct=True)
    m.image(ch, "The trough and the partial recovery. The 12-week target is 4.0% on this measure.")

    m.h1("LEG ONE", "2 · Shelf — the August line review")
    m.body(
        "The single most important action in this plan happens in one meeting. The September 2025 "
        "modular cut Crunchwell Mega from 8 facings to 6 across the Louisiana DMA. The audit shows "
        f"Larksfield averaging {float(end.lf_endcaps.mean()):.2f} endcaps per store against Acme's "
        f"{float(end.acme_endcaps.mean()):.2f}, and Field & Honey holding "
        f"{float(end.fh_facings.mean()):.2f} facings against Crunchwell Mega's "
        f"{float(end.cw_mega_facings.mean()):.2f}.")
    end8 = q.roll_up(end, "city", 7, sum_cols=("stores",),
                     mean_cols=("lf_endcaps", "acme_endcaps", "pl_endcaps", "cw_mega_facings",
                                "fh_facings", "oos_pct"), other="All other LA cities")
    erows = [[r.city, f"{int(r.stores)}", f"{r.cw_mega_facings:.2f}", f"{r.fh_facings:.2f}",
              f"{r.lf_endcaps:.2f}", f"{r.oos_pct:.0f}%"] for r in end8.itertuples()]
    m.table(["City", "Stores", "CW Mega facings", "F&H facings", "Larksfield endcaps", "Mega OOS"],
            erows, widths=[0.20, 0.13, 0.20, 0.17, 0.19, 0.11], size=9.0,
            note="Source: seed_walmart_endcap_audit_la, 62 audited stores.")
    m.callout("How we are framing the ask",
              "Louisiana RTE category dollars are down 2.8%. Restoring Mega facings and winning one "
              "endcap per supercenter rebuilds category dollars, not just Acme share. We take it in "
              "as a joint growth case, not as a supplier complaint (Report 77).", "action")

    m.h1("LEG TWO", "3 · Availability — the fourteen doors")
    m.body(
        f"{len(rouses[rouses.osa < 70])} audited Rouses doors sit below 70% on-shelf availability on "
        f"Crunchwell Original Mega, with up to {int(rouses.oos_days.max())} out-of-stock days in Q1 "
        "2026, months after warehouse fill recovered. Every one of those doors has a Larksfield "
        "endcap. Third-party merchandising for 12 weeks costs approximately $0.4M and is the fastest "
        "measurable intervention in this plan.")
    rrows = [[r.sku_name[:28], r.city, f"{r.osa:.0f}%", f"{int(r.oos_days)}", f"{r.lift:.0f}%"]
             for r in rouses.head(9).itertuples()]
    m.table(["SKU", "City", "OSA", "Q1 OOS days", "Promo response lift"], rrows,
            widths=[0.32, 0.20, 0.14, 0.18, 0.16], size=9.0,
            note="Source: seed_rouses_oos_by_door.")

    m.h1("LEG THREE", "4 · Demand — and why it comes last")
    m.body(
        "The Louisiana retail-media injection returns approximately 2.2 times the portfolio ROI, "
        "which makes it the most efficient media money available to us. It is nonetheless the third "
        "leg, because driving trips to a shelf that is 60% in stock converts our media spend into "
        "Larksfield's endcap sales. The media flight starts once the merchandising programme is in "
        "place, which is week three of the plan.")
    m.body(
        "Trade support at Rouses is targeted and depth-capped at 20% per the RGM policy (Report 64). "
        "We are not buying share back with depth; the elasticity data says that erodes the reference "
        "price and makes the next recovery harder.")

    m.h1("SCHEDULE", "5 · Week by week")
    m.table(["Weeks", "What happens", "Owner"],
            [["1–2", "Merchandising contracts signed; door list confirmed; line-review pack built",
              "Customer Logistics / Marcus Boudreaux"],
             ["3–4", "Merchandising live in 14 doors; Walmart August line review held",
              "Customer Logistics / Marcus Boudreaux"],
             ["4–6", "Retail-media flight begins; Rouses trade events execute at capped depth",
              "Tasha Brooks / NAM"],
             ["6–8", "First OSA re-audit; facing compliance check in Walmart LA stores", "Jordan Hsu"],
             ["9–12", "Share re-read; decide whether leg 3 scales or stops", "Jordan Hsu / Marcus Boudreaux"]],
            widths=[0.12, 0.54, 0.34], align_right_from=9, size=9.0)

    grows = [[r.geo_name[:26], f"{r.fy25:.1f}%", f"{r.q126:.1f}%", f"{int(r.bps)}"]
             for r in geo.head(8).itertuples()]
    m.h1("EARLY WARNING", "6 · The next two dominoes")
    m.table(["Market", "FY25 share", "Q1 FY26 share", "Δ bps"], grows,
            widths=[0.40, 0.20, 0.20, 0.20], size=9.0,
            note="Source: seed_geographies.")
    m.body(
        "Birmingham and Memphis show the same 30 basis point drift Louisiana showed in Q4 2025, with "
        "no local event to explain it. Weekly facing and OSA monitoring in both DMAs costs almost "
        "nothing and buys a quarter of warning. It starts with this plan, not after the next alarm.")

    m.risks([["Line review does not restore facings", "Leg 1 fails; recovery ceiling drops to ~3.6%",
              "Escalate to the FY27 JBP as a category-dollar case; hold endcap ask separately",
              "Marcus Boudreaux"],
             ["Merchandising does not lift OSA above 90%", "Leg 2 fails; media leg stays paused",
              "Switch to direct-store-delivery support in the worst five doors",
              "Customer Logistics"],
             ["Larksfield escalates promotional intensity", "Recovery slows even with shelf restored",
              "Hold depth cap; compete on display and availability, not price", "NAM"],
             ["2026 hurricane season repeats", "Supply-driven relapse",
              "Pre-positioned inventory from week 32 (Report 73)", "VP Supply Chain"]])

    m.recommendations([
        ("Fund the merchandising programme in the 14 focus doors for 12 weeks", "CFO", "By Aug 1"),
        ("Take facing restoration into the Walmart August line review as a non-negotiable",
         "Marcus Boudreaux", "Aug line review"),
        ("Release the Louisiana retail-media injection from week 3, not week 1", "Tasha Brooks",
         "By Aug 15"),
        ("Stand up weekly facing and OSA monitoring in Birmingham and Memphis", "Jordan Hsu",
         "By Aug 15"),
        ("Re-read share, facings and OSA at week 12 and decide whether leg 3 scales",
         "Jordan Hsu", "Late October 2026"),
    ])
    return m.build()


# ============================================= 77 · Walmart negotiation brief ==
def r77_walmart_negotiation_brief():
    m = Memo("77-walmart-august-2026-line-review-negotiation-brief.docx",
             kicker="NEGOTIATION BRIEF · INTERNAL",
             title="Walmart August 2026 Line Review — Negotiation Brief",
             subtitle="Our four asks, what we are prepared to give, the buyer's likely position, and "
                      "our walk-away points",
             byline="Marcus Boudreaux, Director Sales South",
             meta=["Meeting: Walmart August 2026 line review",
                   "Internal only — not for distribution outside Acme",
                   "Companion deck: Report 59 · Recovery plan: Report 76"],
             short="Walmart LR brief",
             doc_type="Internal negotiation brief")

    ret = q.retailers()
    wmt = ret[ret.retailer == "Walmart"].iloc[0]
    wp_w = q.cat_row("Q2-FY2026-MTD", "Wellness Protein", "Walmart Total US")
    wp_t = q.cat_row("Q2-FY2026-MTD", "Wellness Protein", "Target Total US")
    end = q.endcap_la()
    tb = q.trade_events("retailer")
    wt = tb[tb.retailer == "Walmart"].iloc[0]
    la_cat = q.cat_row("Q1-FY2026", "Total", "Louisiana DMA")
    heb = q.heb_delist_risk()

    m.at_a_glance([(f"${wmt.rev:.0f}M", "Acme revenue at Walmart"),
                   (f"{wp_w.acme_share:.1f}%", "our protein share here"),
                   (f"{wp_t.acme_share:.1f}%", "the same number at Target"),
                   ("4", "asks")])

    m.h1("THE SITUATION", "1 · Where we stand going in")
    m.body(
        f"Walmart is ${wmt.rev:.0f}M of Acme revenue at {wmt.acv:.1f}% ACV weight — more than twice "
        f"our next-largest customer. Two issues dominate this review. First, our Wellness Protein "
        f"position here is {wp_w.acme_share:.1f}% against {wp_t.acme_share:.1f}% at Target on "
        "identical assortment and identical shelf price. Second, the September 2025 Louisiana modular "
        "cut Crunchwell Mega from 8 facings to 6, and Louisiana category dollars have fallen "
        f"{la_cat.growth:+.1f}% since.")
    m.body(
        "Both are framed as joint growth problems in the room. Neither is framed as a complaint. The "
        "buyer's incentive is category dollars per linear foot, and both asks improve that number.")

    m.h1("THE ASKS", "2 · Four asks, in priority order")
    m.table(["#", "Ask", "Why it works for Walmart", "Our fallback"],
            [["1", "Full ProteinPeak line authorisation, including PP005 and PP006",
              "Wellness Protein is the fastest-growing pocket in the category "
              f"({wp_w.growth:+.1f}% here); we are under-assorted against demand",
              "Two-SKU authorisation in the top two-thirds of stores by ACV"],
             ["2", "Crunchwell Mega restored to 8 facings in the Louisiana DMA modular",
              f"Louisiana category dollars are {la_cat.growth:+.1f}%; the reset moved space to a "
              "lower-velocity assortment",
              "7 facings plus committed endcap in two windows"],
             ["3", "One endcap per Louisiana supercenter across two windows",
              "Display drives category dollars; our audit shows Larksfield holding the display and "
              "the category still shrinking",
              "One window plus joint OSA programme"],
             ["4", "Chocolate Almond authorisation at the Q4 review",
              "64% top-two-box, clears our action standard by 9 points; extends the fastest-growing "
              "segment", "Q1 FY27 authorisation with a Q4 commitment letter"]],
            widths=[0.05, 0.27, 0.40, 0.28], align_right_from=9, size=9.0,
            note="Source: seed_category_market_size retailer cuts, seed_walmart_endcap_audit_la, "
                 "seed_concept_test_chocolate_almond.")

    ch = chart_bar("r77_protein.png", ["Walmart", "US national", "Target"],
                   [float(wp_w.acme_share),
                    float(q.cat_row("Q2-FY2026-MTD", "Wellness Protein").acme_share),
                    float(wp_t.acme_share)],
                   title="Acme share of Wellness Protein, Q2 FY26 MTD (%)", pct=True,
                   colors_list=["#B24A2E", "#5B6472", "#2E7D75"])
    m.image(ch, "The chart we lead with. Same items, same price, one third of the share.")

    m.h1("WHAT WE GIVE", "3 · What we are prepared to put on the table")
    m.bullets([
        "**Pack Refresh readiness.** Modular-ready planograms and pre-built inventory for the "
        "August 15 2026 Crunchwell Pack Refresh, so the reset costs Walmart nothing in service.",
        "**Trade calendar quality.** FY27 calendar rebuilt to a 0.60 incrementality floor — fewer, "
        f"better-timed events. Q1 ran {int(wt.events)} events at ${wt.spend/1000:.1f}M and an index "
        f"of {wt.idx:.2f}.",
        "**Feature-and-display weight instead of depth.** A 30% increase in feature-and-display "
        "support, funded from the depth reduction, which builds category dollars rather than "
        "discounting them.",
        "**Back-to-school scale.** This account carries the highest kids-household cereal share of "
        "any retailer; we will scale the BTS programme to match.",
        "**Joint OSA programme** in the 14 lowest-performing Louisiana doors, with Acme funding "
        "third-party merchandising.",
    ])

    m.h1("THEIR POSITION", "4 · What we expect from the buyer")
    m.table(["Likely buyer position", "Our response"],
            [["\"Your Crunchwell velocity does not justify 8 facings\"",
              "Velocity is depressed by out-of-stocks, not demand: audited Mega OOS runs at "
              f"{float(end.oos_pct.max()):.0f}% in the worst city. Fix availability and the velocity "
              "case changes."],
             ["\"Protein is a premium item; our shopper is price-led\"",
              "Target's shopper is not three times more premium than yours. The difference is "
              "display and assortment, not demographics — and protein grew "
              f"{wp_w.growth:+.1f}% in this account."],
             ["\"We need deeper promotions to move the category\"",
              "Our Q1 index of " f"{wt.idx:.2f}" " says half of promoted volume was not incremental. "
              "Feature and display index higher on every brand we run them on."],
             ["\"Endcap space is committed\"",
              "One window plus the joint OSA programme is our fallback; we will take a written "
              "commitment for the second window in the FY27 JBP."],
             ["\"Prove the Pack Refresh will not disrupt service\"",
              "Pre-build in weeks 31–32 and a named changeover plan (Report 72)."]],
            widths=[0.38, 0.62], align_right_from=9, size=9.0)

    m.h1("WALK-AWAY", "5 · Our limits")
    m.bullets([
        "**We do not fund facings with depth.** The RGM policy caps Mega depth at 20% and prohibits "
        "stacking with retailer funds (Report 64). This is not negotiable in the room.",
        "**We do not discount ProteinPeak beyond 10%.** A premium item trained to discount stops "
        "being a premium item, and this account would set the reference price for every other.",
        "**We do not accept a Louisiana endcap commitment without a facing commitment.** Display "
        "without shelf presence produces one good week and no base recovery.",
        "**We do not trade Chocolate Almond exclusivity for depth.** If exclusivity is on the table, "
        "the price is distribution breadth, not price investment.",
    ])
    m.callout("One risk to raise before they do",
              f"H-E-B has Crunchwell Cinnamon Twist at a {float(heb.risk.iloc[0]):.2f} delist-risk "
              f"score with a review on {heb.review.iloc[0]}. If Walmart raises portfolio rationalisation, "
              "we should be first to name the SKUs we ourselves are discontinuing (Report 69) rather "
              "than defending everything.", "risk")

    m.h1("SCORECARD", "6 · What we ask to review quarterly")
    m.table(["Measure", "Today", "FY27 target"],
            [["Acme revenue at Walmart", f"${wmt.rev:.0f}M", "$196M"],
             ["Acme Wellness Protein share", f"{wp_w.acme_share:.1f}%", "≥9%"],
             ["Crunchwell Mega facings, Louisiana",
              f"{float(end.cw_mega_facings.mean()):.1f}", "8.0"],
             ["Louisiana Crunchwell share", "3.0%", "≥4.5%"],
             ["Trade incrementality index", f"{wt.idx:.2f}", "≥0.60"]],
            widths=[0.46, 0.27, 0.27],
            note="Source: seed_retailers, seed_category_market_size, seed_walmart_endcap_audit_la, "
                 "seed_trade_promo_events_q1_2026. Targets are the FY27 proposal.")

    m.recommendations([
        ("Lead with the protein share gap, not the Louisiana facings", "Marcus Boudreaux",
         "In the meeting"),
        ("Hold the depth caps regardless of the facing outcome", "Marcus Boudreaux", "In the meeting"),
        ("Secure a written commitment for the second endcap window if the first is refused",
         "Marcus Boudreaux", "In the meeting"),
        ("Report outcomes against the four asks within 48 hours", "Marcus Boudreaux",
         "Post-meeting"),
    ])
    return m.build()


# ================================================ 78 · Kroger prep brief =======
def r78_kroger_prep_brief():
    m = Memo("78-kroger-november-2026-line-review-prep-brief.docx",
             kicker="PREPARATION BRIEF",
             title="Kroger November 2026 Line Review — Preparation Brief",
             subtitle="The switching data, the division picture, and the three questions we need "
                      "answered before we build the pack",
             byline="Priya Raman, Category Manager — Kroger",
             meta=["Meeting: Kroger November 2026 line review",
                   "Pack due: October 2026 · This brief: July 2026",
                   "Companion documents: Reports 59 and 64"],
             short="Kroger Nov LR prep",
             doc_type="Internal preparation brief")

    ret = q.retailers()
    kr = ret[ret.retailer == "Kroger"].iloc[0]
    sw = q.kroger_switching()
    tb = q.trade_events("retailer")
    kt = tb[tb.retailer == "Kroger"].iloc[0]
    rm = q.retail_media()
    kpm = rm[rm.platform == "Kroger Precision Marketing"].iloc[0]
    div = q.pva_retailer(q.Q1)
    kpva = div[div.Retailer == "Kroger"].iloc[0]

    m.at_a_glance([(f"${kr.rev:.0f}M", "Acme revenue at Kroger"),
                   (f"{kpva['var']:+.1f}%", "Q1 vs plan"),
                   (f"{kpm.ratio:.2f}", "Kroger Precision ratio"),
                   ("3", "open questions")])

    m.h1("PURPOSE", "1 · What this brief is for")
    m.body(
        "The November line-review pack is due in October. This brief sets out what we already know, "
        "what the switching study tells us, and the three analytical questions that need answering "
        "before the pack is built — so that we are not doing the analysis in the last week, which is "
        "what happened last cycle.")

    m.h1("THE ACCOUNT", "2 · Where Kroger sits")
    m.table(["Measure", "Value", "Read"],
            [["Acme FY25 revenue", f"${kr.rev:.0f}M", "Second-largest customer"],
             ["ACV weight", f"{kr.acv:.1f}%", "Grocery National"],
             ["Q1 FY26 revenue vs plan", f"{kpva['var']:+.1f}%", "In line with the portfolio"],
             ["Q1 trade events", f"{int(kt.events)}", f"${kt.spend/1000:.1f}M spend"],
             ["Trade incrementality index", f"{kt.idx:.2f}", "Above portfolio average"],
             ["Kroger Precision modelled ratio", f"{kpm.ratio:.2f}", "Second-best platform"],
             ["Account NAM", str(kr.nam), "Tier 1"]],
            widths=[0.36, 0.22, 0.42], align_right_from=1, size=9.5,
            note="Source: seed_retailers, plan_vs_actual, seed_trade_promo_events_q1_2026, "
                 "seed_retail_media_spend_q1_2026.")

    m.h1("THE SWITCHING STUDY", "3 · Where our volume is going inside Kroger")
    srows = [[r.segment, r.from_brand[:26], r.to_brand[:24],
              q.dash(r.rate), f"{r.shift_pt:+.1f}", r.division[:18]] for r in sw.head(10).itertuples()]
    m.table(["Segment", "From", "To", "Switch rate %", "Share pt shift", "Division"], srows,
            widths=[0.18, 0.22, 0.20, 0.14, 0.14, 0.12], align_right_from=3, size=9.0,
            note="Source: seed_kroger_simple_truth_switching.")
    ch = chart_bar("r78_switch.png",
                   [f"{r.from_brand[:12]} → {r.to_brand[:12]}" for r in sw.head(7).itertuples()],
                   [float(x) for x in sw.head(7).shift_pt],
                   title="Share-point shift by switching path, Kroger", color="rust")
    m.image(ch, "The largest single path is traditional family cereal into segment shift — occasions "
                "leaving the aisle, not brands losing a head-to-head.")
    m.bullets([
        "**The largest shifts are segment shifts**, not brand switches: traditional family cereal "
        "into protein-forward, sugar-reduced and ancient-grain positions.",
        "**Where it is a brand switch, Larksfield Field & Honey is the destination** — strongest in "
        "the Kroger-South division, which is consistent with the Louisiana picture.",
        "**Simple Truth takes a meaningful slice** of Crunchwell volume nationally. That is private "
        "label competing on positioning, not on price.",
        "**Implication for the pack:** we lead with segment growth, not with a defensive Crunchwell "
        "argument.",
    ])

    m.h1("THREE QUESTIONS", "4 · What we need before the pack is built")
    m.table(["#", "Question", "Who answers it", "By when"],
            [["1", "How much of the Kroger-South Field & Honey shift is explained by the same "
              "facing and OSA mechanism we found in Louisiana?", "Jordan Hsu with Category Insights",
              "By Sep 5"],
             ["2", "What is the incremental value of full ProteinPeak line authorisation at Kroger, "
              "using the Target-versus-Walmart gap as the analogue?", "Maya Chen / Sage Park",
              "By Sep 15"],
             ["3", "Does a 0.60-index trade calendar hold volume at Kroger, where our index is "
              f"already {kt.idx:.2f} — better than the portfolio?", "Trade Finance", "By Sep 20"]],
            widths=[0.05, 0.49, 0.28, 0.18], align_right_from=9, size=9.0)
    m.callout("Why question 1 matters most",
              "If the Kroger-South shift has the same mechanism as Louisiana — lost facings and poor "
              "on-shelf availability rather than shopper preference — then the November ask is a "
              "shelf ask and the analysis is already largely done. If it is genuinely preference, the "
              "ask is an assortment ask and the pack looks completely different.", "action")

    m.h1("THE LIKELY ASKS", "5 · What we expect to take in")
    m.bullets([
        "**Full ProteinPeak line authorisation**, on the same growth case we are taking to Walmart "
        "(Report 77).",
        "**Chocolate Almond** for Q1 FY2027, subject to the Q4 line reviews and the SteerCo gate "
        "(Report 68).",
        "**Crunchwell Pack Refresh planograms** for the FY27 reset, with pre-built inventory.",
        "**Kroger Precision Marketing weight increase**, funded from the Amazon Ads reallocation — "
        f"Kroger Precision runs at a {kpm.ratio:.2f} modelled ratio (Report 74).",
        "**TrailGrove distribution gaps** in granola and bars, which is the cheapest incremental "
        "volume available in this account.",
    ])

    m.h1("WHAT WE BRING", "6 · The give side")
    m.table(["What we bring", "Value to Kroger"],
            [["FY27 trade calendar at a 0.60 incrementality floor",
              "Fewer, better-timed events; higher category dollars per promoted week"],
             ["Feature-and-display weight funded from depth reduction",
              "Display support that builds the category rather than discounting it"],
             ["Kroger Precision investment increase", "Retail-media revenue at a proven ratio"],
             ["Pack Refresh readiness with pre-built inventory", "No service risk at the reset"],
             ["Segment-growth analysis by division", "Category insight Kroger does not have to build"]],
            widths=[0.42, 0.58], align_right_from=9, size=9.0)

    m.recommendations([
        ("Commission the three analytical questions now, not in October", "Priya Raman", "By Aug 1"),
        ("Reuse the Walmart protein growth case rather than building a new one", "Priya Raman",
         "By Sep 15"),
        ("Fund the Kroger Precision increase from the Amazon reallocation", "Tasha Brooks",
         "By Aug 1"),
        ("Build the pack around segment growth, not Crunchwell defence", "Priya Raman", "October 2026"),
    ])
    return m.build()


# =================================================== 79 · Club channel memo ====
def r79_club_channel_strategy():
    m = Memo("79-club-channel-fy27-strategy-memo.docx",
             kicker="CHANNEL STRATEGY MEMORANDUM",
             title="Club Channel FY2027 Strategy — Costco and Sam's",
             subtitle="Two accounts, one pack architecture question, and why the club channel is "
                      "where GLP-1 will show up first",
             byline="Club Sales with RGM",
             meta=["Accounts: Costco, Sam's Club", "Period: FY2027 with FY29 implications",
                   "Companion documents: Reports 64 and 70", "Version: v1 · July 2026"],
             short="Club FY27 strategy",
             doc_type="Internal channel strategy")

    ret = q.retailers(12)
    club = ret[ret.channel == "Club"]
    pva = q.pva_retailer(q.Q1, top=10)
    tb = q.trade_events("retailer")
    sk = q.skus()
    mac = q.macro(12)

    m.at_a_glance([(f"${club.rev.sum():.0f}M", "Acme club revenue FY25"),
                   (f"{len(club)}", "club accounts"),
                   ("18oz+", "the packs at risk"), ("0.81", "GLP-1 trend strength")])

    m.h1("THE ARGUMENT", "1 · Club is the leading indicator, not the laggard")
    m.lede("If smaller appetites are going to change cereal, they will change club packs first.")
    m.body(
        f"Acme's club business is approximately ${club.rev.sum():.0f}M across "
        f"{', '.join(club.retailer.tolist())}. The channel's economics depend on large pack sizes and "
        "high units per trip, which is exactly the demand pattern most exposed to the GLP-1 appetite "
        f"shift — a trend running at 0.81 strength with a downward volume direction (Report 70). "
        "The FY2027 strategy therefore has two jobs: grow the channel in the near term and start "
        "restructuring the pack architecture before the exposure becomes a decline.")

    crows = [[r.retailer, r.channel, f"{r.acv:.1f}%", money(r.rev), str(r.nam), r.tier]
             for r in club.itertuples()]
    m.table(["Account", "Channel", "ACV weight", "FY25 revenue", "NAM", "Tier"], crows,
            widths=[0.20, 0.14, 0.16, 0.18, 0.20, 0.12], align_right_from=2, size=9.5,
            note="Source: seed_retailers.")

    prows = [[r.Retailer, money(r.plan), money(r.act), f"{r.var:+.1f}%"]
             for r in pva.itertuples()]
    m.h1("PERFORMANCE", "2 · Where club sits against the rest of the book")
    m.table(["Retailer", "Q1 plan", "Q1 actual", "Variance"], prows,
            widths=[0.34, 0.22, 0.22, 0.22],
            note="Source: plan_vs_actual, Q1 FY2026, top ten retailers by plan.")
    ch = chart_bar("r79_retailer.png", list(pva.Retailer), [float(x) for x in pva["var"]],
                   title="Q1 FY2026 revenue variance to plan, by retailer (%)", pct=True,
                   colors_list=["#2E7D75" if v > -3 else ("#B98A2E" if v > -6 else "#B24A2E")
                                for v in pva["var"]])
    m.image(ch, "Club performs in line with the book. The strategic issue here is structural, not "
                "current-year performance.")

    m.h1("PACK ARCHITECTURE", "3 · The question the channel forces")
    m.body(
        "Club needs a value equation the shopper can see at the shelf, which historically means the "
        "largest pack at the lowest price per ounce. Two things now cut against that. First, the "
        "elasticity data says our large packs are our most elastic, so club pricing pressure "
        "transmits directly into the reference price everywhere else. Second, if serving demand "
        "shrinks, the largest pack becomes the least attractive rather than the best value.")
    m.bullets([
        "**Crunchwell 36oz Mega Family Pack (Stage-3, 2027-Q1, $8.5M year-one)** is the club-ready "
        "answer to the value equation and should be positioned as club-first.",
        "**But it should launch with a defended price** — $8.99 target, launch support only, no "
        "depth — precisely because it sets the price-per-ounce anchor for the whole ladder "
        "(Report 64).",
        "**ProteinPeak club pack** is the higher-margin opportunity: premium price per serving, "
        "growing segment, and a shopper who is buying nutrient density rather than volume.",
        "**Single-serve multipacks** are the GLP-1 hedge — they convert a shrinking-serving trend "
        "into a higher price per ounce rather than a volume loss.",
    ])

    srows = [[r.sku_name[:34], r.brand, f"{r.oz:.0f}oz", f"${r.price:.2f}",
              f"${r.price/r.oz:.2f}", money(r.rev)]
             for r in sk[sk.oz >= 14].head(9).itertuples()]
    m.table(["SKU", "Brand", "Pack", "Shelf price", "Price/oz", "FY25 revenue"], srows,
            widths=[0.32, 0.16, 0.12, 0.14, 0.12, 0.14], align_right_from=2, size=9.0,
            note="Source: seeds/skus.csv, packs of 14oz and above.")

    m.h1("FY27 PLAN", "4 · What we do in each account")
    m.table(["Account", "FY27 priority", "What we ask for", "Risk"],
            [["Costco", "Club-first launch of the 36oz Mega Family Pack at a defended price",
              "One national item slot plus a road-show window",
              "Price-per-ounce anchor leaks into grocery"],
             ["Sam's Club", "ProteinPeak club multipack and a TrailGrove club item",
              "Two new items; club-exclusive pack graphics",
              "Cannibalisation of 12oz ProteinPeak at grocery"],
             ["Both", "Single-serve multipack test as the GLP-1 hedge",
              "Test-and-learn window in H2 FY27", "Low volume in year one"]],
            widths=[0.14, 0.32, 0.30, 0.24], align_right_from=9, size=9.0,
            note="Source: seeds/innovation_pipeline.csv (36oz Mega Family, 2027-Q1); FY27 plan is "
                 "the proposal.")
    m.callout("The one thing not to do",
              "Do not fund club growth with depth on the 18oz Mega. It is the most elastic pack in "
              "the portfolio at −1.84 to −2.12, and club pricing on it transmits to every grocery "
              "banner within a quarter. Grow the channel with new pack sizes, not with lower prices "
              "on existing ones.", "risk")

    mrows = [[r.topic, f"{r.strength:.2f}", r.direction, str(r.cats)[:26]]
             for r in mac.itertuples() if any(t in str(r.topic).lower()
                                              for t in ["glp", "protein", "sustainab", "lto",
                                                        "sugar"])]
    m.h1("CONTEXT", "5 · The trends that bear on club")
    m.table(["Trend", "Strength", "Direction", "Categories"], mrows,
            widths=[0.34, 0.14, 0.24, 0.28], align_right_from=1, size=9.0,
            note="Source: seed_macro_trends, filtered to club-relevant trends.")

    m.recommendations([
        ("Position the 36oz Mega Family Pack as a club-first launch at a defended $8.99",
         "Club Sales / RGM Lead", "Q4 FY26 gate"),
        ("Develop a ProteinPeak club multipack for Sam's FY27 review", "Sage Park / Club Sales",
         "By Q1 FY27"),
        ("Run a single-serve multipack test in H2 FY27 as the GLP-1 hedge", "Club Sales",
         "H2 FY27"),
        ("Hold the no-depth rule on the 18oz Mega in club", "RGM Lead", "FY27 policy"),
        ("Report club price-per-ounce against grocery quarterly to catch anchor leakage",
         "Trade Finance", "Quarterly"),
    ])
    return m.build()


# ============================================ 80 · Competitive playbook ========
def r80_larksfield_playbook():
    m = Memo("80-larksfield-field-and-honey-response-playbook.docx",
             kicker="COMPETITIVE RESPONSE PLAYBOOK",
             title="Larksfield Field & Honey — Response Playbook",
             subtitle="What the aggressor has done, what it is likely to do next, and our "
                      "pre-agreed responses on each front",
             byline="Competitive Intelligence with Category Insights",
             meta=["Competitor: Larksfield Foods (Field & Honey)",
                   "Fronts: protein, Louisiana, private-label-adjacent value",
                   "Version: v1 · July 2026"],
             short="F&H playbook",
             doc_type="Internal competitive playbook")

    comp = q.comp_launches("2025-06-01")
    fh = comp[comp.brand == "Field & Honey"]
    natl = q.share_quarter()
    la = q.share_quarter(la=True)
    eq_fh = q.equity("Field & Honey", "US-NAT")
    eq_cw = q.equity("Crunchwell", "US-NAT")
    end = q.endcap_la()
    sw = q.kroger_switching()

    m.at_a_glance([(f"{natl.lf.iloc[-1]:.2f}%", "F&H national share"),
                   (f"{la.lf.iloc[-1]:.2f}%", "F&H Louisiana share"),
                   (f"{len(fh)}", "launches since mid-2025"),
                   ("3", "active fronts")])

    m.h1("THE COMPETITOR", "1 · Who we are dealing with")
    m.body(
        f"Larksfield Foods' Field & Honey holds approximately {natl.lf.iloc[-1]:.2f}% national value "
        f"share against Crunchwell's {natl.cw.iloc[-1]:.2f}%, and has been the share gainer "
        f"nationally through the period. In the Louisiana DMA it holds about {la.lf.iloc[-1]:.2f}%. "
        "It is not the largest competitor in the category, but it is the one taking our volume, and "
        "it is doing so on three fronts simultaneously.")
    crows = [[r.brand, r.sku_new, str(r.launch_date), str(r.claim)[:38],
              f"{r.buzz:.2f}", q.dash(r.status)] for r in fh.itertuples()]
    m.table(["Brand", "SKU", "Launch date", "Claim", "Buzz d30", "Status"], crows,
            widths=[0.16, 0.16, 0.14, 0.32, 0.12, 0.10], align_right_from=4, size=9.0,
            note="Source: seed_competitor_launches.")

    m.h1("THE FRONTS", "2 · Three attacks, one pattern")
    m.h2("2.1 · Protein")
    m.body(
        "The 14 gram protein line extension (LF-FH-14P) launched May 12 2026 with a whole-grain "
        "almond and seed blend claim at $4.79 for 12oz — materially below ProteinPeak's $7.49. This "
        "is a value-protein attack on the segment we are betting the portfolio on. Our answer is "
        "Chocolate Almond into the Q4 line reviews and distribution breadth, not a price response "
        "(Reports 67 and 68).")
    m.h2("2.2 · Louisiana")
    m.body(
        f"The Almond launch in September 2025 coincided with the Walmart modular reset. The endcap "
        f"audit shows Larksfield averaging {float(end.lf_endcaps.mean()):.2f} endcaps per store "
        f"against Acme's {float(end.acme_endcaps.mean()):.2f}, and Field & Honey holding more facings "
        "than Crunchwell Mega in every audited city. Our answer is the three-leg recovery plan, led "
        "by shelf (Report 76).")
    m.h2("2.3 · Value-adjacent positioning")
    m.body(
        "Field & Honey sits between branded and private label on price while claiming better "
        "ingredients. The Kroger switching study shows Crunchwell volume moving to Field & Honey at "
        f"{float(sw[sw.to_brand.str.contains('Field')].rate.iloc[0]) if len(sw[sw.to_brand.str.contains('Field')]) else 19.1}% "
        "in the South division. That is a positioning loss, not a price loss.")

    ch = chart_line("r80_share.png", list(natl.q),
                    {"Field & Honey national": [float(x) for x in natl.lf],
                     "Crunchwell national": [float(x) for x in natl.cw],
                     "Field & Honey Louisiana": [float(x) for x in la.lf],
                     "Crunchwell Louisiana": [float(x) for x in la.cw]},
                    title="Value share (%) — Field & Honey versus Crunchwell", pct=True)
    m.image(ch, "The gap widens nationally and dramatically in Louisiana.")

    m.h1("THE EQUITY PICTURE", "3 · They are winning the attribute we are losing")
    attrs = ["Relevance", "Trust", "Taste", "Quality", "Modernity"]
    m.table(["Attribute", "Field & Honey (FY26Q2)", "Crunchwell (FY26Q2)", "Gap"],
            [[a, f"{eq_fh[a].iloc[-1]:.1f}", f"{eq_cw[a].iloc[-1]:.1f}",
              f"{eq_fh[a].iloc[-1] - eq_cw[a].iloc[-1]:+.1f}"] for a in attrs],
            widths=[0.28, 0.26, 0.26, 0.20], align_right_from=1,
            note="brand_equity_quarterly, US-NAT, latest wave.")
    m.body(
        "The equity comparison is the strategic heart of this playbook. Crunchwell still leads on the "
        "attributes that took decades to build. Field & Honey leads, or is closing, on the attribute "
        "that determines whether anyone buys the category this week. That is why our answer is a "
        "relevance platform rather than a price or heritage response (Report 65).")

    m.h1("PRE-AGREED RESPONSES", "4 · What we do when, decided in advance")
    m.table(["If Larksfield does this", "We do this", "We do not do this", "Owner"],
            [["Extends the 14g protein line to more flavours",
              "Accelerate Chocolate Almond; push distribution breadth at Walmart and Kroger",
              "Cut ProteinPeak price or exceed the 10% depth cap", "Sage Park"],
             ["Takes further endcap space in the South",
              "Contest at the line review with the category-dollar case; fund merchandising in the "
              "worst doors", "Buy display with incremental depth", "Marcus Boudreaux"],
             ["Launches into oat milk or granola adjacency",
              "Accelerate RootDay single-serve and TrailGrove distribution",
              "Enter a price war in a segment where we are the smaller player", "Brand teams"],
             ["Prices below private label on a hero item",
              "Hold everyday price; increase feature-and-display weight",
              "Match on price — Mega elasticity makes it unrecoverable", "RGM Lead"],
             ["Wins a national kids-cereal position",
              "Nothing — Kids Sweet is being harvested (Report 69)",
              "Defend a −2.8% segment out of pride", "VP Brand"]],
            widths=[0.26, 0.32, 0.28, 0.14], align_right_from=9, size=9.0)
    m.callout("The discipline this playbook is really about",
              "Every response above is the same shape: compete on shelf presence, availability, "
              "distribution and relevance — never on price. Field & Honey's price position is "
              "structurally below ours, so a price fight is one we lose slowly and then permanently.",
              "info")

    m.h1("MONITORING", "5 · What we watch, and how often")
    m.table(["Signal", "Source", "Cadence", "Trigger"],
            [["F&H national and DMA value share", "syndicated_weekly", "Weekly",
              "50 bps move in any priority DMA"],
             ["New launches and claims", "seed_competitor_launches", "Monthly",
              "Any protein or oat-milk entry"],
             ["Endcap and facing presence, South region", "Store audits", "Monthly",
              "Any facing loss on a hero SKU"],
             ["Buzz index at day 30 on new items", "seed_competitor_launches", "Per launch",
              "Buzz above 0.80"],
             ["Equity attributes, Relevance and Modernity", "brand_equity_quarterly", "Quarterly",
              "F&H Relevance overtaking Crunchwell"],
             ["Switching paths at Kroger", "seed_kroger_simple_truth_switching", "Semi-annual",
              "South division switch rate above 20%"]],
            widths=[0.30, 0.26, 0.14, 0.30], align_right_from=9, size=9.0)

    m.recommendations([
        ("Adopt the pre-agreed response table so responses are not improvised under pressure",
         "VP Brand / VP Sales NA", "By Aug 15"),
        ("Add Field & Honey to the standing equity tracker read", "Nina Ortega", "Q3 FY26"),
        ("Escalate any hero-SKU facing loss in the South within one week of detection",
         "Marcus Boudreaux", "Standing"),
        ("Re-issue this playbook each half-year with the monitoring triggers scored",
         "Competitive Intelligence", "January 2027"),
    ])
    return m.build()


if __name__ == "__main__":
    for fn in [r71_trade_reallocation_defence, r72_sop_minutes, r73_storm_after_action,
               r74_mmm_readout, r75_retail_media_governance, r76_louisiana_action_plan,
               r77_walmart_negotiation_brief, r78_kroger_prep_brief, r79_club_channel_strategy,
               r80_larksfield_playbook]:
        print("built", os.path.basename(fn()))
