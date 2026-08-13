"""DOCX documents 61-70 — plans, narratives and decision memos.
Run: python generators/memos_a.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import (money, chart_line, chart_bar, chart_grouped, chart_stacked,
                 chart_waterfall, chart_donut)
from docx_lib import Memo
import qlib as q


# ==================================================== 61 · FY27 AOP narrative ==
def r61_fy27_aop_narrative():
    m = Memo("61-acme-fy27-annual-operating-plan-narrative.docx",
             kicker="ANNUAL OPERATING PLAN · FY2027",
             title="FY2027 Annual Operating Plan — Narrative and Assumptions",
             subtitle="The revenue build line by line, the assumptions underneath each one, and "
                      "what breaks if they are wrong",
             byline="Finance & FP&A, reviewed with the CFO",
             meta=["Period: FY2027 (Jan–Dec 2027)",
                   "Companion document: FY27 AOP board pre-read (Report 42)",
                   "Version: v1 · July 2026"],
             short="FY27 AOP narrative",
             doc_type="Internal planning document")

    p1, a1, v1 = q.pva_total(q.Q1)
    p2, a2, v2 = q.pva_total(q.Q2)
    pm = q.pva_month()
    bd = q.pva_brand(q.Q1)
    tb = q.trade_brand()

    P = q.PLAN
    f25 = q.brand_fy25()
    deltas, residual = q.fy27_build()

    m.at_a_glance([(q.m0(P['fy27_rev']), "FY27 revenue plan"),
                   (f"{(P['fy27_rev'] / P['fy25_rev'] - 1) * 100:+.0f}%", "on the FY25 base"),
                   (f"~{P['fy27_ebitda']:.1f}%", "FY27 EBITDA target"),
                   (f"~{q.m0(P['trade_envelope'])}", "FY27 trade envelope")])

    m.h1("THE PREMISE", "1 · How this plan is built")
    m.lede("Bottom-up by brand off the FY25 actual base, with the FY26 variance carried as an "
           "explicit risk overlay rather than absorbed.")
    m.body(
        f"FY2026 has run behind plan every month. Q1 landed {money(a1)} against {money(p1)} of plan "
        f"({v1:+.1f}%) and Q2 through May has run {money(a2)} against {money(p2)} ({v2:+.1f}%). "
        f"The monthly plan was straight-lined at {money(float(pm.plan.iloc[0]))}; actuals have run "
        f"between {money(float(pm.act.min()))} and {money(float(pm.act.max()))}. Building FY2027 as a "
        "percentage on top of the FY2026 **plan** would embed a five-point miss into next year's "
        "starting point before a single decision was made.")
    m.body(
        "So the FY2027 plan is built bottom-up from each brand off the **FY2025 actual base**, and "
        "adds only initiatives with a named owner, a stage-gate or a contract behind them. The FY2026 "
        "variance is carried as a named risk overlay in section 5, not netted into the build. There is "
        "no unallocated growth line in this plan.")
    m.callout("What this means in practice",
              "Any growth in this plan can be traced to a named brand initiative. If an "
              "initiative is cancelled or slips, the revenue comes out of the plan rather than being "
              "absorbed as 'productivity'.", "info")

    m.h1("THE BUILD", f"2 · Where {q.m0(P['fy27_rev'])} comes from")
    m.body(
        "Five brands are asked to grow, one to decline, and the residual is adjacency and mix. Each "
        "block is owned by a brand or function leader who has signed up to the number in their own "
        "plan.")
    order = ["ProteinPeak", "RootDay", "TrailGrove", "Crunchwell", "MorningOats", "HoneyNest"]
    ch = chart_waterfall("r61_build.png",
                         [b.replace("Protein", "Protein\n").replace("Morning", "Morning\n")
                          for b in order] + ["Adjacency\n& mix"],
                         [deltas[b] for b in order] + [residual],
                         title=f"FY25 ${P['fy25_rev']:,.0f}M → FY27 ${P['fy27_rev']:,.0f}M: "
                               "the bridge ($M) — planning estimate")
    m.image(ch, f"Movements off the {q.m0(P['fy25_rev'])} FY25 base. All forward blocks are plan "
                "targets.")
    owners = {"ProteinPeak": ("Sage Park", "Full-year PP005/PP006 plus Walmart and Kroger authorisation"),
              "RootDay": ("RootDay BM", "Oat-milk distribution and the single-serve carton concept"),
              "TrailGrove": ("TrailGrove BM", "Granola and bar distribution build"),
              "Crunchwell": ("Cory Whitman", "Aug 15 2026 Pack Refresh; Louisiana recovery to 4.5% share"),
              "MorningOats": ("MorningOats BM", "Single-serve cups, the +9.8% segment"),
              "HoneyNest": ("HoneyNest BM", "Deliberate: harvest decision, three SKUs discontinued")}
    rows = [[f"FY25 actual base", f"{P['fy25_rev']:,.1f}", "Finance", "Measured; per FACTS.md"]]
    rows += [[b, f"{deltas[b]:+.1f}", owners[b][0], owners[b][1]] for b in order]
    rows.append(["Adjacency and mix", f"{residual:+.1f}", "RGM Lead",
                 "Derived residual: non-brand revenue, pack mix, no list-price increase"])
    rows.append(["FY2027 plan", f"{P['fy27_rev']:,.1f}", "CFO", "All of the above"])
    m.table(["Block", "FY27 $M", "Owner", "What it depends on"], rows,
            widths=[0.30, 0.12, 0.18, 0.40], total_row=True, align_right_from=1, size=9.0,
            note="FY25 brand base from seeds/skus.csv; FY27 brand targets per the FY27 AOP "
                 "(Report 14); the adjacency line is the derived residual.")

    m.h1("BY BRAND", "3 · Brand-level plan and the logic of each number")
    m.body(
        "Four of six brands are asked to grow; one is asked to decline; one is asked to grow "
        "substantially. The asymmetry is the plan.")
    rows = [[r.Brand, money(r.plan), money(r.act), f"{r.var:+.1f}%",
             "On track" if r.var > -3 else ("Watch" if r.var > -10 else "Action")]
            for r in bd.itertuples()]
    m.h2("3.1 · Where each brand sits today (Q1 FY2026)")
    m.table(["Brand", "Q1 plan", "Q1 actual", "Variance", "Status"], rows,
            widths=[0.28, 0.18, 0.18, 0.16, 0.20], status_col=4,
            note="plan_vs_actual, Q1 FY2026.")
    m.h2("3.2 · What each brand is being asked to deliver in FY2027")
    m.table(["Brand", "FY27 plan", "Growth", "The logic"],
            [["Crunchwell", q.m0(P['fy27_brand']['Crunchwell']),
              f"{(P['fy27_brand']['Crunchwell'] / f25['Crunchwell'] - 1) * 100:+.0f}%",
              "Pack Refresh plus Louisiana recovery. Stabilisation, not growth (Report 66)."],
             ["TrailGrove", q.m0(P['fy27_brand']['TrailGrove']),
              f"{(P['fy27_brand']['TrailGrove'] / f25['TrailGrove'] - 1) * 100:+.0f}%",
              "Distribution build in a granola segment growing +3.3%. Cheapest volume we have."],
             ["MorningOats", q.m0(P['fy27_brand']['MorningOats']),
              f"{(P['fy27_brand']['MorningOats'] / f25['MorningOats'] - 1) * 100:+.0f}%",
              "Single-serve cups segment is +9.8%; the rest of the line is flat."],
             ["HoneyNest", q.m0(P['fy27_brand']['HoneyNest']),
              f"{(P['fy27_brand']['HoneyNest'] / f25['HoneyNest'] - 1) * 100:+.0f}%",
              "Harvest. Kids Sweet is −2.8% and structurally pressured."],
             ["ProteinPeak", q.m0(P['fy27_brand']['ProteinPeak']),
              f"{(P['fy27_brand']['ProteinPeak'] / f25['ProteinPeak'] - 1) * 100:+.0f}%",
              "Full-year launch SKUs plus Chocolate Almond plus distribution gains."],
             ["RootDay", q.m0(P['fy27_brand']['RootDay']),
              f"{(P['fy27_brand']['RootDay'] / f25['RootDay'] - 1) * 100:+.0f}%",
              "Oat milk is +18.8%; we hold 3.8% share with room to run."]],
            widths=[0.16, 0.13, 0.12, 0.59], align_right_from=1, size=9.0,
            note="Planning estimate. Segment growth from seed_category_market_size.")

    m.h1("MARGIN", f"4 · The path to ~{P['fy27_ebitda']:.1f}%, and why it comes out of trade")
    m.body(
        f"Acme spends about ${tb.spend_m.sum():.0f}M a year on trade promotion at a portfolio "
        f"incrementality index of {tb.incr.mean():.2f}. That index means roughly half the promoted "
        "volume would have sold anyway. Moving the portfolio index from 0.52 to 0.60 is worth "
        "approximately 60 basis points of EBITDA, and it is the largest single margin lever available "
        "that does not touch A&P or headcount.")
    cht = chart_grouped("r61_trade.png", list(tb.brand),
                        {"Trade spend ($M)": [float(x) for x in tb.spend_m],
                         "Depth (%)": [float(x) for x in tb.depth]},
                        title="FY25 trade spend and average depth by brand")
    m.image(cht, "Trade spend and depth by brand. Crunchwell is both the largest line and the "
                 "deepest discounter.")
    m.bullets([
        "**Trade efficiency: +60 bps.** Index 0.52 to 0.60 through fewer, better-timed events and a "
        "0.45 incrementality floor on new events (Report 64).",
        "**Mix: +20 bps.** ProteinPeak and RootDay carry higher gross margin than the cereal core.",
        "**Media efficiency: +10 bps.** Reallocating retail media from a 0.40-ratio platform to a "
        "1.20-ratio platform (Report 74).",
        "**Cost inflation: −0.0 bps assumed net.** Input costs are assumed flat in real terms; this "
        "is the most exposed assumption in the plan.",
    ])
    m.callout("What we are not doing to make the margin",
              "The plan does not cut A&P in absolute dollars, does not reduce R&D, and does not "
              "assume a list-price increase. If the trade-efficiency programme fails, the margin "
              "target fails with it — we are not holding a hidden A&P cut in reserve.", "risk")

    m.h1("ASSUMPTIONS", "5 · What has to be true")
    m.table(["Assumption", "Owner", "If it is wrong"],
            [["Fill rate holds at ~95% and OTIF at ~90%; no repeat of the Nov 2025 storm impact",
              "VP Supply Chain", "Service-driven share loss; see Report 73"],
             ["Pack Refresh ships Aug 15 2026 and reaches 90% ACV by Q4",
              "Cory Whitman", "−$7M FY27 revenue; Louisiana recovery loses its anchor"],
             ["Wellness Protein segment growth stays in the mid-teens",
              "Sage Park", "−$6M on ProteinPeak if growth halves"],
             ["Trade calendar rebuilt to a 0.60 index without base-volume loss",
              "RGM Lead", "−60 bps EBITDA; revenue unaffected"],
             ["No list-price increase; mix and pack architecture only",
              "RGM Lead", "Revenue risk if competitors price up and we do not follow"],
             ["Input costs flat in real terms",
              "Procurement", "Direct EBITDA exposure, roughly 30 bps per 1% of COGS"],
             ["GLP-1 volume drag no worse than assumed",
              "Strategy", "−$5M revenue per additional point of category volume drag"]],
            widths=[0.46, 0.20, 0.34], align_right_from=9, size=9.0,
            note="Assumption owners are accountable for reporting deviation monthly, not annually.")

    m.h1("SENSITIVITIES", "6 · The three cases")
    m.table(["Case", "FY27 revenue", "FY27 EBITDA margin", "What it assumes"],
            [["Downside", "$856M", "14.4%",
              "Pack Refresh slips a quarter, protein growth halves, trade index stalls at 0.52"],
             ["Plan", q.m0(P['fy27_rev']), f"~{P['fy27_ebitda']:.1f}%", "All seven assumptions hold"],
             ["Upside", "$898M", "15.5%",
              "Walmart protein authorisation lands early, Louisiana recovers past 5.0%, "
              "index reaches 0.62"]],
            widths=[0.14, 0.18, 0.20, 0.48], align_right_from=1, size=9.0,
            note="Cases are planning estimates, not modelled forecasts.")

    m.recommendations([
        (f"Approve the {q.m0(P['fy27_rev'])} FY27 revenue plan and the ~{P['fy27_ebitda']:.1f}% "
         "EBITDA target", "Board", "October 2026"),
        ("Approve the trade-efficiency programme as the primary margin lever", "CFO / RGM Lead",
         "October 2026"),
        ("Require monthly assumption-deviation reporting from each named owner", "FP&A", "From Jan 2027"),
        ("Re-baseline the FY27–FY29 long-range plan against this AOP", "Strategy", "July 2027"),
    ])
    m.signoff([("CFO", "the FY27 revenue and margin plan"),
               ("CEO Gregory Whitfield", "the initiative set and the stop list"),
               ("VP Sales NA, Diane Halverson", "the brand and customer revenue commitments")])
    return m.build()


# ================================================= 62 · LRP strategy narrative =
def r62_lrp_narrative():
    m = Memo("62-acme-fy27-fy29-long-range-plan-narrative.docx",
             kicker="LONG-RANGE PLAN · FY2027–FY2029",
             title="Three-Year Strategy Narrative",
             subtitle="The argument for changing the portfolio mix rather than running the current "
                      "mix harder",
             byline="CEO Gregory Whitfield with Strategy",
             meta=["Horizon: FY2027–FY2029", "Companion deck: Report 43",
                   "Version: v1 · July 2026"],
             short="FY27–29 LRP narrative",
             doc_type="Internal strategy document")

    c25 = q.catgrowth("FY2025")
    wp = q.cat_row("FY2025", "Wellness Protein")
    fs = q.cat_row("FY2025", "Family Sweet")
    ks = q.cat_row("FY2025", "Kids Sweet")
    oat = q.cat_row("FY2025", "Oat")
    sh = q.share_quarter()
    mac = q.macro(8)

    P = q.PLAN
    f25b = q.brand_fy25()
    m.at_a_glance([("$1.02B", "FY29 revenue target"),
                   (f"{P['fy28_ebitda']:.0f}%", "EBITDA margin by FY28"),
                   ("29%", "FY29 revenue in high-growth segments"),
                   ("$150M", "ProteinPeak FY29")])

    m.h1("THE ARGUMENT", "1 · We do not have a growth problem. We have a mix problem.")
    m.lede("Acme's portfolio is weighted into segments that grow about one percent a year. No amount "
           "of execution changes the arithmetic of that.")
    m.body(
        f"The RTE cereal category grew +1.3% in FY2025 to $8.35B. Inside that number, Wellness "
        f"Protein grew {wp.growth:+.1f}% to ${wp.size:,.0f}M, Family Sweet — where Crunchwell lives — "
        f"grew {fs.growth:+.1f}%, and Kids Sweet, HoneyNest's home, declined {ks.growth:+.1f}%. "
        f"Outside cereal, oat milk grew {oat.growth:+.1f}% to ${oat.size:,.0f}M. Acme's revenue is "
        "concentrated in the slowest of those pockets.")
    m.body(
        f"Meanwhile our national share is stable: Acme all-brand value share has held around "
        f"{sh.acme.mean():.2f}% for six quarters. We are holding our position in a slow race. The "
        "three-year job is to change which race we are in.")
    ch = chart_bar("r62_segments.png", [s[:18] for s in c25.head(8).subcategory],
                   [float(x) for x in c25.head(8).growth],
                   title="Segment growth, FY2025 (% YoY)", pct=True,
                   colors_list=["#2E7D75" if v > 5 else ("#B98A2E" if v > 0 else "#B24A2E")
                                for v in c25.head(8).growth])
    m.image(ch, "Where the category grows. Acme's revenue weight sits in the right-hand half of "
                "this chart.")

    m.h1("THE FRAME", "2 · What we are committing to by FY2029")
    m.table(["Measure", "FY25 actual", "FY27 target", "FY29 target"],
            [["Net revenue", q.m0(P['fy25_rev']), q.m0(P['fy27_rev']), "~$1.02B"],
             ["EBITDA margin", f"{P['fy25_ebitda']:.1f}%", f"~{P['fy27_ebitda']:.1f}%",
              f"{P['fy29_ebitda']:.1f}%"],
             ["Revenue in high-growth segments", "14%", "20%", "29%"],
             ["ProteinPeak revenue", q.m0(f25b['ProteinPeak']),
              q.m0(P['fy27_brand']['ProteinPeak']), "$150M"],
             ["Portfolio trade incrementality index", "0.52", "0.60", "0.65"],
             ["Retail-media modelled ratio", "0.65", "0.85", "1.00"]],
            widths=[0.40, 0.20, 0.20, 0.20], align_right_from=1,
            note="FY25 from company facts and seed tables; FY27 and FY29 are targets.")
    m.callout("What a target is, in this document",
              "Every FY27–FY29 figure here is a commitment the executive committee is signing up to, "
              "not a forecast of what the market will do. The gates in section 6 are how the "
              "committee holds itself to them.", "info")

    m.h1("BET 1", "3 · Win Wellness Protein")
    m.body(
        f"Wellness Protein is a ${wp.size:,.0f}M segment growing {wp.growth:+.1f}% a year, and Acme "
        f"holds {wp.acme_share:.1f}% of it. ProteinPeak went from $48M in FY25 to a $62M estimate in "
        "FY26 on the back of two SKUs launched in April 2026, with 53% of launch volume new to Acme. "
        "The three-year commitment is $150M by FY29, which requires share in the mid-teens rather "
        "than the high single digits.")
    m.bullets([
        "**Distribution before innovation.** Cinnamon Crunch and Cocoa Almond sit at 38% and 28% "
        "national ACV. Getting both to the level of Vanilla Almond is worth more than any new SKU.",
        "**Then innovation.** Chocolate Almond (64% top-two-box, clears the 55% action standard) in "
        "FY27, ProteinPeak Bars 12g opening the $2.96B bar segment in FY28.",
        "**Creator-led, not TV-led.** The brand's social sentiment runs +0.44 against Crunchwell's "
        "−0.11. The mix that produced that is the mix we scale.",
        "**Price discipline.** $7.49 held, depth capped at 10%. A premium item trained to discount "
        "stops being a premium item.",
    ])

    m.h1("BET 2", "4 · Stabilise the Crunchwell core")
    m.body(
        "Crunchwell is 38% of company revenue and has been flat for six quarters while the category "
        "grew. The equity data says why: Relevance fell 5.9 points while Trust rose. The three-year "
        "commitment is stabilisation in FY27, relevance recovery in FY28 and modest growth in FY29 — "
        "in that order, with a gate at each step (Report 66).")
    m.body(
        "The reason this is a stabilisation commitment rather than a growth commitment is arithmetic. "
        "Family Sweet grows about 1.4% a year. A brand holding share in that segment grows 1.4%. "
        "Anything more has to come from share, and share has to come from relevance, and relevance "
        "takes more than one planning cycle to move.")

    m.h1("BET 3 & 4", "5 · Better-for-you adjacency and commercial efficiency")
    m.h2("5.1 · Adjacency")
    m.body(
        f"TrailGrove in granola and RootDay in oat milk sit in segments growing +3.3% and "
        f"{oat.growth:+.1f}% respectively, and between them they receive less A&P than Crunchwell "
        "spends on linear television. The FY27–FY29 plan raises their investment modestly and "
        "weights it to distribution rather than innovation (Report 51).")
    m.h2("5.2 · Efficiency")
    m.body(
        "The transition is funded from inside the P&L: trade incrementality from 0.52 to 0.65, "
        "retail-media modelled ratio from 0.65 to 1.00, and the stop list in section 7. None of the "
        "three requires incremental investment from the shareholder.")

    m.h1("GATES", "6 · How the committee holds this plan to account")
    m.table(["Gate", "When", "Test", "Consequence of failure"],
            [["Gate 1", "Q4 FY26", "Pack Refresh in market; Louisiana share above 4.0%",
              "Crunchwell moves to maintenance A&P; money to ProteinPeak"],
             ["Gate 2", "Q4 FY27",
              "ProteinPeak above $100M run-rate with full Walmart and Kroger distribution",
              "Re-plan the FY29 protein commitment downward"],
             ["Gate 3", "FY28 planning",
              "Trade index above 0.60 and retail-media ratio above 0.85",
              "Trade Finance takes calendar control; margin target re-cut"],
             ["Annual", "Every July", "LRP re-baselined against the AOP",
              "Plan is restated rather than quietly missed"]],
            widths=[0.12, 0.16, 0.38, 0.34], align_right_from=9, size=9.0,
            note="Gate tests use measures already reported in this repository, not new instrumentation.")

    m.h1("THE STOP LIST", "7 · What three years of discipline means")
    m.table(["Stop or exit", "Why", "When", "Freed resource"],
            [["RootDay Coconut Blend, HoneyNest Granola Crunch, HoneyNest Cookie Dough",
              "Sub-scale, low velocity, negative contribution", "Q3 FY26", "≈$1.5M trade plus shelf"],
             ["Linear TV as Crunchwell's dominant channel", "Reach without relevance",
              "FY27 planning", "≈$8M to reallocate"],
             ["Amazon Ads at current weight", "Modelled incrementality ratio 0.40", "H2 FY26",
              "≈$0.7M immediately"],
             ["Kids Sweet innovation beyond LTOs", "Segment −2.8%, mom-guilt trend 0.68",
              "FY27 plan", "R&D capacity to protein"],
             ["Defending under-indexed Northeast DMAs", "3.4–3.8% share, no structural advantage",
              "FY27 plan", "Trade and merchandising focus to the South"]],
            widths=[0.32, 0.30, 0.14, 0.24], align_right_from=9, size=9.0,
            note="Source: seeds/innovation_pipeline.csv, seed_marketing_spend, "
                 "seed_retail_media_spend_q1_2026, seed_macro_trends, seed_geographies.")

    mrows = [[r.topic, f"{r.strength:.2f}", r.direction, str(r.cats)[:30]] for r in mac.itertuples()]
    m.h1("CONTEXT", "8 · The trends this plan is built against")
    m.table(["Trend", "Strength", "Direction", "Categories affected"], mrows,
            widths=[0.34, 0.14, 0.22, 0.30], align_right_from=1, size=9.0,
            note="Source: seed_macro_trends, top eight by strength.")
    m.callout("The trend that should worry us most",
              "GLP-1 appetite shift runs at 0.81 strength with a downward volume direction across "
              "cereal, bars and hot cereal. It argues for smaller packs, higher protein and premium "
              "price-per-serving — which is what this plan does, but the pace of the shift is the "
              "biggest single uncertainty in the three-year frame.", "risk")

    m.recommendations([
        (f"Approve the FY27–FY29 frame: {q.m0(P['fy27_rev'])} FY27 → ~$1.02B FY29 at "
         f"{P['fy28_ebitda']:.0f}% margin, with the mix-shift target",
         "Executive committee", "July 2026"),
        ("Adopt the four gates and their stated consequences", "CEO / CFO", "July 2026"),
        ("Publish the stop list to the leadership team so it is visible, not implicit", "Strategy",
         "By Aug 15"),
        ("Add a GLP-1 volume sensitivity to the plan each July", "Strategy / FP&A", "Annually"),
    ])
    m.signoff([("CEO Gregory Whitfield", "the three-year strategic frame"),
               ("CFO", "the financial commitments and the gate consequences")])
    return m.build()


# ==================================================== 63 · H2 reforecast memo ==
def r63_h2_reforecast_memo():
    m = Memo("63-acme-h2-2026-reforecast-memo-to-the-board.docx",
             kicker="REFORECAST MEMORANDUM",
             title="H2 FY2026 Reforecast — Memo to the Board",
             subtitle="What has changed since the FY26 plan was set, what we are reforecasting, and "
                      "what we are not changing",
             byline="Finance & FP&A on behalf of the CFO",
             meta=["To: Acme Corp Board of Directors", "Period: Q3–Q4 FY2026",
                   "Companion deck: Report 44", "Version: v1 · July 2026"],
             short="H2 FY26 reforecast memo",
             doc_type="Internal board memorandum")

    pm = q.pva_month()
    p1, a1, v1 = q.pva_total(q.Q1)
    p2, a2, v2 = q.pva_total(q.Q2)

    m.at_a_glance([("$379M", "H2 reforecast"), ("−0.8%", "vs original H2 plan"),
                   (f"{v2:+.1f}%", "Q2 QTD variance"), ("−$1.4M", "net risk-adjusted position")])

    m.h1("SUMMARY", "1 · The recommendation in one paragraph")
    m.lede("We are recommending an H2 reforecast of $379M and no change to the full-year commitment.")
    m.body(
        f"Through May, FY2026 has delivered {money(a1 + a2)} against {money(p1 + p2)} of plan. "
        f"The monthly gap has narrowed from {float(pm['var'].min()):+.1f}% in February to "
        f"{float(pm['var'].iloc[-1]):+.1f}% in May as the ProteinPeak launch shipped. Holding May's "
        "run-rate and adding the two known H2 events — the August 15 Pack Refresh and a full quarter "
        "of ProteinPeak distribution — produces an H2 landing zone of $379M against $382M of "
        "original plan. The $3M gap is being held as a management risk rather than closed with "
        "promotional volume, which is the discipline the board asked for last cycle.")

    ch = chart_line("r63_month.png", list(pm.Period),
                    {"Plan ($M)": [float(x) for x in pm.plan],
                     "Actual ($M)": [float(x) for x in pm.act]},
                    title="FY2026 net revenue by month, plan versus actual ($M)")
    m.image(ch, "The gap narrows every month from February onward. The reforecast assumes it holds "
                "rather than continues to close.")

    m.h1("METHOD", "2 · How the number was built")
    m.bullets([
        "**Base:** May 2026 actual of " + money(float(pm.act.iloc[-1])) + " per month, held flat.",
        "**Plus** Pack Refresh pipeline fill in Q3 and consumption in Q4.",
        "**Plus** a full quarter of ProteinPeak distribution at current velocities.",
        "**Less** the three HoneyNest and RootDay SKUs discontinued in Q3.",
        "**Less** supply phasing during the Pack Refresh changeover in weeks 33–35.",
        "**No assumption** of Louisiana share recovery beyond the ~35 basis points already measured.",
    ])
    m.table(["Step", "H2 $M"],
            [["Unconstrained demand forecast", "384.0"],
             ["Less: Pack Refresh changeover phasing", "−2.5"],
             ["Less: ProteinPeak allocation at Walmart", "−1.5"],
             ["Less: HoneyNest and RootDay discontinuations", "−1.6"],
             ["Plus: retail-media reallocation upside", "+0.6"],
             ["H2 reforecast", "379.0"]],
            widths=[0.72, 0.28], total_row=True,
            note="Reconciliation agreed in the July S&OP cycle (Report 72).")

    m.h1("LEDGER", "3 · Risks and opportunities behind the number")
    m.table(["Item", "Type", "H2 impact", "Probability", "Owner"],
            [["Pack Refresh on-shelf Aug 15 as planned", "Opportunity", "+$6.0M", "High",
              "Cory Whitman"],
             ["Walmart ProteinPeak full-line authorisation", "Opportunity", "+$4.5M", "Medium",
              "Marcus Boudreaux"],
             ["Retail-media reallocation", "Opportunity", "+$1.6M", "High", "Tasha Brooks"],
             ["Larksfield 14g line takes protein share", "Risk", "−$3.5M", "Medium", "Sage Park"],
             ["Louisiana recovery stalls at 3.0%", "Risk", "−$2.5M", "Medium", "Marcus Boudreaux"],
             ["Pack Refresh slips to Q4", "Risk", "−$6.0M", "Low", "Cory Whitman"],
             ["H-E-B Cinnamon Twist delist", "Risk", "−$1.8M", "Medium", "Marcus Boudreaux"],
             ["Net risk-adjusted position", "Net", "−$1.4M", "—", "Finance"]],
            widths=[0.38, 0.13, 0.15, 0.15, 0.19], total_row=True, align_right_from=2, size=9.0,
            note="Source: seeds/innovation_pipeline.csv, seed_competitor_launches, "
                 "seed_heb_cinnamon_twist_delist_risk. Dollar impacts are planning estimates.")

    m.h1("NOT CHANGING", "4 · What we are deliberately not reforecasting")
    m.bullets([
        "**The full-year revenue commitment.** The shortfall is being reallocated between quarters, "
        "not removed from the year.",
        "**The FY26 A&P envelope.** We are not funding the gap by cutting marketing; the media "
        "reallocation is inside the existing envelope (Report 74).",
        "**The 16% FY28 EBITDA commitment.** Nothing in the H2 picture changes the three-year "
        "margin path.",
        "**The trade budget.** We are changing the mix of events, not the total.",
    ])
    m.callout("The one thing we are asking the board to note",
              "Two of the three largest H2 opportunities — the retail-media reallocation and the "
              "Walmart protein authorisation — are within our control. If we deliver both, the H2 "
              "number is closer to $385M than $379M. The reforecast deliberately does not assume "
              "our own execution.", "action")

    m.risks([["Pack Refresh slips past Aug 15", "−$6.0M H2, LA recovery loses anchor",
              "Weekly stage-gate from Jul 15; Q4 fallback plan agreed", "Cory Whitman"],
             ["2026 hurricane season repeats Nov 2025", "Service-driven share loss in the South",
              "Pre-positioned inventory at Houston and Tyler from week 32", "VP Supply Chain"],
             ["Larksfield escalates on both protein and Louisiana",
              "Slower recovery on two fronts at once",
              "Chocolate Almond into Q4 line reviews; LA media injection", "Sage Park / Marcus Boudreaux"]])

    m.recommendations([
        ("Note the H2 reforecast of $379M and the unchanged full-year commitment", "Board",
         "July 2026"),
        ("Approve the $700K retail-media reallocation", "CFO", "By Aug 1"),
        ("Note the four items we are deliberately not reforecasting", "Board", "July 2026"),
    ])
    return m.build()


# ================================================== 64 · RGM policy document ===
def r64_rgm_policy():
    m = Memo("64-acme-fy27-price-pack-architecture-trade-guardrails.docx",
             kicker="POLICY DOCUMENT · REVENUE GROWTH MANAGEMENT",
             title="FY2027 Price-Pack Architecture and Trade Guardrails",
             subtitle="The rules that govern everyday price, pack ladder and promotional depth "
                      "from August 2026",
             byline="RGM Lead with Trade Finance, approved by the CFO",
             meta=["Effective: August 1 2026", "Applies to: all brands, all customers, North America",
                   "Companion deck: Report 45", "Version: v1 · July 2026"],
             short="FY27 RGM policy",
             doc_type="Internal policy document")

    tb = q.trade_brand()
    ev = q.trade_events_raw()
    el = q.elasticity()
    sk = q.skus("Crunchwell")

    m.at_a_glance([("0.45", "minimum event index"), ("20%", "Mega depth cap"),
                   (f"{tb.incr.mean():.2f}", "portfolio index today"), ("0.60", "FY27 target")])

    m.h1("PURPOSE", "1 · Why this policy exists")
    m.body(
        f"Acme spends approximately ${tb.spend_m.sum():.0f}M a year on trade promotion. In Q1 FY2026 "
        f"we ran {len(ev)} events costing ${ev.spend_kusd.sum()/1000:.1f}M and generating "
        f"${ev.incremental_revenue_kusd.sum()/1000:.1f}M of modelled incremental revenue — an "
        f"incrementality index of {ev.modeled_incrementality_index.mean():.2f}. Roughly half of the "
        "volume we paid to move would have moved anyway.")
    m.body(
        "The pattern behind that number is consistent: our most elastic packs are the ones we "
        f"discount hardest. {el.sku_name.iloc[0]} at {el.retailer.iloc[0]} carries an elasticity of "
        f"{el.elast.iloc[0]:.2f}. Deep, frequent discounting on that pack buys volume at a permanent "
        "cost to the reference price, which is the mechanism behind the Louisiana base erosion. This "
        "policy sets guardrails so that mechanism stops.")

    m.h1("THE LADDER", "2 · Everyday price and pack architecture")
    m.body(
        "The pack ladder defines the role of each pack and the everyday price that supports it. "
        "Everyday price is defended; promotion happens around it, not instead of it.")
    m.table(["Pack", "Role", "Everyday price", "Max depth", "Events per year"],
            [["Crunchwell 13oz Multigrain", "Entry / trial", "$4.49", "15%", "2"],
             ["Crunchwell 14oz hero (post-refresh)", "Core volume", "$4.49", "20%", "4"],
             ["Crunchwell 18oz Mega", "Value / pantry", "$5.49", "20%", "3"],
             ["Crunchwell 36oz Mega Family (2027-Q1)", "Value ceiling", "$8.99 target",
              "Launch support only", "1"],
             ["ProteinPeak 12oz", "Premium / growth", "$7.49", "10%", "3"],
             ["ProteinPeak single-serve cup", "Convenience", "$9.99", "0%", "0 (sampling instead)"],
             ["TrailGrove granola and bars", "Better-for-you volume", "Per SKU", "15%", "4"],
             ["RootDay 64oz oat milk", "Growth adjacency", "Per SKU", "12%", "3"]],
            widths=[0.28, 0.17, 0.16, 0.14, 0.25], align_right_from=2, size=9.0,
            note="Everyday prices from seeds/skus.csv (avg_shelf_price_usd); 36oz Mega Family from "
                 "seeds/innovation_pipeline.csv. Depth caps and event counts are the FY27 policy.")

    che = chart_bar("r64_elast.png",
                    [f"{s.split(' ')[1]} {s.split(' ')[-1]}" for s in el.sku_name],
                    [float(x) for x in el.elast],
                    title="Price elasticity by SKU and retailer (more negative = more elastic)",
                    color="rust")
    m.image(che, "The packs we discount hardest are the most elastic — which is why depth erodes the "
                 "base rather than building it.")

    m.h1("GUARDRAILS", "3 · The five rules")
    m.bullets([
        "**Rule 1 — the 0.45 floor.** No new promoted event may be approved with a modelled "
        "incrementality index below 0.45, unless it is defending a specific distribution commitment "
        "documented in the customer plan.",
        "**Rule 2 — depth caps.** Depth caps in the ladder above are maximums, not targets. Any "
        "exception requires Trade Finance sign-off and is logged.",
        "**Rule 3 — no stacking.** Acme depth may not be stacked with retailer-funded depth on the "
        "same item in the same week. Feature and display are the additive levers, not price.",
        "**Rule 4 — premium items do not discount.** ProteinPeak and single-serve packs use "
        "sampling, display and retail media. A premium item trained to discount stops being premium.",
        "**Rule 5 — index is reported monthly.** Portfolio and brand incrementality index appear "
        "alongside spend in the monthly commercial review, not in an annual post-event analysis.",
    ])
    m.callout("What the 0.45 floor would have done to the Q1 calendar",
              "Applied to Q1 FY2026, the floor removes the lowest-returning mechanics and frees "
              "roughly $2.4M for feature-and-display weight, which indexes higher on every brand we "
              "run it on. It does not reduce the trade budget.", "action")

    trows = [[r.brand, money(r.spend_m), f"{r.depth:.1f}%", f"{r.incr:.2f}",
              "≤20%" if r.brand == "Crunchwell" else ("≤10%" if r.brand == "ProteinPeak" else "≤15%")]
             for r in tb.itertuples()]
    m.h1("BASELINE", "4 · Where each brand starts from")
    m.table(["Brand", "FY25 trade spend", "Average depth", "Index", "FY27 depth cap"], trows,
            widths=[0.24, 0.22, 0.18, 0.14, 0.22],
            note="Source: seed_trade_spend_fy25. Caps are the FY27 policy.")

    m.h1("EXCEPTIONS", "5 · How exceptions work")
    m.body(
        "Exceptions exist because line reviews are negotiations. They are not, however, "
        "discretionary at the account level. Any deviation from the ladder or the caps requires "
        "written Trade Finance approval, states the distribution commitment it is defending, and "
        "carries an expiry date. Exceptions are reviewed quarterly and reported to the CFO in "
        "aggregate.")
    m.table(["Exception type", "Approver", "Maximum duration", "Reporting"],
            [["Depth above cap for a line-review commitment", "Trade Finance + RGM Lead",
              "One event window", "Monthly commercial review"],
             ["Event below the 0.45 index floor", "RGM Lead", "One quarter", "Quarterly to CFO"],
             ["New pack price outside the ladder", "CFO", "Permanent (ladder amended)",
              "At approval"],
             ["Premium-item discount", "CFO", "One event window", "Quarterly to CFO"]],
            widths=[0.36, 0.24, 0.20, 0.20], align_right_from=9, size=9.0)

    m.recommendations([
        ("Adopt the ladder and the five guardrails with effect from August 1 2026", "CFO", "Aug 1 2026"),
        ("Rebuild the Q3 and Q4 FY26 calendars against the 0.45 floor", "NAM team / Trade Finance",
         "By Aug 15"),
        ("Add portfolio and brand index to the monthly commercial review pack", "Trade Finance",
         "From August"),
        ("Bring the 36oz Mega Family Pack forward into the FY27 innovation gate",
         "Innovation / RGM Lead", "Q4 FY26"),
        ("Review exception volume and index progress at the January 2027 commercial review",
         "RGM Lead", "January 2027"),
    ])
    m.signoff([("CFO", "the policy and the exception process"),
               ("RGM Lead", "the ladder and the depth caps"),
               ("Diane Halverson, VP Sales NA", "customer-facing application of the caps")])
    return m.build()


# =============================================== 65 · Crunchwell creative brief =
def r65_crunchwell_creative_brief():
    m = Memo("65-crunchwell-fy27-creative-platform-agency-brief.docx",
             kicker="AGENCY BRIEF · CREATIVE PLATFORM",
             title="Crunchwell FY2027 Creative Platform Brief",
             subtitle="The relevance problem, the evidence behind it, and what we need the platform "
                      "to do about it",
             byline="Cory Whitman, Brand Director — Crunchwell",
             meta=["To: creative and media agency partners",
                   "Brief date: July 2026 · Response due: September 2026",
                   "Companion deck: Report 46"],
             short="Crunchwell FY27 brief",
             doc_type="Internal creative brief")

    eqp = q.equity("Crunchwell", "US-NAT")
    eqla = q.equity("Crunchwell", "LA-DMA")
    coh = q.cohorts()
    sent = q.sentiment()
    mk = q.mkt_spend("Crunchwell")
    mac = q.macro(8)

    m.at_a_glance([(f"{eqp['Relevance'].iloc[-1] - eqp['Relevance'].iloc[0]:+.1f} pp", "Relevance"),
                   (f"{eqp['Trust'].iloc[-1] - eqp['Trust'].iloc[0]:+.1f} pp", "Trust"),
                   (f"{eqp['Modernity'].iloc[-1]:.1f}", "Modernity today"),
                   (f"{float(sent[sent.brand=='Crunchwell'].sent.iloc[0]):+.2f}", "social sentiment")])

    m.h1("THE JOB", "1 · What we need the platform to do")
    m.lede("Make Crunchwell wanted again. Not trusted — we already have that — wanted.")
    m.body(
        f"Crunchwell has held about 6.0% national value share for six quarters while the category "
        "grew and Larksfield's Field & Honey grew 7.4%. The equity tracker explains why. Across six "
        f"waves, Relevance fell from {eqp['Relevance'].iloc[0]:.1f} to {eqp['Relevance'].iloc[-1]:.1f} "
        f"top-two-box, while Trust rose from {eqp['Trust'].iloc[0]:.1f} to {eqp['Trust'].iloc[-1]:.1f} "
        f"and Quality from {eqp['Quality'].iloc[0]:.1f} to {eqp['Quality'].iloc[-1]:.1f}. Modernity "
        f"sits at {eqp['Modernity'].iloc[-1]:.1f}, the weakest attribute in the set.")
    m.body(
        "That combination has a specific meaning. Consumers believe the product is good and do not "
        "think it is for them right now. The platform's job is to close that gap without spending a "
        "dollar against attributes we already own.")

    ch = chart_line("r65_equity.png", list(eqp.index),
                    {a: [float(x) for x in eqp[a]] for a in
                     ["Relevance", "Trust", "Taste", "Quality", "Modernity"]},
                    title="Crunchwell brand equity, top-two-box (%) — US National", pct=True)
    m.image(ch, "Six waves of equity data. Relevance is the line that moves; everything else holds.")

    m.h1("THE EVIDENCE", "2 · Four things we know")
    m.h2("2.1 · The shopper base is turning over")
    m.body(
        f"Loyal-family household penetration moved from {coh['loyal-family'].iloc[0]:.1f}% to "
        f"{coh['loyal-family'].iloc[-1]:.1f}% while cereal-skipper households grew from "
        f"{coh['cereal-skipper'].iloc[0]:.1f}% to {coh['cereal-skipper'].iloc[-1]:.1f}%. We are "
        "losing breakfast occasions, not brand preference. Nobody is switching away from Crunchwell "
        "in anger; they are skipping the meal.")
    m.h2("2.2 · This is not a price problem")
    m.body(
        f"Price-shopper penetration is flat at about {coh['price-shopper'].iloc[-1]:.1f}% and "
        "measured price sensitivity is stable across waves. A value platform would spend against a "
        "problem we do not have.")
    m.h2("2.3 · Louisiana is the acute case")
    m.body(
        f"In the Louisiana DMA, Relevance sits at {eqla['Relevance'].iloc[-1]:.1f} against "
        f"{eqp['Relevance'].iloc[-1]:.1f} nationally, while Trust holds at "
        f"{eqla['Trust'].iloc[-1]:.1f}. Eight weeks of empty shelf next to a competitor endcap is a "
        "relevance event as much as an availability event. Louisiana is where the platform gets "
        "tested first.")
    m.h2("2.4 · The conversation is against us")
    m.body(
        f"Crunchwell social sentiment runs {float(sent[sent.brand=='Crunchwell'].sent.iloc[0]):+.2f} "
        f"on {int(sent[sent.brand=='Crunchwell'].mentions.iloc[0])} mentions in 2026, while "
        f"ProteinPeak — the same company, a different mix — runs "
        f"{float(sent[sent.brand=='ProteinPeak'].sent.iloc[0]):+.2f}.")

    m.h1("THE PLATFORM", "3 · Our recommendation, and what we will judge against")
    m.body(
        "Our working platform is **\"Made for the morning you actually have\"** — a reframe from "
        "nostalgic family ritual to the compressed, chaotic weekday morning that the data says people "
        "are actually living. We are not wedded to the words. We are wedded to the target: Relevance "
        "and Modernity, without touching Trust or Taste.")
    m.table(["We will judge the platform on", "How", "Standard"],
            [["Does it move Relevance?", "Kantar-shape tracker, quarterly waves",
              "Relevance 62.7 → 65.5 by FY27Q4"],
             ["Does it move Modernity?", "Same tracker", "Modernity 48.8 → 52"],
             ["Does it protect Trust and Taste?", "Same tracker", "No decline beyond 1 point"],
             ["Does it work in the South?", "LA-DMA cut of the tracker plus share",
              "LA share 3.0% → 4.5%"],
             ["Does it work creator-first?", "Social sentiment and earned reach",
              "Sentiment from −0.11 to positive"]],
            widths=[0.34, 0.34, 0.32], align_right_from=9, size=9.0,
            note="Measures from brand_equity_quarterly, syndicated_weekly, social_mentions.")

    m.h1("THE ALTERNATIVES", "4 · Four platforms we have already rejected, and why")
    m.bullets([
        "**Value.** Rejected. Price-shopper penetration is flat and price sensitivity is stable. "
        "There is no value problem to solve.",
        "**Heritage.** Rejected. Trust is already at 72.9 and rising. We would be paying to reinforce "
        "an asset we own.",
        "**Health.** Rejected. That is ProteinPeak's and TrailGrove's ground. Crunchwell competing "
        "there cannibalises the two brands that are actually growing.",
        "**Kids.** Rejected. Kids Sweet is a −2.8% segment and the mom-guilt trend runs at 0.68 "
        "strength. HoneyNest is being harvested for exactly this reason (Report 69).",
    ])

    chm = chart_donut("r65_mix.png", [c[:20] for c in mk.channel.head(6)],
                      [float(x) for x in mk.spend_m.head(6)],
                      title="Crunchwell A&P by channel today ($M)")
    m.h1("MEDIA IMPLICATIONS", "5 · The mix has to move with the message")
    m.image(chm, "Today's mix is linear-TV-led — reach against a shrinking occasion.")
    m.body(
        f"Crunchwell's A&P runs about ${mk.spend_m.sum():.1f}M with Linear TV as the largest single "
        "line. The FY27 recommendation holds total A&P flat and moves roughly a third of the TV line "
        "into CTV, creator and retail media, with Louisiana weighted at 2.2 times the portfolio ROI "
        "on the retail-media leg. Creative needs to be built for that mix from the start, not "
        "adapted into it.")

    m.h1("PRACTICALITIES", "6 · Timing, budget and non-negotiables")
    m.table(["Item", "Detail"],
            [["Platform launch", "With the Crunchwell Pack Refresh, on shelf August 15 2026"],
             ["Working budget", "≈$18M FY27 A&P, total held flat versus FY26"],
             ["Lead market", "Louisiana DMA and the South region"],
             ["Non-negotiable 1", "The pack and the message launch together, not three months apart"],
             ["Non-negotiable 2", "Creator-first execution in the South; TV supports, does not lead"],
             ["Non-negotiable 3", "No value or price messaging in the platform"],
             ["Response due", "September 2026, for FY27 production"]],
            widths=[0.28, 0.72], align_right_from=9, size=9.5)
    m.callout("One request about sequencing",
              "In Louisiana, availability comes before message. Fourteen audited doors still sit "
              "below 70% on-shelf availability. Media into an empty shelf is wasted, so the local "
              "campaign flight follows the merchandising fix rather than leading it.", "risk")

    m.recommendations([
        ("Agency response against this brief, including one deliberately uncomfortable option",
         "Agency partners", "September 2026"),
        ("Platform selection with VP Brand and the CFO", "Cory Whitman", "By Sep 30 2026"),
        ("Production against the Pack Refresh timing", "Agency / Cory Whitman", "Q4 FY26"),
        ("Add Relevance and Modernity to the reported brand scorecard", "Insights", "FY27Q1"),
    ])
    return m.build()


# ============================================ 66 · Crunchwell turnaround memo ==
def r66_crunchwell_turnaround_memo():
    m = Memo("66-crunchwell-fy27-fy29-turnaround-commitment-memo.docx",
             kicker="COMMITMENT MEMORANDUM",
             title="Crunchwell FY2027–FY2029 Turnaround — Commitment and Stop Conditions",
             subtitle="What the brand team is committing to, year by year, and the conditions under "
                      "which the committee should stop funding it",
             byline="Cory Whitman, Brand Director — Crunchwell, with Finance",
             meta=["To: Crunchwell SteerCo", "Horizon: FY2027–FY2029",
                   "Companion deck: Report 47", "Version: v1 · July 2026"],
             short="Crunchwell commitment",
             doc_type="Internal commitment memorandum")

    pv = q.pva_brand_month("Crunchwell")
    la = q.share_quarter(la=True)
    eqp = q.equity("Crunchwell", "US-NAT")
    geo = q.geos()
    tb = q.trade_brand()
    cwt = tb[tb.brand == "Crunchwell"].iloc[0]

    m.at_a_glance([(f"{float(pv['var'].mean()):+.1f}%", "FY26 variance to plan"),
                   (f"{la.cw.iloc[-1]:.2f}%", "Louisiana share"),
                   (f"{eqp['Relevance'].iloc[-1]:.1f}", "Relevance"),
                   (q.m0(q.PLAN['fy27_brand']['Crunchwell']), "FY27 commitment")])

    m.h1("THE COMMITMENT", "1 · What we are and are not promising")
    m.lede("FY2027 is a stabilisation year. We are not committing to growth until FY2029.")
    m.body(
        f"Crunchwell is $312M of FY2025 revenue running between {float(pv['var'].min()):.1f}% and "
        f"{float(pv['var'].max()):.1f}% against plan every month of FY2026, with a 340 basis point "
        "hole in Louisiana and a five-point national relevance decline. Committing to growth in "
        "FY2027 would be a commitment we could not keep, and the SteerCo has been clear that it "
        "would rather have a hard commitment it can hold us to.")
    m.table(["Year", "Job", "Revenue commitment", "Lead measures", "Gate"],
            [["FY2027", "Stabilise", "$318M (+1.9% on FY25 actual)",
              "Louisiana share ≥4.5%; Pack Refresh 90% ACV; trade index ≥0.60", "Q4 FY27"],
             ["FY2028", "Rebuild relevance", "$326M (+2.5%)",
              "Relevance ≥65; Modernity ≥52; Mega Family Pack in market", "Q4 FY28"],
             ["FY2029", "Grow", "$336M (+3.1%)",
              "Trade rate ≤22% of gross; two new SKUs at scale", "FY30 planning"]],
            widths=[0.11, 0.16, 0.22, 0.35, 0.16], align_right_from=9, size=9.0,
            note="Revenue commitments are targets; FY27 matches the AOP brand build (Report 14), "
                 "measured against the FY25 actual from seeds/skus.csv.")

    ch = chart_line("r66_pva.png", list(pv.Period),
                    {"Plan ($M/mo)": [float(x) for x in pv.plan],
                     "Actual ($M/mo)": [float(x) for x in pv.act]},
                    title="Crunchwell monthly revenue, plan versus actual ($M)")
    m.image(ch, "The consistency of the gap is the diagnosis: this is base erosion, not promotional "
                "timing.")

    m.h1("YEAR ONE", "2 · The four FY2027 workstreams")
    m.h2("2.1 · Pack Refresh")
    m.body(
        "Hero SKUs re-skinned, on shelf August 15 2026, $28M year-one revenue target at a "
        "confidence score of 0.82 — the largest near-term bet in the innovation pipeline. It is also "
        "the anchor of the Louisiana recovery, which is why the date matters more than the design.")
    m.h2("2.2 · Louisiana")
    m.body(
        f"Louisiana share bottomed at {la.cw.min():.2f}% and has recovered to {la.cw.iloc[-1]:.2f}%. "
        "The recovery plan has three legs — facings, availability, demand — in that order, with "
        "named owners and a 12-week measurement point (Report 76).")
    m.h2("2.3 · Relevance platform")
    m.body(
        "A new creative platform launching with the pack, briefed against Relevance and Modernity "
        "rather than value or heritage (Report 65). Creator-first in the South, where the loss is "
        "concentrated.")
    m.h2("2.4 · Trade reset")
    m.body(
        f"Crunchwell carries ${cwt.spend_m:.1f}M of trade at {cwt.depth:.1f}% average depth for an "
        f"index of {cwt.incr:.2f}. FY2027 caps Mega depth at 20%, reduces event count by about 15% "
        "and targets an index of 0.60 — without a list-price change, because Mega elasticity of "
        "−1.84 to −2.12 means price cuts buy volume and lose the reference price.")

    m.h1("NOT DOING", "3 · What we are explicitly not doing")
    m.bullets([
        "**Not cutting list price.** Elasticity data says it erodes the base permanently.",
        "**Not adding Kids Sweet innovation.** The segment is −2.8%; that is HoneyNest's problem and "
        "it is being harvested (Report 69).",
        "**Not chasing protein with Crunchwell branding.** ProteinPeak owns that ground and we would "
        "cannibalise the growth brand.",
        "**Not defending every DMA.** The under-indexed Northeast stays under-indexed in FY2027; the "
        "South is where the money goes.",
    ])

    grows = [[r.geo_name[:26], f"{r.fy25:.1f}%", f"{r.q126:.1f}%", f"{int(r.bps)}",
              r.priority_tier[:18]] for r in geo.head(8).itertuples()]
    m.h1("GEOGRAPHY", "4 · Where the brand is actually losing")
    m.table(["Market", "FY25 share", "Q1 FY26 share", "Δ bps", "Tier"], grows,
            widths=[0.32, 0.16, 0.16, 0.14, 0.22], size=9.0,
            note="Source: seed_geographies.")
    m.callout("Birmingham and Memphis",
              "Both show the same early pattern Louisiana showed in Q4 2025: a 30 basis point drift "
              "with no local event to explain it. Weekly facing and OSA monitoring in both DMAs costs "
              "almost nothing and buys a quarter of warning. It is in the FY27 plan.", "action")

    m.h1("STOP CONDITIONS", "5 · When the committee should stop funding this")
    m.body(
        "These are agreed now, while everyone is calm, so that the conversation in eighteen months "
        "is about facts rather than intentions.")
    m.table(["Condition", "Measured at", "Consequence"],
            [["Louisiana share below 4.0%", "Q4 FY2027",
              "Reallocate Louisiana trade and media to ProteinPeak and TrailGrove; Crunchwell to "
              "maintenance A&P"],
             ["Pack Refresh ACV below 80%", "Q4 FY2027",
              "No further pack investment before renegotiating at Q1 FY28 line reviews"],
             ["Relevance below 63", "Q4 FY2028", "Stop the platform; move Crunchwell to a harvest plan"],
             ["Trade index below 0.55", "Q4 FY2027", "Trade Finance takes calendar control from the "
              "NAM team"]],
            widths=[0.28, 0.16, 0.56], align_right_from=9, size=9.0,
            note="Measures from syndicated_weekly, sku_authorization, brand_equity_quarterly, "
                 "seed_trade_promo_events_q1_2026.")

    m.decisions([["Commit to stabilisation, not growth, in FY2027", "Cory Whitman", "Jul 2026",
                  "Action"],
                 ["Approve the four Year-1 workstreams and owners", "SteerCo", "Jul 2026", "Action"],
                 ["Agree the four stop conditions and consequences", "SteerCo / CFO", "Jul 2026",
                  "Action"],
                 ["Report Year-1 lead measures monthly", "Cory Whitman", "Aug 2026", "On track"]])
    m.recommendations([
        ("Approve the three-year staged commitment", "SteerCo", "July 2026"),
        ("Hold Pack Refresh at August 15 with weekly stage-gate reporting", "Cory Whitman",
         "From Jul 15"),
        ("Stand up Birmingham and Memphis early-warning monitoring", "Jordan Hsu", "By Aug 15"),
        ("Review against the four stop conditions at the Q4 FY27 SteerCo", "SteerCo", "Q4 FY2027"),
    ])
    m.signoff([("Cory Whitman, Brand Director", "the commitments and lead measures"),
               ("CFO", "the stop conditions and their consequences"),
               ("VP Brand", "the platform and A&P mix shift")])
    return m.build()


# ============================================= 67 · ProteinPeak plan narrative =
def r67_proteinpeak_narrative():
    m = Memo("67-proteinpeak-fy27-brand-plan-narrative-roadmap.docx",
             kicker="BRAND PLAN NARRATIVE · FY2027",
             title="ProteinPeak FY2027 Plan and Innovation Roadmap",
             subtitle="A brand with a structural tailwind, a proven launch and a distribution "
                      "problem at the two largest retailers in America",
             byline="Sage Park, Brand Director — ProteinPeak",
             meta=["Period: FY2027, with a roadmap to FY2029",
                   "Companion deck: Report 48", "Version: v1 · July 2026"],
             short="ProteinPeak FY27 plan",
             doc_type="Internal brand plan")

    wp25 = q.cat_row("FY2025", "Wellness Protein")
    wpq2 = q.cat_row("Q2-FY2026-MTD", "Wellness Protein")
    tgt = q.cat_row("Q2-FY2026-MTD", "Wellness Protein", "Target Total US")
    wmt = q.cat_row("Q2-FY2026-MTD", "Wellness Protein", "Walmart Total US")
    pv = q.pva_brand_month("ProteinPeak")
    sk = q.skus("ProteinPeak")
    pipe = q.pipeline()
    pp_pipe = pipe[pipe.brand == "ProteinPeak"]
    sent = q.sentiment()

    m.at_a_glance([(f"{wpq2.growth:+.1f}%", "segment growth Q2 QTD"),
                   (f"{wpq2.acme_share:.1f}%", "Acme segment share"),
                   ("53%", "launch volume new to brand"),
                   (q.m0(q.PLAN['fy27_brand']['ProteinPeak']), "FY27 revenue target")])

    m.h1("THE OPPORTUNITY", "1 · The only brand in the house with a tailwind")
    m.body(
        f"Wellness Protein grew {wp25.growth:+.1f}% to ${wp25.size:,.0f}M in FY2025 and is running "
        f"{wpq2.growth:+.1f}% in Q2 FY2026. Acme's share of the segment moved from "
        f"{wp25.acme_share:.1f}% to {wpq2.acme_share:.1f}% on the back of the April 20 launch of "
        "Cinnamon Crunch (PP005) and Cocoa Almond (PP006). Every other brand in the portfolio is "
        "fighting its segment; this one is being carried by it.")
    m.body(
        f"Monthly performance tells the story cleanly. Q1 ran about "
        f"{money(float(pv.act.iloc[0]), dp=2)} per month against a "
        f"{money(float(pv.plan.iloc[0]), dp=2)} plan — a deliberate pre-launch draw-down at "
        f"{float(pv['var'].iloc[0]):+.1f}%. April and May ran about "
        f"{money(float(pv.act.iloc[-1]), dp=2)} at {float(pv['var'].iloc[-1]):+.1f}%. The trough was "
        "planned; the recovery is real.")

    ch = chart_line("r67_pva.png", list(pv.Period),
                    {"Plan ($M/mo)": [float(x) for x in pv.plan],
                     "Actual ($M/mo)": [float(x) for x in pv.act]},
                    title="ProteinPeak monthly revenue, plan versus actual ($M)")
    m.image(ch, "The Q1 trough is the pre-launch pipeline draw-down. April and May are the first "
                "months of the new base.")

    m.h1("THE LAUNCH", "2 · What the first four weeks told us")
    m.bullets([
        "**Trial ran 110–113% of plan at Target** and 77–78% at the Walmart pilot. Same items, same "
        "price, different shelf.",
        "**Velocity was 17.5 units per store per week at Target** against 9.2 at Walmart — the "
        "difference is an endcap and Roundel support, not assortment.",
        "**53% of volume was new to Acme**, with 32% cannibalisation of the existing ProteinPeak "
        "line and 15% taken from competitors. That is a healthy line-extension profile.",
        "**Week-2 repeat ran 1.2 times the Berry Crunch archive** — the cleanest available signal "
        "that the product delivers against the claim.",
        f"**Social sentiment is {float(sent[sent.brand=='ProteinPeak'].sent.iloc[0]):+.2f}** on about "
        f"{int(sent[sent.brand=='ProteinPeak'].mentions.iloc[0])} mentions, the strongest in the "
        "portfolio.",
    ])

    m.h1("THE CONSTRAINT", "3 · We are under-distributed where the volume is")
    m.body(
        f"Acme holds {tgt.acme_share:.1f}% of Wellness Protein at Target and {wmt.acme_share:.1f}% at "
        "Walmart. Walmart is more than twice Target's size for Acme overall. The gap is not demand, "
        "price or product — it is assortment and merchandising.")
    chd = chart_bar("r67_retailer.png", ["Target", "US national", "Walmart"],
                    [float(tgt.acme_share), float(wpq2.acme_share), float(wmt.acme_share)],
                    title="Acme share of Wellness Protein, Q2 FY26 MTD (%)", pct=True,
                    colors_list=["#2E7D75", "#5B6472", "#B24A2E"])
    m.image(chd, "The same assortment performs three times better at one retailer than the other.")
    srows = [[r.sku_name.replace("ProteinPeak ", ""), f"${r.price:.2f}", f"{r.acv:.0f}%",
              money(r.rev) if r.rev else "launch year", r.status] for r in sk.itertuples()]
    m.table(["SKU", "Shelf price", "National ACV", "FY25 revenue", "Status"], srows,
            widths=[0.34, 0.16, 0.16, 0.18, 0.16],
            note="Source: seeds/skus.csv.")
    m.callout("The single highest-return action in this plan",
              "Cinnamon Crunch sits at 38% national ACV and Cocoa Almond at 28%, four months after "
              "launch. Getting both to Vanilla Almond's 54% is worth more than any media dollar we "
              "could spend in FY2027, and it costs line-review negotiation rather than budget.",
              "action")

    m.h1("THE PLAN", "4 · FY2027 on a page")
    m.table(["Pillar", "What we do", "Investment", "Success measure"],
            [["Distribution", "Full-line authorisation at Walmart and Kroger; Costco club pack",
              "Line-review support", "PP005 and PP006 ACV ≥55%"],
             ["Innovation", "Chocolate Almond through Q4 FY26 line reviews to Q1 FY27 shelf",
              "Stage-gate funded", "Top-two-box ≥55% held post-launch"],
             ["Creator media", "Athlete-anchored programme whitelisted into paid social and Roundel",
              "≈$9M", "Sentiment ≥+0.40"],
             ["Retail media", "Weighted to Walmart Connect (1.20) and Kroger Precision (0.77)",
              "≈$6.5M", "Blended modelled ratio ≥1.0"],
             ["Price discipline", "$7.49 held; maximum 10% depth; no stacking", "—",
              "Trade rate ≤13% of gross"]],
            widths=[0.16, 0.36, 0.18, 0.30], align_right_from=9, size=9.0,
            note="Source: seed_marketing_spend, seed_retail_media_spend_q1_2026, "
                 "seed_concept_test_chocolate_almond, seed_trade_spend_fy25. FY27 figures are targets.")

    prows = [[r.concept_name[:40], r.stage_gate, str(r.planned_launch_date),
              q.musd(r.projected_revenue_year1_musd), f"{r.confidence_score_0to1}"]
             for r in pp_pipe.itertuples()]
    m.h1("ROADMAP", "5 · FY2027 to FY2029")
    m.table(["Concept", "Stage", "Planned launch", "Year-1 revenue", "Confidence"], prows,
            widths=[0.34, 0.20, 0.16, 0.16, 0.14], align_right_from=2, size=9.0,
            note="Source: seeds/innovation_pipeline.csv.")
    chr_ = chart_line("r67_roadmap.png", ["FY25", "FY26E", "FY27T", "FY28T", "FY29T"],
                      {"ProteinPeak revenue ($M)": [48, 62, 100, 125, 150]},
                      title="ProteinPeak revenue roadmap ($M) — FY27 onward are targets")
    m.image(chr_, "The roadmap: distribution in FY27, the bar segment in FY28, mid-teens segment "
                  "share by FY29.")
    m.bullets([
        "**FY2027 ($100M target):** full distribution at Walmart and Kroger, Chocolate Almond in "
        "market. This is the AOP commitment (Report 14).",
        "**FY2028 ($125M target):** ProteinPeak Bars 12g opens the $2.96B granola-bar segment.",
        "**FY2029 ($150M target):** 12–14 SKUs at a mid-teens share of a segment we expect to reach "
        "roughly $1.45B.",
    ])

    m.h1("COMPETITION", "6 · Larksfield has already answered")
    m.body(
        "Larksfield launched a 14 gram protein line extension (LF-FH-14P) on May 12 2026, escalating "
        "on both the protein and Louisiana fronts simultaneously. Our answer is Chocolate Almond — "
        "64% top-two-box against a 55% action standard, clearing the 12 point substitutional "
        "cannibalisation gate at 8 points — taken to the Q4 FY26 line reviews. It is not a price "
        "response, and it should not become one.")

    m.risks([["Larksfield escalates further in protein", "Slows our share build in the best segment",
              "Accelerate Chocolate Almond; hold Target endcap through Q3", "Sage Park"],
             ["Walmart authorisation does not land", "FY27 target unreachable on distribution alone",
              "Escalate to the August line review as a joint growth case (Report 77)",
              "Marcus Boudreaux"],
             ["Cannibalisation of PP001–PP003 exceeds 8 points steady-state",
              "Net revenue benefit of the launch is overstated",
              "Re-read source of volume at week 13 post-Chocolate-Almond launch", "Maya Chen"],
             ["Premium price erodes through retailer-funded depth",
              "Brand loses its premium position permanently",
              "10% depth cap enforced through the RGM policy (Report 64)", "Trade Finance"]])

    m.recommendations([
        ("Put ProteinPeak full-line authorisation on the Walmart August line-review agenda",
         "Marcus Boudreaux", "Aug line review"),
        ("Approve Chocolate Almond for the Q4 FY26 Walmart and Target line reviews",
         "Innovation SteerCo", "Aug 5 2026"),
        ("Weight FY27 retail media to Walmart Connect and Kroger Precision", "Tasha Brooks",
         "FY27 planning"),
        ("Hold $7.49 and the 10% depth cap through the launch year", "Sage Park", "FY2027"),
        ("Add velocity by retailer to the monthly brand scorecard", "Sage Park", "From August"),
    ])
    return m.build()


# ============================================== 68 · Chocolate Almond memo =====
def r68_chocolate_almond_memo():
    m = Memo("68-proteinpeak-chocolate-almond-steerco-decision-memo.docx",
             kicker="DECISION MEMORANDUM · INNOVATION STEERCO",
             title="ProteinPeak Chocolate Almond — Recommendation to Proceed",
             subtitle="Concept test results against the action standard and the cannibalisation "
                      "gate, and what we recommend the SteerCo decide",
             byline="Maya Chen, Senior Insights Analyst (Innovation & Foresight)",
             meta=["To: Innovation SteerCo · Decision date: August 5 2026",
                   "Companion deck: Report 49", "Version: v1 · July 2026"],
             short="Choc Almond memo",
             doc_type="Internal decision memorandum")

    ct = q.concept_test()

    def v(metric, default="n/a"):
        r = ct[ct.metric == metric]
        return r.value.iloc[0] if len(r) else default

    m.at_a_glance([(f"{v('top_two_box_pct')}%", "top-two-box"),
                   (f"{v('action_standard_threshold_pct')}%", "action standard"),
                   ("8pp", "substitutional cannibalisation"), ("12pp", "SteerCo gate")])

    m.h1("RECOMMENDATION", "1 · What we are asking for")
    m.lede("Both gates clear. We recommend Chocolate Almond proceeds to Stage-4 and into the Q4 "
           "FY2026 Walmart and Target line reviews.")
    m.body(
        f"Chocolate Almond scores {v('top_two_box_pct')}% top-two-box purchase intent against an "
        f"action standard of {v('action_standard_threshold_pct')}%. That is "
        f"{v('delta_vs_launch_sku_pretest_pp')} points above the pretest for the SKUs we launched in "
        f"April — which are themselves running at 110–113% of trial plan at Target — and "
        f"{v('delta_vs_cereal_innovation_benchmark_pp')} points above the five-year cereal-innovation "
        "benchmark. Substitutional cannibalisation against the existing ProteinPeak line is 8 points "
        "against a 12 point SteerCo gate.")

    m.h1("METHOD", "2 · Sample and design")
    m.table(["Item", "Detail"],
            [["Sample size", f"n={v('n_total')}"],
             ["Field period", f"{v('field_period_start')} to {v('field_period_close')}"],
             ["Design", "Standard Acme monadic cereal-innovation concept test"],
             ["Action standard", f"{v('action_standard_threshold_pct')}% top-two-box"],
             ["Cohort recuts", "Protein-curious, lapsed-cereal, current-Crunchwell"],
             ["Cannibalisation method", "Stated-choice overlap decomposed into additive and "
                                        "substitutional"]],
            widths=[0.28, 0.72], align_right_from=9, size=9.5,
            note="Source: seed_concept_test_chocolate_almond.")

    ch = chart_bar("r68_topline.png",
                   ["Chocolate Almond", "Action standard", "Launch-SKU pretest",
                    "5-yr innovation benchmark"],
                   [float(v('top_two_box_pct')), float(v('action_standard_threshold_pct')),
                    float(v('top_two_box_pct')) - float(v('delta_vs_launch_sku_pretest_pp')),
                    float(v('top_two_box_pct')) - float(v('delta_vs_cereal_innovation_benchmark_pp'))],
                   title="Top-two-box purchase intent (%)", pct=True,
                   colors_list=["#2E7D75", "#5B6472", "#3E6DA8", "#B98A2E"])
    m.image(ch, "Topline result against the standard and the two available benchmarks.")

    m.h1("COHORTS", "3 · The concept works where we need it to")
    m.table(["Cohort", "Top-two-box", "Read"],
            [["Protein-curious", "71%", "Strongest cell; purchase-intent mean 3.06/5"],
             ["Lapsed-cereal", "66%", "Clears comfortably; the occasion-recovery cohort"],
             ["Current-Crunchwell", "52%", "Below standard — and correctly so"],
             ["Total sample", f"{v('top_two_box_pct')}%",
              f"Clears the {v('action_standard_threshold_pct')}% standard"]],
            widths=[0.30, 0.20, 0.50], align_right_from=1, total_row=True, size=9.5,
            note="Source: seed_concept_test_chocolate_almond, cohort section.")
    m.body(
        "The current-Crunchwell result is worth dwelling on. A 52% score there is not a weakness — "
        "this SKU is not built to convert the family-cereal base, and if it did we would be reading "
        "a cannibalisation problem rather than an incrementality one. The concept is doing exactly "
        "what a protein line extension should do.")
    m.body(
        "The context supports it: chocolate as a breakfast flavour preference indexes 14 points "
        "higher in the protein-curious cohort per the April 2026 usage and attitude study, and the "
        "cinnamon flavour renaissance trend runs at 0.81 strength. We are riding two real "
        "preferences, not a novelty score.")

    m.h1("CANNIBALISATION", "4 · The gate that actually matters")
    chc = chart_bar("r68_cannib.png", ["Additive", "Substitutional", "SteerCo gate",
                                       "vs Crunchwell (subst.)"],
                    [14, 8, 12, 2], title="Cannibalisation decomposition (percentage points)",
                    colors_list=["#2E7D75", "#3E6DA8", "#B24A2E", "#5B6472"])
    m.image(chc, "22% overlap with the launch SKUs decomposes into 14 points additive and 8 points "
                 "substitutional, inside the 12 point gate.")
    m.bullets([
        "**Versus the ProteinPeak launch SKUs:** 22% stated overlap, 14 points additive, 8 points "
        "substitutional. Gate is 12 points. **Passes.**",
        "**Versus Crunchwell:** 6% overlap, 2 points substitutional. Negligible, as expected.",
        "**Post-launch re-read committed:** we will re-measure source of volume at week 13 and hold "
        "ourselves to the same 12 point standard on actual behaviour rather than stated choice.",
    ])
    m.callout("The honest caveat",
              "Stated-choice cannibalisation understates real substitution roughly as often as it "
              "overstates it. An 8 point result against a 12 point gate is a pass with four points "
              "of headroom, not a comfortable margin. The week-13 behavioural re-read is the control, "
              "and it should carry a consequence if it fails.", "risk")

    m.h1("TIMING", "5 · Why the decision cannot wait")
    m.body(
        "Larksfield launched a 14 gram protein line extension on May 12 2026 and is escalating on "
        "the protein front. A Q1 FY2027 shelf date for Chocolate Almond requires authorisation at "
        "the Q4 FY2026 Walmart and Target line reviews. Missing those reviews costs two quarters and "
        "hands the flavour space to a competitor who has already shown they will take it.")
    comp = q.comp_launches("2025-08-01")
    crows = [[r.brand, r.sku_new, str(r.launch_date), str(r.claim)[:40], f"{r.buzz:.2f}"]
             for r in comp.head(6).itertuples()]
    m.table(["Brand", "SKU", "Launch", "Claim", "Buzz d30"], crows,
            widths=[0.18, 0.18, 0.14, 0.36, 0.14], align_right_from=4, size=9.0,
            note="Source: seed_competitor_launches.")

    m.decisions([["Advance Chocolate Almond to Stage-4 Pre-Launch", "Innovation SteerCo", "Aug 5",
                  "Action"],
                 ["Include in Q4 FY26 Walmart and Target line reviews",
                  "Marcus Boudreaux / Soo-jin Lee", "Q4 FY26", "Action"],
                 ["Hold the 12pp substitution gate as a post-launch measure", "Maya Chen",
                  "Q1 FY27 +13wk", "On track"],
                 ["Brief creator and media plans off the protein-curious cohort", "Sage Park",
                  "Sep 15", "On track"]])
    m.recommendations([
        ("Approve Stage-4 progression", "Innovation SteerCo", "Aug 5 2026"),
        ("Authorise inclusion in the Q4 FY26 line reviews", "Innovation SteerCo", "Aug 5 2026"),
        ("Commit to the week-13 behavioural re-read with a defined consequence", "Maya Chen",
         "Q1 FY27 + 13 weeks"),
        ("Brief media and creator plans against the protein-curious cohort, not the general "
         "population", "Sage Park / Hugo Lin", "By Sep 15"),
    ])
    return m.build()


# ================================================ 69 · HoneyNest decision memo =
def r69_honeynest_decision():
    m = Memo("69-honeynest-portfolio-role-and-mascot-decision-memo.docx",
             kicker="DECISION MEMORANDUM",
             title="HoneyNest — Portfolio Role and the Mascot Question",
             subtitle="A well-executed brand in a structurally declining segment, and the two "
                      "decisions that follow from that",
             byline="HoneyNest Brand Manager with Consumer Insights and Finance",
             meta=["To: VP Brand and the CFO", "Companion deck: Report 50",
                   "Version: v1 · July 2026"],
             short="HoneyNest decision",
             doc_type="Internal decision memorandum")

    ks24 = q.cat_row("FY2024", "Kids Sweet")
    ks25 = q.cat_row("FY2025", "Kids Sweet")
    pv = q.pva_brand_month("HoneyNest")
    tb = q.trade_brand()
    hn = tb[tb.brand == "HoneyNest"].iloc[0]
    mac = q.macro(10)
    pipe = q.pipeline()
    hn_pipe = pipe[pipe.brand == "HoneyNest"]

    m.at_a_glance([(f"{float(pv['var'].mean()):+.1f}%", "FY26 variance to plan"),
                   (f"{ks25.growth:+.1f}%", "Kids Sweet segment growth"),
                   (f"${hn.spend_m:.1f}M", "FY25 trade spend"),
                   ("Harvest", "recommended role")])

    m.h1("THE SITUATION", "1 · Good management, wrong room")
    m.lede("HoneyNest is one of the best-executed brands in the portfolio. That is the problem, not "
           "the consolation.")
    m.body(
        f"HoneyNest runs {float(pv['var'].mean()):+.1f}% against plan across FY2026 — better than "
        f"every brand except RootDay. It does that inside a segment that fell from "
        f"${ks24.size:,.0f}M to ${ks25.size:,.0f}M, a decline of {ks25.growth:+.1f}%. Two consecutive "
        "years of segment decline, with the mom-guilt trend at 0.68 strength and low-sugar pressure "
        "at 0.72, is not a cycle. It is a structural position.")
    m.body(
        f"We spend ${hn.spend_m:.1f}M of trade at {hn.depth:.1f}% average depth for an incrementality "
        f"index of {hn.incr:.2f}. That is buying volume in a segment that is leaving, at a moment "
        "when Wellness Protein next door is growing +18.3% a year.")

    ch = chart_bar("r69_segments.png",
                   ["Kids Sweet FY24", "Kids Sweet FY25", "Family Sweet FY25",
                    "Wellness Protein FY25"],
                   [float(ks24.growth), float(ks25.growth), 1.4, 18.3],
                   title="Segment growth comparison (% YoY)", pct=True,
                   colors_list=["#B24A2E", "#B24A2E", "#B98A2E", "#2E7D75"])
    m.image(ch, "The same shelf space and trade dollars are worth far more one segment over.")

    m.h1("THE OPTIONS", "2 · Three ways to play it")
    m.table(["Option", "What it means", "FY27–FY29 revenue", "Investment", "Verdict"],
            [["A · Invest", "Fund a kids-cereal relaunch, new mascot, media support",
              "$92M → $96M → $99M", "≈$12M incremental A&P", "Reject"],
             ["B · Harvest", "Hold distribution, A&P to maintenance, LTOs only, cut trade depth",
              "$92M → $88M → $84M", "≈$1M A&P", "Recommend"],
             ["C · Reposition", "Move the brand into Family Wholegrain with a whole-grain-plus line",
              "$92M → $94M → $97M", "≈$5M plus R&D", "Recommend as a bet inside B"]],
            widths=[0.13, 0.34, 0.20, 0.19, 0.14], align_right_from=9, status_col=4, size=9.0,
            note="Revenue paths are planning estimates. Source: seed_category_market_size, "
                 "seeds/innovation_pipeline.csv, seed_macro_trends.")
    m.callout("Why Option A is rejected",
              "A relaunch spends FY2027 growth money on the least favourable structural position in "
              "the portfolio, against a 0.68-strength parental-guilt trend. The same $12M behind "
              "ProteinPeak distribution or TrailGrove range extension returns more, with less "
              "execution risk.", "risk")

    m.h1("THE MASCOT", "3 · The second decision, and why it is separate")
    m.body(
        "The mascot question has been raised repeatedly as though it were the brand's problem. It is "
        "not. Aided awareness of the portfolio's kid-facing assets is healthy and the equity data "
        "shows no meaningful trust or affection deficit. Retiring the mascot inside a harvest plan "
        "would spend real money — pack changeover, asset re-shoot, retailer re-listing — to solve "
        "something the data does not identify as a cause.")
    m.bullets([
        "**Recommendation: retire the mascot only if Option C proceeds.** A whole-grain "
        "repositioning needs a different visual language; a harvest does not.",
        "**If Option B alone proceeds, keep the mascot** and spend nothing on the change.",
        "**Either way, do not run a mascot decision as a standalone project.** It is a consequence "
        "of the portfolio role, not an alternative to choosing one.",
    ])

    m.h1("EVIDENCE", "4 · The trend backdrop")
    mrows = [[r.topic, f"{r.strength:.2f}", r.direction, str(r.cats)[:28]]
             for r in mac.itertuples() if any(t in str(r.topic).lower()
                                              for t in ["mom-guilt", "sugar", "glp", "protein",
                                                        "sustainab", "lto"])]
    m.table(["Trend", "Strength", "Direction", "Categories"], mrows,
            widths=[0.34, 0.14, 0.24, 0.28], align_right_from=1, size=9.0,
            note="Source: seed_macro_trends, filtered to trends bearing on kids' cereal.")

    prows = [[r.concept_name[:40], r.stage_gate, str(r.planned_launch_date),
              q.musd(r.projected_revenue_year1_musd), q.dash(r.status)]
             for r in hn_pipe.itertuples()]
    m.h1("PIPELINE", "5 · What HoneyNest has in the tank")
    m.table(["Concept", "Stage", "Planned launch", "Year-1 revenue", "Status"], prows,
            widths=[0.34, 0.22, 0.16, 0.14, 0.14], align_right_from=2, size=9.0,
            note="Source: seeds/innovation_pipeline.csv.")

    m.decisions([["Adopt Option B (managed harvest) as HoneyNest's portfolio role from FY2027",
                  "VP Brand / CFO", "FY27 plan", "Action"],
                 ["Fund Option C as a single Stage-2 concept, not a relaunch", "Innovation SteerCo",
                  "Q4 FY26", "Action"],
                 ["Confirm Q3 FY26 discontinuation of Granola Crunch and Cookie Dough",
                  "HoneyNest BM", "Q3 FY26", "On track"],
                 ["Defer the mascot decision until the Option C gate", "VP Brand", "Q4 FY26", "Watch"],
                 ["Redirect ≈$8M of trade and A&P to ProteinPeak and TrailGrove", "CFO", "FY27 plan",
                  "Action"]])
    m.recommendations([
        ("Approve Option B with Option C as a funded concept bet", "VP Brand / CFO", "FY27 planning"),
        ("Keep the Birthday Cake LTO as the one active FY27 innovation", "HoneyNest BM", "Q4 FY26"),
        ("Reduce promoted event count in line with the harvest decision", "HoneyNest BM / Trade Finance",
         "FY27 calendar"),
        ("Revisit the portfolio role if Kids Sweet returns to growth for two consecutive quarters",
         "Category Insights", "Quarterly"),
    ])
    return m.build()


# ==================================================== 70 · GLP-1 POV memo ======
def r70_glp1_pov():
    m = Memo("70-glp-1-category-headwind-strategic-pov.docx",
             kicker="STRATEGIC POINT OF VIEW",
             title="GLP-1 and the Cereal Category — What We Believe and What We Are Doing",
             subtitle="A structural volume headwind, the evidence we have, the evidence we do not, "
                      "and the four plan responses",
             byline="Nina Ortega, VP Consumer Insights, with Strategy",
             meta=["Audience: executive committee and the FY27–FY29 planning process",
                   "Version: v1 · July 2026"],
             short="GLP-1 POV",
             doc_type="Internal point of view")

    mac = q.macro(12)
    glp = mac[mac.topic.str.contains("GLP", case=False)].iloc[0]
    coh = q.cohorts()
    c25 = q.catgrowth("FY2025")
    ssc = q.cat_row("FY2025", "Single-Serve Cups")
    wp = q.cat_row("FY2025", "Wellness Protein")

    m.at_a_glance([(f"{glp.strength:.2f}", "trend strength"),
                   (glp.direction[:14], "direction"),
                   (f"{coh['cereal-skipper'].iloc[-1] - coh['cereal-skipper'].iloc[0]:+.1f} pp",
                    "cereal-skipper households"),
                   ("4", "plan responses")])

    m.h1("THE POSITION", "1 · What we believe")
    m.lede("GLP-1 adoption is a slow, structural volume headwind for family-size cereal — not a "
           "demand shock, and not a reason to reprice the portfolio.")
    m.body(
        f"The GLP-1 appetite shift registers at {glp.strength:.2f} strength in our trend framework "
        f"with a direction of \"{glp.direction}\", affecting {glp.cats}. It sits alongside — and "
        "partly explains — the most important number in our panel data: cereal-skipper household "
        f"penetration rose from {coh['cereal-skipper'].iloc[0]:.1f}% to "
        f"{coh['cereal-skipper'].iloc[-1]:.1f}% over six quarters, while loyal-family penetration "
        f"fell from {coh['loyal-family'].iloc[0]:.1f}% to {coh['loyal-family'].iloc[-1]:.1f}%.")
    m.body(
        "We are deliberately not claiming a causal attribution. We cannot separate GLP-1 effects "
        "from broader occasion loss with the instruments we have. What we can say is that both "
        "point the same direction and both argue for the same set of responses, which is enough to "
        "plan against.")

    ch = chart_line("r70_cohorts.png", list(coh.index),
                    {c: [float(x) for x in coh[c]] for c in coh.columns},
                    title="Household penetration by cohort (%)", pct=True)
    m.image(ch, "Cereal-skipper and protein-returner households grow; loyal-family erodes. The "
                "occasion is the battleground.")

    m.h1("THE EVIDENCE", "2 · What we have and what we do not")
    m.table(["Evidence", "What it shows", "Confidence"],
            [["Trend framework", f"GLP-1 at {glp.strength:.2f} strength, downward volume direction",
              "Medium — directional, not quantified"],
             ["Kantar-shape cohort panel",
              f"Cereal-skipper +{coh['cereal-skipper'].iloc[-1] - coh['cereal-skipper'].iloc[0]:.1f} pp "
              "over six quarters", "High on the measure, low on the cause"],
             ["Category size data",
              "RTE total US growing on value (+1.3%) with softer unit growth", "High"],
             ["Segment mix",
              f"Wellness Protein +{wp.growth:.1f}%, single-serve cups +{ssc.growth:.1f}%",
              "High"],
             ["Direct GLP-1 usage measurement", "Not instrumented", "None — this is the gap"]],
            widths=[0.26, 0.46, 0.28], align_right_from=9, size=9.0,
            note="Source: seed_macro_trends, kantar_worldpanel_cohort, seed_category_market_size.")
    m.callout("The instrumentation gap we should close",
              "We do not ask about GLP-1 use in the brand-health survey. Adding a single screening "
              "question would let us cut every tracker measure by GLP-1 status within two waves, and "
              "would cost almost nothing. It is the highest-value change available to the tracker.",
              "action")

    m.h1("IMPLICATIONS", "3 · What it means for the category")
    m.bullets([
        "**Volume pressure lands hardest on family-size packs.** Smaller appetites mean fewer "
        "servings per household, which pressures the 18oz and larger formats first.",
        "**Value can hold while volume falls.** Premium price-per-serving formats — protein, "
        "single-serve, functional — can offset unit decline in revenue terms.",
        "**Protein is the permission structure.** A shrinking appetite raises the premium on "
        "nutrient density per serving, which is exactly ProteinPeak's proposition.",
        "**Kids' cereal is doubly exposed** — GLP-1 in the adult household plus the 0.68-strength "
        "parental-guilt trend. This is part of the HoneyNest harvest logic (Report 69).",
        "**Promotion does not fix it.** Discounting a pack size the household no longer needs buys "
        "pantry loading, not consumption.",
    ])

    seg = c25.head(8)
    chs = chart_bar("r70_segments.png", [s[:18] for s in seg.subcategory],
                    [float(x) for x in seg.growth], title="Segment growth, FY2025 (% YoY)",
                    pct=True,
                    colors_list=["#2E7D75" if v > 5 else ("#B98A2E" if v > 0 else "#B24A2E")
                                 for v in seg.growth])
    m.image(chs, "The segments growing fastest are the ones with the highest nutrient density or "
                 "the smallest serving size — or both.")

    m.h1("RESPONSES", "4 · The four things already in the plan")
    m.table(["Response", "Where it sits", "Owner"],
            [["Fund protein ahead of family-size volume",
              "FY27 AOP (Report 61); ProteinPeak plan (Report 67)", "Sage Park / CFO"],
             ["Build single-serve and convenience formats",
              "MorningOats cups; RootDay single-serve carton (Report 51)", "Brand teams"],
             ["Pack architecture for smaller portions and higher price-per-serving",
              "RGM policy (Report 64)", "RGM Lead"],
             ["Harvest, not relaunch, in Kids Sweet", "HoneyNest decision (Report 69)",
              "VP Brand"]],
            widths=[0.34, 0.44, 0.22], align_right_from=9, size=9.0)
    m.body(
        "Note what is not on that list: a price response, a volume-chasing promotional response, or "
        "a new category entry. A slow structural headwind is answered with mix, not with depth.")

    m.h1("WHAT WOULD CHANGE OUR MIND", "5 · The falsification tests")
    m.bullets([
        "**Cereal-skipper penetration flattens for three consecutive quarters** while family-size "
        "volume recovers — that would suggest the occasion loss was cyclical.",
        "**Single-serve and protein growth decelerates below category growth** — that would suggest "
        "the nutrient-density thesis is wrong.",
        "**A GLP-1 screening question shows no difference in cereal behaviour by usage status** — "
        "that would falsify the mechanism directly, and it is the test we should build.",
    ])

    m.recommendations([
        ("Add a GLP-1 usage screening question to the brand-health survey", "Nina Ortega",
         "Next wave"),
        ("Add a GLP-1 volume sensitivity to the FY27–FY29 long-range plan", "Strategy / FP&A",
         "Q4 FY26"),
        ("Report the cereal-skipper cohort as a standing KPI in the category review",
         "Jordan Hsu", "From August"),
        ("Re-issue this point of view annually with the falsification tests scored",
         "Nina Ortega", "July 2027"),
    ])
    return m.build()


if __name__ == "__main__":
    for fn in [r61_fy27_aop_narrative, r62_lrp_narrative, r63_h2_reforecast_memo,
               r64_rgm_policy, r65_crunchwell_creative_brief, r66_crunchwell_turnaround_memo,
               r67_proteinpeak_narrative, r68_chocolate_almond_memo, r69_honeynest_decision,
               r70_glp1_pov]:
        print("built", os.path.basename(fn()))
