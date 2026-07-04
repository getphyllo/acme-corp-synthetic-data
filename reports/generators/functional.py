"""Functional / cross-functional reports (25-29). Run: python generators/functional.py

  25  Q2 FY26 S&OP / IBP Executive Review
  26  Q2 FY26 Supply Chain & Customer Service Review
  27  H1 FY26 Trade Promotion Effectiveness & Post-Event Analysis
  28  H1 FY26 Marketing Mix & Media Effectiveness Review
  29  Q2 FY26 Brand Equity & Consumer Health Tracker Readout

Every headline number traces to acme.duckdb, seeds/*.csv, or FACTS.md.
Forward numbers are labelled plan/target/planning estimate in-document.
Note: shipments.Fill_Rate_Pct is a FRACTION (0.95 = 95%) -> *100 for display.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import (Doc, df, seed_csv, money, palette,
                 chart_line, chart_bar, chart_grouped, chart_stacked,
                 chart_waterfall, chart_donut)


# --------------------------------------------------------------- helpers ----
def _company_month(period):
    r = df(f"""SELECT SUM(Plan_Revenue_USD)/1e6 p, SUM(Actual_Revenue_USD)/1e6 a
               FROM plan_vs_actual WHERE Period='{period}'""").iloc[0]
    return float(r.p), float(r.a)


def _brand_var(brand, periods):
    ps = ",".join(f"'{p}'" for p in periods)
    r = df(f"""SELECT (SUM(Actual_Revenue_USD)-SUM(Plan_Revenue_USD))/SUM(Plan_Revenue_USD)*100 v
               FROM plan_vs_actual WHERE Brand='{brand}' AND Period IN ({ps})""").iloc[0]
    return float(r.v)


# ============================================================== REPORT 25 ===
def r25_sop_ibp_executive_review():
    d = Doc("25-q2-2026-sop-ibp-executive-review.pdf",
            kicker="S&OP / IBP EXECUTIVE REVIEW",
            title="Q2 FY2026 S&OP / Integrated Business Planning Executive Review",
            subtitle="Reconciling the demand, supply, inventory and financial plans into one consensus number",
            owner="S&OP Lead; cross-functional (Demand, Supply, Finance)",
            period="Q2 FY2026 cycle (actuals through May)", short="Q2 S&OP/IBP",
            doc_type="Integrated Business Planning executive review",
            date_str="June 2026")

    p_may, a_may = _company_month("2026-05")
    var_may = (a_may - p_may) / p_may * 100
    jm = df("""SELECT SUM(Plan_Revenue_USD)/1e6 p, SUM(Actual_Revenue_USD)/1e6 a
               FROM plan_vs_actual WHERE Period BETWEEN '2026-01' AND '2026-05'""").iloc[0]
    gap_jm = float(jm.a) - float(jm.p)

    d.cover_facts([
        ("Consensus demand vs plan (May)", f"{var_may:+.1f}% · improving from −5.2% in Q1"),
        ("Cumulative gap-to-budget (Jan–May)", f"{money(gap_jm)} ({(gap_jm/float(jm.p))*100:+.1f}%)"),
        ("Fill rate (supply)", "94.7% May — fully storm-recovered"),
        ("Two drivers of the gap", "Crunchwell Louisiana (down) · ProteinPeak (recovering up)"),
        ("Consensus call", "Hold FY26 on the ProteinPeak launch; fund the LA recovery"),
    ])

    d.exec_summary(
        f"This cycle reconciles the demand, supply, inventory and financial plans into a single "
        f"consensus. The company ran {var_may:.1f}% behind plan in May, an improvement from −5.2% "
        f"through Q1 — the trajectory is closing, not widening. Supply has fully recovered from the "
        f"Hurricane Tonya disruption (fill back to ~95% after a ~52% storm trough), so the residual "
        f"gap is a demand-and-mix story concentrated in two known places: Crunchwell's Louisiana "
        f"erosion on the downside, and a ProteinPeak launch recovering on the upside. The consensus "
        f"recommendation is to hold the FY26 number on the strength of the launch read.",
        bullets=[
            f"<b>Consensus demand</b> is {var_may:+.1f}% to plan in May, up from −5.2% in Q1. The "
            "cumulative Jan–May gap-to-budget is " + money(gap_jm) + ".",
            "<b>ProteinPeak</b> is the swing factor on the upside: Apr–May actuals recovered to "
            "−6% to plan from −25% pre-launch, as PP005/PP006 shipped from April 20.",
            "<b>Crunchwell Louisiana</b> is the structural downside — a −340 bps local share loss "
            "with a funded three-leg recovery (see the Supply Chain read, Report 26, for the LA / "
            "Houston-DC service dimension).",
            "<b>Supply is no longer a constraint:</b> fill rate is back at ~95% and launch supply "
            "for ProteinPeak held at ~94% through the April ramp.",
        ])

    # ---- 1 · Consensus scorecard
    d.h1("1 · Consensus scorecard")
    d.kpis([
        ("Demand vs plan (May)", f"{var_may:+.1f}%", "was −5.2% in Q1"),
        ("Gap-to-budget (Jan–May)", money(gap_jm), "cumulative"),
        ("Fill rate", "94.7%", "storm-recovered"),
        ("ProteinPeak vs plan", "−6.1%", "was −25% pre-launch"),
    ])
    d.body(
        "The scorecard reads amber and improving. Demand is behind plan but the miss is narrowing "
        "each month; supply and inventory are green; and the financial gap is fully attributable to "
        "the two managed drivers below. The purpose of this cycle is to confirm the consensus number "
        "and lock the decisions that keep the FY26 commitment intact.")

    # demand actual vs plan by month
    md = df("""SELECT Period,
                 ROUND(SUM(Plan_Revenue_USD)/1e6,1) plan,
                 ROUND(SUM(Actual_Revenue_USD)/1e6,1) act
               FROM plan_vs_actual WHERE Period BETWEEN '2025-10' AND '2026-05'
               GROUP BY 1 ORDER BY 1""")
    ch1 = chart_line("r25_demand_vs_plan.png", list(md.Period),
                     {"Plan": [float(x) for x in md.plan],
                      "Actual (consensus)": [float(x) for x in md.act]},
                     title="Company net revenue — consensus actual vs plan ($M/mo)", h=2.9)
    d.image(ch1, "Actual closes toward plan through Q2 as the ProteinPeak launch pipe fills. "
                 "Plan holds at $63.7M/mo; May actual $61.6M.")
    d.source("plan_vs_actual (SAP/Acme ERP shape), monthly FY26.")

    # ---- 2 · Demand plan
    d.pagebreak()
    d.h1("2 · Demand plan — consensus vs plan")
    d.body(
        "Consensus demand improved from −5.2% in Q1 to −3.4% in May. Four of six brands sit within "
        "2 points of plan; the movement in the number is dominated by ProteinPeak (recovering) and "
        "Crunchwell (structurally soft). The demand plan below is the reconciled consensus after the "
        "demand-review and management-review steps of this cycle.")

    bd = df("""SELECT Brand,
                 ROUND((SUM(CASE WHEN Period IN ('2026-01','2026-02','2026-03')
                     THEN Actual_Revenue_USD-Plan_Revenue_USD END))
                   /NULLIF(SUM(CASE WHEN Period IN ('2026-01','2026-02','2026-03')
                     THEN Plan_Revenue_USD END),0)*100,1) q1v,
                 ROUND((SUM(CASE WHEN Period IN ('2026-04','2026-05')
                     THEN Actual_Revenue_USD-Plan_Revenue_USD END))
                   /NULLIF(SUM(CASE WHEN Period IN ('2026-04','2026-05')
                     THEN Plan_Revenue_USD END),0)*100,1) q2v
               FROM plan_vs_actual GROUP BY 1 ORDER BY q2v ASC""")
    rows = []
    for r in bd.itertuples():
        trend = "Improving" if r.q2v > r.q1v + 1 else ("Stable" if abs(r.q2v - r.q1v) <= 1 else "Softening")
        status = "On track" if r.q2v > -3 else ("Watch" if r.q2v > -10 else "Action")
        rows.append([r.Brand, f"{r.q1v:+.1f}%", f"{r.q2v:+.1f}%", trend, status])
    d.h2("2.1 · Brand demand vs plan — Q1 vs Q2 (Apr–May)")
    d.table(["Brand", "Q1 var", "Q2 var (Apr–May)", "Trend", "Consensus status"], rows,
            widths=[0.26, 0.17, 0.22, 0.17, 0.18])
    d.source("plan_vs_actual, FY26 periods (Q2 = Apr–May actuals).")
    d.callout("ProteinPeak is the consensus upside",
              "ProteinPeak ran −25% to plan in Q1 by design — the FY26 build was loaded onto the "
              "Cinnamon Crunch and Cocoa Almond SKUs that did not ship until April 20. Apr–May "
              "actuals recovered to −6.1%. If the launch holds through the Week-8 read, the demand "
              "consensus improves further into Q3.", "win")

    # ---- 3 · Supply plan
    d.h1("3 · Supply plan — fully recovered")
    d.body(
        "Supply is no longer the constraint on the number. Company fill rate is back at ~95% and "
        "on-time performance has normalised after the Hurricane Tonya disruption (Nov–Dec 2025), "
        "which cut fill on the affected Gulf-coast lanes to a ~52% storm trough. The recovery path "
        "below closes out the supply side of the reconciliation; the detailed service view — DC and "
        "plant performance, cut-reason analysis — is in the Supply Chain & Service review (Report 26).")
    fm = df("""SELECT strftime(CAST(Week_Start AS DATE),'%Y-%m') mo,
                 ROUND(AVG(Fill_Rate_Pct)*100,1) fill
               FROM shipments
               WHERE Week_Start BETWEEN '2025-10-01' AND '2026-05-31'
               GROUP BY 1 ORDER BY 1""")
    ch2 = chart_line("r25_fill_recovery.png", list(fm.mo),
                     {"Company fill rate": [float(x) for x in fm.fill]},
                     title="Fill-rate recovery, all-network monthly (%)", pct=True, h=2.7)
    d.image(ch2, "All-network fill dips in Nov–Dec 2025 (Hurricane Tonya, ~52% on affected lanes) "
                 "and is fully recovered to ~95% by Q1 FY26.")
    d.source("shipments (Fill_Rate_Pct, fraction × 100); storm trough per FACTS (51.6% Storm cut).")

    # ---- 4 · Financial reconciliation & gap-to-budget
    d.h1("4 · Financial reconciliation — consensus-to-budget gap")
    d.body(
        "Reconciling the consensus demand plan to the financial budget leaves the gap-to-budget "
        "below. It is not broad-based: Crunchwell and ProteinPeak together account for essentially "
        "all of the Q1 gap, and ProteinPeak's portion is closing as the launch ramps. The remaining "
        "structural exposure is Crunchwell — the flagship's plan gap is steady at roughly −6% and is "
        "the single biggest call in this cycle.")
    gb = df("""SELECT Brand, ROUND((SUM(Actual_Revenue_USD)-SUM(Plan_Revenue_USD))/1e6,2) gap
               FROM plan_vs_actual WHERE Period IN ('2026-01','2026-02','2026-03')
               GROUP BY 1 ORDER BY gap ASC""")
    ch3 = chart_bar("r25_gap_to_budget.png", list(gb.Brand), [float(x) for x in gb.gap],
                    title="Q1 FY26 consensus-to-budget gap by brand ($M)",
                    colors_list=[palette["rust"] if v < -1 else palette["gold"] for v in gb.gap],
                    horizontal=True, unit="M", h=2.7)
    d.image(ch3, "Crunchwell (−$4.5M) and ProteinPeak (−$4.4M) are the whole Q1 gap. "
                 "ProteinPeak's portion is closing post-launch; Crunchwell's is structural.")
    d.source("plan_vs_actual, Q1 FY26 (Jan–Mar).")

    # ---- 5 · Decisions & risks
    d.h1("5 · Consensus decisions & risks")
    d.callout("Watch-items into Q3 (Jul–Sep, forward/plan)",
              "(1) ProteinPeak launch durability — the demand upside depends on repeat holding at "
              "the Week-8 read. (2) Crunchwell Louisiana recovery execution against Field & Honey's "
              "14g-protein escalation. (3) Crunchwell Pack Refresh (launch prep, Aug 15) is the "
              "biggest near-term demand bet and must land on time to support the H2 plan.", "risk")
    d.recommendations([
        ("Adopt the consensus demand plan: hold the FY26 number on the ProteinPeak launch recovery, "
         "contingent on the Week-8 repeat read.",
         "S&OP Lead / Finance", "This cycle"),
        ("Fund the Crunchwell Louisiana three-leg recovery (facings, targeted trade, LA retail media) "
         "as the priority demand action.",
         "Marcus Boudreaux / Demand", "Q2 — now"),
        ("Confirm supply is de-risked: maintain ~95% fill and protect Crunchwell Pack Refresh launch "
         "supply for the Aug 15 date (planning target).",
         "VP Supply Chain", "Q2–Q3"),
        ("Re-run the consensus at the July MBR with the Week-8 launch read to reaffirm or revise the "
         "hold-the-number call.",
         "S&OP Lead", "July MBR"),
    ])
    return d.build()


# ============================================================== REPORT 26 ===
def r26_supply_chain_service_review():
    d = Doc("26-q2-2026-supply-chain-customer-service-review.pdf",
            kicker="SUPPLY CHAIN & SERVICE REVIEW",
            title="Q2 FY2026 Supply Chain & Customer Service Review",
            subtitle="Fill rate, OTIF, cut-reason analysis, and recovery from Hurricane Tonya",
            owner="VP Supply Chain; Customer Logistics",
            period="Q2 FY2026 (H1 view, actuals through May)", short="Supply Chain Q2",
            doc_type="Supply chain & customer service performance review",
            date_str="June 2026")

    # live current-state metrics (Q1-Q2 FY26)
    cur = df("""SELECT ROUND(AVG(Fill_Rate_Pct)*100,1) fill, ROUND(AVG(On_Time_Pct)*100,1) otif
                FROM shipments WHERE Week_Start >= '2026-01-01'""").iloc[0]
    trough = df("""SELECT ROUND(AVG(Fill_Rate_Pct)*100,1) f
                   FROM shipments WHERE Cut_Reason='Storm'
                   AND Week_Start BETWEEN '2025-11-10' AND '2025-12-08'""").iloc[0].f

    d.cover_facts([
        ("Fill rate (Q1–Q2 FY26)", f"{cur.fill:.1f}% — normalised"),
        ("On-time (OTIF proxy)", f"{cur.otif:.1f}%"),
        ("Hurricane Tonya trough (Nov 2025)", "51.6% fill on affected Gulf lanes"),
        ("Cut reasons", "Storm 51.6% · Production_Lag 83% · Quality_Hold 83% · None 95%"),
        ("Recovery", "Full — back to ~95% fill by Jan 2026"),
    ])

    d.exec_summary(
        f"Network service has fully recovered. Fill rate is running {cur.fill:.1f}% and on-time "
        f"{cur.otif:.1f}% across Q1–Q2 FY26 — at or above the ~95% fill / ~90% OTIF baseline. The "
        f"defining event of the period was Hurricane Tonya (Nov 2025), which cut fill on the "
        f"Houston, Thibodaux and Tyler DC lanes to a ~52% storm trough before a full recovery by "
        f"January. Away from the storm, non-storm cuts remain small and well-understood. Supply "
        f"readiness for the ProteinPeak launch held through the April ramp.",
        bullets=[
            f"<b>Current state is green:</b> fill {cur.fill:.1f}%, on-time {cur.otif:.1f}% "
            "(Q1–Q2 FY26) — the disruption is closed.",
            "<b>Hurricane Tonya (Nov 2025)</b> was the sole service failure — Storm-flagged lines "
            "ran ~51.6% fill on the Houston / Thibodaux / Tyler DCs, dragging the November all-"
            "network number to ~90%.",
            "<b>Cut-reason mix</b> is healthy: Storm 51.6%, Production_Lag ~83%, Quality_Hold ~83%, "
            "and the 98% of lines with no cut fill at ~95%.",
            "<b>The storm compounded the Crunchwell Louisiana problem</b> — the Houston DC supply "
            "collapse is one leg of the −340 bps LA share loss (cross-ref Report 39, LA / Houston DC).",
        ])

    # ---- 1 · Service scorecard
    d.h1("1 · Service scorecard")
    d.kpis([
        ("Fill rate", f"{cur.fill:.1f}%", "Q1–Q2 FY26"),
        ("On-time (OTIF)", f"{cur.otif:.1f}%", "vs ~90% baseline"),
        ("Storm trough", "51.6%", "affected lanes Nov"),
        ("Non-storm cuts", "<2% of lines", "well-controlled"),
    ])
    d.body(
        "The service picture is a single sharp event bracketed by a stable baseline. Outside "
        "Nov–Dec 2025, fill has held at the ~95% target in every month of the two-year history. "
        "The job now is to hold that baseline and carry the storm learnings into hurricane-season "
        "contingency for the Gulf DCs.")

    # ---- 2 · The storm and recovery
    d.h1("2 · Hurricane Tonya — collapse and recovery")
    d.body(
        "Hurricane Tonya made landfall on the Gulf coast in November 2025 and took the Houston, "
        "Thibodaux and Tyler distribution lanes offline for roughly four weeks. Storm-flagged "
        "shipment lines ran at a ~51.6% fill rate through the trough, pulling the all-network "
        "monthly fill down to ~90% in November and December before a full recovery to ~95% by "
        "January 2026. The chart tracks the all-network monthly fill and on-time series across the "
        "disruption window.")
    sm = df("""SELECT strftime(CAST(Week_Start AS DATE),'%Y-%m') mo,
                 ROUND(AVG(Fill_Rate_Pct)*100,1) fill,
                 ROUND(AVG(On_Time_Pct)*100,1) otif
               FROM shipments WHERE Week_Start BETWEEN '2025-08-01' AND '2026-05-31'
               GROUP BY 1 ORDER BY 1""")
    ch1 = chart_line("r26_fill_otif.png", list(sm.mo),
                     {"Fill rate": [float(x) for x in sm.fill],
                      "On-time (OTIF)": [float(x) for x in sm.otif]},
                     title="All-network fill rate & OTIF — storm dip and recovery (%)",
                     pct=True, h=3.0)
    d.image(ch1, "Nov–Dec 2025 storm dip is visible in both fill and OTIF; both recover to baseline "
                 "by Jan 2026. Storm-lane fill bottomed near 52%.")
    d.source("shipments (Fill_Rate_Pct, On_Time_Pct × 100), 2025-08 → 2026-05.")

    # ---- 3 · Cut-reason analysis
    d.pagebreak()
    d.h1("3 · Cut-reason analysis")
    d.body(
        "Decomposing the cut reasons separates the one systemic failure (Storm) from the small, "
        "controllable losses. The 98% of shipment lines with no cut flag fill at ~95% — the healthy "
        "baseline. Storm lines are the outlier at ~52%; Production_Lag and Quality_Hold both sit "
        "around 83% and are order-of-magnitude smaller in volume.")
    cr = df("""SELECT Cut_Reason,
                 COUNT(*) n,
                 ROUND(AVG(Fill_Rate_Pct)*100,1) fill
               FROM shipments GROUP BY 1 ORDER BY n DESC""")
    # display headline fill from FACTS for the flagged reasons; use live counts
    label_map = {"None": ("None (baseline)", 95.0),
                 "Storm": ("Storm (Hurricane Tonya)", 51.6),
                 "Production_Lag": ("Production Lag", 83.0),
                 "Quality_Hold": ("Quality Hold", 83.0),
                 "Launch_Allocation": ("Launch Allocation", 83.4)}
    rows = []
    cat_labels, cat_fill = [], []
    total_n = int(cr.n.sum())
    for r in cr.itertuples():
        lab, fill = label_map.get(r.Cut_Reason, (r.Cut_Reason, float(r.fill)))
        rows.append([lab, f"{r.n:,}", f"{r.n/total_n*100:.1f}%", f"{fill:.1f}%"])
        if r.Cut_Reason != "Launch_Allocation":
            cat_labels.append(lab.split(" (")[0]); cat_fill.append(fill)
    d.h2("3.1 · Fill rate by cut reason")
    d.table(["Cut reason", "Lines", "Share of lines", "Fill rate"], rows,
            widths=[0.40, 0.20, 0.22, 0.18])
    d.source("shipments (line counts live; flagged-reason fill per FACTS).")
    ch2 = chart_bar("r26_cut_reason.png", cat_labels, cat_fill,
                    title="Fill rate by cut reason (%)", pct=True,
                    colors_list=[palette["teal"] if v >= 90 else palette["rust"] for v in cat_fill],
                    h=2.7)
    d.image(ch2, "The baseline (no cut) fills at ~95%. Storm is the systemic failure; "
                 "Production Lag and Quality Hold are small, controllable losses at ~83%.")

    # ---- 4 · DC & plant performance
    d.h1("4 · DC & plant performance")
    d.body(
        "The storm damage was geographically concentrated. Ranking the distribution lanes by their "
        "storm-window fill isolates the Gulf-coast DCs — Houston (Target, H-E-B, Walmart), "
        "Thibodaux (Rouses), Tyler (Brookshire's), plus Hammond and Memphis — as the failure set. "
        "Every other lane held its ~95% baseline through the same window.")
    dc = df("""SELECT Retailer_DC, ROUND(AVG(Fill_Rate_Pct)*100,1) fill, COUNT(*) n
               FROM shipments WHERE Cut_Reason='Storm'
               AND Week_Start BETWEEN '2025-11-10' AND '2025-12-08'
               GROUP BY 1 ORDER BY fill ASC LIMIT 7""")
    dc_rows = [[r.Retailer_DC, f"{r.fill:.1f}%", f"{r.n}"] for r in dc.itertuples()]
    d.h2("4.1 · Storm-affected DC lanes (Nov 2025 trough)")
    d.table(["Distribution centre lane", "Storm-window fill", "Lines"], dc_rows,
            widths=[0.56, 0.26, 0.18])
    d.source("shipments, Cut_Reason='Storm', 2025-11-10 → 2025-12-08.")
    d.callout("The storm is also a Louisiana-share story",
              "The Houston-DC supply collapse is one of the five root causes behind Crunchwell's "
              "−340 bps Louisiana share loss — a stock-out window that let Field & Honey and private "
              "label take facings on the ground. The service recovery is necessary but not "
              "sufficient for share recovery. See the Louisiana / Houston-DC diagnostic (Report 39).",
              "info")

    # ---- 5 · ProteinPeak launch supply readiness
    d.h1("5 · ProteinPeak launch supply readiness")
    ppr = df("""SELECT strftime(CAST(Week_Start AS DATE),'%Y-%m') mo,
                  ROUND(AVG(Fill_Rate_Pct)*100,1) fill,
                  ROUND(AVG(On_Time_Pct)*100,1) otif
                FROM shipments WHERE Brand='ProteinPeak' AND Week_Start >= '2026-01-01'
                GROUP BY 1 ORDER BY 1""")
    d.body(
        "The ProteinPeak launch (PP005 Cinnamon Crunch, PP006 Cocoa Almond) shipped from April 20 "
        "into the Q2 build. Launch supply held: brand fill stayed near ~94% through the April volume "
        "ramp — units shipped rose sharply without a service degradation — and on-time recovered to "
        "~96% by May. Supply was ready for the launch; the constraint on the ProteinPeak number was "
        "demand-side trial, not availability.")
    ppr_rows = [[r.mo, f"{r.fill:.1f}%", f"{r.otif:.1f}%"] for r in ppr.itertuples()]
    d.table(["Month", "ProteinPeak fill", "On-time"], ppr_rows,
            widths=[0.34, 0.33, 0.33])
    d.source("shipments, Brand='ProteinPeak', 2026-01 → 2026-05.")

    d.callout("Contingency for the next Gulf storm season",
              "Tonya exposed a single point of failure: the Gulf-coast DC cluster carries the LA and "
              "Texas service load with no fast alternate lane. Hurricane season runs Jun–Nov; the "
              "recovery is done, but the contingency plan (alternate sourcing, safety-stock buffer "
              "on the Gulf lanes) must be in place before the Q3 peak.", "risk")
    d.recommendations([
        ("Hold the ~95% fill / ~90% OTIF baseline; monitor weekly for any drift off target.",
         "Customer Logistics", "Ongoing"),
        ("Stand up a Gulf-coast storm contingency (alternate sourcing + safety stock) before the "
         "Q3 hurricane peak.",
         "VP Supply Chain", "Before Q3"),
        ("Reduce Production_Lag and Quality_Hold cuts — small but avoidable ~83% fill losses.",
         "Plant Operations", "Q3"),
        ("Protect Crunchwell Pack Refresh launch supply for the Aug 15 date (planning target); "
         "no repeat of a launch-window stock-out.",
         "Supply Planning", "Q3"),
    ])
    return d.build()


# ============================================================== REPORT 27 ===
def r27_trade_promo_pea():
    d = Doc("27-h1-2026-trade-promotion-effectiveness-pea.pdf",
            kicker="TRADE PROMOTION EFFECTIVENESS · PEA",
            title="H1 FY2026 Trade Promotion Effectiveness & Post-Event Analysis",
            subtitle="Reading incrementality, ROI and forward-buy leakage across the Q1 event book",
            owner="Revenue Growth Mgmt; Trade Finance",
            period="H1 FY2026 (Q1 event detail)", short="Trade PEA H1",
            doc_type="Trade promotion post-event analysis (PEA)",
            date_str="June 2026")

    tot = df("""SELECT COUNT(*) n, SUM(spend_kusd)/1000 spend, SUM(incremental_revenue_kusd)/1000 incr,
                  AVG(modeled_lift_pct) lift, AVG(modeled_incrementality_index) idx
                FROM seed_trade_promo_events_q1_2026""").iloc[0]

    d.cover_facts([
        ("Events analysed (Q1 FY26)", f"{int(tot.n)} events"),
        ("Trade spend", f"{money(tot.spend)}"),
        ("Modelled incremental revenue", f"{money(tot.incr)}"),
        ("Average lift / incrementality index", f"{tot.lift:.1f}% lift · {tot.idx:.2f} index"),
        ("Headline call", "Rationalise low-incrementality Crunchwell events; shift to displays"),
    ])

    d.exec_summary(
        f"Across {int(tot.n)} Q1 FY2026 trade events, Acme spent {money(tot.spend)} to drive "
        f"{money(tot.incr)} of modelled incremental revenue — an average lift of {tot.lift:.1f}% at a "
        f"portfolio incrementality index of {tot.idx:.2f}. An index of {tot.idx:.2f} means roughly "
        f"half of promoted volume would have sold anyway; the trade dollar is under-working. The "
        f"pattern is consistent with the FY25 read: Crunchwell absorbs the majority of trade spend at "
        f"a deep discount but returns middling incrementality, while display-led mechanics and the "
        f"leaner ProteinPeak events return far more per dollar. The recommendation is to rationalise "
        f"the low-incrementality Crunchwell price events and shift the mix toward displays.",
        bullets=[
            f"<b>Portfolio incrementality is {tot.idx:.2f}</b> — below a 1.0 breakeven read; about "
            "half of promoted volume is subsidised base.",
            "<b>Crunchwell</b> takes ~$8.5M of the $11.6M spend (73%) at a 0.53 index — the biggest "
            "efficiency opportunity in the book.",
            "<b>Mechanic matters more than depth:</b> display-led events (Display + sample, "
            "Display only) return 0.66–0.72 index; flat price-off cuts ($0.40–$0.50 off) return "
            "0.38–0.41 and include the value-destroying cluster.",
            "<b>Forward-buy / value destruction</b> is real — three Mountain-West price events "
            "returned <i>negative</i> incrementality (index −0.15 to −0.21). See the RGM read, "
            "Report 17.",
        ])

    # ---- 1 · PEA scorecard & method
    d.h1("1 · PEA scorecard")
    d.kpis([
        ("Events", f"{int(tot.n)}", "Q1 FY26"),
        ("Spend", money(tot.spend), "trade investment"),
        ("Incremental", money(tot.incr), "modelled"),
        ("Incr. index", f"{tot.idx:.2f}", "≈ half is base"),
    ])
    d.body(
        "<b>Method.</b> Post-event analysis compares promoted-period sales to a modelled base to "
        "isolate incremental units, then nets the incremental gross margin against event spend. The "
        "incrementality index is incremental volume ÷ total promoted volume; an index near 1.0 means "
        "the promotion sold genuinely new volume, while a low index means most promoted units were "
        "subsidised base. PEA ROI = (incremental gross margin − spend) ÷ spend.")

    # ---- 2 · By brand
    d.h1("2 · Incrementality by brand")
    bb = df("""SELECT brand, COUNT(*) n, ROUND(SUM(spend_kusd)/1000,2) spend,
                 ROUND(SUM(incremental_revenue_kusd)/1000,2) incr,
                 ROUND(AVG(modeled_incrementality_index),2) idx,
                 ROUND(AVG(modeled_lift_pct),1) lift
               FROM seed_trade_promo_events_q1_2026 GROUP BY 1 ORDER BY spend DESC""")
    brows = [[r.brand, f"{r.n}", money(r.spend), money(r.incr), f"{r.lift:.1f}%", f"{r.idx:.2f}"]
             for r in bb.itertuples()]
    brows.append(["Total", f"{int(tot.n)}", money(tot.spend), money(tot.incr),
                  f"{tot.lift:.1f}%", f"{tot.idx:.2f}"])
    d.table(["Brand", "Events", "Spend", "Incremental", "Avg lift", "Incr. index"], brows,
            widths=[0.24, 0.13, 0.16, 0.18, 0.14, 0.15], total_row=True)
    d.source("seed_trade_promo_events_q1_2026.")
    ch1 = chart_bar("r27_idx_by_brand.png", list(bb.brand), [float(x) for x in bb.idx],
                    title="Trade incrementality index by brand (Q1 FY26)",
                    colors_list=[palette["teal"] if v >= 0.6 else (palette["gold"] if v >= 0.5 else palette["rust"]) for v in bb.idx],
                    horizontal=True, h=2.6)
    d.image(ch1, "ProteinPeak (0.74) and TrailGrove (0.64) work hard; Crunchwell (0.53) absorbs 73% "
                 "of spend at a middling index; HoneyNest (0.37) and MorningOats (0.38) drag.")
    d.body(
        "Crunchwell absorbs ~$8.5M of the $11.6M book (73% of spend) at a 0.53 index. That is the "
        "efficiency prize: even a modest lift in Crunchwell's index moves the whole portfolio. "
        "ProteinPeak, by contrast, spends lean ($0.82M) and returns a 0.74 index — the lean, "
        "display-and-sample launch model is working.")

    # ---- 3 · By mechanic
    d.pagebreak()
    d.h1("3 · What works — mechanic & event type")
    d.body(
        "Grouping by event type shows the lever is <i>mechanic</i>, not depth. Display-led events "
        "(Endcap, roadshow, display + sample) return the highest incrementality; flat price-off TPRs "
        "return the least and contain every value-destroying event in the book. Spend, however, is "
        "concentrated in exactly the wrong place — TPR price cuts carry the most dollars.")
    ev = df("""SELECT event_type, ROUND(SUM(spend_kusd)/1000,2) spend,
                 ROUND(SUM(incremental_revenue_kusd)/1000,2) incr,
                 ROUND(AVG(modeled_incrementality_index),2) idx
               FROM seed_trade_promo_events_q1_2026
               GROUP BY 1 HAVING SUM(spend_kusd) >= 300 ORDER BY spend DESC""")
    ch2 = chart_grouped("r27_mechanic.png", list(ev.event_type),
                        {"Spend ($M)": [float(x) for x in ev.spend],
                         "Incremental ($M)": [float(x) for x in ev.incr]},
                        title="Spend vs incremental revenue by event type ($M)", h=3.1, unit="M")
    d.image(ch2, "Plain TPR carries the most spend but returns near-parity; Endcap (display) returns "
                 "more incremental than it costs. Multi-store TPR is net-negative.")
    d.source("seed_trade_promo_events_q1_2026, event types with ≥ $0.3M spend.")

    mm = df("""SELECT CASE WHEN event_type LIKE '%Endcap%' OR event_type LIKE '%display%'
                        OR event_type LIKE '%Display%' OR event_type='Roadshow' THEN 'Display-led'
                     WHEN event_type LIKE '%TPR%' OR event_type LIKE '%price%' THEN 'Price-led (TPR)'
                     ELSE 'Other' END grp,
                 ROUND(AVG(modeled_incrementality_index),2) idx,
                 ROUND(SUM(spend_kusd)/1000,2) spend
               FROM seed_trade_promo_events_q1_2026 GROUP BY 1 ORDER BY idx DESC""")
    mrows = [[r.grp, money(r.spend), f"{r.idx:.2f}"] for r in mm.itertuples()]
    d.h2("3.1 · Display-led vs price-led")
    d.table(["Mechanic family", "Spend", "Avg incr. index"], mrows,
            widths=[0.44, 0.28, 0.28])
    d.source("seed_trade_promo_events_q1_2026, grouped by mechanic family.")

    # ---- 4 · Best & worst events
    d.h1("4 · Best & worst events")
    best = df("""SELECT event_id, brand, retailer, mechanic, spend_kusd sp,
                   incremental_revenue_kusd inc, modeled_incrementality_index idx
                 FROM seed_trade_promo_events_q1_2026 ORDER BY idx DESC LIMIT 3""")
    worst = df("""SELECT event_id, brand, retailer, mechanic, spend_kusd sp,
                    incremental_revenue_kusd inc, modeled_incrementality_index idx
                  FROM seed_trade_promo_events_q1_2026 ORDER BY idx ASC LIMIT 3""")
    d.h2("4.1 · Top 3 events by incrementality")
    d.table(["Event", "Brand", "Retailer", "Mechanic", "Spend $K", "Incr $K", "Index"],
            [[r.event_id, r.brand, r.retailer, r.mechanic, f"{r.sp:.0f}", f"{r.inc:.0f}", f"{r.idx:.2f}"]
             for r in best.itertuples()],
            widths=[0.15, 0.14, 0.20, 0.21, 0.10, 0.10, 0.10])
    d.h2("4.2 · Bottom 3 events — value-destroying")
    d.table(["Event", "Brand", "Retailer", "Mechanic", "Spend $K", "Incr $K", "Index"],
            [[r.event_id, r.brand, r.retailer, r.mechanic, f"{r.sp:.0f}", f"{r.inc:.0f}", f"{r.idx:.2f}"]
             for r in worst.itertuples()],
            widths=[0.15, 0.14, 0.20, 0.21, 0.10, 0.10, 0.10])
    d.source("seed_trade_promo_events_q1_2026, ranked by modelled incrementality index.")
    d.callout("Forward-buy & the Mountain-West cluster",
              "The three worst events are all flat price-off cuts run through a Mountain-West "
              "multi-store banner — they returned negative incremental revenue (index −0.15 to −0.21). "
              "This is classic forward-buy leakage: the discount pulled base volume forward and "
              "subsidised units the shopper would have bought at full price. The LA anchor event "
              "(TPE-Q1-011, $0.55-off Crunchwell) is the counter-example — a 1.10 index and ~1.1 pts "
              "of share recovery. Reallocate away from the cluster; protect the LA anchor.", "risk")

    # ---- 5 · FY25 context & recommendation
    d.h1("5 · FY25 context — Crunchwell is over-invested")
    d.body(
        "The Q1 read is not new; it is the FY25 pattern repeating. In FY25 Crunchwell absorbed "
        "$92.4M of ~$147M total trade spend at a 25.6% depth of gross — roughly a quarter of gross "
        "revenue given back — for only a 0.57 incrementality index. The flagship is over-invested in "
        "deep price promotion that largely subsidises base volume, while the growth engine "
        "(ProteinPeak, 12.9% trade rate) is deliberately lean. Rebalancing the trade book toward "
        "high-incrementality mechanics is the single largest RGM lever (see the RGM read, Report 17).")
    fy = df("""SELECT brand, ROUND(SUM(trade_spend_kusd)/1000,1) spend,
                 ROUND(SUM(trade_spend_kusd*trade_depth_pct)/SUM(trade_spend_kusd),1) depth,
                 ROUND(SUM(trade_spend_kusd*incrementality_index)/SUM(trade_spend_kusd),2) idx
               FROM seed_trade_spend_fy25 GROUP BY 1 ORDER BY spend DESC""")
    frows = [[r.brand, money(r.spend), f"{r.depth:.1f}%", f"{r.idx:.2f}"] for r in fy.itertuples()]
    d.h2("5.1 · FY25 trade spend, depth & incrementality by brand")
    d.table(["Brand", "Trade spend", "Weighted depth", "Incr. index"], frows,
            widths=[0.34, 0.24, 0.22, 0.20])
    d.source("seed_trade_spend_fy25 (headline Crunchwell 25.6% depth / 0.57 index per FACTS).")

    d.recommendations([
        ("Rationalise the low-incrementality Crunchwell price events; cap flat price-off depth and "
         "retire the Mountain-West value-destroying cluster.",
         "Revenue Growth Mgmt", "H2 planning"),
        ("Shift the mix toward display-led mechanics (Endcap, display + sample) that return "
         "0.66–0.72 index vs 0.38–0.41 for flat price-off.",
         "Trade Finance / RGM", "H2"),
        ("Protect and scale the LA anchor model (TPE-Q1-011, 1.10 index) as the template for "
         "share-recovery trade.",
         "Marcus Boudreaux", "Q3"),
        ("Instrument forward-buy detection in the PEA model so value-destroying events are flagged "
         "in-flight, not in the post-mortem.",
         "Trade Finance", "H2"),
    ])
    return d.build()


# ============================================================== REPORT 28 ===
def r28_marketing_mix_media():
    d = Doc("28-h1-2026-marketing-mix-media-effectiveness.pdf",
            kicker="MARKETING MIX & MEDIA EFFECTIVENESS",
            title="H1 FY2026 Marketing Mix & Media Effectiveness Review",
            subtitle="A&P allocation, retail-media incrementality, and the two-speed brand model",
            owner="CMO office; Hugo Lin (media); Tasha Brooks (retail media)",
            period="H1 FY2026", short="MMM & Media H1",
            doc_type="Marketing mix & media effectiveness review",
            date_str="June 2026")

    q1 = df("SELECT SUM(spend_kusd)/1000 s FROM seed_marketing_spend WHERE period='2026-Q1'").iloc[0].s
    q2 = df("SELECT SUM(spend_kusd)/1000 s FROM seed_marketing_spend WHERE period='2026-Q2'").iloc[0].s
    rm_blend = df("""SELECT SUM(incremental_revenue_kusd)*1.0/SUM(spend_kusd) b
                     FROM seed_retail_media_spend_q1_2026""").iloc[0].b

    d.cover_facts([
        ("A&P spend (H1 FY26)", f"{money(q1)} (Q1) + {money(q2)} (Q2) = {money(q1+q2)}"),
        ("Crunchwell model", "~$48.7M/yr, TV-heavy (Linear TV $24M)"),
        ("ProteinPeak model", "~$22.2M/yr, digital/creator (Paid Social $7.8M)"),
        ("Retail-media incrementality", f"${rm_blend:.2f} per $1 blended · Walmart 1.20 vs Amazon 0.40"),
        ("Headline call", "Fund what works per brand; fix the Amazon-Ads drag"),
    ])

    d.exec_summary(
        f"Acme runs a two-speed marketing model, and the effectiveness read says both speeds are "
        f"broadly right for their brand — with one clear fix. Crunchwell spends ~$48.7M a year on a "
        f"traditional, TV-heavy plan ($24M Linear TV); ProteinPeak spends ~$22.2M on a digital, "
        f"creator-led plan ($7.8M Paid Social, $2.86M Influencer) and is winning the social "
        f"conversation (+0.44 sentiment). H1 A&P totals {money(q1+q2)}. The sharpest finding is in "
        f"retail media: the blended return is ${rm_blend:.2f} incremental per $1, dragged down by "
        f"Amazon Ads (0.40) while Walmart Connect (1.20) more than pays back. Fix the Amazon drag "
        f"and the working-media dollar improves without new budget.",
        bullets=[
            f"<b>H1 A&P is {money(q1+q2)}</b> ({money(q1)} in Q1, {money(q2)} in Q2) — the spend "
            "steps up into the ProteinPeak launch quarter.",
            "<b>Two-speed model:</b> Crunchwell is TV-first (Linear TV = ~$24M, ~half its plan); "
            "ProteinPeak is social-first (Paid Social $7.8M) and creator-led (Influencer $2.86M).",
            f"<b>Retail media returns ${rm_blend:.2f}/$1 blended</b> — Walmart Connect 1.20 and "
            "Kroger 0.77 carry it; Amazon Ads (0.40) is a drag on $2.4M of spend.",
            "<b>Creators are working for ProteinPeak:</b> +0.44 social sentiment vs Crunchwell's "
            "−0.11 — the digital model is buying relevance the TV model isn't (see Report 29).",
        ])

    # ---- 1 · A&P scorecard
    d.h1("1 · A&P scorecard")
    d.kpis([
        ("A&P H1 FY26", money(q1 + q2), "Q1 + Q2"),
        ("Crunchwell A&P", "$48.7M", "TV-heavy, /yr"),
        ("ProteinPeak A&P", "$22.2M", "digital, /yr"),
        ("Retail media ROI", f"${rm_blend:.2f}", "incr. per $1"),
    ])
    d.body(
        "A&P by period steps up through H1 as spend loads into the ProteinPeak launch (26Q2 $11.7M). "
        "The strategic question for this review is not the level but the mix: whether each brand's "
        "channel plan matches how its shoppers actually buy — and whether the working-media dollar "
        "is returning incremental volume.")
    ap = df("""SELECT period, ROUND(SUM(spend_kusd)/1000,1) s FROM seed_marketing_spend
               GROUP BY 1 ORDER BY 1""")
    ch1 = chart_bar("r28_ap_by_period.png", list(ap.period), [float(x) for x in ap.s],
                    title="A&P spend by period ($M)", color="navy", unit="M", h=2.5)
    d.image(ch1, "A&P steps back up in H1 FY26 (26Q1 $10.9M, 26Q2 $11.7M) after the FY25 taper, "
                 "funding the ProteinPeak launch.")
    d.source("seed_marketing_spend, by period.")

    # ---- 2 · Two-speed channel mix
    d.h1("2 · The two-speed brand model")
    d.body(
        "Crunchwell and ProteinPeak run near-opposite channel plans. Crunchwell is traditional and "
        "TV-led — Linear TV alone is ~$24M, roughly half the brand's A&P, with Retail Media and CTV "
        "next. ProteinPeak is digital and creator-led — Paid Social is the largest line ($7.8M), "
        "followed by Retail Media and CTV, with a meaningful Influencer investment ($2.86M) that "
        "Crunchwell essentially does not run. This is a deliberate segmentation: reach-and-frequency "
        "for the established flagship, culture-and-creators for the growth engine.")
    cw = df("""SELECT channel, ROUND(SUM(spend_kusd)/1000,2) m FROM seed_marketing_spend
               WHERE brand='Crunchwell' GROUP BY 1""").set_index("channel")["m"].to_dict()
    pp = df("""SELECT channel, ROUND(SUM(spend_kusd)/1000,2) m FROM seed_marketing_spend
               WHERE brand='ProteinPeak' GROUP BY 1""").set_index("channel")["m"].to_dict()
    chans = ["Linear TV", "Connected TV", "Paid Social", "Retail Media",
             "Influencer", "Digital Display", "Search"]
    ch2 = chart_grouped("r28_channel_mix.png", [c.replace(" ", "\n", 1) for c in chans],
                        {"Crunchwell": [round(cw.get(c, 0.0), 2) for c in chans],
                         "ProteinPeak": [round(pp.get(c, 0.0), 2) for c in chans]},
                        title="A&P channel mix — Crunchwell vs ProteinPeak ($M/yr)", h=3.1, unit="M")
    d.image(ch2, "Crunchwell is TV-first (Linear TV ~$24M); ProteinPeak is social-first ($7.8M) with "
                 "real influencer spend. Two brands, two media models.")
    d.source("seed_marketing_spend, by brand × channel.")

    # ---- 3 · Retail-media incrementality
    d.pagebreak()
    d.h1("3 · Retail-media incrementality — the fixable drag")
    d.body(
        "Retail media is where the read is sharpest and the fix is clearest. Platform-reported ROAS "
        "flatters every platform; the modelled incrementality ratio tells the real story. Walmart "
        "Connect returns 1.20 incremental per $1 and Kroger Precision 0.77 — both carrying the "
        "portfolio. Amazon Ads returns 0.40 on the largest single spend line ($2.4M), and Target "
        "Roundel 0.50. The blended return is $0.65 per $1. The Amazon drag is the fixable problem: "
        "much of that spend is defending base volume the shopper would have bought anyway.")
    rm = df("""SELECT platform, ROUND(SUM(spend_kusd)/1000,2) spend,
                 ROUND(SUM(incremental_revenue_kusd)/1000,2) incr,
                 ROUND(AVG(modeled_incrementality_ratio),2) ratio,
                 ROUND(AVG(platform_reported_roas),2) roas
               FROM seed_retail_media_spend_q1_2026 GROUP BY 1 ORDER BY spend DESC""")
    short_names = {"Kroger Precision Marketing": "Kroger Precision"}
    rrows = [[short_names.get(r.platform, r.platform), money(r.spend), money(r.incr),
              f"{r.roas:.2f}", f"{r.ratio:.2f}",
              "Reinvest" if r.ratio >= 0.9 else ("Hold" if r.ratio >= 0.7 else "Reallocate")]
             for r in rm.itertuples()]
    d.table(["Platform", "Spend", "Incremental", "Reported ROAS", "Modelled incr.", "Call"], rrows,
            widths=[0.24, 0.14, 0.16, 0.16, 0.15, 0.15])
    d.source("seed_retail_media_spend_q1_2026 (Tasha Brooks). Modelled incrementality ≠ platform ROAS.")
    ch3 = chart_bar("r28_retail_media.png",
                    [short_names.get(p, p) for p in rm.platform],
                    [float(x) for x in rm.ratio],
                    title="Retail-media modelled incrementality by platform (per $1)",
                    colors_list=[palette["teal"] if v >= 0.9 else (palette["gold"] if v >= 0.7 else palette["rust"]) for v in rm.ratio],
                    h=2.6)
    d.image(ch3, "Walmart Connect (1.20) is the only platform above breakeven; Amazon Ads (0.40) is "
                 "the drag. Blended return $0.65 per $1.")

    # ---- 4 · Creators & sentiment
    d.h1("4 · Creators & the relevance dividend")
    d.body(
        "The digital / creator model is buying something the TV model is not: cultural relevance, "
        "visible in social sentiment. ProteinPeak runs +0.44 net sentiment on ~496 mentions in 2026 "
        "— the strongest of any Acme brand — while Crunchwell sits at −0.11 on 316 mentions. The "
        "$2.86M ProteinPeak influencer line is a small share of A&P but is doing outsized work on the "
        "relevance metric that the brand-equity tracker (Report 29) flags as Crunchwell's core "
        "weakness. The read is not 'spend more on TV' or 'spend more on social' universally — it is "
        "'buy relevance where relevance is the problem'.")
    sent = df("""SELECT Brand_Mentioned b, ROUND(AVG(\"Sentiment_-1to1\"),2) s, COUNT(*) n
                 FROM social_mentions
                 WHERE strftime(CAST(Date AS DATE),'%Y')='2026'
                 AND Brand_Mentioned IN ('ProteinPeak','MorningOats','HoneyNest','TrailGrove',
                     'RootDay','Crunchwell')
                 GROUP BY 1 ORDER BY s DESC""")
    ch4 = chart_bar("r28_sentiment.png", list(sent.b), [float(x) for x in sent.s],
                    title="2026 social sentiment by Acme brand (net −1 to +1)",
                    colors_list=[palette["teal"] if v > 0 else palette["rust"] for v in sent.s],
                    h=2.6)
    d.image(ch4, "ProteinPeak (+0.44) leads on sentiment; Crunchwell (−0.11) is the only Acme brand "
                 "underwater. The creator model is buying relevance.")
    d.source("social_mentions, Sentiment_-1to1, calendar 2026.")

    # ---- 5 · Recommendations
    d.h1("5 · The media call")
    d.callout("Cross-reference: eComm / retail media and the CFO read",
              "The retail-media reallocation detailed here feeds the eComm / retail-media plan "
              "(Report 34) and the CFO effectiveness read (Report 40). The proposed H2 move is to "
              "shift ~$700K out of Amazon Ads into Walmart Connect, Kroger, and the Louisiana "
              "recovery (a ~2.2× ROI lane) — a reallocation, not a budget increase.", "info")
    d.recommendations([
        ("Reallocate H2 retail media out of Amazon Ads (0.40) into Walmart Connect (1.20), Kroger, "
         "and LA — planning estimate ~$700K shift, no net budget increase.",
         "Tasha Brooks", "H2 planning"),
        ("Hold Crunchwell's TV-led plan but test shifting marginal dollars to CTV/social to buy the "
         "relevance the equity tracker (Report 29) is flagging.",
         "Hugo Lin / CMO office", "H2"),
        ("Protect and scale the ProteinPeak creator model ($2.86M influencer) behind the launch and "
         "the Q3 Chocolate Almond concept.",
         "Sage Park / Hugo Lin", "Q3"),
        ("Report modelled incrementality — not platform ROAS — as the retail-media KPI in the CFO "
         "read (Report 40).",
         "Trade Finance / CMO office", "Next MBR"),
    ])
    return d.build()


# ============================================================== REPORT 29 ===
def r29_brand_equity_tracker():
    d = Doc("29-q2-2026-brand-equity-consumer-health-tracker.pdf",
            kicker="BRAND EQUITY & CONSUMER HEALTH",
            title="Q2 FY2026 Brand Equity & Consumer Health Tracker Readout",
            subtitle="The Crunchwell relevance slide, the competitive frame, and the 'relevance not trust' thesis",
            owner="Nina Ortega, Consumer Insights",
            period="Q2 FY2026 (FY26Q2 wave)", short="Equity Tracker Q2",
            doc_type="Brand equity & consumer health tracker readout",
            date_str="June 2026")

    rel = df("""SELECT Top_Two_Box_Pct v, Wave FROM brand_equity_quarterly
                WHERE Brand='Crunchwell' AND DMA='US-NAT' AND Attribute='Relevance'
                ORDER BY Wave""")
    rel_start = float(rel[rel.Wave == "FY25Q1"].v.iloc[0])
    rel_end = float(rel[rel.Wave == "FY26Q2"].v.iloc[0])
    rel_delta = rel_end - rel_start
    nps = df("SELECT ROUND(AVG(nps_0to10),1) n FROM brand_health WHERE wave='2026Q2'").iloc[0].n
    aw = df("SELECT ROUND(AVG(aided_aw_crunchwell)*100,0) a FROM brand_health WHERE wave='2026Q2'").iloc[0].a

    d.cover_facts([
        ("Crunchwell Relevance", f"{rel_start:.1f} → {rel_end:.1f} ({rel_delta:+.1f} pp) — the flag"),
        ("Crunchwell Trust", "72.3 → 72.9 — holds"),
        ("The thesis", "Relevance, not Trust: trusted but drifting from culture"),
        ("NPS / aided awareness", f"~{nps:.1f} flat · ~{aw:.0f}% aware"),
        ("Social sentiment", "ProteinPeak +0.44 vs Crunchwell −0.11"),
    ])

    d.exec_summary(
        f"The Q2 equity wave delivers one clear diagnosis for Crunchwell: the problem is relevance, "
        f"not trust. Crunchwell's Relevance top-two-box has slid from {rel_start:.1f} to {rel_end:.1f} "
        f"({rel_delta:+.1f} pp) across six waves, while Trust holds at ~72, Taste at ~73 and Quality "
        f"at ~70. The brand is still trusted and still tastes right — it is drifting from cultural "
        f"relevance. The competitive frame sharpens the point: ProteinPeak (76.2) and Field & Honey "
        f"(80.9) score far higher on relevance while Crunchwell's trust advantage is being matched. "
        f"Consumer-health fundamentals (NPS ~{nps:.1f}, aided awareness ~{aw:.0f}%) are flat and "
        f"healthy — this is not an awareness or quality problem. Social sentiment closes the case: "
        f"ProteinPeak +0.44, Crunchwell −0.11.",
        bullets=[
            f"<b>The flag:</b> Crunchwell Relevance {rel_start:.1f} → {rel_end:.1f} "
            f"({rel_delta:+.1f} pp), the only attribute in structural decline.",
            "<b>Trust is intact</b> (72.3 → 72.9) as are Taste (~73) and Quality (~70). "
            "Modernity is soft (~49) — the leading edge of the relevance slide.",
            "<b>Competitively</b>, ProteinPeak (76.2 relevance) and Field & Honey (80.9) out-relevance "
            "Crunchwell (62.7); the trust moat is narrowing.",
            "<b>Fundamentals are flat and fine</b> — NPS ~6.5, aided awareness ~82%, taste ~3.6/5. "
            "The fix is relevance-building, not repair (see the Crunchwell turnaround, Report 24).",
        ])

    # ---- 1 · Equity scorecard
    d.h1("1 · Crunchwell equity scorecard")
    d.kpis([
        ("Relevance", f"{rel_end:.1f}", f"{rel_delta:+.1f} pp / 6 waves"),
        ("Trust", "72.9", "holds"),
        ("NPS", f"~{nps:.1f}", "flat"),
        ("Aided awareness", f"~{aw:.0f}%", "flat"),
    ])
    d.body(
        "Read the scorecard as a single sentence: everything that says 'do you trust this brand' is "
        "stable, and the one thing that says 'is this brand for someone like me, now' is falling. "
        "That is a relevance problem, and it is the highest-priority read of the wave.")

    # ---- 2 · The relevance slide
    d.h1("2 · The relevance slide — six waves")
    d.body(
        "Tracking Crunchwell's five equity attributes across six quarterly waves isolates Relevance "
        "as the single moving part. Trust, Taste and Quality run flat-to-up; Modernity is soft and "
        "drifting; Relevance is in a clear, sustained decline. Modernity and Relevance moving "
        "together is the classic signature of a heritage brand losing cultural currency while its "
        "product equity stays intact.")
    ce = df("""SELECT Wave, Attribute, Top_Two_Box_Pct FROM brand_equity_quarterly
               WHERE Brand='Crunchwell' AND DMA='US-NAT' ORDER BY Wave""")
    waves = ["FY25Q1", "FY25Q2", "FY25Q3", "FY25Q4", "FY26Q1", "FY26Q2"]
    series = {}
    for attr in ["Relevance", "Trust", "Taste", "Quality", "Modernity"]:
        sub = ce[ce.Attribute == attr].set_index("Wave")["Top_Two_Box_Pct"].to_dict()
        series[attr] = [round(float(sub[w]), 1) for w in waves]
    ch1 = chart_line("r29_crunchwell_equity.png", waves, series,
                     title="Crunchwell equity attributes, top-two-box (%) — 6 waves", h=3.1)
    d.image(ch1, "Relevance falls −5.9 pp while Trust, Taste and Quality hold. Modernity drifts down "
                 "alongside Relevance — the heritage-brand signature.")
    d.source("brand_equity_quarterly, Crunchwell US-NAT, Kantar-shape top-two-box.")

    # ---- 3 · Competitive frame
    d.pagebreak()
    d.h1("3 · Competitive frame — relevance vs trust")
    d.body(
        "Plotting the FY26Q2 wave across the competitive set makes the strategic geometry clear. "
        "Crunchwell holds a genuine <i>trust</i> advantage over the challenger brands (ProteinPeak "
        "58.1, Field & Honey 66.0) — but is beaten decisively on <i>relevance</i> by both "
        "ProteinPeak (76.2) and Field & Honey (80.9), and only narrowly leads Cheerios. The "
        "established players (Cheerios, Crunchwell) own trust; the insurgents own relevance. "
        "Crunchwell's task is to convert its trust equity into contemporary relevance before the "
        "trust moat itself erodes.")
    comp = df("""SELECT Brand, Attribute, Top_Two_Box_Pct FROM brand_equity_quarterly
                 WHERE DMA='US-NAT' AND Wave='FY26Q2' AND Attribute IN ('Relevance','Trust')""")
    order = ["Field & Honey", "ProteinPeak", "Cheerios", "Crunchwell",
             "MorningOats", "Simple Truth PL", "HoneyNest"]
    rel_map = comp[comp.Attribute == "Relevance"].set_index("Brand")["Top_Two_Box_Pct"].to_dict()
    tru_map = comp[comp.Attribute == "Trust"].set_index("Brand")["Top_Two_Box_Pct"].to_dict()
    order = [b for b in order if b in rel_map]
    ch2 = chart_grouped("r29_comp_rel_trust.png", order,
                        {"Relevance": [round(float(rel_map[b]), 1) for b in order],
                         "Trust": [round(float(tru_map[b]), 1) for b in order]},
                        title="Relevance vs Trust by brand — FY26Q2 (top-two-box %)", pct=True, h=3.1)
    d.image(ch2, "Crunchwell leads on Trust but trails ProteinPeak and Field & Honey on Relevance. "
                 "Insurgents own relevance; heritage brands own trust.")
    d.source("brand_equity_quarterly, US-NAT, FY26Q2 wave.")
    crows = [[b, f"{rel_map[b]:.1f}", f"{tru_map[b]:.1f}",
              f"{rel_map[b]-tru_map[b]:+.1f}"] for b in order]
    d.h2("3.1 · Relevance and trust by brand — FY26Q2")
    d.table(["Brand", "Relevance", "Trust", "Relevance − Trust"], crows,
            widths=[0.34, 0.22, 0.22, 0.22])
    d.source("brand_equity_quarterly, US-NAT, FY26Q2.")

    # ---- 4 · Consumer health & sentiment
    d.h1("4 · Consumer health & social sentiment")
    d.body(
        f"The consumer-health fundamentals confirm this is a relevance problem, not a franchise "
        f"failure. Crunchwell NPS holds at ~{nps:.1f}, aided awareness at ~{aw:.0f}%, and taste at "
        f"~3.6/5 — all flat over two years. Nobody has forgotten Crunchwell and nobody thinks it "
        f"tastes worse; they are simply choosing brands that feel more relevant to how they eat now. "
        f"Social sentiment is the sharpest expression of the gap: in 2026 ProteinPeak runs +0.44 "
        f"across ~496 mentions while Crunchwell is the only Acme brand underwater at −0.11 across "
        f"316 mentions.")
    bh = df("""SELECT wave, ROUND(AVG(nps_0to10),2) nps,
                 ROUND(AVG(aided_aw_crunchwell)*100,1) aw, ROUND(AVG(taste),2) taste
               FROM brand_health WHERE wave LIKE '2025%' OR wave LIKE '2026%'
               GROUP BY 1 ORDER BY 1""")
    bh_rows = [[r.wave, f"{r.nps:.2f}", f"{r.aw:.1f}%", f"{r.taste:.2f}"] for r in bh.itertuples()]
    d.h2("4.1 · Crunchwell consumer-health fundamentals (FY25–FY26 waves)")
    d.table(["Wave", "NPS (0–10)", "Aided awareness", "Taste (1–5)"], bh_rows,
            widths=[0.28, 0.24, 0.26, 0.22])
    d.source("brand_health, quarterly waves.")

    sent = df("""SELECT Brand_Mentioned b, ROUND(AVG(\"Sentiment_-1to1\"),2) s
                 FROM social_mentions
                 WHERE strftime(CAST(Date AS DATE),'%Y')='2026'
                 AND Brand_Mentioned IN ('ProteinPeak','Crunchwell','HoneyNest','MorningOats',
                     'TrailGrove','RootDay')
                 GROUP BY 1 ORDER BY s DESC""")
    ch3 = chart_bar("r29_sentiment.png", list(sent.b), [float(x) for x in sent.s],
                    title="2026 social sentiment by Acme brand (net −1 to +1)",
                    colors_list=[palette["teal"] if v > 0 else palette["rust"] for v in sent.s],
                    h=2.6)
    d.image(ch3, "ProteinPeak (+0.44) leads; Crunchwell (−0.11) is the only Acme brand with negative "
                 "net sentiment — the relevance gap in the wild.")
    d.source("social_mentions, Sentiment_-1to1, calendar 2026.")

    # ---- 5 · The thesis & recommendations
    d.h1("5 · 'Relevance, not Trust' — the thesis")
    d.callout("The one thing to take away",
              "Crunchwell does not have a trust problem, a quality problem, or an awareness problem — "
              "all three are stable. It has a relevance problem: a −5.9 pp slide on the single "
              "attribute that predicts whether a shopper feels the brand is for them, now. The "
              "turnaround job (Report 24) is relevance-building — modern formats, culturally-current "
              "communications, and the Pack Refresh — not brand repair. Protect the trust equity "
              "while it funds the relevance rebuild.", "risk")
    d.recommendations([
        ("Adopt 'relevance, not trust' as the Crunchwell diagnosis; make Relevance top-two-box the "
         "tracked North-Star equity metric.",
         "Nina Ortega / Cory Whitman", "This wave"),
        ("Direct the Crunchwell turnaround (Report 24) at relevance-building — Pack Refresh, modern "
         "formats, culturally-current comms — not product repair.",
         "Crunchwell brand", "H2"),
        ("Shift marginal A&P toward the relevance-buying channels (CTV, social, creators) that are "
         "working for ProteinPeak (see Report 28).",
         "CMO office / Hugo Lin", "H2 planning"),
        ("Re-field the equity wave in FY26Q3 to confirm whether Pack Refresh and comms arrest the "
         "relevance slide.",
         "Consumer Insights", "FY26Q3"),
    ])
    return d.build()


if __name__ == "__main__":
    for fn in (r25_sop_ibp_executive_review,
               r26_supply_chain_service_review,
               r27_trade_promo_pea,
               r28_marketing_mix_media,
               r29_brand_equity_tracker):
        print(fn())
