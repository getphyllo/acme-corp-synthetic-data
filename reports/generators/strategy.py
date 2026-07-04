"""Corporate strategy reports (15-17). Run: python generators/strategy.py

15 — Long-Range Strategic Plan FY27–FY29 (Whitfield / Corporate Strategy)
16 — H2 FY26 Operating Plan & Reforecast (Finance / Halverson)
17 — Revenue Growth Management (NRM) & Pricing Architecture (RGM Lead / CFO office)

Every headline number traces to FACTS.md, acme.duckdb, or a seed CSV. FY27+ and
next-two-quarter figures are planning targets and are labelled as such in-document.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import (Doc, df, seed_csv, money, chart_line, chart_bar, chart_grouped,
                 chart_stacked, chart_waterfall, chart_donut)


def _qsum(periods):
    ps = ",".join(f"'{p}'" for p in periods)
    r = df(f"SELECT SUM(Plan_Revenue_USD)/1e6 p, SUM(Actual_Revenue_USD)/1e6 a "
           f"FROM plan_vs_actual WHERE Period IN ({ps})").iloc[0]
    return float(r.p), float(r.a)


# ============================================================== REPORT 15 ====
def r15_long_range_plan():
    d = Doc("15-acme-fy27-fy29-long-range-strategic-plan.pdf",
            kicker="LONG-RANGE PLAN · FY27–FY29",
            title="Acme Corp — Long-Range Strategic Plan, FY27–FY29",
            subtitle="A three-year plan to grow to ~$1B and lift EBITDA margin to 16%",
            owner="Gregory Whitfield, CEO; Corporate Strategy & Finance",
            period="FY27–FY29", short="LRP FY27–29",
            doc_type="Board-level strategic plan", date_str="July 2026")

    d.cover_facts([
        ("Starting point (FY25)", "$812M net revenue, +5.1% · EBITDA 14.2%"),
        ("Net-revenue target", "~$880M FY27 → ~$950M FY28 → ~$1.02B FY29"),
        ("Implied CAGR (target)", "~7–8% off FY25 base"),
        ("EBITDA-margin target", "14.2% → 16.0% by FY28"),
        ("Where we win", "Wellness Protein · oat milk · RGM · eCommerce"),
        ("Where we're exposed", "GLP-1 volume, private label, Larksfield in the South"),
    ])

    d.exec_summary(
        "Acme enters the plan period as the #4 US ready-to-eat cereal maker with a $812M, +5.1% FY25 "
        "and a franchise that is stable nationally but under pressure in two specific places — Crunchwell's "
        "relevance and its Louisiana share. The three-year job is not a turnaround; it is a mix shift. We grow "
        "the company to roughly $1.02B by FY29 by leaning into the two fastest pockets we already play in "
        "(Wellness Protein and oat milk), fixing Crunchwell's relevance rather than its trust, and converting "
        "commercial rigour — revenue growth management and retail-media discipline — into margin. Every "
        "revenue and margin figure past FY26 in this document is a <b>planning target</b>, not a forecast of "
        "measured results.",
        bullets=[
            "<b>The commitment:</b> net revenue to ~$880M (FY27), ~$950M (FY28) and ~$1.02B (FY29) — a "
            "~7–8% CAGR off the $812M FY25 base — with EBITDA margin lifting from 14.2% to 16.0% by FY28.",
            "<b>Five growth pillars</b> carry the plan: win Wellness Protein (ProteinPeak $48M→~$140M by FY29, "
            "target), fix Crunchwell relevance (68.6→62.7 and falling), ride oat milk with RootDay (+18.8% "
            "category), monetise the portfolio through revenue growth management, and scale eCommerce and "
            "retail media.",
            "<b>Portfolio roles are explicit:</b> grow ProteinPeak and RootDay, maintain TrailGrove and "
            "MorningOats, fix Crunchwell, and prune the HoneyNest tail in a structurally declining "
            "Kids-Sweet segment (−2.8%).",
            "<b>The risks are named and sized:</b> the GLP-1 appetite shift (0.81 strength, volume-down), "
            "private-label pressure, and Larksfield's escalation of the protein and Louisiana fronts. The "
            "plan funds against each rather than assuming them away.",
        ])

    # ---- 1 · Where we are
    d.h1("1 · Where we are")
    p_q1, a_q1 = _qsum(["2026-01", "2026-02", "2026-03"])
    var_q1 = (a_q1 - p_q1) / p_q1 * 100
    d.kpis([
        ("FY25 net revenue", "$812M", "+5.1% YoY"),
        ("EBITDA margin", "14.2%", "target 16% by FY28"),
        ("US RTE share", "5.7%", "#4 nationally"),
        ("Q1 FY26 vs plan", f"{var_q1:+.1f}%", "trajectory improving"),
        ("Fastest pocket", "+18.3%", "Wellness Protein"),
    ])
    d.body(
        "FY25 closed at $812M net revenue, up 5.1%, at a 14.2% EBITDA margin — a healthy base, but one built "
        "on a portfolio whose centre of gravity (Crunchwell, Family Sweet) grows at category rate (~1.4%) "
        "while the pockets we most want to own grow at ten times that. The near-term reads amber: Q1 FY26 "
        f"landed {var_q1:.1f}% behind plan ({money(a_q1)} vs {money(p_q1)}), concentrated in Crunchwell's "
        "Louisiana erosion and a deliberate ProteinPeak pre-launch draw-down. Neither is a national franchise "
        "problem, and both are actively managed (see the Q1 Company Business Review, Report 11). The strategic "
        "question this plan answers is not “how do we stop the bleeding” — it is “where do we "
        "put the next three years of investment so the company compounds.”")
    d.callout("The one-line diagnosis",
              "Acme is a trusted, slow-growth portfolio sitting next to two fast-growth pockets it already "
              "competes in. The plan is a deliberate mix shift toward Wellness Protein and oat milk, funded by "
              "commercial discipline on the mature core — not a bet on reviving a declining segment.", "info")

    # ---- 2 · Three-year financial commitments
    d.h1("2 · Three-year financial commitments (planning targets)")
    d.body(
        "The financial frame below is the Board-level commitment for the plan period. FY25 and FY26 anchor to "
        "actuals and the current-year plan; FY27–FY29 are <b>planning targets</b>. The shape is deliberate: "
        "revenue growth accelerates as the ProteinPeak build compounds and the Crunchwell turnaround stabilises "
        "the core, while margin expands ahead of revenue as revenue growth management and media discipline "
        "convert to gross profit.")
    fin_rows = [
        ["FY25 (actual)", "$812M", "+5.1%", "14.2%", "Base year"],
        ["FY26 (plan)", "~$764M*", "run-rate", "~14%", "Reset year; hold on ProteinPeak launch"],
        ["FY27 (target)", "~$880M", "~+8%", "~15%", "Protein + RGM inflect"],
        ["FY28 (target)", "~$950M", "~+8%", "16.0%", "Margin commitment year"],
        ["FY29 (target)", "~$1.02B", "~+7%", "16%+", "Cross the $1B line"],
    ]
    d.h2("2.1 · Revenue and margin commitment")
    d.table(["Fiscal year", "Net revenue", "Growth", "EBITDA margin", "Role in the plan"], fin_rows,
            widths=[0.18, 0.16, 0.13, 0.16, 0.37])
    d.source("FY25 net revenue & EBITDA per FACTS.md; FY26 run-rate = $63.7M/mo plan basis "
             "(plan_vs_actual). *FY26 shown at annualised plan run-rate; FY27–FY29 are planning targets.")

    traj = chart_line(
        "r15_revenue_trajectory.png",
        ["FY25", "FY26", "FY27", "FY28", "FY29"],
        {"Net revenue ($M) — actual then target": [812, 764, 880, 950, 1020]},
        title="Net-revenue trajectory: FY25 actual → FY29 target ($M)", h=2.9)
    d.image(traj, "FY25 actual and FY26 plan run-rate; FY27–FY29 are planning targets, ~7–8% CAGR to ~$1.02B.")

    d.callout("What the margin commitment requires",
              "Lifting EBITDA margin ~180 bps to 16% by FY28 is roughly $17M of structural profit on the FY28 "
              "revenue base. About half is planned to come from revenue growth management (pricing, mix, trade "
              "efficiency — see Report 17) and half from mix shift into higher-margin Wellness Protein and "
              "premium oat milk. It is a commitment underwritten by named levers, not by cost-out alone.", "info")

    # ---- 3 · Five growth pillars
    d.pagebreak()
    d.h1("3 · The five growth pillars")
    d.body(
        "The plan resolves to five pillars. The first three are where growth comes from; the last two are how "
        "we fund and deliver it. Each pillar has an owner, a measurable target, and a linked operating plan.")

    d.h2("3.1 · Win Wellness Protein (ProteinPeak)")
    d.body(
        "Wellness Protein is the category's fastest pocket — $710M (FY24) to $840M (FY25), +18.3%, and running "
        "+18.6% in the Q2 FY26 read — and it is where Acme is gaining share (7.1% → 7.6% → 8.4%). ProteinPeak "
        "is the engine: $48M in FY25 (+24.6%), building to ~$80M in FY26 on the April Cinnamon Crunch / Cocoa "
        "Almond launch, and to <b>~$140M by FY29 (target)</b> on a rolling innovation cadence and mass-channel "
        "expansion beyond the Target stronghold (Acme holds 18.4% Wellness-Protein share at Target vs 5.2% at "
        "Walmart). The detailed roadmap sits in the ProteinPeak plan, Report 23.")
    d.h2("3.2 · Fix Crunchwell relevance")
    d.body(
        "Crunchwell is trusted but drifting. Top-two-box Relevance has fallen from 68.6 (FY25Q1) to 62.7 "
        "(FY26Q2), −5.9 points, while Trust holds (72.3 → 72.9). This is a relevance problem, not a trust "
        "problem — the brand is respected but losing cultural pull, most acutely in Louisiana (−340 bps of "
        "local share). The fix is the August Pack Refresh ($28M year-one innovation, launch 2026-08-15) plus "
        "the funded Louisiana recovery; the full turnaround plan is Report 24.")
    d.h2("3.3 · Ride oat milk (RootDay)")
    d.body(
        "Oat milk (Plant-Based) is a $1.64B, +18.8% category where RootDay is a small but fast-growing player "
        "(FY25 ~$62M). The plan protects and extends RootDay's position in a structurally-growing space, with "
        "innovation (single-serve, coffee-creamer adjacencies) staged behind the protein build.")
    d.h2("3.4 · Revenue growth management & margin")
    d.body(
        "The margin commitment runs through revenue growth management: pricing architecture, promotion "
        "efficiency, price-pack architecture, trade terms, and mix. Crunchwell's trade rate (~25.6% of gross, "
        "0.57 incrementality) and the blended $0.65-per-$1 retail-media return are the two largest efficiency "
        "prizes. The lever-by-lever plan and the quantified prize are in Report 17.")
    d.h2("3.5 · eCommerce & retail media")
    d.body(
        "eCommerce and retail media are the fastest-growing route to shopper. The FY27–FY29 plan scales the "
        "channels that pay back — Walmart Connect (1.20 incrementality) and Kroger Precision (0.77) — and "
        "structurally de-weights the Amazon-Ads drag (0.40), reinvesting the freed dollars into the pockets "
        "and geographies with the highest marginal ROI.")

    seg = chart_bar(
        "r15_segment_growth.png",
        ["Wellness\nProtein", "Oat milk\n(Plant-Based)", "Granola", "Family\nSweet", "Kids\nSweet"],
        [18.3, 18.8, 3.3, 1.4, -2.8],
        title="Category growth by segment where Acme plays (FY25 YoY, %)", pct=True,
        colors_list=["#2E7D75", "#2E7D75", "#2E7D5B", "#B98A2E", "#B24A2E"], h=2.7)
    d.image(seg, "The plan tilts investment toward the two +18% pockets and away from the −2.8% Kids-Sweet tail.")
    d.source("seed_category_market_size (NielsenIQ-shape), FY25 US National.")

    # ---- 4 · Portfolio roles
    d.h1("4 · Portfolio roles: grow, maintain, fix, prune")
    d.body(
        "Not every brand gets the same mandate or the same money. The plan assigns each brand an explicit role "
        "so investment follows strategy rather than history. FY25 revenue is actual; FY29 direction is the "
        "planning intent, not a per-brand forecast.")
    port_rows = [
        ["ProteinPeak", "$48M", "GROW", "Wellness Protein +18%; Acme gaining share", "Fund the build to ~$140M (target)"],
        ["RootDay", "$62M", "GROW", "Oat milk +18.8%; small but fast", "Protect + extend in a growing space"],
        ["TrailGrove", "$152M", "MAINTAIN", "Granola +3.3%; healthy, stable", "Hold share, self-funding"],
        ["MorningOats", "$87–98M", "MAINTAIN", "Hot cereal flat; cups +9.8%", "Tilt to single-serve growth"],
        ["Crunchwell", "$312M", "FIX", "Relevance 68.6→62.7; LA −340 bps", "Pack Refresh + LA recovery (Report 24)"],
        ["HoneyNest", "$94M", "PRUNE", "Kids Sweet −2.8%, structural decline", "Prune tail SKUs; harvest for cash"],
    ]
    d.table(["Brand", "FY25 rev", "Role", "Why", "FY27–29 mandate"], port_rows,
            widths=[0.15, 0.11, 0.12, 0.31, 0.31], align=["LEFT", "RIGHT", "CENTER", "LEFT", "LEFT"])
    d.source("seeds/skus.csv (FY25 brand revenue); seed_category_market_size; brand_equity_quarterly.")
    d.callout("The prune decision, stated plainly",
              "HoneyNest sits in Kids Sweet, a segment shrinking −2.8% a year against a rising “mom-guilt” "
              "trend (0.68 strength, volume-down). The plan does not reinvest to defend the whole line; it prunes "
              "the tail SKUs, keeps the profitable core plus LTO calendar, and redirects the freed shelf and cash "
              "toward Wellness Protein. Managed decline is a decision, not a failure.", "action")

    # ---- 5 · Capabilities & enablers
    d.h1("5 · Capabilities & enablers")
    d.body(
        "The pillars depend on four capabilities the plan explicitly funds. <b>Innovation throughput:</b> a "
        "stage-gated pipeline that keeps ProteinPeak launching on a rolling cadence (Cinnamon Crunch and Cocoa "
        "Almond live; Chocolate Almond concept clears its 55% action standard at 64% top-two-box). "
        "<b>Revenue growth management:</b> the pricing, trade and mix engine that underwrites the margin "
        "commitment. <b>Commercial / retail-media analytics:</b> the incrementality discipline that stops us "
        "over-paying for cannibalised Amazon volume. <b>Supply resilience:</b> after Hurricane Tonya cut fill "
        "to ~52% in the affected DCs, the plan hardens the Gulf supply chain so a single weather event cannot "
        "cost a region its share again.")
    d.bullets([
        "<b>Innovation:</b> protect the ProteinPeak launch cadence; hold the Crunchwell Pack Refresh to its "
        "2026-08-15 date; keep the concept funnel above the 55% action standard.",
        "<b>RGM:</b> stand up the five-lever operating rhythm in Report 17 as a permanent capability, not a "
        "one-time project.",
        "<b>Analytics:</b> make modelled incrementality — not platform-reported ROAS — the currency for "
        "trade and media allocation.",
        "<b>Supply:</b> Gulf-region resilience and DC redundancy so fill holds ~95% through the storm season.",
    ])

    # ---- 6 · Risks
    d.h1("6 · Risks to the plan")
    d.body(
        "Three risks are large enough to move the trajectory. The plan funds against each rather than assuming "
        "them away.")
    risk_rows = [
        ["GLP-1 appetite shift", "0.81, volume-down", "Category-wide breakfast volume erosion as appetite-suppressant use grows",
         "Skew mix to protein & satiety positioning; value-per-serving over volume"],
        ["Private label", "High-ACV PL launches", "Great Value Honey Almond / Nut at 84–86% ACV pressures the value core",
         "RGM price-pack architecture; defend with entry price-points, not deeper trade"],
        ["Larksfield escalation", "Two-front", "Field & Honey 14g-protein line ext (May 2026) hits protein + Louisiana at once",
         "ProteinPeak innovation pace; funded LA recovery; endcap-defense media"],
    ]
    d.table(["Risk", "Signal", "What it does to the plan", "Mitigation in-plan"], risk_rows,
            widths=[0.18, 0.16, 0.32, 0.34], align=["LEFT", "LEFT", "LEFT", "LEFT"])
    d.source("seed_macro_trends (strength 0–1); seed_competitor_launches; seed_retailers (ACV).")
    d.callout("The risk that shapes the mix",
              "The GLP-1 shift (0.81, volume-down) is the single trend most likely to bend category volume over "
              "the plan period. It is also the strategic reason to be over-weight Wellness Protein: as appetite "
              "falls, spend concentrates in fewer, higher-value, protein-forward occasions. The mix shift in this "
              "plan is partly a hedge against the biggest risk to it.", "risk")

    d.recommendations([
        ("Adopt the FY27–FY29 revenue and 16%-by-FY28 margin commitment as the Board-level plan of record.",
         "Gregory Whitfield / CFO", "This LRP cycle"),
        ("Fund the ProteinPeak build to the ~$140M FY29 target and mass-channel expansion beyond Target.",
         "Sage Park / Corporate Strategy", "FY27 planning"),
        ("Execute the Crunchwell fix — Pack Refresh (Aug 15) + funded LA recovery (see Report 24).",
         "Cory Whitman / Marcus Boudreaux", "H2 FY26 → FY27"),
        ("Stand up revenue growth management as a permanent capability against the margin commitment (Report 17).",
         "RGM Lead / CFO office", "FY27 onward"),
        ("Confirm the HoneyNest prune and redeploy the freed shelf and cash to Wellness Protein.",
         "Priya Raman / Finance", "FY27 planning"),
    ])
    return d.build()


# ============================================================== REPORT 16 ====
def r16_h2_operating_plan():
    d = Doc("16-acme-h2-2026-operating-plan-reforecast.pdf",
            kicker="OPERATING PLAN · H2 FY2026",
            title="Acme Corp — H2 FY2026 Operating Plan & Reforecast",
            subtitle="Q3–Q4 plan by brand and month, and the path to landing the year",
            owner="Finance; Diane Halverson, VP Sales NA",
            period="Q3–Q4 FY2026 (Jul–Dec 2026)", short="H2 FY26 Plan",
            doc_type="Operating plan & in-year reforecast", date_str="July 2026")

    # actuals Jan-May, full-year plan
    fy26_plan = df("SELECT SUM(Plan_Revenue_USD)/1e6 p FROM plan_vs_actual WHERE Period LIKE '2026-%'").iloc[0].p
    h1_plan, h1_act = _qsum(["2026-01", "2026-02", "2026-03", "2026-04", "2026-05"])
    h1_var = (h1_act - h1_plan) / h1_plan * 100

    d.cover_facts([
        ("H1 actuals (Jan–May)", f"{money(h1_act)} vs {money(h1_plan)} plan · {h1_var:+.1f}%"),
        ("Trajectory", "−5.2% (Q1) improving to −3.4% (May)"),
        ("H2 mandate", "Land FY26 near plan on the ProteinPeak + Crunchwell ramp"),
        ("Biggest H2 lever", "Crunchwell Pack Refresh — launches 2026-08-15"),
        ("Spend re-aim", "~$700K out of Amazon Ads into Walmart / Kroger / LA"),
        ("Note", "Jun–Dec figures are plan / forecast; Jan–May are actuals"),
    ])

    d.exec_summary(
        "H1 FY26 landed behind plan but on an improving line: the month-on-month variance narrowed from "
        "−5.2% in January to −3.4% in May as the ProteinPeak launch pipe filled and Louisiana began to "
        "recover. This operating plan reforecasts the balance of the year and lays out the Q3–Q4 path — by "
        "brand and by month — to land FY26 close to plan. <b>All figures for June through December are plan / "
        "forecast; January through May are actuals.</b> The H2 build is carried by four named drivers, the "
        "largest of which is the Crunchwell Pack Refresh landing on 15 August.",
        bullets=[
            f"<b>Where we are:</b> H1 (Jan–May) net revenue {money(h1_act)} vs {money(h1_plan)} plan "
            f"({h1_var:+.1f}%), with the monthly gap improving from −5.2% to −3.4%.",
            "<b>H2 drivers:</b> (1) ProteinPeak launch ramp continues off the April Cinnamon Crunch / Cocoa "
            "Almond in-market; (2) the Crunchwell Pack Refresh ($28M year-one innovation, launch 2026-08-15); "
            "(3) Louisiana recovery; (4) trade and retail-media reallocation (~$700K out of Amazon).",
            "<b>The reforecast call:</b> hold the FY26 number near plan by loading the recoverable revenue "
            "into Q3–Q4, where the innovation and the improving base coincide.",
            "<b>Watch-item:</b> the plan assumes the Pack Refresh ships on time and the Walmart-pilot "
            "execution gap closes; both are tracked weekly. The CFO reforecast read is Report 40.",
        ])

    # ---- 1 · Where H1 landed
    d.h1("1 · Where H1 landed")
    d.kpis([
        ("H1 net revenue", money(h1_act), f"{h1_var:+.1f}% vs plan"),
        ("Jan variance", "−5.2%", "trough"),
        ("May variance", "−3.4%", "improving"),
        ("Monthly plan", "$63.7M", "FY26 run-rate"),
        ("Q1 total", "$181.1M", "vs $191.2M plan"),
    ])
    d.body(
        "The half closed behind plan, but the shape matters more than the level. Q1 ran −5.3% ($181.1M actual "
        "vs $191.2M plan), then the monthly variance narrowed steadily — −5.2% in January, −5.4% in February, "
        "−5.2% in March, then −3.5% in April and −3.4% in May — as ProteinPeak's April relaunch began "
        "shipping and Louisiana share stabilised. The improving trajectory is the reason this plan holds the "
        "full-year number rather than cutting it: the two things that dragged H1 are both turning.")

    # monthly actual vs plan (Jan-May) + H2 plan (Jun-Dec)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    actuals = [60.40, 60.31, 60.43, 61.52, 61.57, None, None, None, None, None, None, None]
    # H2 plan: ramp from ~62.0 (Jun) toward plan as Pack Refresh (Aug 15) + ProteinPeak build in.
    h2_plan = [None, None, None, None, None, 62.0, 62.4, 63.0, 63.4, 63.7, 63.7, 63.7]
    plan_line = [63.73] * 12
    ch_month = chart_line(
        "r16_monthly_actual_vs_plan.png", months,
        {"Actual (Jan–May)": actuals, "H2 plan (Jun–Dec)": h2_plan, "Plan basis": plan_line},
        title="Monthly net revenue: actuals (Jan–May) vs H2 plan (Jun–Dec) ($M)", h=3.0, annotate_last=False)
    d.image(ch_month, "H2 plan closes the gap to the $63.7M/mo plan basis as innovation and base recovery land. "
                      "Jun–Dec are plan; Jan–May are actuals.")
    d.source("plan_vs_actual (SAP/Acme ERP shape). Jun–Dec = operating plan; Jan–May = actuals.")

    # ---- 2 · The variance trajectory
    d.h1("2 · The variance trajectory — why we hold the year")
    var_trend = chart_line(
        "r16_variance_trend.png",
        ["Jan", "Feb", "Mar", "Apr", "May"],
        {"Variance to plan (%)": [-5.2, -5.4, -5.2, -3.5, -3.4]},
        title="Monthly net-revenue variance to plan (%) — improving through H1", pct=True, h=2.6)
    d.body(
        "The variance-to-plan line is the clearest single argument for the H2 plan. Through Q1 the gap held "
        "near −5.2%, then compressed by ~1.8 points in April–May as ProteinPeak shipped and Louisiana turned. "
        "Extrapolating the recovery — not the trough — into H2 is what makes landing near plan achievable. The "
        "plan does not assume a snap-back to zero variance; it assumes the improvement already visible in the "
        "data continues as the H2 drivers layer in.")
    d.image(var_trend, "The gap compressed ~1.8 points April–May. The H2 plan continues that line, it does not "
                       "assume a reset.")
    d.source("plan_vs_actual monthly variance, FY26 Jan–May actuals.")

    # ---- 3 · H2 plan by brand
    d.pagebreak()
    d.h1("3 · H2 plan by brand")
    d.body(
        "The H2 revenue build is not evenly spread. It is loaded onto the two brands with live innovation — "
        "ProteinPeak (launch ramp) and Crunchwell (Pack Refresh) — while the maintain-role brands hold their "
        "steady, on-track lines. The table below shows the H1 actual run-rate against the H2 plan mandate by "
        "brand. H2 figures are plan.")
    brand_rows = [
        ["Crunchwell", "$23.7M/mo", "−5.7 to −6.0%", "Pack Refresh (Aug 15) + LA recovery", "Recover toward plan"],
        ["ProteinPeak", "$5.44M/mo*", "−6.1% (post-launch)", "Launch ramp continues; mass expansion", "Close the gap on the build"],
        ["TrailGrove", "steady", "−1.6% (on track)", "Hold; self-funding", "Hold plan"],
        ["MorningOats", "steady", "−1.1% (on track)", "Cup / single-serve tilt", "Hold plan"],
        ["HoneyNest", "steady", "−1.1% (on track)", "LTO calendar (Birthday Cake Q4)", "Hold plan"],
        ["RootDay", "steady", "−0.3% (on track)", "Oat-milk category tailwind", "Hold plan"],
    ]
    d.table(["Brand", "H1 actual run-rate", "H1 var to plan", "H2 driver", "H2 mandate"], brand_rows,
            widths=[0.15, 0.19, 0.19, 0.28, 0.19], align=["LEFT", "RIGHT", "RIGHT", "LEFT", "LEFT"])
    d.source("plan_vs_actual FY26 by brand. *ProteinPeak Apr–May post-launch run-rate; Jan–Mar ran −25.4% "
             "pre-launch. H2 = plan.")

    # brand H2 plan bar (illustrative monthly plan contribution by brand)
    brand_h2 = chart_bar(
        "r16_brand_h2_plan.png",
        ["Crunchwell", "TrailGrove", "MorningOats", "HoneyNest", "RootDay", "ProteinPeak"],
        [25.19, 12.7, 7.3, 7.8, 5.2, 5.80],
        title="H2 plan — monthly net revenue by brand ($M, plan basis)",
        colors_list=["#B24A2E", "#1F2A44", "#1F2A44", "#B98A2E", "#2E7D5B", "#2E7D75"], h=2.7)
    d.image(brand_h2, "Crunchwell (fix) and ProteinPeak (grow) carry the H2 recovery; the maintain brands hold "
                      "their on-track lines. Plan basis, monthly.")
    d.source("plan_vs_actual monthly plan by brand (plan basis).")

    # ---- 4 · The four H2 drivers
    d.h1("4 · The four drivers that land the year")
    d.h2("4.1 · ProteinPeak launch ramp")
    d.body(
        "The April Cinnamon Crunch (PP005) and Cocoa Almond (PP006) launch is the single biggest additive "
        "driver. Trial ran 110–113% of plan at Target and 77–78% at the Walmart pilot; Target velocity "
        "(~17.5 units/store/week) is nearly double Walmart's (~9.2). Source-of-volume is healthy — 53% "
        "new-to-brand — so the ramp is real demand, not cannibalisation. H2 continues the ramp and works the "
        "Walmart-pilot execution gap.")
    d.h2("4.2 · Crunchwell Pack Refresh — launches 2026-08-15")
    d.body(
        "The Crunchwell Pack Refresh (Hero SKUs) is a $28M year-one innovation at 0.82 confidence, launching "
        "15 August — squarely in H2 and the largest near-term revenue bet in the plan. It is the commercial "
        "counter to Crunchwell's relevance decline and lands into the same window as the Louisiana recovery, "
        "so H2 is where the Crunchwell line inflects toward plan.")
    d.h2("4.3 · Louisiana recovery")
    d.body(
        "Louisiana Crunchwell share fell −340 bps (6.4%→3.0%) into Q1 and has begun recovering (all-channel "
        "value share 5.80 in 26Q1 to 6.31 in 26Q2). The funded three-leg recovery — facing recovery, targeted "
        "trade, and an LA retail-media injection at ~2.2× the portfolio ROI — contributes recoverable revenue "
        "across H2.")
    d.h2("4.4 · Trade & retail-media reallocation")
    d.body(
        "The plan re-aims working dollars toward what pays back. Roughly $700K comes out of Amazon Ads "
        "(0.40 incrementality — a drag) and into Walmart Connect (1.20), Kroger Precision (0.77) and the "
        "Louisiana recovery, at ~2.2× ROI. The reallocation does not add spend; it improves the return on "
        "the spend already committed. The full effectiveness read is the CFO reforecast, Report 40.")
    d.callout("The reforecast, in one line",
              "H1 landed −5.3% to −3.4% and improving. H2 loads the recoverable revenue into the window where "
              "the ProteinPeak ramp, the Crunchwell Pack Refresh (Aug 15), the Louisiana recovery and the spend "
              "reallocation all coincide. The call is to hold the FY26 number near plan rather than cut it — "
              "contingent on the Pack Refresh shipping on time and the Walmart-pilot gap closing.", "info")

    # ---- 5 · Risks & the H2 ask
    d.h1("5 · Risks & the H2 ask")
    d.callout("What could stop the landing",
              "(1) Pack Refresh slips past 15 August — the single largest H2 dependency. (2) The Walmart-pilot "
              "ProteinPeak execution gap fails to close, capping the ramp at the Target ceiling. (3) Larksfield's "
              "14g-protein line extension (May 2026) escalates the Louisiana and protein fronts as the recovery "
              "is still fragile.", "risk")
    d.recommendations([
        ("Hold the FY26 number near plan; load recoverable revenue into Q3–Q4 per this reforecast.",
         "Finance / Diane Halverson", "H2 — now"),
        ("Protect the Crunchwell Pack Refresh to its 2026-08-15 launch date — the largest H2 dependency.",
         "Cory Whitman", "By Aug 15"),
        ("Close the ProteinPeak Walmart-pilot execution gap; hold Target momentum.",
         "Sage Park / Maya Chen", "Q3"),
        ("Execute the ~$700K Amazon-to-Walmart/Kroger/LA reallocation at ~2.2× ROI.",
         "Tasha Brooks", "Q3 flight"),
        ("Bring the reconciled H2 landing view to the CFO reforecast (Report 40) at the next MBR.",
         "Finance", "Next MBR"),
    ])
    return d.build()


# ============================================================== REPORT 17 ====
def r17_rgm_pricing():
    d = Doc("17-acme-fy26-revenue-growth-management-pricing.pdf",
            kicker="REVENUE GROWTH MANAGEMENT",
            title="Acme Corp — Revenue Growth Management & Pricing Architecture",
            subtitle="Five NRM levers and a quantified prize for FY26, forward to FY27",
            owner="RGM Lead; CFO office",
            period="FY2026 · forward to FY27", short="RGM & Pricing",
            doc_type="Revenue growth management plan", date_str="July 2026")

    # trade aggregate by brand
    tb = df("""SELECT brand,
                 ROUND(SUM(trade_spend_kusd)/1000,1) spend_m,
                 ROUND(SUM(trade_spend_kusd*trade_depth_pct)/SUM(trade_spend_kusd),1) depth,
                 ROUND(SUM(trade_spend_kusd*incrementality_index::DOUBLE)/SUM(trade_spend_kusd),2) incr
               FROM seed_trade_spend_fy25 GROUP BY 1 ORDER BY spend_m DESC""")
    total_trade = df("SELECT ROUND(SUM(trade_spend_kusd)/1000,1) t FROM seed_trade_spend_fy25").iloc[0].t

    d.cover_facts([
        ("Total FY25 trade spend", f"{money(total_trade)} across the portfolio"),
        ("Heaviest line", "Crunchwell ~25.6% of gross, 0.57 incrementality"),
        ("Retail-media return", "$0.65 incremental per $1 (Amazon 0.40 drags)"),
        ("Pricing gap widening", "Crunchwell→Field & Honey 8% → 14%"),
        ("Whitespace concept", "Crunchwell Mega Family Pack 36oz — $8.5M"),
        ("The prize (benchmark)", "RGM typically worth 3–5% of gross profit / yr"),
    ])

    d.exec_summary(
        "Acme spends roughly $146M a year in trade and another ~$4M a quarter in retail media, and it is not "
        "spending either efficiently. Crunchwell's trade runs at ~25.6% of gross for a 0.57 incrementality "
        "index; retail media returns $0.65 incremental per dollar, dragged by Amazon Ads at 0.40. That "
        "inefficiency is the opportunity. This plan lays out the five revenue-growth-management levers — "
        "pricing, promotion, price-pack architecture, trade terms, and mix — each with a specific, "
        "data-grounded action for FY26 and a line to FY27. Against an industry benchmark that RGM analytics "
        "are typically worth 3–5% of gross profit a year, the levers here are how Acme funds roughly half of "
        "its 16%-by-FY28 margin commitment.",
        bullets=[
            "<b>Pricing:</b> the Crunchwell-to-Field&Honey price gap has widened from 8% to 14%; elasticities "
            "differ sharply by SKU (Crunchwell Mega −1.84 to −2.12; ProteinPeak −0.92 to −1.18), so pricing "
            "must be surgical, not across-the-board.",
            f"<b>Promotion:</b> Crunchwell trades at ~25.6% of gross for only 0.57 incrementality — the largest "
            "single efficiency prize in the portfolio; Q1 FY26 events ran a 0.52 incrementality index.",
            "<b>Price-pack architecture:</b> the Crunchwell Mega Family Pack 36oz ($8.5M concept) is priced "
            "whitespace that trades pantry-loaders up rather than discounting the existing pack.",
            "<b>Trade terms & mix:</b> shift terms toward incrementality-based funding, and let mix do the "
            "work — every point of volume that moves to Wellness Protein is higher-margin than the Family-Sweet "
            "point it replaces.",
        ])

    # ---- 1 · The prize
    d.h1("1 · The prize, and why it's here")
    d.kpis([
        ("FY25 trade spend", money(total_trade), "portfolio total"),
        ("Crunchwell trade rate", "~25.6%", "of gross · 0.57 incr"),
        ("Retail-media ROI", "$0.65", "incremental per $1"),
        ("Q1 promo incr. index", "0.52", "43 events, $11.6M"),
        ("Benchmark prize", "3–5%", "of gross profit / yr"),
    ])
    d.body(
        "Revenue growth management is not a pricing exercise; it is the discipline of extracting more gross "
        "profit from the same volume by managing five levers together. Acme has a large prize because it "
        "currently manages them loosely: ~$146M of annual trade at a portfolio incrementality below 0.6, and "
        "a retail-media portfolio returning $0.65 on the dollar. Industry benchmarks put well-run RGM at "
        "<b>3–5% of gross profit per year</b> (cited as an industry benchmark, not an Acme measurement). On "
        "Acme's base that is the larger part of the ~$17M of structural profit the 16%-by-FY28 margin "
        "commitment requires (see the Long-Range Plan, Report 15).")

    # ---- 2 · Lever 1: pricing
    d.h1("2 · Lever 1 — Pricing architecture")
    d.body(
        "Pricing must be surgical because elasticity is not uniform. The elasticity estimates below (log-log "
        "MMM, high-confidence SKUs) show Crunchwell's Mega packs are the most price-sensitive in the portfolio "
        "(−1.84 to −2.12 — pantry-loadable, easy to over-discount), while ProteinPeak's premium SKUs are the "
        "least (−0.92 to −1.18). The strategic implication: take price where the shopper is inelastic "
        "(ProteinPeak, premium granola) and hold or protect price where they are not, rather than a "
        "portfolio-wide list move.")
    el = df("""SELECT sku_name, brand, ROUND(MIN(price_elasticity),2) e
               FROM seed_sku_elasticity_estimates
               WHERE sku_id IN ('CR002','CR001','HN003','TG007','MO001','RD001','PP001')
                 AND confidence_0to1>=0.6
               GROUP BY 1,2 ORDER BY e""")
    short_names = {"Crunchwell Original Mega 18oz": "Crunchwell Mega",
                   "HoneyNest Chocolate 12oz": "HoneyNest Choc",
                   "Crunchwell Original Family 14oz": "Crunchwell Family",
                   "RootDay Oat Milk Original 32oz": "RootDay Oat Milk",
                   "MorningOats Instant Original 8ct": "MorningOats Instant",
                   "TrailGrove Bars Honey Almond": "TrailGrove Bars",
                   "ProteinPeak Vanilla Almond Original 12oz": "ProteinPeak Vanilla"}
    cats = [short_names.get(r.sku_name, r.sku_name) for r in el.itertuples()]
    vals = [abs(float(r.e)) for r in el.itertuples()]
    el_colors = ["#B24A2E" if v >= 1.6 else ("#B98A2E" if v >= 1.2 else "#2E7D75") for v in vals]
    ch_el = chart_bar("r17_price_elasticity.png", cats, vals,
                      title="Price elasticity by SKU (|elasticity|, higher = more price-sensitive)",
                      colors_list=el_colors, horizontal=True, h=2.9)
    d.image(ch_el, "Crunchwell Mega is the most elastic (protect price / avoid deep discounting); ProteinPeak "
                   "premium is the least (headroom to take price).")
    d.source("seed_sku_elasticity_estimates (log-log MMM, confidence ≥ 0.60; most-elastic estimate per SKU).")
    d.callout("The widening price gap",
              "The Crunchwell-to-Field&Honey price gap has widened from ~8% to ~14%. On elastic Crunchwell packs "
              "that gap invites trade-down at exactly the moment Larksfield is escalating in the South. The "
              "pricing lever is not “raise price” — it is close the gap surgically on the elastic packs "
              "while taking headroom on the inelastic premium tier.", "action")

    # ---- 3 · Lever 2: promotion
    d.h1("3 · Lever 2 — Promotion efficiency")
    d.body(
        "Promotion is where the biggest, most immediate dollars sit. Crunchwell alone spent ~$92.4M in FY25 "
        "trade at ~27% depth for a 0.57 incrementality index — meaning a large share of promoted volume would "
        "have sold anyway. The portfolio pattern below shows the prize concentrates in the two heaviest, "
        "lowest-incrementality lines (Crunchwell, HoneyNest). Q1 FY26 events ran 43 promotions, $11.6M spend, "
        "at a 0.52 incrementality index and 14.3% average lift — confirming the structural inefficiency is "
        "still live.")
    tr_rows = [[r.brand, money(r.spend_m), f"{r.depth:.1f}%", f"{r.incr:.2f}",
                "Rework — heavy & low incr." if (r.spend_m > 15 and r.incr < 0.6) else
                ("Efficient" if r.incr >= 0.55 else "Trim depth")]
               for r in tb.itertuples()]
    tr_rows.append(["Total portfolio", money(total_trade), "—", "~0.55", "Shift to incrementality funding"])
    d.h2("3.1 · FY25 trade by brand — spend, depth, incrementality")
    d.table(["Brand", "Trade spend", "Avg depth", "Incr. index", "RGM call"], tr_rows,
            widths=[0.20, 0.18, 0.16, 0.16, 0.30], total_row=True)
    d.source("seed_trade_spend_fy25 (spend-weighted depth & incrementality). Total ~$146.7M.")

    ch_incr = chart_bar("r17_trade_incrementality.png", list(tb.brand),
                        [float(x) for x in tb.incr],
                        title="Trade incrementality index by brand (>1.0 = fully incremental)",
                        colors_list=["#B24A2E" if v < 0.5 else ("#B98A2E" if v < 0.58 else "#2E7D75")
                                     for v in tb.incr], h=2.6)
    d.image(ch_incr, "No brand's trade is fully incremental; RootDay (0.42) and ProteinPeak (0.45) are the "
                     "weakest, Crunchwell (0.59) the largest absolute prize by spend.")
    d.source("seed_trade_spend_fy25, spend-weighted incrementality index by brand.")

    # promo depth vs incrementality scatter-style (grouped bar as proxy)
    depth_incr = chart_grouped(
        "r17_depth_vs_incr.png",
        list(tb.brand),
        {"Avg promo depth (%)": [float(r.depth) for r in tb.itertuples()],
         "Incrementality × 30 (indexed)": [float(r.incr) * 30 for r in tb.itertuples()]},
        title="Promo depth vs incrementality — deeper is not more incremental", h=2.9)
    d.body(
        "The relationship is the whole argument: deeper promotions do not buy more incrementality. Crunchwell "
        "and HoneyNest run the deepest discounts (24–27%) yet sit mid-pack on incrementality (0.51–0.59), "
        "while shallow-depth ProteinPeak (11.9%) and RootDay (9.5%) are the least incremental for different "
        "reasons — small base, wrong mechanic. The lever is to trade depth for frequency-and-quality on the "
        "heavy lines, not to promote more.")
    d.image(depth_incr, "Depth and incrementality are decoupled — the case for reworking mechanics rather than "
                        "cutting or deepening spend. Incrementality shown indexed (×30) for scale.")
    d.source("seed_trade_spend_fy25, spend-weighted by brand. Incrementality scaled ×30 for comparability.")

    # ---- 4 · Levers 3–5
    d.pagebreak()
    d.h1("4 · Levers 3–5 — Price-pack, trade terms, mix")
    d.h2("4.1 · Lever 3 — Price-pack architecture")
    d.body(
        "Price-pack architecture creates value by giving the shopper a reason to trade up rather than a reason "
        "to wait for a deal. The clearest whitespace is the <b>Crunchwell Mega Family Pack 36oz</b> — an $8.5M "
        "year-one concept (Stage-3 prototype, 0.62 confidence, planned FY27). A larger pack at a value "
        "price-per-ounce captures the pantry-loading Mega shopper who is otherwise the most price-elastic "
        "(−1.84 to −2.12) and most likely to buy only on deep promotion. It converts a promotion-dependent "
        "buyer into a bigger, full-margin basket. Single-serve formats (MorningOats cups, +9.8%) are the "
        "second architecture prize.")
    d.h2("4.2 · Lever 4 — Trade terms")
    d.body(
        "Trade terms should pay for incrementality, not display. Today's terms fund depth and frequency "
        "loosely; the FY26–FY27 move is to tie a growing share of trade funding to modelled incrementality "
        "and to pay-for-performance mechanics, starting with the heaviest, lowest-incrementality lines "
        "(Crunchwell, HoneyNest). The retail-media portfolio is the proof of concept: Walmart Connect returns "
        "1.20 incremental per dollar and Amazon Ads only 0.40, so the same logic — fund what is incremental — "
        "reallocates ~$700K out of Amazon in H2 (see Report 16 and the trade PEA, Report 27).")
    d.h2("4.3 · Lever 5 — Mix")
    d.body(
        "Mix is the quiet lever and, over the plan horizon, the largest. Every point of volume that shifts "
        "from Family Sweet (+1.4% category, mature margin) to Wellness Protein (+18.3% category, premium "
        "margin) improves the blended gross margin without any pricing action at all. The ProteinPeak build "
        "in the Long-Range Plan (Report 15) is therefore also an RGM lever: it grows revenue and lifts margin "
        "mix simultaneously. Managing mix means protecting the premium price-points that make the shift "
        "accretive rather than trading them away in promotion.")
    d.callout("Retail-media incrementality — the model for trade terms",
              "Q1 FY26 retail media returned $0.65 incremental per $1: Walmart Connect 1.20 and Kroger Precision "
              "0.77 carry the portfolio, Amazon Ads 0.40 drags it. Paying for modelled incrementality rather "
              "than platform-reported ROAS is exactly the terms discipline this plan extends to trade.", "info")

    # ---- 5 · The action plan
    d.h1("5 · Lever-by-lever action plan & the quantified prize")
    d.body(
        "The five levers resolve to a single operating rhythm with a quantified prize. The prize band below "
        "uses the industry RGM benchmark (3–5% of gross profit) applied directionally to Acme's spend base; "
        "it is a planning estimate, not a measured Acme result.")
    action_rows = [
        ["Pricing", "Close Crunchwell→F&H gap surgically; take headroom on inelastic premium", "RGM Lead", "FY26 H2 → FY27"],
        ["Promotion", "Rework Crunchwell/HoneyNest mechanics; trade depth for quality; incrementality-fund", "RGM / Trade", "FY26 H2"],
        ["Price-pack", "Launch Crunchwell Mega Family Pack 36oz ($8.5M concept); scale single-serve", "Priya Raman", "FY27-Q1"],
        ["Trade terms", "Tie a growing share of funding to modelled incrementality; pay-for-performance", "CFO office / Trade", "FY27 terms cycle"],
        ["Mix", "Accelerate Wellness-Protein shift; protect premium price-points", "Sage Park / RGM", "FY26 → FY29"],
    ]
    d.table(["Lever", "FY26–FY27 action", "Owner", "When"], action_rows,
            widths=[0.14, 0.52, 0.18, 0.16], align=["LEFT", "LEFT", "LEFT", "LEFT"])
    d.source("Levers grounded in seed_trade_spend_fy25, seed_sku_elasticity_estimates, "
             "seed_retail_media_spend_q1_2026, seed_innovation_pipeline.")
    d.callout("The prize, sized and caveated",
              "At the industry benchmark of 3–5% of gross profit per year, disciplined RGM is worth a material, "
              "multi-million-dollar structural gain on Acme's ~$146M trade and retail-media base — the larger "
              "share of the ~$17M of profit the 16%-by-FY28 margin commitment needs. This is an industry "
              "benchmark applied as a planning estimate, not a measured Acme result; the CFO effectiveness read "
              "(Report 40) tracks realised capture.", "win")

    d.h1("6 · Risks to capture")
    d.callout("What erodes the prize",
              "(1) Reflexive depth response to Larksfield's promo intensity re-inflates Crunchwell trade before "
              "mechanics are reworked. (2) Pricing headroom on premium is competed away if ProteinPeak loses "
              "the innovation edge. (3) Trade-terms change meets retailer resistance at the FY27 terms cycle — "
              "start with the cat-captain accounts where Acme has leverage (Kroger).", "risk")
    d.recommendations([
        ("Rework Crunchwell and HoneyNest promo mechanics — trade depth for quality; fund on incrementality.",
         "RGM Lead / Trade", "FY26 H2"),
        ("Close the Crunchwell→Field&Honey price gap surgically on elastic packs; take premium headroom.",
         "RGM Lead", "FY26 H2 → FY27"),
        ("Advance the Crunchwell Mega Family Pack 36oz price-pack concept to launch ($8.5M year-one).",
         "Priya Raman", "FY27-Q1"),
        ("Shift trade terms toward modelled-incrementality funding, starting with cat-captain accounts.",
         "CFO office / Trade", "FY27 terms cycle"),
        ("Track realised RGM capture against the 3–5% benchmark in the CFO effectiveness read (Report 40).",
         "CFO office", "Quarterly"),
    ])
    return d.build()


if __name__ == "__main__":
    print(r15_long_range_plan())
    print(r16_h2_operating_plan())
    print(r17_rgm_pricing())
