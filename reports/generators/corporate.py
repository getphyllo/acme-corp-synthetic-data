"""Corporate / enterprise-level reports (11-17, 40). Run: python generators/corporate.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import (Doc, df, seed_csv, money, chart_line, chart_bar, chart_grouped,
                 chart_stacked, chart_waterfall, chart_donut)


def _qsum(periods):
    ps = ",".join(f"'{p}'" for p in periods)
    r = df(f"SELECT SUM(Plan_Revenue_USD)/1e6 p, SUM(Actual_Revenue_USD)/1e6 a "
           f"FROM plan_vs_actual WHERE Period IN ({ps})").iloc[0]
    return float(r.p), float(r.a)


def r11_company_q1_qbr():
    d = Doc("11-acme-q1-2026-company-business-review.pdf",
            kicker="QUARTERLY BUSINESS REVIEW",
            title="Acme Corp — Q1 FY2026 Company Business Review",
            subtitle="Enterprise performance across all six brands and four regions",
            owner="Diane Halverson, VP Sales NA (sponsor); Finance & Insights (prep)",
            period="Q1 FY2026 (Jan–Mar 2026)", short="Q1 2026 Company BR",
            doc_type="Internal quarterly business review", date_str="April 2026")

    p_q1, a_q1 = _qsum(["2026-01", "2026-02", "2026-03"])
    var_q1 = (a_q1 - p_q1) / p_q1 * 100
    d.cover_facts([
        ("Net revenue vs plan (Q1)", f"{money(a_q1)} actual vs {money(p_q1)} plan · {var_q1:+.1f}%"),
        ("FY25 net revenue", "$812M (+5.1% YoY)"),
        ("EBITDA margin", "14.2% (target 16% by FY28)"),
        ("Biggest miss", "ProteinPeak −25% (pre-launch); Crunchwell LA −340 bps"),
        ("Headline call", "Hold the number for FY26 on the Q2 ProteinPeak launch"),
    ])

    d.exec_summary(
        "Acme closed Q1 FY2026 at " + money(a_q1) + " net revenue, "
        f"{var_q1:.1f}% behind the ${p_q1:,.0f}M plan — a shortfall concentrated in two known, "
        "well-understood places rather than a broad-based demand problem. National RTE-cereal share "
        "held at 7.9% (Acme all-brand), category dollars grew +1.1%, and four of six brands landed "
        "within 2 points of plan. The gap is Crunchwell's Louisiana share erosion and a ProteinPeak "
        "line that is being deliberately under-shipped ahead of its April 20 relaunch.",
        bullets=[
            f"<b>The number:</b> Q1 net revenue {money(a_q1)} vs {money(p_q1)} plan ({var_q1:+.1f}%). "
            "The trajectory improves through the quarter as ProteinPeak launch pipe fills.",
            "<b>Crunchwell Louisiana</b> is −340 bps of local share (a five-hypothesis root cause: Walmart "
            "reset, Larksfield promo intensity, Hurricane Tonya supply, private label, Hispanic-shopper shift). "
            "Recovery plan is scoped and funded for Q2.",
            "<b>ProteinPeak</b> ran −25% to plan in Q1 by design — the +$32M FY26 build sits on the Cinnamon "
            "Crunch and Cocoa Almond launch that ships from April 20.",
            "<b>Spend efficiency</b> is the watch-item for the CFO: Q1 retail media returned $0.65 incremental "
            "per $1, dragged by Amazon Ads; trade incrementality sits at 0.52.",
        ])

    d.h1("1 · Enterprise scorecard")
    d.kpis([
        ("Net revenue (Q1)", money(a_q1), f"{var_q1:+.1f}% vs plan"),
        ("RTE share (Acme, natl)", "7.9%", "flat vs LY"),
        ("Category $ growth", "+1.1%", "RTE total US"),
        ("Retail-media ROI", "$0.65", "incremental per $1"),
        ("Fill rate", "94.9%", "storm-recovered"),
    ])
    d.body(
        "The scorecard reads amber, not red. Revenue is behind plan, but share, distribution and brand "
        "equity are broadly stable, and the two sources of the miss are both actively managed. The "
        "quarter's job was to keep the base intact while pre-loading the Q2 innovation; that job was done.")

    # brand plan-vs-actual Q1
    bd = df("""SELECT Brand,
                 ROUND(SUM(Plan_Revenue_USD)/1e6,1) plan,
                 ROUND(SUM(Actual_Revenue_USD)/1e6,1) act,
                 ROUND((SUM(Actual_Revenue_USD)-SUM(Plan_Revenue_USD))/SUM(Plan_Revenue_USD)*100,1) var
               FROM plan_vs_actual WHERE Period IN ('2026-01','2026-02','2026-03')
               GROUP BY 1 ORDER BY plan DESC""")
    rows = [[r.Brand, f"${r.plan:,.1f}M", f"${r.act:,.1f}M", f"{r.var:+.1f}%",
             "On track" if r.var > -3 else ("Watch" if r.var > -10 else "Action")] for r in bd.itertuples()]
    rows.append(["Total Acme", f"${p_q1:,.1f}M", f"${a_q1:,.1f}M", f"{var_q1:+.1f}%", "Amber"])
    d.h2("Brand net revenue vs plan — Q1 FY2026")
    d.table(["Brand", "Plan", "Actual", "Var %", "Status"], rows,
            widths=[0.30, 0.18, 0.18, 0.16, 0.18], total_row=True)
    d.source("plan_vs_actual (SAP/Acme ERP shape), Q1 FY2026 periods.")

    ch = chart_bar("r11_brand_var.png", list(bd.Brand), list(bd["var"]),
                   title="Q1 revenue variance to plan, by brand (%)", pct=True,
                   colors_list=["#2E7D75" if v > -3 else ("#B98A2E" if v > -10 else "#B24A2E") for v in bd["var"]],
                   horizontal=True, h=2.6)
    d.image(ch, "Four of six brands within 2 pts of plan. ProteinPeak's gap is a planned pre-launch draw-down.")

    d.pagebreak()
    d.h1("2 · Share & category context")
    sh = df("""SELECT SUBSTR(Week,1,4)||'-Q'||CAST(CEIL(CAST(SUBSTR(Week,7,2) AS INT)/13.0) AS INT) q,
                 AVG(Acme_Value_Share)*100 acme, AVG(Crunchwell_Value_Share)*100 cw,
                 AVG(Larksfield_Value_Share)*100 lf
               FROM syndicated_weekly WHERE Category='RTE Cereal' AND DMA<>'LA-DMA'
                 AND Week>='2025-W01' GROUP BY 1 ORDER BY 1""")
    ch2 = chart_line("r11_share.png", list(sh.q),
                     {"Acme (all brands)": [round(x, 2) for x in sh.acme],
                      "Crunchwell": [round(x, 2) for x in sh.cw],
                      "Larksfield": [round(x, 2) for x in sh.lf]},
                     title="National RTE-cereal value share (%)", pct=True, h=2.9)
    d.body(
        "National share is stable: Acme all-brand value share holds at 7.9%, Crunchwell at 6.0%, and "
        "Larksfield — the share gainer nationally and the aggressor in the South — at 14.0%. The "
        "category grew +1.1% in dollars, led by Wellness Protein (+17%) and dragged by Kids Sweet (−3%). "
        "The strategic read: our share problem is regional (Louisiana) and segment-shaped (protein, "
        "where we under-index), not a national franchise decline.")
    d.image(ch2)
    d.callout("Segment mix is the real story",
              "Wellness Protein is the category's fastest-growing pocket at +17–18% and now $840M. "
              "Acme holds 7.6% and is building fast behind ProteinPeak. Family Sweet — where Crunchwell "
              "lives — grows +1.4%. Where we play determines how hard we have to run.", "info")

    d.h1("3 · The two problems, sized")
    d.h2("3.1 · Crunchwell Louisiana — −340 bps of local share")
    d.body(
        "Crunchwell's Louisiana DMA share fell from ~6.4% (Q4 FY24 Mass/Grocery peak) to 3.0% in Q1 FY2026. "
        "Root cause is now attributed across five hypotheses: the Walmart September modular reset that cut "
        "Crunchwell Mega from 8 to 6 facings (~55%), Larksfield promo intensification at Rouses (~20%), the "
        "Hurricane Tonya supply collapse that dropped Houston-DC fill to ~52% (~12%), Walmart private-label "
        "pressure (~8%), and a Hispanic-shopper mix shift (~5%). A three-leg recovery is funded for Q2: "
        "facing recovery, targeted trade, and a LA retail-media injection at 2.2× the portfolio ROI.")
    d.h2("3.2 · ProteinPeak — a planned Q1 trough before the Q2 build")
    d.body(
        "ProteinPeak ran −25% to plan in Q1 because the $48M→$80M FY26 build is loaded onto two new SKUs — "
        "Cinnamon Crunch (PP005) and Cocoa Almond (PP006) — that did not ship until April 20. The Q1 miss is "
        "the pre-launch pipeline draw-down, not a demand signal; the launch read (Report 12 / 02) shows trial "
        "at 110% of plan at Target in the first four weeks.")

    d.h1("4 · Commercial & spend efficiency")
    rm = seed_csv("retail_media_spend_q1_2026.csv")
    rmg = rm.groupby("platform").agg(spend=("spend_kusd", "sum"),
                                     inc=("incremental_revenue_kusd", "sum"),
                                     ratio=("modeled_incrementality_ratio", "mean")).reset_index()
    rmg = rmg.sort_values("spend", ascending=False)
    rrows = [[r.platform, f"${r.spend/1000:.1f}M", f"${r.inc/1000:.2f}M", f"{r.ratio:.2f}",
              "Reinvest" if r.ratio >= 1 else "Reallocate"] for r in rmg.itertuples()]
    tot_sp = rmg.spend.sum() / 1000; tot_inc = rmg.inc.sum() / 1000
    rrows.append(["Total retail media", f"${tot_sp:.1f}M", f"${tot_inc:.2f}M",
                  f"{tot_inc/tot_sp:.2f}", "Rebalance H2"])
    d.h2("Retail-media incrementality — Q1 FY2026")
    d.table(["Platform", "Spend", "Incremental", "Incr. ratio", "Call"], rrows,
            widths=[0.34, 0.16, 0.18, 0.16, 0.16], total_row=True)
    d.body(
        "The CFO's question — “is the working-media dollar working?” — has a clear Q1 answer: Walmart Connect "
        "(1.20) and Kroger Precision (0.77) carry the portfolio; Amazon Ads (0.40) is the drag. The blended "
        "$0.65-per-$1 return funds a proposed H2 reallocation out of Amazon and into Walmart/Kroger and the "
        "Louisiana recovery, detailed in the CFO effectiveness read (Report 40 / 05).")
    d.source("retail_media_spend_q1_2026, trade_promo_events_q1_2026, sku_elasticity_estimates.")

    d.h1("5 · Risks & the Q2 ask")
    d.callout("Watch-items into Q2",
              "(1) ProteinPeak launch execution at Walmart-pilot, tracking behind Target. "
              "(2) Field & Honey's 14g-protein line extension (LCH00032, May 12) escalates the LA and protein "
              "fronts simultaneously. (3) Retail-media efficiency must improve before H2 budget is committed.", "risk")
    d.recommendations([
        ("Fund and launch the Crunchwell Louisiana three-leg recovery (facings, trade, LA retail media at 2.2× ROI).",
         "Marcus Boudreaux", "Q2 — now"),
        ("Protect the ProteinPeak launch: close the Walmart-pilot execution gap; hold Target momentum.",
         "Maya Chen / Sage Park", "Wk 4–12"),
        ("Reallocate H2 retail media out of Amazon Ads into Walmart Connect, Kroger, and LA.",
         "Tasha Brooks", "H2 planning"),
        ("Hold the FY26 number: reaffirm $80M ProteinPeak target contingent on Week-8 read.",
         "Finance / Diane Halverson", "May MBR"),
    ])
    return d.build()


def r12_company_q2_qbr():
    d = Doc("12-acme-q2-2026-company-business-review.pdf",
            kicker="QUARTERLY BUSINESS REVIEW",
            title="Acme Corp — Q2 FY2026 Company Business Review",
            subtitle="Enterprise performance, quarter-to-date through May 2026",
            owner="Diane Halverson, VP Sales NA (sponsor); Finance & Insights (prep)",
            period="Q2 FY2026 QTD (Apr–May 2026)", short="Q2 2026 Company BR",
            doc_type="Internal quarterly business review", date_str="June 2026")

    p, a = _qsum(["2026-04", "2026-05"])
    var = (a - p) / p * 100
    ph, ah = _qsum(["2026-01", "2026-02", "2026-03", "2026-04", "2026-05"])
    varh = (ah - ph) / ph * 100
    d.cover_facts([
        ("Net revenue vs plan (Q2 QTD)", f"{money(a)} vs {money(p)} plan · {var:+.1f}%"),
        ("Improvement vs Q1", "gap narrowed from −5.3% to −3.4%"),
        ("The win", "ProteinPeak launch — trial 110% of plan at Target"),
        ("Still open", "Crunchwell Louisiana; Walmart-pilot protein"),
        ("New threat", "Field & Honey 14g protein (LCH00032, May 12)"),
    ])

    d.exec_summary(
        "The quarter is turning. Q2-to-date net revenue is " + money(a) + f" against {money(p)} plan "
        f"({var:+.1f}%) — a clear improvement on Q1's −5.3%, driven by the ProteinPeak relaunch landing "
        "ahead of plan at Target and the Crunchwell Louisiana bleed beginning to stabilize. The base is "
        "intact, the innovation is working, and the H1 exit rate supports holding the FY26 number.",
        bullets=[
            f"<b>The number:</b> Q2 QTD {money(a)} vs {money(p)} plan ({var:+.1f}%); H1 {money(ah)} vs "
            f"{money(ph)} plan ({varh:+.1f}%). The trajectory is the story — each month closer to plan.",
            "<b>ProteinPeak is delivering:</b> Cinnamon Crunch and Cocoa Almond drove the line from −25% (Q1, "
            "pre-launch) to −6% post-launch; trial hit 110% of plan at Target, source-of-volume is 53% "
            "new-to-brand. The $48M→$80M FY26 build is on track.",
            "<b>Crunchwell Louisiana is stabilizing:</b> local share ticked from 3.97% (Q1) to 4.16% (Q2) as "
            "the recovery plan engages — early, not yet won.",
            "<b>Watch:</b> Walmart-pilot protein still soft (5.2% Acme share vs 18.4% at Target), and Field & "
            "Honey's 14g-protein extension escalates two fronts at once.",
        ])

    d.h1("1 · Enterprise scorecard")
    d.kpis([
        ("Net rev (Q2 QTD)", money(a), f"{var:+.1f}% vs plan"),
        ("H1 gap", f"{varh:+.1f}%", "narrowing"),
        ("ProteinPeak", "+$1.1M/mo", "vs Q1 run-rate"),
        ("Crunchwell LA share", "4.16%", "up from 3.97%"),
        ("PP social sentiment", "+0.44", "on 496 mentions"),
    ])

    bd = df("""SELECT Brand,
                 ROUND(SUM(Plan_Revenue_USD)/1e6,1) plan, ROUND(SUM(Actual_Revenue_USD)/1e6,1) act,
                 ROUND((SUM(Actual_Revenue_USD)-SUM(Plan_Revenue_USD))/SUM(Plan_Revenue_USD)*100,1) var
               FROM plan_vs_actual WHERE Period IN ('2026-04','2026-05') GROUP BY 1 ORDER BY plan DESC""")
    rows = [[r.Brand, f"${r.plan:,.1f}M", f"${r.act:,.1f}M", f"{r.var:+.1f}%",
             "On track" if r.var > -3 else ("Improving" if r.Brand == "ProteinPeak" else "Watch")]
            for r in bd.itertuples()]
    rows.append(["Total Acme", f"${p:,.1f}M", f"${a:,.1f}M", f"{var:+.1f}%", "Improving"])
    d.h2("Brand net revenue vs plan — Q2 QTD (Apr–May)")
    d.table(["Brand", "Plan", "Actual", "Var %", "Status"], rows,
            widths=[0.30, 0.18, 0.18, 0.16, 0.18], total_row=True)
    d.source("plan_vs_actual, Apr–May 2026.")

    # trajectory chart Jan-May
    tr = df("""SELECT Period, ROUND((SUM(Actual_Revenue_USD)-SUM(Plan_Revenue_USD))/SUM(Plan_Revenue_USD)*100,1) v
               FROM plan_vs_actual WHERE Period BETWEEN '2026-01' AND '2026-05' GROUP BY 1 ORDER BY 1""")
    ch = chart_line("r12_traj.png", [x[5:] for x in tr.Period],
                    {"Variance to plan (%)": [float(v) for v in tr.v]},
                    title="Company variance to plan is narrowing (monthly, %)", h=2.7)
    d.image(ch, "The gap to plan closed from −5.2% in January to −3.4% in May as the ProteinPeak launch pipe filled.")

    d.pagebreak()
    d.h1("2 · The ProteinPeak launch is the quarter's win")
    d.body(
        "ProteinPeak's April 20 relaunch of Cinnamon Crunch (PP005) and Cocoa Almond (PP006) is doing what the "
        "FY26 plan needed it to do. Trial ran 110% of plan at Target and 77% at the Walmart pilot; velocity is "
        "17.5 units/store/week at Target vs 9.2 at Walmart. Repeat in week two is ~1.2× the Berry Crunch "
        "benchmark, and source-of-volume is a healthy 53% new-to-brand / 32% cannibalization / 15% competitive "
        "switch. Social sentiment sits at +0.44 on ~496 mentions. The read: demand is real and the brand is "
        "accretive to the category, not just to itself.")
    sov = df("""SELECT Switching_Flag f, COUNT(*) n FROM household_transactions
               WHERE Product_SKU IN ('PP005','PP006') AND Switching_Flag<>'No' GROUP BY 1""")
    lab = {"New_To_Brand": "New to brand", "Cannibalization": "Cannibalization", "Competitor_Switch": "Competitor switch"}
    ch2 = chart_donut("r12_sov.png", [lab.get(x, x) for x in sov.f], list(sov.n),
                      title="ProteinPeak source of volume")
    d.image(ch2, "Source of volume, PP005+PP006 (household panel). More than half is genuinely new demand.", width=4.6)

    d.h1("3 · The base held; two fronts remain open")
    d.h2("3.1 · Crunchwell Louisiana — stabilizing, not recovered")
    d.body(
        "Louisiana Crunchwell share moved from 3.97% (Q1) to 4.16% (Q2) as the three-leg recovery — facing "
        "recovery, targeted trade, and a LA retail-media injection at 2.2× portfolio ROI — began to engage. "
        "This is an early inflection, not a win; the full read is in the South Region review (Report 39) and "
        "the turnaround plan (Report 24).")
    d.h2("3.2 · The competitive step-up")
    d.callout("Field & Honey escalates",
              "Larksfield's Field & Honey launched a 14g-protein line extension (LCH00032) on May 12, pushing "
              "into ProteinPeak's segment while it continues to press Crunchwell in the South. For the first "
              "time we face the same competitor on both the protein and the family-sweet fronts. Response is "
              "coordinated across the ProteinPeak plan (23) and the Crunchwell turnaround (24).", "risk")

    d.h1("4 · Priorities into the back half")
    d.recommendations([
        ("Scale the ProteinPeak launch nationally; close the Walmart-pilot execution and protein-share gap.",
         "Sage Park / Marcus Boudreaux", "Q3"),
        ("Sustain the Louisiana inflection; hold facings and trade through the Pack Refresh launch (Aug 15).",
         "Marcus Boudreaux", "Q3"),
        ("Stand up the coordinated Field & Honey response across protein and family-sweet.",
         "Cory Whitman / Sage Park", "Q3"),
        ("Confirm the FY26 landing in the H2 reforecast; hold the $80M ProteinPeak target.",
         "Finance", "June MBR"),
    ])
    return d.build()


def r13_ceo_board_review():
    d = Doc("13-acme-h1-2026-ceo-board-review.pdf",
            kicker="BOARD OF DIRECTORS · H1 FY2026",
            title="Acme Corp — CEO Half-Year Business Review",
            subtitle="Enterprise performance, strategy, and outlook for the Board",
            owner="Gregory Whitfield, CEO", period="H1 FY2026 (Jan–Jun 2026)",
            short="CEO Board Review H1", doc_type="Board review", date_str="July 2026")

    ph, ah = _qsum(["2026-01", "2026-02", "2026-03", "2026-04", "2026-05"])
    varh = (ah - ph) / ph * 100
    d.cover_facts([
        ("FY25 net revenue", "$812M (+5.1% YoY)"),
        ("EBITDA margin", "14.2% · target 16% by FY28"),
        ("H1 FY26 vs plan", f"{money(ah)} vs {money(ph)} · {varh:+.1f}% (improving)"),
        ("Strategic thesis", "Win protein · fix Crunchwell relevance · ride oat milk"),
        ("The bet landing now", "ProteinPeak launch on plan; Pack Refresh ships Aug 15"),
    ])

    d.exec_summary(
        "Acme enters the second half of FY2026 behind plan but with momentum and a clear strategic hand. The "
        f"H1 shortfall ({varh:+.1f}% to plan) is concentrated in two managed situations — Crunchwell's Louisiana "
        "erosion and a deliberate pre-launch trough in ProteinPeak — not in a broad demand failure. The "
        "ProteinPeak relaunch is landing on plan, the category's fastest-growing pockets (protein, oat milk) are "
        "where we are investing, and the flagship's issue is diagnosed as relevance, not trust — a fixable, "
        "brand-building problem. The FY28 16%-margin commitment remains intact.",
        bullets=[
            "<b>Performance:</b> H1 net revenue behind plan but the monthly gap halved (−5.2% Jan → −3.4% May). "
            "Four of six brands are within 2 points of plan.",
            "<b>Franchise health:</b> national RTE share stable (Acme 7.9%, Crunchwell 6.0%); the risks are "
            "regional (Louisiana) and segment-shaped (under-indexed in protein), both addressed in-plan.",
            "<b>Strategy on track:</b> ProteinPeak $48M→$80M FY26 build delivering; Crunchwell Pack Refresh "
            "($28M) ships Aug 15; RootDay rides oat milk (+18.8%).",
            "<b>Ask of the Board:</b> endorse the FY27–FY29 long-range plan (Report 15) and the FY27 AOP "
            "(Report 14), including the margin path to 16%.",
        ])

    d.h1("1 · Where the business stands")
    d.kpis([
        ("FY25 net revenue", "$812M", "+5.1% YoY"),
        ("EBITDA margin", "14.2%", "→ 16% by FY28"),
        ("H1 vs plan", f"{varh:+.1f}%", "gap halving"),
        ("RTE share (natl)", "7.9%", "stable"),
        ("#4", "US RTE cereal", "behind GM, Kellanova, Larksfield"),
    ])
    d.body(
        "Acme is a $812M, six-brand cereal-and-adjacencies company, #4 in US RTE cereal. The portfolio spans a "
        "large, slow-growing core (Crunchwell family sweet), two fast adjacencies we are leaning into "
        "(ProteinPeak in wellness protein, RootDay in oat milk), and a stable middle (TrailGrove, MorningOats, "
        "HoneyNest). The half's financial gap is real but improving and well-understood.")

    # brand mix chart
    bm = df("SELECT brand, SUM(fy25_revenue_musd) rev FROM read_csv_auto('seeds/skus.csv') GROUP BY 1 ORDER BY rev DESC")
    ch = chart_bar("r13_portfolio.png", list(bm.brand), [round(x, 0) for x in bm.rev],
                   title="Portfolio by FY25 net revenue ($M)", color="navy", horizontal=True,
                   unit="", h=2.7)
    d.image(ch, "Crunchwell is 38% of revenue; the growth is being funded from the fast adjacencies.")

    d.h2("Financial summary")
    d.table(
        ["Metric", "FY25 actual", "H1 FY26", "FY27 target"],
        [["Net revenue", "$812M", f"{money(ah)} (−4.5% to plan)", "~$880M (planning)"],
         ["YoY growth", "+5.1%", "improving through H1", "~+7% (planning)"],
         ["EBITDA margin", "14.2%", "on track", "~15.0% → 16% FY28"],
         ["RTE share (national)", "7.9%", "7.9% (stable)", "hold / build in protein"],
         ["Wellness Protein share", "7.6%", "8.4% (Q2)", "grow (ProteinPeak)"]],
        widths=[0.30, 0.22, 0.26, 0.22])
    d.source("FY25 headline; H1 FY26 from plan_vs_actual; FY27 figures are planning targets (see Reports 14, 15).")

    d.h1("2 · The strategic thesis")
    d.body(
        "Our three-part thesis is unchanged and is where the FY27–FY29 plan concentrates capital:")
    d.bullets([
        "<b>Win Wellness Protein.</b> The category's fastest pocket (+18.3%, now $840M). ProteinPeak is our "
        "vehicle; the Q2 launch proves the demand. Target already gives us 18.4% segment share.",
        "<b>Fix Crunchwell relevance.</b> Brand equity shows relevance down 5.9 points over six quarters while "
        "trust holds — a brand-building problem, not a quality problem. The Pack Refresh, Hispanic format, and "
        "a modern brand program answer it.",
        "<b>Ride oat milk with RootDay.</b> The oat-milk adjacency grows +18.8%; RootDay is on plan and "
        "under-scaled relative to the opportunity.",
    ])

    d.h1("3 · The two H1 problems, and what we are doing")
    d.body(
        "<b>Crunchwell Louisiana (−340 bps of local share)</b> is attributed across five hypotheses — a Walmart "
        "reset, Larksfield promo intensity, a hurricane supply shock, private label, and a shopper-mix shift — "
        "and is now stabilizing under a funded recovery. <b>ProteinPeak's −25% Q1</b> was a planned pre-launch "
        "draw-down; post-launch it runs −6% and improving. Neither is a surprise, and both are inside the plan.")

    d.h1("4 · Capital allocation")
    d.body(
        "Capital and working investment follow the thesis, not history. Three principles govern FY27 planning:")
    d.bullets([
        "<b>Fund the fast pockets.</b> Protein and oat-milk innovation and working media are protected; "
        "A&P tilts from Crunchwell linear TV toward protein, creator, and proven retail media.",
        "<b>Earn the trade dollar.</b> The ~$150M trade envelope is held but rebalanced toward incrementality "
        "(portfolio index ~0.52 today); low-return Crunchwell events are the funding source.",
        "<b>Protect the core selectively.</b> The Crunchwell Pack Refresh ($28M innovation) and Louisiana "
        "recovery are funded; the HoneyNest tail is pruned to release margin.",
    ])

    d.h1("5 · Outlook, and the Board ask")
    d.callout("Risks we are watching",
              "GLP-1 / appetite-suppressant adoption (a slow structural drag on breakfast volume), private-label "
              "strength at Walmart and Kroger, and Larksfield/Field & Honey escalating into protein. None change "
              "the thesis; all are reflected in the FY27–FY29 targets.", "risk")
    d.body(
        "We expect to land FY26 close to plan on the strength of the ProteinPeak ramp and the Aug 15 Crunchwell "
        "Pack Refresh (H2 reforecast in Report 40). The FY27–FY29 plan commits to ~7–8% net-revenue growth and "
        "the 16% EBITDA margin by FY28, funded by revenue growth management and mix.")
    d.recommendations([
        ("Endorse the FY27–FY29 long-range plan and its growth/margin commitments.",
         "Board", "This session"),
        ("Approve the FY27 Annual Operating Plan and trade/A&P envelopes.",
         "Board / CFO", "This session"),
        ("Note the ProteinPeak and Crunchwell strategic plans as the two priority bets.",
         "Board", "This session"),
    ])
    return d.build()


def r14_fy27_aop():
    d = Doc("14-acme-fy27-annual-operating-plan.pdf",
            kicker="ANNUAL OPERATING PLAN · FY2027",
            title="Acme Corp — FY2027 Annual Operating Plan",
            subtitle="Top-down targets, bottom-up brand build, and investment envelopes",
            owner="CFO office; Corporate FP&A; Brand & Sales leads",
            period="FY2027 (planning)", short="FY27 AOP",
            doc_type="Annual operating plan", date_str="Built H2 FY2026")

    d.cover_facts([
        ("FY25 net revenue (actual)", "$812M (+5.1%)"),
        ("FY27 net revenue target", "~$880M (planning · +~7% on FY25)"),
        ("EBITDA margin path", "14.2% → 15.0% FY27 → 16% FY28"),
        ("Trade envelope", "~$150M (rationalized toward incrementality)"),
        ("A&P envelope", "~$95M (shift to protein & digital)"),
    ])
    d.body("<i>All FY27 figures on this page and throughout are planning targets, not measured actuals.</i>")

    d.exec_summary(
        "The FY2027 Annual Operating Plan sets a ~$880M net-revenue target (planning) — roughly +7% on the FY25 "
        "$812M base — and starts the margin climb to the 16%-by-FY28 commitment. The plan is built top-down from "
        "the growth thesis (protein, oat milk, Crunchwell stabilization) and bottom-up from each brand, funded by "
        "a rationalized trade envelope and an A&P mix that shifts toward the pockets that are actually growing.",
        bullets=[
            "<b>Top line:</b> ~$880M net revenue (planning), led by ProteinPeak (~$100M) and a stabilized "
            "Crunchwell (~$318M).",
            "<b>Margin:</b> EBITDA to ~15.0% in FY27 en route to 16% in FY28, via revenue growth management and "
            "trade efficiency, not volume-chasing.",
            "<b>Trade:</b> hold the envelope near $150M but shift dollars from low-incrementality Crunchwell "
            "events (0.57) toward higher-return mechanics (Report 27 / 17).",
            "<b>A&P:</b> ~$95M, tilting from Crunchwell linear TV toward protein, creator, and retail media "
            "where incrementality is proven.",
        ])

    d.h1("1 · Top-down targets")
    d.kpis([
        ("Net revenue", "~$880M", "planning target"),
        ("Growth", "+~7%", "on FY25 base"),
        ("EBITDA margin", "~15.0%", "→ 16% FY28"),
        ("Trade", "~$150M", "rationalized"),
        ("A&P", "~$95M", "mix shift"),
    ])
    d.body(
        "Leadership's FY27 North Star: grow net revenue mid-single-digits while beginning the margin expansion. "
        "The number is deliberately not built on the slow core alone — it requires the protein and oat-milk "
        "adjacencies to carry disproportionate growth while Crunchwell stops the bleeding.")

    d.h1("2 · Bottom-up brand build")
    # FY25 base + FY27 planning targets
    base = df("SELECT brand, ROUND(SUM(fy25_revenue_musd),0) rev FROM read_csv_auto('seeds/skus.csv') GROUP BY 1")
    fy25 = {r.brand: r.rev for r in base.itertuples()}
    fy27 = {"Crunchwell": 318, "TrailGrove": 162, "MorningOats": 92, "HoneyNest": 92,
            "RootDay": 74, "ProteinPeak": 100}
    order = ["Crunchwell", "ProteinPeak", "TrailGrove", "MorningOats", "HoneyNest", "RootDay"]
    roles = {"Crunchwell": "Stabilize / fix relevance", "ProteinPeak": "Grow aggressively",
             "TrailGrove": "Grow steadily", "MorningOats": "Grow single-serve", "HoneyNest": "Defend / prune",
             "RootDay": "Ride oat milk"}
    rows = []
    for b in order:
        f25 = fy25.get(b, 0); f27 = fy27[b]
        g = (f27 - f25) / f25 * 100
        rows.append([b, f"${f25:,.0f}M", f"${f27:,.0f}M", f"{g:+.0f}%", roles[b]])
    tot25 = sum(fy25.get(b, 0) for b in order); tot27 = sum(fy27.values())
    rows.append(["Six brands", f"${tot25:,.0f}M", f"${tot27:,.0f}M",
                 f"{(tot27-tot25)/tot25*100:+.0f}%", "+ adjacencies to ~$880M"])
    d.table(["Brand", "FY25 actual", "FY27 target", "Growth", "Portfolio role"], rows,
            widths=[0.20, 0.17, 0.17, 0.13, 0.33], total_row=True)
    d.source("FY25 from seeds/skus.csv; FY27 figures are planning targets. Total reconciles to ~$880M with non-brand/adjacency revenue.")
    ch = chart_grouped("r14_build.png", order,
                       {"FY25 actual": [fy25.get(b, 0) for b in order],
                        "FY27 target": [fy27[b] for b in order]},
                       title="Brand net revenue: FY25 actual vs FY27 target ($M)", h=3.0)
    d.image(ch, "The growth is loaded onto ProteinPeak (+108%) and protected on Crunchwell; the middle holds.")

    d.pagebreak()
    d.h1("3 · Investment envelopes")
    d.h2("3.1 · Trade (~$150M)")
    d.body(
        "FY25 trade was ~$146M, with Crunchwell alone at $92M and a portfolio incrementality index of ~0.52. "
        "FY27 holds the envelope near $150M but rebalances it toward incrementality: fewer deep, "
        "forward-buy-heavy Crunchwell events, more high-return mechanics and protein support. The revenue "
        "growth management plan (Report 17) and the trade post-event analysis (Report 27) drive the reallocation.")
    d.h2("3.2 · A&P / working media (~$95M)")
    d.body(
        "A&P shifts with the growth. Crunchwell's linear-TV weight comes down at the margin; protein, creator, "
        "and retail-media investment goes up where incrementality is proven (Walmart Connect 1.20, Kroger 0.77) "
        "and away from where it is not (Amazon Ads 0.40). The media effectiveness review (Report 28) is the basis.")

    d.h1("4 · Assumptions, phasing & risks")
    d.bullets([
        "<b>Phasing:</b> H1-weighted innovation (Crunchwell Pack Refresh carrying from Aug 2026; ProteinPeak "
        "Chocolate Almond in Q3 FY26); protein and BTS programs front-loaded.",
        "<b>Category assumptions:</b> RTE +1–1.5%, Wellness Protein +15–18%, oat milk +15%+, Kids Sweet −2–3%.",
        "<b>Macro risk:</b> GLP-1 appetite shift as a slow volume drag; private-label strength; commodity/input "
        "cost on the margin path.",
        "<b>Competitive risk:</b> Field & Honey pressing both protein and family-sweet.",
    ])
    d.callout("Plan integrity",
              "The FY27 AOP is the one-year expression of the FY27–FY29 long-range plan (Report 15). It is "
              "consistent with the H2 FY26 reforecast (Report 40) and the brand-level annual plans (Reports "
              "18–24). Trade and A&P envelopes are directional planning numbers pending final board approval.", "info")
    d.recommendations([
        ("Approve the ~$880M net-revenue target and ~15.0% EBITDA margin for FY27.", "Board / CFO", "AOP sign-off"),
        ("Lock the trade (~$150M) and A&P (~$95M) envelopes with the rationalization rules.", "CFO / RGM", "AOP sign-off"),
        ("Cascade brand targets into the FY27 brand plans and retailer JBPs (Reports 35–38).", "Sales / Brand", "Q3 FY26"),
    ])
    return d.build()


if __name__ == "__main__":
    for fn in (r11_company_q1_qbr, r12_company_q2_qbr, r13_ceo_board_review, r14_fy27_aop):
        print(fn())
