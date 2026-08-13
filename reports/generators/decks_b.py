"""PPTX decks 52-60 — functional reviews, insights and customer. Run: python generators/decks_b.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import (money, chart_line, chart_bar, chart_grouped, chart_stacked,
                 chart_waterfall, chart_donut)
from pptx_lib import Deck
import qlib as q


# ================================================================ 52 · S&OP ===
def r52_sop_ibp_review():
    k = Deck("52-q2-2026-sop-ibp-executive-review.pptx",
             kicker="S&OP / IBP EXECUTIVE REVIEW",
             title="Q2 FY2026 Integrated Business Planning Review",
             subtitle="Demand, supply and financial plans reconciled to one number for Q3 and Q4",
             byline="S&OP Lead with Demand Planning, Supply Chain and FP&A · July 2026",
             short="Q2 FY26 S&OP")

    pm = q.pva_month()
    p2, a2, v2 = q.pva_total(q.Q2)
    fill = q.fill_month("2025-09-01")
    cuts = q.cut_reasons("2025-10-01")
    pipe = q.pipeline()

    k.agenda(["The consensus number", "Demand review", "Supply review",
              "Product / innovation review", "Reconciliation and gaps",
              "Management decisions required", "Actions"])

    k.exec_summary(
        f"The Q2 cycle closes with demand, supply and finance aligned on an H2 number of $379M — "
        f"$3M below original plan and built off the May actual of {money(float(pm.act.iloc[-1]))}. "
        "The two constraints in the cycle are Pack Refresh changeover capacity in August and "
        "ProteinPeak line capacity if Walmart authorises the full line. Neither is a demand problem.",
        tiles=[(f"{v2:+.1f}%", "Q2 QTD demand vs plan"),
               (f"{float(fill.fill.iloc[-1]):.1f}%", "fill rate, latest month"),
               (f"{float(fill.otif.iloc[-1]):.1f}%", "on-time in full"),
               ("$379M", "consensus H2 number")],
        bullets=[
            "**Demand:** unconstrained forecast is $384M for H2; the consensus number is $379M after "
            "supply and phasing constraints.",
            "**Supply:** fill rate has fully recovered from the November 2025 storm event and is "
            "running at normal service levels.",
            "**Product:** the Pack Refresh (Aug 15) is the gating item — changeover consumes line "
            "capacity in weeks 33–35.",
            "**Gap to plan is $3M**, held as a management risk rather than closed with promotional volume.",
        ], headline="One number, agreed across three functions")

    chf = chart_line("r52_fill.png", list(fill.mo),
                     {"Fill rate (%)": [float(x) for x in fill.fill],
                      "On-time in full (%)": [float(x) for x in fill.otif]},
                     title="Customer service metrics by month (%)", pct=True, h=3.0)
    k.chart_bullets("SUPPLY", "Service has fully recovered from the storm event", chf,
                    ["**November 2025** is the Hurricane Tonya trough — fill fell to ~52% on "
                     "storm-cut lines at the Houston, Thibodaux and Tyler DCs.",
                     f"**Latest month runs {float(fill.fill.iloc[-1]):.1f}% fill and "
                     f"{float(fill.otif.iloc[-1]):.1f}% OTIF** — normal service.",
                     "**The lesson stands** (see the after-action review, Report 73): our recovery "
                     "took two quarters and cost roughly 12% of the Louisiana share decline.",
                     "**Q3 watch item:** Pack Refresh changeover in weeks 33–35 tightens Battle Creek "
                     "line availability."],
                    note="Source: shipments (Fill_Rate_Pct, On_Time_Pct), monthly averages.")

    crows = [[r.reason, f"{r.cut_k:,.1f}K", f"{r.fill:.1f}%", f"{int(r.lines):,}"]
             for r in cuts.itertuples()]
    k.table("CUT ANALYSIS", "Where units are lost between order and shipment",
            ["Cut reason", "Units cut", "Avg fill on those lines", "Order lines"], crows,
            widths=[0.34, 0.22, 0.26, 0.18],
            callout=("Launch allocation is now the second-largest cut reason",
                     "Launch_Allocation cuts are a choice, not a failure — we deliberately short "
                     "base SKUs to protect launch fill. It needs to be visible in the demand plan "
                     "rather than showing up as a service miss.", "info"),
            note="Source: shipments, order lines since October 2025.")

    stage = q.pipeline_stage()
    chs = chart_bar("r52_pipeline.png", [s.replace("Stage-", "S") for s in stage.stage_gate],
                    [float(x) for x in stage.n], title="Innovation concepts by stage gate (count)",
                    color="sky", h=2.9)
    prows = [[r.concept_name[:34], r.brand, str(r.planned_launch_date),
              q.musd(r.projected_revenue_year1_musd), q.dash(r.status)]
             for r in pipe[pipe.stage_gate.isin(["Stage-5 Launch Prep", "Stage-4 Pre-Launch",
                                                 "Stage-6 In-Market"])].itertuples()]
    k.chart_table("PRODUCT REVIEW", "Three launches inside the planning horizon", chs,
                  ["Concept", "Brand", "Launch", "Year-1", "Status"], prows,
                  widths=[0.34, 0.18, 0.18, 0.14, 0.16], size=9.0,
                  note="Source: seeds/innovation_pipeline.csv, Stage-4 to Stage-6.")

    k.table("RECONCILIATION", "From unconstrained demand to the consensus number",
            ["Step", "H2 $M", "Owner", "Note"],
            [["Unconstrained demand forecast", "384.0", "Demand Planning", "Statistical + brand overlay"],
             ["Less: Pack Refresh changeover phasing", "−2.5", "Supply Chain", "Weeks 33–35 line capacity"],
             ["Less: ProteinPeak allocation at Walmart", "−1.5", "Supply Chain",
              "Only if full line authorised early"],
             ["Less: HoneyNest discontinuations", "−1.6", "Brand", "Granola Crunch, Cookie Dough"],
             ["Plus: retail-media reallocation upside", "+0.6", "Tasha Brooks", "LA injection at 2.2x ROI"],
             ["Consensus H2 number", "379.0", "S&OP", "Signed off this cycle"]],
            widths=[0.40, 0.13, 0.20, 0.27], align_right_from=1, total_row=True, size=9.5,
            note="Reconciliation is a planning artefact; base actuals from plan_vs_actual.")

    k.reco("DECISIONS", "What the executive team needs to settle",
           [("Approve the $379M consensus H2 number and carry the $3M gap as management risk",
             "CFO / S&OP", "July cycle"),
            ("Protect Pack Refresh changeover capacity in weeks 33–35 ahead of base SKU fill",
             "VP Supply Chain", "By Aug 1"),
            ("Pre-agree the ProteinPeak allocation rule if Walmart authorises the full line early",
             "Supply Chain / Sage Park", "By Aug 15"),
            ("Make Launch_Allocation cuts a visible line in the demand plan, not a service miss",
             "Demand Planning", "Next cycle")])

    k.close("One number. Two constraints. Both ours to manage.",
            ["$379M consensus for H2, $3M below plan.",
             "Service is fully recovered; capacity is the live constraint.",
             "The gap is held, not promoted away."])
    return k.build()


# ============================================ 53 · Supply chain & service =====
def r53_supply_chain_service():
    k = Deck("53-q2-2026-supply-chain-customer-service-review.pptx",
             kicker="SUPPLY CHAIN & CUSTOMER SERVICE",
             title="Q2 FY2026 Service Review",
             subtitle="Fill, OTIF, on-shelf availability and what the storm taught us about "
                      "recovery speed",
             byline="VP Supply Chain with Customer Logistics · July 2026",
             short="Q2 FY26 supply chain")

    fill = q.fill_month("2025-08-01")
    dc = q.fill_dc("2026-01-01")
    cuts = q.cut_reasons("2025-10-01")
    osa = q.osa_banner("2026-01-01")
    rouses = q.rouses_oos()

    k.agenda(["Service scorecard", "The storm and the recovery curve", "DC-level performance",
              "Cut reasons", "On-shelf availability", "The Rouses problem",
              "Q3 risks", "Actions"])

    k.exec_summary(
        f"Service is back to normal: {float(fill.fill.iloc[-1]):.1f}% fill and "
        f"{float(fill.otif.iloc[-1]):.1f}% OTIF in the latest month, against the ~52% storm trough in "
        "November 2025. The residual problem is not warehouse fill — it is on-shelf availability at "
        "specific Louisiana doors, where OSA in the high 50s and low 60s persists months after supply "
        "recovered. That is an execution problem, not a supply problem.",
        tiles=[(f"{float(fill.fill.iloc[-1]):.1f}%", "fill rate"),
               (f"{float(fill.otif.iloc[-1]):.1f}%", "on-time in full"),
               (f"{float(rouses.osa.min()):.0f}%", "worst Rouses door OSA"),
               (f"{float(rouses.oos_days.max()):.0f}", "OOS days, worst door, Q1")],
        bullets=[
            "**Warehouse service is fixed.** Fill and OTIF are at pre-storm levels across every DC.",
            f"**Store-level availability is not.** {len(rouses[rouses.osa < 70])} audited Rouses doors "
            "sit below 70% OSA on Crunchwell Original Mega, with up to "
            f"{float(rouses.oos_days.max()):.0f} out-of-stock days in Q1.",
            "**Every low-OSA door has a Larksfield endcap.** Empty shelf plus competitor display is "
            "how a supply event becomes a share event.",
            "**Q3 constraint:** the Pack Refresh changeover in weeks 33–35, which we are protecting "
            "at the cost of base-SKU fill.",
        ], headline="Warehouse fixed. Shelf not fixed.")

    chf = chart_line("r53_fill.png", list(fill.mo),
                     {"Fill rate (%)": [float(x) for x in fill.fill],
                      "OTIF (%)": [float(x) for x in fill.otif]},
                     title="Fill rate and OTIF by month (%)", pct=True, h=3.0)
    k.chart("THE CURVE", "A two-quarter recovery from a two-week event", chf,
            lede="The November trough is Hurricane Tonya. The shape of the recovery — not the depth "
                 "of the trough — is the thing worth fixing.",
            note="Source: shipments, monthly averages of Fill_Rate_Pct and On_Time_Pct.")

    drows = [[r.dc, f"{r.fill:.1f}%", f"{r.otif:.1f}%", f"{int(r.lines):,}"]
             for r in dc.itertuples()]
    crows = [[r.reason, f"{r.cut_k:,.1f}K", f"{r.fill:.1f}%"] for r in cuts.itertuples()]
    k.table("BY DC", "Lowest-performing retailer DCs, calendar 2026",
            ["Retailer DC", "Fill", "OTIF", "Order lines"], drows,
            widths=[0.46, 0.18, 0.18, 0.18],
            note="Source: shipments, 2026 year-to-date, ranked by fill rate ascending.")

    chc = chart_bar("r53_cuts.png", [r[:16] for r in cuts.reason],
                    [float(x) for x in cuts.cut_k],
                    title="Units cut by reason since Oct 2025 (000s)", color="rust", h=2.9)
    k.chart_table("CUT REASONS", "Storm, production lag and quality hold — in that order", chc,
                  ["Cut reason", "Units cut", "Fill on those lines"], crows,
                  widths=[0.42, 0.29, 0.29],
                  note="Source: shipments, Cut_Reason.")

    orows = [[r.banner, f"{r.osa:.1f}%", f"{r.pog:.1f}%", f"{r.facings:.2f}"]
             for r in osa.itertuples()]
    k.table("ON SHELF", "Banner-level OSA and planogram compliance, 2026",
            ["Banner", "OSA", "Planogram compliance", "Avg facings"], orows,
            widths=[0.34, 0.2, 0.26, 0.2],
            callout=("Averages hide the problem",
                     "Banner averages sit in the mid-90s. The Louisiana door-level audit shows OSA in "
                     "the 58–70% range on the exact SKUs losing share. Store-level, not banner-level, "
                     "is the unit of management here.", "risk"),
            note="Source: perfect_store, 2026 year-to-date.")

    rrows = [[r.sku_name[:30], r.city, f"{r.osa:.0f}%", f"{int(r.oos_days)}", f"{r.lift:.0f}%",
              str(r.lf_endcap)] for r in rouses.head(9).itertuples()]
    k.table("THE ROUSES PROBLEM", "Door-level audit: empty shelf next to a competitor endcap",
            ["SKU", "City", "OSA", "Q1 OOS days", "Promo lift", "Larksfield endcap"], rrows,
            widths=[0.30, 0.16, 0.12, 0.16, 0.14, 0.18], size=9.5,
            note="Source: seed_rouses_oos_by_door, audited doors.")

    k.risk("Q3 RISKS", "What could break service in the back half",
           [["Pack Refresh changeover, weeks 33–35",
             "Base-SKU fill dips 3–5 points for two weeks",
             "Pre-build hero SKUs in week 31–32; communicate to top-10 customers in advance",
             "VP Supply Chain"],
            ["ProteinPeak full-line authorisation at Walmart",
             "Launch allocation cuts spread to base protein SKUs",
             "Pre-agreed allocation rule with the brand team; capacity booked",
             "Supply Chain / Sage Park"],
            ["Louisiana store execution does not improve",
             "Recovery plan under-delivers even with supply fixed",
             "Weekly door-level OSA reporting; third-party merchandising in the 14 worst doors",
             "Marcus Boudreaux"],
            ["2026 hurricane season",
             "Repeat of the November 2025 pattern",
             "Pre-positioned inventory at Houston and Tyler from week 32; alternate DC routing agreed",
             "VP Supply Chain"]],
           note="Source: shipments, seed_rouses_oos_by_door, seed_innovation_pipeline.")

    k.reco("ACTIONS", "Four things out of this review",
           [("Fund third-party merchandising in the 14 worst Louisiana doors for 12 weeks",
             "Marcus Boudreaux", "From Aug 1"),
            ("Pre-build Pack Refresh hero SKUs in weeks 31–32 to protect base fill",
             "VP Supply Chain", "By Jul 31"),
            ("Move OSA reporting from banner to door level for the top-100 Acme volume stores",
             "Customer Logistics", "By Sep 1"),
            ("Pre-position Louisiana inventory ahead of the 2026 hurricane season",
             "VP Supply Chain", "By Aug 15")])

    k.close("The warehouse is fixed. The shelf is where the money is.",
            ["Fill and OTIF are back to normal service levels.",
             "Fourteen Louisiana doors are still below 70% OSA.",
             "Every one of them has a Larksfield endcap."])
    return k.build()


# ================================================== 54 · Trade effectiveness ==
def r54_trade_effectiveness():
    k = Deck("54-h1-2026-trade-promotion-effectiveness.pptx",
             kicker="TRADE PROMOTION EFFECTIVENESS",
             title="H1 FY2026 Post-Event Analysis",
             subtitle="43 events, $11.6M of spend, and the question of how much of the lift we "
                      "actually bought",
             byline="RGM with Trade Finance · for the commercial review · July 2026",
             short="H1 FY26 trade PEA")

    ev = q.trade_events_raw()
    byret = q.trade_events("retailer")
    bybrand = q.trade_events("brand")
    bymech = q.trade_events("mechanic")
    tb = q.trade_brand()

    tot_sp = ev.spend_kusd.sum() / 1000
    tot_inc = ev.incremental_revenue_kusd.sum() / 1000
    avg_lift = ev.modeled_lift_pct.mean()
    avg_idx = ev.modeled_incrementality_index.mean()

    k.agenda(["The headline", "By retailer", "By brand", "By mechanic",
              "The best and worst events", "What we stop doing", "Actions"])

    k.exec_summary(
        f"Q1 FY2026 ran {len(ev)} promoted events costing ${tot_sp:.1f}M and generating "
        f"${tot_inc:.1f}M of modelled incremental revenue at an average lift of {avg_lift:.1f}% and "
        f"an incrementality index of {avg_idx:.2f}. An index of {avg_idx:.2f} means roughly half of "
        "the volume we paid to move would have moved anyway. The spread between our best and worst "
        "mechanics is wide enough that fixing the mix — not cutting the budget — is the answer.",
        tiles=[(f"{len(ev)}", "events in the quarter"), (f"${tot_sp:.1f}M", "trade spend"),
               (f"${tot_inc:.1f}M", "modelled incremental revenue"),
               (f"{avg_idx:.2f}", "average incrementality index")],
        bullets=[
            f"**The portfolio index is {avg_idx:.2f}.** Best-in-class for this category is 0.65–0.70; "
            "we have a full 15 points of headroom.",
            f"**Average modelled lift is {avg_lift:.1f}%** — respectable on the surface, but lift and "
            "incrementality are different questions, and only the second one is worth paying for.",
            f"**Crunchwell carries ${float(bybrand[bybrand.brand=='Crunchwell'].spend.iloc[0])/1000:.1f}M "
            "of the quarter's spend** — the concentration risk and the biggest single opportunity.",
            "**The recommendation is a 0.45 index floor** on new events, which reallocates roughly "
            "$2.4M a quarter into mechanics that work.",
        ], headline="Half the volume we bought was already ours")

    chr_ = chart_grouped("r54_retailer.png", list(byret.retailer.head(7)),
                         {"Spend ($K)": [float(x) for x in byret.spend.head(7)],
                          "Incremental ($K)": [float(x) for x in byret.inc.head(7)]},
                         title="Q1 trade spend and modelled incremental revenue by retailer ($K)",
                         h=3.1)
    rrows = [[r.retailer, f"{int(r.events)}", money(r.spend / 1000, dp=1),
              money(r.inc / 1000, dp=1), f"{r.idx:.2f}",
              "Reinvest" if r.idx >= 0.55 else "Reallocate"]
             for r in byret.head(8).itertuples()]
    k.chart_table("BY RETAILER", "Where the money goes and what it returns", chr_,
                  ["Retailer", "Events", "Spend", "Incr.", "Index"],
                  [r[:5] for r in rrows], widths=[0.30, 0.16, 0.19, 0.19, 0.16], size=9.0,
                  note="Source: seed_trade_promo_events_q1_2026.")

    chb = chart_bar("r54_brand.png", list(bybrand.brand), [float(x) for x in bybrand.idx],
                    title="Modelled incrementality index by brand, Q1 FY26", color="sky", h=2.9)
    k.chart_bullets("BY BRAND", "The lean promoters are the efficient ones", chb,
                    [f"**ProteinPeak promotes least and converts best** — trade rate ~12.9% of gross "
                     "against Crunchwell's ~25.6%.",
                     "**Crunchwell's index is respectable on a huge base**, which is why the absolute "
                     "waste is concentrated there.",
                     "**HoneyNest is the worst combination:** heavy depth in a declining segment "
                     "(see the portfolio decision, Report 50).",
                     "**Rule of thumb from this quarter:** every 5 points of average depth costs "
                     "roughly 0.04 of index."],
                    note="Source: seed_trade_promo_events_q1_2026, seed_trade_spend_fy25.")

    bymech8 = q.roll_up(bymech, "mechanic", 8, sum_cols=("events", "spend", "inc"),
                        mean_cols=("lift", "idx"), other="All other mechanics")
    mrows = [[r.mechanic, f"{int(r.events)}", money(r.spend / 1000, dp=1), f"{r.lift:.1f}%",
              f"{r.idx:.2f}", "Keep" if r.idx >= 0.45 else "Stop"]
             for r in bymech8.itertuples()]
    k.table("BY MECHANIC", "Not every mechanic earns its place on the calendar",
            ["Mechanic", "Events", "Spend", "Avg lift", "Index", "Call"], mrows,
            widths=[0.30, 0.12, 0.16, 0.14, 0.13, 0.15], size=9.5,
            callout=("The 0.45 floor",
                     "Applying a 0.45 index floor to the Q1 calendar would have removed the "
                     "lowest-returning mechanics and freed roughly $2.4M for feature-and-display "
                     "weight, which indexes higher on every brand we run it on.", "action"),
            note="Source: seed_trade_promo_events_q1_2026, grouped by mechanic.")

    best = ev.nlargest(5, "modeled_incrementality_index")
    worst = ev.nsmallest(5, "modeled_incrementality_index")
    k.two_col("EXTREMES", "The five best and five worst events of the quarter",
              "Best five (by index)",
              [f"**{r.brand} at {r.retailer}** — {r.mechanic}, {r.depth_pct:.0f}% off, "
               f"index {r.modeled_incrementality_index:.2f}" for r in best.itertuples()],
              "Worst five (by index)",
              [f"**{r.brand} at {r.retailer}** — {r.mechanic}, {r.depth_pct:.0f}% off, "
               f"index {r.modeled_incrementality_index:.2f}" for r in worst.itertuples()],
              note="Source: seed_trade_promo_events_q1_2026, ranked by modelled incrementality index.")

    k.reco("ACTIONS", "What changes in the Q3 and Q4 calendar",
           [("Adopt a 0.45 modelled-incrementality floor for all new events",
             "RGM Lead / Trade Finance", "From Aug 1"),
            ("Reallocate the freed ~$2.4M/quarter into feature-and-display weight, not depth",
             "NAM team", "Q3–Q4 calendar"),
            ("Cap Crunchwell Mega depth at 20% and stop depth stacking with retailer funds",
             "Marcus Boudreaux", "Q3 calendar"),
            ("Cut HoneyNest promoted events in line with the harvest decision (Report 50)",
             "HoneyNest BM", "FY27 calendar"),
            ("Report index alongside spend in the monthly commercial review", "Trade Finance",
             "From August")])

    k.close(f"An index of {avg_idx:.2f} is the cheapest money in the plan.",
            [f"{len(ev)} events, ${tot_sp:.1f}M, ${tot_inc:.1f}M modelled incremental.",
             "0.45 floor frees ~$2.4M a quarter without cutting the budget.",
             "Fewer, better events — starting with the Q3 calendar."])
    return k.build()


# ==================================================== 55 · Media effectiveness =
def r55_media_effectiveness():
    k = Deck("55-h1-2026-marketing-mix-media-effectiveness.pptx",
             kicker="MARKETING MIX & MEDIA EFFECTIVENESS",
             title="H1 FY2026 Media Read",
             subtitle="What the mix model and the retail-media incrementality work say we should "
                      "stop, start and shift",
             byline="Hugo Lin, Director — Performance Marketing, with the CMO · July 2026",
             short="H1 FY26 media read")

    rm = q.retail_media()
    rmb = q.retail_media_brand()
    per = q.mkt_by_period()
    cw = q.mkt_spend("Crunchwell")
    pp = q.mkt_spend("ProteinPeak")
    sent = q.sentiment()

    ratio = rm.inc_m.sum() / rm.spend_m.sum()

    k.agenda(["The headline", "Spend by period and brand", "Retail-media incrementality",
              "Platform-reported versus modelled", "Two brands, two mixes",
              "Creator and social signal", "The H2 reallocation", "Actions"])

    k.exec_summary(
        f"Q1 retail media spent ${rm.spend_m.sum():.1f}M and returned ${rm.inc_m.sum():.2f}M of "
        f"modelled incremental revenue — ${ratio:.2f} per dollar. The average hides everything that "
        f"matters: Walmart Connect returns {float(rm[rm.platform=='Walmart Connect'].ratio.iloc[0]):.2f} "
        f"while Amazon Ads returns {float(rm[rm.platform=='Amazon Ads'].ratio.iloc[0]):.2f} on more "
        "than twice the spend. The recommendation is a $700K in-quarter reallocation and a structural "
        "mix shift for FY27.",
        tiles=[(f"${ratio:.2f}", "modelled incremental per $1"),
               (f"{float(rm[rm.platform=='Walmart Connect'].ratio.iloc[0]):.2f}", "best platform ratio"),
               (f"{float(rm[rm.platform=='Amazon Ads'].ratio.iloc[0]):.2f}", "worst platform ratio"),
               ("$700K", "recommended reallocation")],
        bullets=[
            f"**Amazon Ads is ${float(rm[rm.platform=='Amazon Ads'].spend_m.iloc[0]):.1f}M of the "
            f"${rm.spend_m.sum():.1f}M** at a modelled ratio of "
            f"{float(rm[rm.platform=='Amazon Ads'].ratio.iloc[0]):.2f}. It is the single largest "
            "efficiency leak we have.",
            "**Platform-reported ROAS is not the measure.** Amazon reports positive ROAS on the same "
            "spend our incrementality model marks as substantially cannibalised.",
            "**Crunchwell and ProteinPeak run opposite mixes** — TV-led versus creator-led — and the "
            "creator-led brand is the one growing.",
            f"**Social sentiment tracks the mix:** ProteinPeak +{float(sent[sent.brand=='ProteinPeak'].sent.iloc[0]):.2f} "
            f"versus Crunchwell {float(sent[sent.brand=='Crunchwell'].sent.iloc[0]):+.2f}.",
        ], headline="The average is fine. The distribution is not.")

    chr_ = chart_bar("r55_ratio.png", list(rm.platform), [float(x) for x in rm.ratio],
                    title="Modelled incrementality ratio by platform, Q1 FY26",
                    colors_list=["#B24A2E" if v < 0.55 else ("#B98A2E" if v < 1.0 else "#2E7D75")
                                 for v in rm.ratio], h=2.9)
    rows = [[r.platform, money(r.spend_m), money(r.inc_m, dp=2), f"{r.rroas:.2f}", f"{r.ratio:.2f}"]
            for r in rm.itertuples()]
    rows.append(["Total", money(rm.spend_m.sum()), money(rm.inc_m.sum(), dp=2),
                 f"{rm.rroas.mean():.2f}", f"{ratio:.2f}"])
    k.chart_table("INCREMENTALITY", "Two platforms are subsidising two others", chr_,
                  ["Platform", "Spend", "Modelled incr.", "Reported ROAS", "Modelled ratio"],
                  rows, widths=[0.32, 0.16, 0.18, 0.17, 0.17], total_row=True, size=9.0,
                  note="Source: seed_retail_media_spend_q1_2026. Modelled ratio governs decisions; "
                       "platform-reported ROAS is shown for contrast.")

    chg = chart_grouped("r55_gap.png", list(rm.platform),
                        {"Platform-reported ROAS": [float(x) for x in rm.rroas],
                         "Modelled incrementality": [float(x) for x in rm.ratio]},
                        title="Reported ROAS versus modelled incrementality", h=3.1)
    k.chart_bullets("THE GAP", "Why we govern on modelled incrementality", chg,
                    ["**Every platform reports a better number than the model produces.** That is "
                     "expected — platform attribution counts conversions the model attributes to base.",
                     "**Amazon has the widest gap:** reported "
                     f"{float(rm[rm.platform=='Amazon Ads'].rroas.iloc[0]):.2f} against modelled "
                     f"{float(rm[rm.platform=='Amazon Ads'].ratio.iloc[0]):.2f}.",
                     "**Walmart Connect is the narrowest gap** and the only platform above 1.0 on "
                     "the modelled measure.",
                     "**Governance rule:** budget decisions use modelled incrementality; platform "
                     "dashboards are for in-flight optimisation only (see Report 75)."],
                    note="Source: seed_retail_media_spend_q1_2026.")

    chc = chart_donut("r55_cw.png", [c[:18] for c in cw.channel.head(6)],
                      [float(x) for x in cw.spend_m.head(6)], title="Crunchwell A&P mix ($M)")
    chp = chart_donut("r55_pp.png", [c[:18] for c in pp.channel.head(6)],
                      [float(x) for x in pp.spend_m.head(6)], title="ProteinPeak A&P mix ($M)")
    k.charts2("TWO MIXES", "The growing brand and the flat brand spend differently", chc, chp,
              captions=[f"Crunchwell: ${cw.spend_m.sum():.1f}M, Linear-TV-led. Reach against a "
                        "shrinking occasion.",
                        f"ProteinPeak: ${pp.spend_m.sum():.1f}M, paid-social and creator-led with "
                        "retail media close behind."],
              note="Source: seed_marketing_spend by brand and channel.")

    chper = chart_bar("r55_period.png", list(per.period), [float(x) for x in per.spend_m],
                      title="Total A&P spend by period ($M)", color="navy", unit="M", h=2.9)
    k.chart_table("PHASING", "Spend is lumpy in a category that is bought weekly", chper,
                  ["Period", "A&P $M"],
                  [[r.period, money(r.spend_m)] for r in per.itertuples()],
                  widths=[0.55, 0.45],
                  note="Source: seed_marketing_spend, by period.")

    k.table("THE MOVE", "The H2 reallocation, platform by platform",
            ["Platform", "Q1 spend", "H2 recommendation", "Rationale"],
            [["Amazon Ads", money(float(rm[rm.platform == 'Amazon Ads'].spend_m.iloc[0])),
              "−$700K", "Ratio 0.40; largest leak in the plan"],
             ["Walmart Connect", money(float(rm[rm.platform == 'Walmart Connect'].spend_m.iloc[0])),
              "+$350K", "Ratio 1.20; the only platform above 1.0"],
             ["Kroger Precision", money(float(rm[rm.platform == 'Kroger Precision Marketing'].spend_m.iloc[0])),
              "+$200K", "Ratio 0.77 and improving"],
             ["Louisiana injection (cross-platform)", "—", "+$150K",
              "2.2x portfolio ROI on the LA recovery leg"],
             ["Net", money(rm.spend_m.sum()), "$0", "Reallocation, not incremental budget"]],
            widths=[0.28, 0.16, 0.20, 0.36], align_right_from=9, total_row=True, size=9.5,
            note="Source: seed_retail_media_spend_q1_2026; H2 figures are the recommended plan.")

    k.reco("ACTIONS", "What we are asking for",
           [("Approve the $700K reallocation out of Amazon Ads", "CFO / Tasha Brooks", "By Aug 1"),
            ("Adopt modelled incrementality as the single budget-governing metric",
             "Hugo Lin / Tasha Brooks", "From Aug 1"),
            ("Shift a third of Crunchwell's Linear TV line into CTV, creator and retail media in FY27",
             "CMO / Cory Whitman", "FY27 planning"),
            ("Smooth A&P phasing to match weekly category purchase behaviour", "Hugo Lin",
             "FY27 planning"),
            ("Re-read incrementality at week 8 and week 13 post-reallocation", "Hugo Lin", "Q4 FY26")])

    k.close("Stop paying the platform that reports best and delivers least.",
            [f"${ratio:.2f} per dollar blended, 0.40 at Amazon, 1.20 at Walmart.",
             "$700K moves now; the Crunchwell mix shift moves in FY27.",
             "One metric governs: modelled incrementality."])
    return k.build()


# ===================================================== 56 · Brand equity ======
def r56_brand_equity_tracker():
    k = Deck("56-q2-2026-brand-equity-consumer-health-tracker.pptx",
             kicker="BRAND EQUITY & CONSUMER HEALTH",
             title="Q2 FY2026 Tracker Read",
             subtitle="Six waves of equity data across the portfolio, and the one attribute that "
                      "explains the Crunchwell problem",
             byline="Nina Ortega, VP Consumer Insights · July 2026",
             short="Q2 FY26 equity tracker")

    cw = q.equity("Crunchwell", "US-NAT")
    cwla = q.equity("Crunchwell", "LA-DMA")
    pp = q.equity("ProteinPeak", "US-NAT")
    fh = q.equity("Field & Honey", "US-NAT")
    nps = q.nps()
    sent = q.sentiment()
    coh = q.cohorts()

    k.agenda(["What the tracker is telling us", "Crunchwell national", "Crunchwell Louisiana",
              "ProteinPeak", "Competitive: Field & Honey", "NPS and awareness",
              "Social sentiment", "Cohort penetration", "Implications"])

    k.exec_summary(
        f"Across six waves, Crunchwell's Relevance fell from {cw['Relevance'].iloc[0]:.1f} to "
        f"{cw['Relevance'].iloc[-1]:.1f} while Trust rose from {cw['Trust'].iloc[0]:.1f} to "
        f"{cw['Trust'].iloc[-1]:.1f}. That is the single most important finding in the tracker: the "
        "brand is credible and increasingly irrelevant. ProteinPeak shows the opposite profile, and "
        "Field & Honey is gaining on both.",
        tiles=[(f"{cw['Relevance'].iloc[-1] - cw['Relevance'].iloc[0]:+.1f} pp", "Crunchwell Relevance"),
               (f"{cw['Trust'].iloc[-1] - cw['Trust'].iloc[0]:+.1f} pp", "Crunchwell Trust"),
               (f"{float(nps.nps.iloc[-1]):.1f}", "NPS, latest wave"),
               (f"{float(nps.aided.iloc[-1]):.0f}%", "aided awareness")],
        bullets=[
            "**Relevance, not Trust.** Every diagnostic points the same way: consumers believe in "
            "Crunchwell and do not think it is for them.",
            f"**Modernity at {cw['Modernity'].iloc[-1]:.1f}** is the weakest attribute in the set. "
            "The Pack Refresh is the direct intervention.",
            f"**Louisiana is worse than national on every attribute** — Relevance at "
            f"{cwla['Relevance'].iloc[-1]:.1f} versus {cw['Relevance'].iloc[-1]:.1f} nationally.",
            f"**ProteinPeak's profile is inverted:** Relevance {pp['Relevance'].iloc[-1]:.1f} and "
            f"Modernity {pp['Modernity'].iloc[-1]:.1f}, both above Crunchwell.",
        ], headline="One finding matters more than the rest")

    attrs = ["Relevance", "Trust", "Taste", "Quality", "Modernity"]
    chcw = chart_line("r56_cw.png", list(cw.index),
                      {a: [float(x) for x in cw[a]] for a in attrs},
                      title="Crunchwell equity, top-two-box (%) — US National", pct=True, h=3.2)
    k.chart_table("CRUNCHWELL", "Six waves, five attributes, one problem", chcw,
                  ["Attribute", "FY25Q1", "FY26Q2", "Δ pp"],
                  [[a, f"{cw[a].iloc[0]:.1f}", f"{cw[a].iloc[-1]:.1f}",
                    f"{cw[a].iloc[-1] - cw[a].iloc[0]:+.1f}"] for a in attrs],
                  widths=[0.34, 0.22, 0.22, 0.22],
                  note="Source: brand_equity_quarterly, Crunchwell US-NAT.")

    chla = chart_grouped("r56_la.png", attrs,
                         {"US National": [float(cw[a].iloc[-1]) for a in attrs],
                          "Louisiana DMA": [float(cwla[a].iloc[-1]) for a in attrs]},
                         title="Crunchwell equity, FY26Q2: national versus Louisiana (%)",
                         pct=True, h=3.1)
    k.chart_bullets("LOUISIANA", "The share loss shows up in the equity data too", chla,
                    [f"**Relevance {cwla['Relevance'].iloc[-1]:.1f} in Louisiana** against "
                     f"{cw['Relevance'].iloc[-1]:.1f} nationally.",
                     f"**Trust holds locally at {cwla['Trust'].iloc[-1]:.1f}** — the franchise is "
                     "not damaged, the presence is.",
                     "**Reading it with the distribution data:** eight weeks of empty shelf next to a "
                     "Larksfield endcap is a relevance event as much as an availability event.",
                     "**Implication for the recovery plan:** facings and OSA first, then message. "
                     "Message into an empty shelf is wasted."],
                    note="Source: brand_equity_quarterly (LA-DMA vs US-NAT), seed_rouses_oos_by_door.")

    chpp = chart_line("r56_pp.png", list(pp.index),
                      {a: [float(x) for x in pp[a]] for a in attrs},
                      title="ProteinPeak equity, top-two-box (%)", pct=True, h=3.0)
    chfh = chart_line("r56_fh.png", list(fh.index),
                      {a: [float(x) for x in fh[a]] for a in attrs},
                      title="Field & Honey (Larksfield) equity, top-two-box (%)", pct=True, h=3.0)
    k.charts2("THE CONTRAST", "One brand building, one competitor building faster", chpp, chfh,
              captions=[f"ProteinPeak: Relevance {pp['Relevance'].iloc[-1]:.1f}, "
                        f"Modernity {pp['Modernity'].iloc[-1]:.1f} — the profile of a brand people "
                        "want to be seen buying.",
                        f"Field & Honey: Relevance {fh['Relevance'].iloc[-1]:.1f} and rising. "
                        "The aggressor is winning the attribute we are losing."],
              note="Source: brand_equity_quarterly.")

    nrows = [[r.wave, f"{r.nps:.2f}", f"{r.aided:.1f}%", f"{r.taste:.2f}", f"{r.price_sens:.2f}"]
             for r in nps.itertuples()]
    k.table("CONSUMER HEALTH", "NPS, awareness, taste and price sensitivity by wave",
            ["Wave", "NPS", "Aided awareness", "Taste (1–5)", "Price sensitivity (1–5)"], nrows,
            widths=[0.20, 0.16, 0.24, 0.20, 0.20],
            callout=("Awareness is not the problem",
                     f"Aided awareness runs around {float(nps.aided.mean()):.0f}% and NPS is flat at "
                     f"about {float(nps.nps.mean()):.1f}. Price sensitivity is stable. We are not "
                     "short of awareness, affection or affordability — we are short of relevance.",
                     "info"),
            note="Source: brand_health (n=16,500 responses across waves).")

    srows = [[r.brand, f"{int(r.mentions):,}", f"{r.sent:+.2f}", f"{r.reach_m:.1f}M"]
             for r in sent.head(8).itertuples()]
    chs = chart_bar("r56_sent.png", list(sent.brand.head(8)), [float(x) for x in sent.sent.head(8)],
                    title="Social sentiment by brand, 2026 (−1 to +1)",
                    colors_list=["#2E7D75" if v > 0.15 else ("#B98A2E" if v > 0 else "#B24A2E")
                                 for v in sent.sent.head(8)], h=2.9)
    k.chart_table("SOCIAL", "Conversation confirms the tracker", chs,
                  ["Brand", "Mentions", "Sentiment", "Reach"], srows,
                  widths=[0.34, 0.22, 0.22, 0.22], size=9.0,
                  note="Source: social_mentions, calendar 2026.")

    k.reco("IMPLICATIONS", "What the insights team is asking the business to do",
           [("Adopt Relevance and Modernity as reported KPIs on the Crunchwell scorecard",
             "Nina Ortega / Cory Whitman", "FY27Q1"),
            ("Sequence the Louisiana recovery as availability first, message second",
             "Marcus Boudreaux", "From Aug 1"),
            ("Brief the FY27 Crunchwell platform against Relevance, not Trust or value",
             "Cory Whitman", "By Jul 15"),
            ("Add Field & Honey to the standing competitive tracker read", "Comp Intel", "Q3 FY26"),
            ("Recut the tracker by the four Kantar cohorts each wave, not just nationally",
             "Jordan Hsu", "Next wave")])

    k.close("Trusted, liked, affordable — and not for me.",
            ["Relevance −5.9 pp; Trust +0.6 pp.",
             "Louisiana is worse on every attribute except Trust.",
             "The Pack Refresh and the platform both aim at the right target."])
    return k.build()


# =============================================== 57 · Category state of business
def r57_category_sob():
    k = Deck("57-q3-2026-category-state-of-the-business.pptx",
             kicker="CATEGORY STATE OF THE BUSINESS",
             title="Q3 FY2026 Category Read",
             subtitle="Three data sources, three answers, one reconciliation — and the consumer "
                      "narrative for the back half",
             byline="Nina Ortega, VP Consumer Insights · executive committee, July 22 2026",
             short="Q3 FY26 category SOB")

    c25 = q.catgrowth("FY2025")
    wp = q.cat_row("Q2-FY2026-MTD", "Wellness Protein")
    tot = q.cat_row("Q2-FY2026-MTD", "Total")
    la = q.cat_row("Q1-FY2026", "Total", "Louisiana DMA")
    sh = q.share_quarter()
    coh = q.cohorts()
    mac = q.macro(9)

    k.agenda(["The reconciliation problem", "Category size and growth", "Segment winners and losers",
              "Acme share by instrument", "Cohort dynamics", "Macro trends",
              "The consumer narrative", "What it means for FY27"])

    k.exec_summary(
        "The category is growing slowly and unevenly: RTE Cereal total US is up about 1.4% in Q2 "
        f"QTD while Wellness Protein is up {wp.growth:+.1f}%. Our three instruments — syndicated "
        "retail measurement, household panel and internal POS — disagree on the level of Acme's "
        "share by up to two points, and reconciling them is most of the analytical work. The "
        "direction, though, is unanimous.",
        tiles=[(f"{tot.growth:+.1f}%", "RTE total US growth, Q2 QTD"),
               (f"{wp.growth:+.1f}%", "Wellness Protein growth"),
               (f"{la.growth:+.1f}%", "Louisiana category growth"),
               (f"{sh.acme.iloc[-1]:.2f}%", "Acme share, syndicated")],
        bullets=[
            "**Three instruments, three answers.** Syndicated value share reads Acme at "
            f"{sh.acme.iloc[-1]:.2f}%; the category database reads {tot.acme_share:.1f}%; internal POS "
            "reads differently again. Each is right on its own definition.",
            f"**The Louisiana category itself is shrinking** at {la.growth:+.1f}% — roughly a fifth of "
            "our local share story is the pond, not the fish.",
            "**Cohort dynamics are the real narrative:** cereal-skipper households are growing and "
            "loyal-family is eroding. We are losing breakfast occasions, not brand preference.",
            "**GLP-1 sits at 0.81 trend strength with a downward volume direction** — the most "
            "important structural item on this page.",
        ], headline="The reconciliation is the read")

    top = c25.head(9)
    chs = chart_bar("r57_segments.png", [s[:18] for s in top.subcategory],
                    [float(x) for x in top.growth],
                    title="Segment growth, FY25 (% YoY)", pct=True,
                    colors_list=["#2E7D75" if v > 5 else ("#B98A2E" if v > 0 else "#B24A2E")
                                 for v in top.growth], horizontal=False, h=3.0)
    srows = [[r.subcategory, r.category[:16], f"${r.size:,.0f}M", f"{r.growth:+.1f}%",
              f"{r.share:.1f}%"] for r in top.itertuples()]
    k.chart_table("THE CATEGORY", "Growth is concentrated in three pockets", chs,
                  ["Segment", "Category", "Size", "Growth", "Acme share"], srows,
                  widths=[0.28, 0.22, 0.18, 0.16, 0.16], size=9.0,
                  note="Source: seed_category_market_size, FY2025 US National.")

    la_sh = q.share_quarter(la=True)
    chsh = chart_line("r57_share.png", list(sh.q),
                      {"Acme national": [float(x) for x in sh.acme],
                       "Larksfield national": [float(x) for x in sh.lf],
                       "Private label national": [float(x) for x in sh.pl],
                       "Acme Louisiana": [float(x) for x in la_sh.acme]},
                      title="RTE-cereal value share (%)", pct=True, h=3.1)
    k.chart_bullets("SHARE", "Nationally stable, locally broken", chsh,
                    [f"**Acme national holds at {sh.acme.iloc[-1]:.2f}%** across six quarters — "
                     "stability, not growth.",
                     f"**Larksfield at {sh.lf.iloc[-1]:.2f}%** and still the share gainer nationally.",
                     f"**Private label at {sh.pl.iloc[-1]:.2f}%** is flat — this is not a "
                     "trade-down story.",
                     f"**Acme Louisiana at {la_sh.acme.iloc[-1]:.2f}%** after bottoming at "
                     f"{la_sh.acme.min():.2f}% — the recovery has started but is a long way from done."],
                    note="Source: syndicated_weekly, RTE Cereal, quarterly averages.")

    chc = chart_line("r57_cohorts.png", list(coh.index),
                     {c: [float(x) for x in coh[c]] for c in coh.columns},
                     title="Household penetration by cohort (%)", pct=True, h=3.1)
    k.chart_table("THE CONSUMER", "Occasions, not preference", chc,
                  ["Cohort", "FY25Q1", "FY26Q2", "Direction"],
                  [[c, f"{coh[c].iloc[0]:.1f}%", f"{coh[c].iloc[-1]:.1f}%",
                    "Growing" if coh[c].iloc[-1] > coh[c].iloc[0] else "Eroding"]
                   for c in coh.columns],
                  widths=[0.34, 0.2, 0.2, 0.26], size=9.5,
                  note="Source: kantar_worldpanel_cohort, US-NAT.")

    mrows = [[r.topic, f"{r.strength:.2f}", r.phase, r.direction, str(r.cats)[:26]]
             for r in mac.itertuples()]
    k.table("MACRO", "Nine trends, ranked by strength",
            ["Trend", "Strength", "Phase", "Direction", "Categories"], mrows,
            widths=[0.30, 0.13, 0.14, 0.19, 0.24], size=9.0,
            callout=("The one to plan against",
                     "GLP-1 appetite shift at 0.81 strength with a downward volume direction is the "
                     "trend most likely to change the shape of the category by FY29. It argues for "
                     "smaller packs, higher protein and premium price-per-serving — all three of "
                     "which are in the FY27 plan.", "risk"),
            note="Source: seed_macro_trends, ranked by strength.")

    k.two_col("NARRATIVE", "The consumer story for the back half",
              "What is true",
              ["Breakfast is being skipped, not switched — cereal-skipper penetration is up 2.5 points.",
               "Protein is the permission structure for the occasion to come back.",
               "Chocolate and cinnamon are the flavour cues with momentum (0.81 cinnamon trend).",
               "Value-seeking is stable; this is not a recession story.",
               "Kids' cereal is structurally pressured by parent guilt, not by price."],
              "What it means for FY27",
              ["Fund protein and single-serve; both answer the occasion problem directly.",
               "Reposition Crunchwell on relevance, not on value or heritage.",
               "Harvest Kids Sweet rather than relaunching it.",
               "Plan pack architecture for smaller portions and higher price-per-serving.",
               "Treat Louisiana as an execution recovery, not a consumer-preference problem."],
              note="Source: kantar_worldpanel_cohort, seed_macro_trends, seed_category_market_size, "
                   "brand_equity_quarterly.")

    k.reco("ACTIONS", "What the executive committee is asked to take from this",
           [("Adopt the occasion-loss narrative as the FY27 planning frame", "Executive committee",
             "FY27 planning"),
            ("Publish one reconciled share number per brand per month with the instrument named",
             "Nina Ortega / Jordan Hsu", "From August"),
            ("Fund protein and single-serve ahead of family-size volume in FY27",
             "VP Brand / CFO", "FY27 planning"),
            ("Add a GLP-1 sensitivity to the FY27–FY29 long-range plan", "Strategy / FP&A",
             "Q4 FY26"),
            ("Recut the tracker and panel by cohort every wave", "Jordan Hsu", "Next wave")])

    k.close("People are not switching away from us. They are skipping breakfast.",
            ["Cereal-skipper households up 2.5 points in six quarters.",
             "Protein and single-serve are the answers we already own.",
             "One reconciled share number, published monthly."])
    return k.build()


# ================================================= 58 · Louisiana diagnostic ===
def r58_louisiana_diagnostic():
    k = Deck("58-louisiana-dma-share-decline-diagnostic-recovery.pptx",
             kicker="DIAGNOSTIC & RECOVERY PLAN",
             title="Crunchwell Louisiana — What Happened and What We Do About It",
             subtitle="Five hypotheses, one attribution, and a three-leg recovery plan with "
                      "named owners",
             byline="Jordan Hsu (diagnostic) with Marcus Boudreaux (recovery) · July 2026",
             short="LA diagnostic")

    la = q.share_quarter(la=True)
    natl = q.share_quarter()
    ch = q.share_channel(la=True)
    dist = q.distribution(la=True)
    geo = q.geos()
    end = q.endcap_la()
    rouses = q.rouses_oos()
    pos = q.pos("Crunchwell", "LA-DMA")

    k.agenda(["The number", "National versus Louisiana", "Channel and distribution",
              "The Walmart shelf audit", "The Rouses door audit", "Five hypotheses, one attribution",
              "The three-leg recovery plan", "Leading indicators to watch", "The ask"])

    k.exec_summary(
        "Crunchwell's Louisiana share fell from about 6.4% at the Mass/Grocery peak to 3.0% in Q1 "
        f"FY2026 — 340 basis points — against a flat national trend. The value-weighted all-channel "
        f"cut reads milder ({la.cw.max():.2f}% to {la.cw.min():.2f}%) in the same direction. Root "
        "cause is now attributed across five hypotheses, with the September 2025 Walmart modular "
        "reset accounting for roughly 55% of it. The recovery plan has three legs and is funded.",
        tiles=[("−340 bps", "canonical peak-to-trough"), ("55%", "attributed to the Walmart reset"),
               (f"{float(rouses.osa.min()):.0f}%", "worst door OSA"),
               ("2.2x", "ROI on the LA media leg")],
        bullets=[
            "**The signal existed before the alarm.** Q4 2025 was already down; the quarter-level "
            "read was three months ahead of the escalation.",
            f"**Louisiana share bottomed at {la.cw.min():.2f}% in {la.q.iloc[la.cw.idxmin()]}** and has "
            f"recovered to {la.cw.iloc[-1]:.2f}% — roughly a third of the loss, no more.",
            "**Attribution:** Walmart facing reset ~55%, Larksfield promo intensity ~20%, Hurricane "
            "Tonya supply ~12%, private label ~8%, Hispanic-shopper mix ~5%.",
            "**The category shrank too** — Louisiana RTE is −2.8% — so roughly a fifth of the story "
            "is the pond, not the fish.",
        ], headline="340 basis points, five causes, one dominant one")

    chsh = chart_line("r58_share.png", list(la.q),
                      {"Crunchwell Louisiana": [float(x) for x in la.cw],
                       "Crunchwell national": [float(x) for x in natl.cw],
                       "Larksfield Louisiana": [float(x) for x in la.lf]},
                      title="Value share (%) — Louisiana versus national", pct=True, h=3.1)
    k.chart_bullets("THE NUMBER", "A local break against a flat national line", chsh,
                    [f"**Crunchwell Louisiana {la.cw.iloc[0]:.2f}% → {la.cw.min():.2f}% → "
                     f"{la.cw.iloc[-1]:.2f}%.**",
                     f"**National held at about {natl.cw.iloc[-1]:.2f}%** through the same period — "
                     "this is not a franchise problem.",
                     f"**Larksfield held roughly {la.lf.mean():.1f}% locally** while taking our "
                     "displaced volume through endcap presence rather than share-of-shelf gains.",
                     "**The canonical headline is the Mass/Grocery peak-to-trough**: 6.4% → 3.0%. "
                     "Both cuts are shown so the numbers reconcile across documents."],
                    note="Source: syndicated_weekly (LA-DMA vs ex-LA), docs/louisiana-decline.md "
                         "canonical headline.")

    chch = chart_bar("r58_channel.png", list(ch.Channel),
                     [float(a - b) for a, b in zip(ch.after, ch.before)],
                     title="Crunchwell LA share change by channel, H2 2025 → 2026 (pp)", h=2.9)
    drows = [[r.q, f"{r.acv:.1f}%", f"{int(r.tdp)}", f"{r.facings:.2f}", f"{r.promo:.1f}%"]
             for r in dist.itertuples()]
    k.chart_table("CHANNEL & SHELF", "Grocery and E-commerce fell hardest; facings fell with them",
                  chch, ["Quarter", "ACV", "TDP", "Avg facings", "Promo share"], drows,
                  widths=[0.24, 0.19, 0.19, 0.20, 0.18],
                  note="Source: syndicated_weekly, LA-DMA, RTE Cereal.")

    end8 = q.roll_up(end, "city", 8, sum_cols=("stores",),
                     mean_cols=("lf_endcaps", "acme_endcaps", "pl_endcaps", "cw_mega_facings",
                                "fh_facings", "oos_pct"), other="All other LA cities")
    erows = [[r.city, f"{int(r.stores)}", f"{r.lf_endcaps:.2f}", f"{r.acme_endcaps:.2f}",
              f"{r.cw_mega_facings:.2f}", f"{r.fh_facings:.2f}", f"{r.oos_pct:.0f}%"]
             for r in end8.itertuples()]
    k.table("WALMART AUDIT", "The shelf tells the story better than the share number does",
            ["City", "Stores", "Larksfield endcaps", "Acme endcaps", "CW Mega facings",
             "F&H facings", "Mega OOS"], erows,
            widths=[0.18, 0.11, 0.17, 0.15, 0.15, 0.13, 0.11], size=9.0,
            callout=("The mechanism, in one line",
                     "Larksfield averages more than two endcaps per store to Acme's fraction of one, "
                     "and Field & Honey holds more facings than Crunchwell Mega in every audited "
                     "city. The reset did not just cut our facings — it handed the display to the "
                     "competitor.", "risk"),
            note="Source: seed_walmart_endcap_audit_la, 62 audited stores.")

    rrows = [[r.sku_name[:28], r.city, f"{r.osa:.0f}%", f"{int(r.oos_days)}", f"{r.lift:.0f}%",
              str(r.lf_endcap)] for r in rouses.head(8).itertuples()]
    k.table("ROUSES AUDIT", "Fifteen doors, and the pattern is the same in all of them",
            ["SKU", "City", "OSA", "Q1 OOS days", "Promo response", "Larksfield endcap"], rrows,
            widths=[0.30, 0.16, 0.12, 0.16, 0.16, 0.10], size=9.5,
            note="Source: seed_rouses_oos_by_door.")

    cha = chart_bar("r58_attrib.png",
                    ["H1 Walmart reset", "H2 Larksfield promo", "H3 Storm supply",
                     "H4 Private label", "H5 Hispanic mix"],
                    [55, 20, 12, 8, 5], title="Attribution of the 340 bps decline (%)",
                    colors_list=["#B24A2E", "#B98A2E", "#3E6DA8", "#5B6472", "#5B6472"], h=2.9)
    k.chart_bullets("ATTRIBUTION", "Five hypotheses tested, one dominant cause", cha,
                    ["**H1 — Walmart modular reset (Sep 2025):** Crunchwell Mega cut from 8 facings "
                     "to 6. The largest single driver at ~55%.",
                     "**H2 — Larksfield promo intensity at Rouses:** ~20%, and the endcap audit shows "
                     "the mechanism.",
                     "**H3 — Hurricane Tonya supply:** ~12%. Houston-DC fill fell to about 52% and "
                     "OSA has still not fully recovered at door level.",
                     "**H4/H5 — private label and Hispanic-shopper mix:** ~8% and ~5%. Both real, "
                     "both slow-moving; neither can explain an eight-week break."],
                    note="Source: seed_walmart_endcap_audit_la, seed_rouses_oos_by_door, shipments, "
                         "syndicated_weekly, seed_geographies.")

    k.table("RECOVERY PLAN", "Three legs, named owners, measurable in 12 weeks",
            ["Leg", "What we do", "Investment", "Owner", "12-week measure"],
            [["1 · Shelf", "Restore Crunchwell Mega to 8 facings at Walmart LA; win one endcap per "
              "supercenter", "Line-review ask", "Marcus Boudreaux", "Facings ≥7.5 avg; 1+ endcap"],
             ["2 · Availability", "Third-party merchandising in the 14 worst doors; Rouses OSA "
              "recovery programme", "≈$0.4M", "Customer Logistics", "OSA ≥90% in audited doors"],
             ["3 · Demand", "LA retail-media injection plus targeted Rouses trade at capped depth",
              "≈$1.1M", "Tasha Brooks / NAM", "LA share ≥4.0%"]],
            widths=[0.13, 0.34, 0.14, 0.19, 0.20], align_right_from=9, size=9.5,
            note="Source: recovery plan as funded; ROI on the media leg is 2.2x portfolio average "
                 "per seed_retail_media_spend_q1_2026.")

    grows = [[r.geo_name[:24], f"{r.fy25:.1f}%", f"{r.q126:.1f}%", f"{int(r.bps)}", r.priority_tier[:16]]
             for r in geo.head(8).itertuples()]
    k.table("EARLY WARNING", "Birmingham and Memphis are the next two dominoes",
            ["Market", "FY25", "Q1 FY26", "Δ bps", "Tier"], grows,
            widths=[0.32, 0.16, 0.16, 0.14, 0.22], size=9.5,
            callout=("Do not wait for the alarm again",
                     "Birmingham (−30 bps) and Memphis (−30 bps) show the same early pattern "
                     "Louisiana showed in Q4 2025. Weekly facing and OSA monitoring in both DMAs "
                     "costs almost nothing and buys a quarter of warning.", "action"),
            note="Source: seed_geographies.")

    k.reco("THE ASK", "What we need agreed today",
           [("Take the facing restoration (6 → 8 on Mega) into the Walmart August line review as a "
             "non-negotiable", "Marcus Boudreaux", "Aug line review"),
            ("Fund third-party merchandising in the 14 worst doors for 12 weeks", "Customer Logistics",
             "From Aug 1"),
            ("Release the LA retail-media injection at 2.2x portfolio ROI", "Tasha Brooks", "By Aug 1"),
            ("Stand up weekly facing and OSA monitoring in Birmingham and Memphis",
             "Jordan Hsu / Marcus Boudreaux", "By Aug 15"),
            ("Re-read share, facings and OSA at week 12 and decide whether leg 3 scales",
             "Jordan Hsu", "Late October")])

    k.close("We lost the shelf, then we lost the shopper.",
            ["340 bps, and 55% of it was a facing decision we did not contest.",
             "Three legs: shelf, availability, demand — in that order.",
             "Birmingham and Memphis are showing the same pattern now."])
    return k.build()


# ==================================================== 59 · Walmart JBP =========
def r59_walmart_jbp():
    k = Deck("59-walmart-fy27-joint-business-plan-line-review.pptx",
             kicker="JOINT BUSINESS PLAN · FY2027",
             title="Walmart FY2027 Joint Business Plan",
             subtitle="Category growth, the modular ask, and the protein gap we need to close "
                      "together",
             byline="Marcus Boudreaux, Director Sales South, with the Walmart team · August 2026",
             short="Walmart FY27 JBP")

    ret = q.retailers()
    wmt = ret[ret.retailer == "Walmart"].iloc[0]
    pva = q.pva_retailer(q.Q1)
    wmt_pva = pva[pva.Retailer == "Walmart"].iloc[0]
    wp_w = q.cat_row("Q2-FY2026-MTD", "Wellness Protein", "Walmart Total US")
    wp_t = q.cat_row("Q2-FY2026-MTD", "Wellness Protein", "Target Total US")
    end = q.endcap_la()
    tb = q.trade_events("retailer")
    wtrade = tb[tb.retailer == "Walmart"].iloc[0]
    bts = q.bts()

    k.agenda(["The partnership today", "Where we are against plan", "The protein gap",
              "The Louisiana modular issue", "Trade productivity",
              "Our FY27 proposal", "Innovation calendar", "The joint scorecard", "The asks"])

    k.exec_summary(
        f"Walmart is ${wmt.rev:.0f}M of Acme revenue at {wmt.acv:.1f}% ACV weight — our largest "
        f"customer by a factor of two. Q1 ran {wmt_pva['var']:+.1f}% to plan, in line with the "
        "portfolio. Two things need fixing jointly in FY27: our Wellness Protein position at Walmart "
        f"({wp_w.acme_share:.1f}% share against {wp_t.acme_share:.1f}% at Target on the same items), "
        "and the Louisiana modular that cut Crunchwell Mega facings.",
        tiles=[(f"${wmt.rev:.0f}M", "Acme revenue at Walmart"),
               (f"{wmt.acv:.1f}%", "ACV weight"),
               (f"{wp_w.acme_share:.1f}%", "Acme Wellness Protein share at Walmart"),
               (f"{wp_t.acme_share:.1f}%", "the same number at Target")],
        bullets=[
            f"**The protein gap is the growth story.** Same products, same price, "
            f"{wp_t.acme_share:.1f}% share at Target versus {wp_w.acme_share:.1f}% here. Closing half "
            "of it is worth roughly $9M of retail sales.",
            "**The Louisiana modular cost both of us.** Crunchwell Mega went from 8 facings to 6 in "
            "the September 2025 reset; category dollars in the DMA are down 2.8%.",
            f"**Trade productivity:** {int(wtrade.events)} Q1 events, ${wtrade.spend/1000:.1f}M of "
            f"spend at an index of {wtrade.idx:.2f}. We are proposing fewer, deeper, better-timed "
            "events for FY27.",
            f"**Back-to-school works here:** ${float(bts[bts.retailer=='Walmart'].inc_m.iloc[0]):.1f}M "
            "of incremental category dollars in the 2025 window at "
            f"{float(bts[bts.retailer=='Walmart'].kids_share.iloc[0]):.1f}% "
            "kids-household cereal share — the highest of any retailer.",
        ], headline="Two fixes and one growth story")

    chp = chart_bar("r59_protein.png", ["Walmart", "Target", "US national"],
                    [float(wp_w.acme_share), float(wp_t.acme_share),
                     float(q.cat_row("Q2-FY2026-MTD", "Wellness Protein").acme_share)],
                    title="Acme share of Wellness Protein, Q2 FY26 MTD (%)", pct=True,
                    colors_list=["#B24A2E", "#2E7D75", "#5B6472"], h=2.9)
    k.chart_bullets("THE GAP", "The same items perform three times better one retailer over", chp,
                    [f"**{wp_w.acme_share:.1f}% at Walmart against {wp_t.acme_share:.1f}% at "
                     "Target.** Identical assortment, identical shelf price.",
                     f"**Walmart's Wellness Protein segment grew {wp_w.growth:+.1f}%** — the demand "
                     "is here; the assortment and the merchandising are not.",
                     "**ProteinPeak velocity is 9.2 units/store/week here versus 17.5 at Target** "
                     "with an endcap and Roundel support.",
                     "**The ask is assortment plus one merchandising event**, not price."],
                    note="Source: seed_category_market_size retailer cuts, "
                         "seed_proteinpeak_q2_launch velocities.")

    end8 = q.roll_up(end, "city", 8, sum_cols=("stores",),
                     mean_cols=("lf_endcaps", "acme_endcaps", "pl_endcaps", "cw_mega_facings",
                                "fh_facings", "oos_pct"), other="All other LA cities")
    erows = [[r.city, f"{int(r.stores)}", f"{r.cw_mega_facings:.2f}", f"{r.fh_facings:.2f}",
              f"{r.lf_endcaps:.2f}", f"{r.oos_pct:.0f}%"] for r in end8.itertuples()]
    k.table("THE MODULAR", "What the September reset did in Louisiana",
            ["City", "Stores audited", "Crunchwell Mega facings", "Field & Honey facings",
             "Larksfield endcaps", "Mega OOS"], erows,
            widths=[0.20, 0.15, 0.20, 0.18, 0.16, 0.11], size=9.0,
            callout=("The joint case",
                     "Louisiana RTE category dollars are down 2.8% and Crunchwell share is down "
                     "340 bps. Restoring Mega to 8 facings and one endcap per supercenter rebuilds "
                     "category dollars, not just our share — which is why we are bringing it as a "
                     "joint ask rather than a supplier complaint.", "action"),
            note="Source: seed_walmart_endcap_audit_la, seed_category_market_size (Louisiana DMA).")

    cht = chart_grouped("r59_trade.png", ["Q1 FY26"],
                        {"Spend ($K)": [float(wtrade.spend)],
                         "Modelled incremental ($K)": [float(wtrade.inc)]},
                        title="Walmart trade spend and modelled incremental revenue, Q1 ($K)", h=2.7)
    k.chart_table("TRADE", "Fewer, better events in FY27", cht,
                  ["Measure", "Q1 FY26", "FY27 proposal"],
                  [["Events", f"{int(wtrade.events)}", "−15%"],
                   ["Spend", money(wtrade.spend / 1000, dp=1), "Flat"],
                   ["Average depth", "29.5% (FY25 Crunchwell)", "≤20% on Mega"],
                   ["Incrementality index", f"{wtrade.idx:.2f}", "≥0.60"],
                   ["Feature-and-display weight", "Baseline", "+30%"]],
                  widths=[0.42, 0.29, 0.29], size=9.5,
                  note="Source: seed_trade_promo_events_q1_2026, seed_trade_spend_fy25. "
                       "FY27 column is the proposal.")

    k.two_col("FY27 PROPOSAL", "What we bring and what we ask",
              "What Acme brings",
              ["ProteinPeak full-line support: endcap creative, sampling and Walmart Connect weight "
               "at the ratio-1.20 platform.",
               "Crunchwell Pack Refresh (Aug 15 2026) with modular-ready planograms and pre-built "
               "inventory.",
               "Chocolate Almond as a Q1 FY27 exclusive-window opportunity.",
               "Trade calendar rebuilt to a 0.60 incrementality floor — fewer, better events.",
               "Back-to-school programme scaled to the 41.6% kids-household share this account owns."],
              "What we ask Walmart for",
              ["Crunchwell Mega restored to 8 facings in the Louisiana DMA modular.",
               "One endcap per Louisiana supercenter in two windows.",
               "Full ProteinPeak line authorisation, including Cinnamon Crunch and Cocoa Almond.",
               "Joint OSA programme for the 14 lowest-performing Louisiana doors.",
               "Early visibility of the FY27 modular calendar so we can pre-build."],
              note="Source: seed_walmart_endcap_audit_la, seed_innovation_pipeline, "
                   "seed_numerator_bts_occasion_2025, seed_retail_media_spend_q1_2026.")

    k.table("SCORECARD", "The joint measures we will review quarterly",
            ["Measure", "Today", "FY27 target", "Owner"],
            [["Acme revenue at Walmart", f"${wmt.rev:.0f}M", "$196M", "Marcus Boudreaux"],
             ["Acme Wellness Protein share", f"{wp_w.acme_share:.1f}%", "≥9%", "Sage Park"],
             ["Crunchwell Mega facings, LA DMA",
              f"{float(end.cw_mega_facings.mean()):.1f}", "8.0", "Walmart merchandising"],
             ["Louisiana Crunchwell share", "3.0%", "≥4.5%", "Joint"],
             ["Trade incrementality index", f"{wtrade.idx:.2f}", "≥0.60", "Trade Finance"],
             ["OSA, 14 focus doors", f"{float(q.rouses_oos().osa.mean()):.0f}% (proxy)", "≥90%",
              "Joint"]],
            widths=[0.34, 0.18, 0.18, 0.30], align_right_from=1, size=9.5,
            note="Source: seed_retailers, seed_category_market_size, seed_walmart_endcap_audit_la, "
                 "seed_trade_promo_events_q1_2026. Targets are the FY27 proposal.")

    k.reco("THE ASKS", "Five decisions for the August line review",
           [("Restore Crunchwell Mega to 8 facings in the Louisiana modular",
             "Walmart merchandising", "Aug line review"),
            ("Authorise the full ProteinPeak line including PP005 and PP006", "Walmart buying",
             "Aug line review"),
            ("Agree one endcap per Louisiana supercenter across two windows", "Joint", "Q3–Q4 FY26"),
            ("Approve the FY27 trade calendar at a 0.60 incrementality floor", "Joint", "Sep 2026"),
            ("Stand up the joint OSA programme in the 14 focus doors", "Joint", "From Aug 15")])

    k.close("Same products, three times the share one retailer over.",
            [f"{wp_t.acme_share:.1f}% at Target versus {wp_w.acme_share:.1f}% here.",
             "Eight facings on Mega rebuilds category dollars in Louisiana, not just our share.",
             "Fewer, better trade events on both sides of the table."])
    return k.build()


# ================================================ 60 · Target BTS + JBP ========
def r60_target_bts_jbp():
    k = Deck("60-target-fy27-jbp-back-to-school-program.pptx",
             kicker="SHOPPER PROGRAMME & JBP · FY2027",
             title="Target Back-to-School 2026 and the FY27 Plan",
             subtitle="Three brands, one window, and the retailer where our growth engine "
                      "over-indexes",
             byline="Wes Okafor, Senior Manager — Shopper Marketing, with Soo-jin Lee (Target NAM) · "
                    "July 2026",
             short="Target BTS + FY27")

    ret = q.retailers()
    tgt = ret[ret.retailer == "Target"].iloc[0]
    wp_t = q.cat_row("Q2-FY2026-MTD", "Wellness Protein", "Target Total US")
    bts = q.bts()
    tbts = bts[bts.retailer == "Target"].iloc[0]
    pva = q.pva_retailer(q.Q1)
    tp = pva[pva.Retailer == "Target"].iloc[0]
    ppl = q.pp_launch()

    k.agenda(["Why Target matters more than its size", "The back-to-school window",
              "Three brands on one programme", "The protein over-index",
              "Media and Roundel plan", "Measurement", "FY27 JBP frame", "The asks"])

    k.exec_summary(
        f"Target is ${tgt.rev:.0f}M of Acme revenue — third largest — but it is where our growth "
        f"engine works best: Acme holds {wp_t.acme_share:.1f}% of Wellness Protein here against "
        "5.2% at Walmart. The back-to-school window (July 13 to August 23) is the largest shopper "
        f"occasion of the year in this account, worth ${tbts.inc_m:.1f}M of incremental category "
        "dollars in 2025 with a protein-curious cohort overlap of "
        f"{tbts.protein_overlap:.1f}% — the highest of any retailer.",
        tiles=[(f"{wp_t.acme_share:.1f}%", "Acme Wellness Protein share at Target"),
               (f"${tbts.inc_m:.1f}M", "BTS incremental category $, 2025"),
               (f"{tbts.protein_overlap:.1f}%", "protein-curious cohort overlap"),
               (f"{tp['var']:+.1f}%", "Q1 revenue vs plan at Target")],
        bullets=[
            "**Target is the proof case for ProteinPeak.** Trial ran 110–113% of plan and velocity "
            "hit 17.5 units/store/week on the April endcap — nearly double the Walmart pilot.",
            f"**The BTS window is protein-shaped here.** {tbts.protein_overlap:.1f}% overlap with the "
            f"protein-curious cohort against {float(bts[bts.retailer=='Walmart'].protein_overlap.iloc[0]):.1f}% "
            "at Walmart, where the window is kids-shaped.",
            "**Three brands, one programme:** ProteinPeak (protein-curious), TrailGrove (lunchbox "
            "occasion) and MorningOats single-serve cups (dorm and commuter).",
            "**Asset deadline drives everything** — circular, Roundel and in-store creative lock "
            "roughly three weeks before the window opens.",
        ], headline="The account where our growth engine already works")

    chb = chart_grouped("r60_bts.png", list(bts.retailer),
                        {"Kids-HH cereal share (%)": [float(x) for x in bts.kids_share],
                         "Protein-curious overlap (%)": [float(x) for x in bts.protein_overlap]},
                        title="Back-to-school occasion shape by retailer, 2025 (%)", pct=True, h=3.1)
    brows = [[r.retailer, f"{r.kids_share:.1f}%", f"{r.protein_overlap:.1f}%", money(r.inc_m)]
             for r in bts.itertuples()]
    k.chart_table("THE WINDOW", "Same season, different shopper, different programme", chb,
                  ["Retailer", "Kids-HH share", "Protein overlap", "Incremental $"], brows,
                  widths=[0.28, 0.24, 0.24, 0.24], size=9.5,
                  note="Source: seed_numerator_bts_occasion_2025.")

    k.table("THE PROGRAMME", "Three brands, three occasions, one window",
            ["Brand", "Occasion", "Mechanic", "Roundel weight", "Success measure"],
            [["ProteinPeak", "Protein-curious adult breakfast",
              "Endcap + sampling, no price discount", "45%", "Trial index ≥110; repeat ≥1.1x"],
             ["TrailGrove", "Lunchbox and after-school",
              "Feature + multi-buy at capped depth", "30%", "Units/store/week +15% vs LY"],
             ["MorningOats cups", "Dorm, commuter, single-serve",
              "Circular feature + Target Circle offer", "25%", "Segment share +50 bps"]],
            widths=[0.15, 0.24, 0.26, 0.13, 0.22], align_right_from=9, size=9.5,
            callout=("What we are not doing",
                     "No deep price discounting on ProteinPeak. The launch data says this shopper "
                     "responds to display and sampling, not to depth — and a discount here trains a "
                     "premium buyer to wait for promotions.", "info"),
            note="Source: seed_numerator_bts_occasion_2025, seed_proteinpeak_q2_launch, "
                 "seed_trade_spend_fy25.")

    prows = [[r.sku_name[:32], r.retailer, r.event_type[:20], str(r.start_date), str(r.end_date)]
             for r in ppl[ppl.retailer == "Target"].itertuples()]
    k.table("THE PRECEDENT", "What the April launch window looked like at Target",
            ["SKU", "Retailer", "Event type", "Start", "End"], prows,
            widths=[0.32, 0.16, 0.22, 0.15, 0.15], size=9.5,
            note="Source: seed_proteinpeak_q2_launch.")

    chv = chart_bar("r60_velocity.png", ["Target (endcap + Roundel)", "Walmart (pilot)"],
                    [17.5, 9.2], title="ProteinPeak velocity, units/store/week", color="teal", h=2.7)
    k.chart_bullets("WHY IT WORKS HERE", "Display plus retail media, not price", chv,
                    ["**17.5 units/store/week at Target** against 9.2 at the Walmart pilot on the "
                     "same items at the same price.",
                     "**The difference is the endcap and Roundel support**, not assortment depth.",
                     f"**Target Circle membership overlap is high** in the BTS cohort, which makes "
                     "Roundel audience targeting unusually efficient in this window.",
                     "**Read-across:** the BTS programme should replicate the April structure — "
                     "display plus targeted media plus sampling."],
                    note="Source: seed_proteinpeak_q2_launch, seed_numerator_bts_occasion_2025.")

    k.two_col("FY27 FRAME", "Beyond the window",
              "What Acme commits for FY27",
              [f"Grow Acme revenue at Target from ${tgt.rev:.0f}M toward $76M.",
               "Chocolate Almond into the Q1 FY27 assortment following the Q4 line review.",
               "Roundel investment weighted to the protein-curious and BTS audiences.",
               "Crunchwell Pack Refresh planograms ready for the FY27 reset.",
               "No incremental depth on ProteinPeak; growth from display and distribution."],
              "What we ask Target for",
              ["BTS endcap for ProteinPeak in the July 13 to August 23 window.",
               "Circular feature for TrailGrove and MorningOats cups in weeks 30 and 33.",
               "Chocolate Almond authorisation at the Q4 FY26 line review.",
               "Shelf-space parity for the ProteinPeak line at the FY27 reset.",
               "Joint post-window read on trial, repeat and incremental category dollars."],
              note="Source: seed_retailers, seed_innovation_pipeline, seed_concept_test_chocolate_almond.")

    k.reco("THE ASKS", "What has to be agreed and by when",
           [("Confirm the BTS endcap and circular positions", "Soo-jin Lee / Target buying",
             "By Jun 12 (asset lock)"),
            ("Lock creative and Roundel audiences for all three brands", "Wes Okafor / Hugo Lin",
             "By Jul 1"),
            ("Authorise Chocolate Almond at the Q4 FY26 line review", "Target buying", "Q4 FY26"),
            ("Agree the joint post-window measurement plan", "Wes Okafor", "By Jul 1"),
            ("Read trial, repeat and incremental dollars at window close", "Wes Okafor / Maya Chen",
             "Sep 2026")])

    k.close("The window is protein-shaped here. Build for that.",
            [f"{tbts.protein_overlap:.1f}% protein-curious overlap — the highest of any retailer.",
             "Display, sampling and Roundel — no depth on a premium item.",
             f"${tbts.inc_m:.1f}M of incremental category dollars is the prize."])
    return k.build()


if __name__ == "__main__":
    for fn in [r52_sop_ibp_review, r53_supply_chain_service, r54_trade_effectiveness,
               r55_media_effectiveness, r56_brand_equity_tracker, r57_category_sob,
               r58_louisiana_diagnostic, r59_walmart_jbp, r60_target_bts_jbp]:
        print("built", os.path.basename(fn()))
