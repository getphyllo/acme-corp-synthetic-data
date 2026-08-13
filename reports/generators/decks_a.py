"""PPTX decks 41-51 — enterprise, strategy and brand. Run: python generators/decks_a.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import (money, chart_line, chart_bar, chart_grouped, chart_stacked,
                 chart_waterfall, chart_donut)
from pptx_lib import Deck
import qlib as q


# ============================================================== 41 · Q2 QBR ==
def r41_company_q2_qbr():
    k = Deck("41-acme-q2-2026-company-business-review.pptx",
             kicker="QUARTERLY BUSINESS REVIEW",
             title="Acme Corp — Q2 FY2026 Company Business Review",
             subtitle="Enterprise performance through May, the ProteinPeak launch read, "
                      "and what it means for the back half",
             byline="Diane Halverson, VP Sales NA (sponsor) · Finance & Insights (prep) · July 2026",
             short="Q2 2026 Company BR")

    p1, a1, v1 = q.pva_total(q.Q1)
    p2, a2, v2 = q.pva_total(q.Q2)
    pm = q.pva_month()
    bd = q.pva_brand(q.Q2)
    sh = q.share_quarter()
    rm = q.retail_media()

    k.agenda(["Where the quarter landed", "Brand-by-brand read", "Share and category context",
              "The ProteinPeak launch, four weeks in", "Louisiana: is the recovery working?",
              "Spend efficiency — trade and retail media", "Supply and service",
              "Risks into H2", "The ask"])

    k.exec_summary(
        f"Q2 FY2026 through May ran {money(a2)} against {money(p2)} of plan ({v2:+.1f}%) — a two-point "
        f"improvement on Q1's {v1:+.1f}%, and the first quarter since the Louisiana break where the "
        "trend line moves the right way. The improvement is almost entirely ProteinPeak coming out of "
        "its pre-launch trough. Crunchwell has not yet turned.",
        tiles=[(f"{v2:+.1f}%", "Q2 QTD revenue vs plan"), (f"{v1:+.1f}%", "Q1 revenue vs plan"),
               (f"{sh.acme.iloc[-1]:.2f}%", "Acme national RTE share"),
               (f"${rm.inc_m.sum()/rm.spend_m.sum():.2f}", "retail-media incremental per $1")],
        bullets=[
            f"**Revenue:** {money(a2)} vs {money(p2)} plan QTD. April {money(float(pm.act.iloc[3]))} "
            f"({pm['var'].iloc[3]:+.1f}%), May {money(float(pm.act.iloc[4]))} ({pm['var'].iloc[4]:+.1f}%) — "
            "the gap narrows month on month.",
            "**ProteinPeak** moved from −25.4% (Q1, pre-launch) to −6.1% in May on the back of the "
            "April 20 Cinnamon Crunch and Cocoa Almond launch. Trial is running 110–113% of plan at Target.",
            "**Crunchwell** is still −5.7 to −6.0% every month. Louisiana has recovered ~35 bps off the "
            "trough but is nowhere near the 6.4% starting point. The Pack Refresh (Aug 15) is the next lever.",
            "**Efficiency, not demand,** is the CFO's issue: retail media returns "
            f"${rm.inc_m.sum()/rm.spend_m.sum():.2f} per $1 with Amazon Ads at "
            f"{rm[rm.platform=='Amazon Ads'].ratio.iloc[0]:.2f}, and trade incrementality sits at 0.52.",
        ])

    ch = chart_line("r41_month.png", list(pm.Period),
                    {"Plan": [float(x) for x in pm.plan], "Actual": [float(x) for x in pm.act]},
                    title="Net revenue, plan vs actual ($M/month)", h=3.0)
    k.chart_bullets("THE NUMBER", "Five months of a closing gap", ch,
                    ["**Plan is flat** at $63.7M/month — the FY26 operating plan was built straight-lined.",
                     "**Actuals ran $60.3–60.4M** through Q1, then stepped up to $61.5M and $61.6M "
                     "in April and May as launch volume shipped.",
                     "**The gap halves** from −5.4% at the February low to −3.4% in May.",
                     "**Read:** the H2 reforecast (Report 44) should assume the improvement holds, "
                     "not that it accelerates."],
                    note="Source: plan_vs_actual, periods 2026-01 to 2026-05.")

    rows = [[r.Brand, money(r.plan), money(r.act), f"{r.var:+.1f}%",
             "On track" if r.var > -3 else ("Watch" if r.var > -10 else "Action")]
            for r in bd.itertuples()]
    rows.append(["Total Acme", money(p2), money(a2), f"{v2:+.1f}%", "Watch"])
    chb = chart_bar("r41_brandvar.png", list(bd.Brand), [float(x) for x in bd["var"]],
                    title="Q2 QTD revenue variance to plan, by brand (%)", pct=True,
                    colors_list=["#2E7D75" if v > -3 else ("#B98A2E" if v > -10 else "#B24A2E")
                                 for v in bd["var"]], h=3.0)
    k.chart_table("BRAND READ", "Four of six brands inside two points of plan", chb,
                  ["Brand", "Plan", "Actual", "Var", "Status"], rows,
                  widths=[0.30, 0.18, 0.18, 0.16, 0.18], total_row=True, status_col=4,
                  note="Source: plan_vs_actual, 2026-04 and 2026-05.")

    la = q.share_quarter(la=True)
    ch2 = chart_line("r41_share.png", list(sh.q),
                     {"Acme national": [float(x) for x in sh.acme],
                      "Crunchwell national": [float(x) for x in sh.cw],
                      "Crunchwell Louisiana": [float(x) for x in la.cw]},
                     title="RTE-cereal value share (%)", pct=True, h=3.0)
    k.chart("SHARE", "National share holds; Louisiana is the hole in the floor", ch2,
            lede="Acme all-brand share is flat-to-up nationally. The share problem is one DMA deep.",
            note="Source: syndicated_weekly, RTE Cereal. Canonical LA headline (Mass/Grocery, "
                 "peak-to-trough) is 6.4% → 3.0%, −340 bps; the all-channel value-weighted cut shown "
                 "here is milder in the same direction.")

    cat = q.catgrowth("FY2025")
    top = cat.head(6)
    chc = chart_bar("r41_cat.png", [t[:16] for t in top.subcategory], [float(x) for x in top.growth],
                    title="Category growth by subcategory, FY25 (% YoY)", pct=True, color="teal", h=2.9)
    k.chart_bullets("CATEGORY", "Where we play decides how hard we have to run", chc,
                    ["**Wellness Protein** grew +18.3% to $840M and is +18.6% again in Q2 QTD. "
                     "Acme share there moved 7.6% → 8.4%.",
                     "**Family Sweet** — Crunchwell's home — grew +1.4%. A flat brand in a flat "
                     "segment is a share-neutral, growth-negative position.",
                     "**Kids Sweet is −2.8%.** HoneyNest is executing well inside a shrinking pocket "
                     "(see the portfolio decision, Report 50).",
                     "**Oat milk +18.8%** is RootDay's tailwind and the most under-funded upside "
                     "in the portfolio."],
                    note="Source: seed_category_market_size, FY2025 US National.")

    k.tiles("LAUNCH READ", "ProteinPeak, four weeks in",
            [("110–113", "trial index at Target", "vs plan; Walmart pilot 77–78"),
             ("53%", "new-to-brand volume", "32% cannibalization, 15% competitive"),
             ("1.2×", "week-2 repeat", "vs Berry Crunch archive"),
             ("+0.44", "social sentiment", "~496 mentions in 2026"),
             ("17.5", "Target velocity", "units/store/week vs 9.2 Walmart")],
            body="The launch is working where it was designed to work. Target over-indexes for "
                 "Wellness Protein (18.4% Acme share vs 5.2% at Walmart), and the endcap plus Roundel "
                 "package converted. The Walmart pilot is the underperformer and needs a distribution "
                 "fix, not a media fix.",
            note="Source: seed_proteinpeak_q2_launch, household_transactions PP005/PP006, "
                 "social_mentions, seed_category_market_size.")

    rmr = [[r.platform, money(r.spend_m), money(r.inc_m, dp=2), f"{r.ratio:.2f}",
            "Reinvest" if r.ratio >= 1 else "Reallocate"] for r in rm.itertuples()]
    rmr.append(["Total", money(rm.spend_m.sum()), money(rm.inc_m.sum(), dp=2),
                f"{rm.inc_m.sum()/rm.spend_m.sum():.2f}", "Rebalance"])
    k.table("EFFICIENCY", "Retail media: one platform is carrying the ratio",
            ["Platform", "Spend", "Incremental", "Incr. ratio", "Call"], rmr,
            widths=[0.34, 0.16, 0.18, 0.16, 0.16], total_row=True, status_col=4,
            callout=("The $700K question",
                     "Moving ~$700K out of Amazon Ads into Walmart Connect, Kroger Precision and a "
                     "Louisiana injection converts $0.40-per-dollar spend into $1.20-per-dollar spend. "
                     "It is the cheapest incremental revenue available to us in H2.", "action"),
            note="Source: seed_retail_media_spend_q1_2026, modelled incrementality (not platform ROAS).")

    k.risk("RISKS", "What we are watching into H2",
           [["Larksfield's 14g protein line (LCH00032, May 12)",
             "Slows ProteinPeak's share build in its best pocket",
             "Accelerate Chocolate Almond to the Q4 line reviews; hold Target endcap through Q3",
             "Sage Park"],
            ["Crunchwell Pack Refresh slips past Aug 15",
             "Louisiana recovery loses its anchor and Q4 shipment build",
             "Weekly stage-gate with R&D and packaging; pre-build hero SKUs",
             "Cory Whitman"],
            ["Amazon Ads spend not reallocated",
             "≈$0.6M of avoidable H2 inefficiency at current ratios",
             "Reallocation decision at the July commercial review",
             "Tasha Brooks"],
            ["GLP-1 volume drag (trend strength 0.81)",
             "Structural pressure on family-size cereal volume",
             "Pack-architecture work in the RGM plan (Report 45)",
             "RGM Lead"]],
           note="Source: seed_competitor_launches, seed_innovation_pipeline, seed_macro_trends.")

    k.reco("THE ASK", "Four decisions out of this review",
           [("Approve the $700K retail-media reallocation out of Amazon Ads into Walmart Connect, "
             "Kroger Precision and Louisiana", "Tasha Brooks / CFO", "By Aug 1"),
            ("Hold the FY26 revenue commitment on the protein build; reforecast H2 on May's run-rate, "
             "not on Q1's", "Finance", "H2 reforecast, July"),
            ("Fix Walmart ProteinPeak distribution at the August line review rather than adding media",
             "Marcus Boudreaux", "Aug line review"),
            ("Confirm Pack Refresh on-shelf for Aug 15 with a weekly stage-gate",
             "Cory Whitman", "From July 15")])

    k.close("The trend turned. The base has not.",
            [f"Q2 QTD {v2:+.1f}% vs plan, improving from {v1:+.1f}% in Q1.",
             "ProteinPeak is doing its job — 53% of launch volume is new to Acme.",
             "Crunchwell is still −6% a month, and that is the FY27 problem.",
             "Today's decision is the $700K reallocation."])
    return k.build()


# ==================================================== 42 · FY27 AOP pre-read ==
def r42_fy27_aop_board_preread():
    k = Deck("42-acme-fy27-annual-operating-plan-board-preread.pptx",
             kicker="ANNUAL OPERATING PLAN · BOARD PRE-READ",
             title="Acme Corp FY2027 Annual Operating Plan",
             subtitle="The revenue build, the margin path to 16%, and the four bets the plan rests on",
             byline="Finance & FP&A, reviewed with the CFO · for the October board meeting · July 2026",
             short="FY27 AOP pre-read")

    p1, a1, v1 = q.pva_total(q.Q1)
    bd = q.pva_brand(q.Q1)

    k.agenda(["FY26 landing zone", "The FY27 revenue build", "Brand-level plan",
              "Margin path to 16% EBITDA", "Where the growth money goes",
              "Capacity and supply assumptions", "Risks and sensitivities", "The approval ask"])

    P = q.PLAN
    f25 = q.brand_fy25()
    deltas, residual = q.fy27_build()

    k.exec_summary(
        f"The FY2027 plan targets {q.m0(P['fy27_rev'])} of net revenue — roughly "
        f"{(P['fy27_rev'] / P['fy25_rev'] - 1) * 100:+.0f}% on the {q.m0(P['fy25_rev'])} FY25 base — "
        f"and starts the margin climb from {P['fy25_ebitda']:.1f}% to the "
        f"{P['fy28_ebitda']:.0f}%-by-FY28 commitment. Growth is loaded onto Wellness Protein and oat "
        "milk, not onto pricing, and the FY26 variance to plan is carried as an explicit risk overlay "
        "rather than absorbed into productivity.",
        tiles=[(q.m0(P['fy27_rev']), "FY27 net revenue target"),
               (f"{(P['fy27_rev'] / P['fy25_rev'] - 1) * 100:+.0f}%", "growth on the FY25 base"),
               (f"~{P['fy27_ebitda']:.1f}%", "FY27 EBITDA margin target"),
               (f"~{q.m0(P['trade_envelope'])}", "FY27 trade envelope")],
        bullets=[
            f"**The number:** {q.m0(P['fy27_rev'])} net revenue and ~{P['fy27_ebitda']:.1f}% EBITDA "
            f"margin, consistent with the FY27 AOP (Report 14) and the long-range plan (Report 15).",
            f"**FY26 is the risk overlay, not the base.** Q1 landed {money(a1)} against {money(p1)} of "
            f"plan ({v1:+.1f}%); every FY27 initiative carries a named owner who reports deviation "
            "monthly.",
            f"**The build is bottom-up:** ProteinPeak "
            f"{q.m0(f25['ProteinPeak'])} → {q.m0(P['fy27_brand']['ProteinPeak'])} carries "
            f"{deltas['ProteinPeak'] / sum(v for v in deltas.values() if v > 0) * 100:.0f}% of the "
            "gross brand growth; the Pack Refresh anchors Crunchwell stabilisation.",
            f"**Margin comes out of trade,** not A&P: the ~{q.m0(P['trade_envelope'])} envelope holds "
            "while incrementality moves 0.52 → 0.60.",
            "**All FY27 figures are plan targets**, not measured results.",
        ], headline="What the board is being asked to approve")

    order = ["ProteinPeak", "RootDay", "TrailGrove", "Crunchwell", "MorningOats", "HoneyNest"]
    wf = chart_waterfall(
        "r42_build.png",
        [b.replace("Protein", "Protein\n").replace("Morning", "Morning\n") for b in order]
        + ["Adjacency\n& mix"],
        [deltas[b] for b in order] + [residual],
        title=f"FY25 ${P['fy25_rev']:,.0f}M → FY27 ${P['fy27_rev']:,.0f}M: the bridge ($M) — "
              f"planning estimate", unit="")
    k.chart("THE BUILD", f"{q.m0(P['fy27_rev'])} is one big bet and five small ones", wf,
            lede=f"Bars are movements off the {q.m0(P['fy25_rev'])} FY25 base. Every block is a named, "
                 "owned initiative — nothing in the build is unallocated growth.",
            note="Planning estimate. FY25 brand base from seeds/skus.csv; FY27 brand targets per the "
                 "FY27 AOP (Report 14); adjacency and mix is the derived residual to "
                 f"{q.m0(P['fy27_rev'])}.")

    carries = {"Crunchwell": "Pack Refresh + Louisiana recovery",
               "TrailGrove": "Granola and bar distribution build",
               "MorningOats": "Single-serve cups (+9.8% segment)",
               "HoneyNest": "Managed decline, Kids Sweet −2.8%",
               "ProteinPeak": "Full-year PP005/PP006 + Chocolate Almond",
               "RootDay": "Oat milk segment +18.8%"}
    rows = [[b, q.m0(f25[b]), q.m0(P['fy27_brand'][b]),
             f"{(P['fy27_brand'][b] / f25[b] - 1) * 100:+.0f}%", carries[b]]
            for b in ["Crunchwell", "TrailGrove", "ProteinPeak", "MorningOats", "HoneyNest", "RootDay"]]
    rows.append(["Six brands", q.m0(sum(f25.values())), q.m0(sum(P['fy27_brand'].values())),
                 f"{(sum(P['fy27_brand'].values()) / sum(f25.values()) - 1) * 100:+.0f}%",
                 f"+ adjacency to {q.m0(P['fy27_rev'])}"])
    k.table("BRAND PLAN", "FY2027 by brand — the drag is deliberate",
            ["Brand", "FY25 actual", "FY27 target", "Growth", "What carries it"], rows,
            widths=[0.17, 0.16, 0.15, 0.13, 0.39], total_row=True, align_right_from=1,
            note="FY25 from seeds/skus.csv; FY27 targets are the AOP brand build (Report 14). "
                 f"Brand total reconciles to {q.m0(P['fy27_rev'])} with non-brand and adjacency revenue.")

    tb = q.trade_brand()
    cht = chart_bar("r42_trade.png", list(tb.brand), [float(x) for x in tb.incr],
                    title="FY25 trade incrementality index, by brand", color="sky", h=2.8)
    k.chart_bullets("MARGIN", "The margin comes out of trade, not out of A&P", cht,
                    [f"**${tb.spend_m.sum():.0f}M of trade spend** in FY25 at a portfolio "
                     f"incrementality index of {tb.incr.mean():.2f}. Every 0.01 of index is real money.",
                     f"**Crunchwell alone is ${tb.spend_m.iloc[0]:.1f}M** at "
                     f"{tb.depth.iloc[0]:.1f}% average depth — the heaviest promoted line in the house.",
                     "**FY27 assumption:** portfolio index 0.52 → 0.60 through fewer, deeper, "
                     "better-timed events. Worth roughly 60 bps of EBITDA.",
                     "**A&P holds** in absolute dollars and shifts mix toward retail media and "
                     "creator, per the media effectiveness read (Report 55)."],
                    note="Source: seed_trade_spend_fy25, seed_trade_promo_events_q1_2026.")

    k.two_col("ASSUMPTIONS", "What has to be true",
              "Operating assumptions",
              ["Fill rate holds at ~95% and OTIF at ~90% — no repeat of the Nov 2025 storm impact.",
               "Pack Refresh ships Aug 15 2026 and is fully distributed by Q4.",
               "Wellness Protein segment growth stays in the mid-teens.",
               "No incremental list-price increase in FY27; mix and pack architecture only.",
               "Trade calendar rebuilt to 0.60 incrementality without volume loss."],
              "Sensitivities (FY27 revenue)",
              ["Pack Refresh slips one quarter: −$7M.",
               "Wellness Protein growth halves to +9%: −$12M on ProteinPeak.",
               "Louisiana stays at 3.0% share rather than recovering to 4.5%: −$3M.",
               "Trade index stalls at 0.52: no revenue effect, −60 bps EBITDA.",
               "GLP-1 volume drag one point worse than assumed: −$5M."],
              note="Sensitivities are planning estimates, not modelled forecasts.")

    k.reco("THE ASK", "What we need from the board",
           [(f"Approve the {q.m0(P['fy27_rev'])} FY27 revenue plan and the ~{P['fy27_ebitda']:.1f}% "
             "EBITDA target", "Board", "October 2026"),
            ("Approve the trade-efficiency programme as the primary margin lever (0.52 → 0.60)",
             "CFO / RGM Lead", "October 2026"),
            ("Note the FY27–FY29 long-range plan (Report 43) as the frame for this AOP",
             "CEO / Strategy", "October 2026"),
            ("Approve capex for Pack Refresh changeover and protein line capacity",
             "CFO / VP Supply Chain", "October 2026")])

    k.close("Fund the protein, stabilise the core, take the margin out of trade.",
            [f"{q.m0(P['fy27_rev'])} and ~{P['fy27_ebitda']:.1f}% — the AOP the long-range plan implies.",
             f"ProteinPeak carries {q.m0(deltas['ProteinPeak'])} of the {q.m0(sum(v for v in deltas.values() if v > 0))} "
             "of gross brand growth.",
             f"The {P['fy28_ebitda']:.0f}% FY28 margin commitment stays intact."])
    return k.build()


# ============================================== 43 · FY27-FY29 long-range plan =
def r43_long_range_plan():
    k = Deck("43-acme-fy27-fy29-long-range-strategic-plan.pptx",
             kicker="LONG-RANGE PLAN · FY27–FY29",
             title="Acme Corp Three-Year Strategic Plan",
             subtitle="From a flat cereal franchise to a portfolio weighted toward where the "
                      "category is actually growing",
             byline="CEO Gregory Whitfield & Strategy · executive committee review · July 2026",
             short="FY27–FY29 LRP")

    cat25 = q.catgrowth("FY2025")
    wp = q.cat_row("FY2025", "Wellness Protein")
    P = q.PLAN
    f25 = q.brand_fy25()

    k.agenda(["The strategic problem in one page", "Three-year financial frame",
              "Portfolio: where we play by FY29", "Bet 1 — win Wellness Protein",
              "Bet 2 — stabilise the Crunchwell core", "Bet 3 — better-for-you adjacency",
              "Bet 4 — commercial efficiency", "What we stop doing", "Milestones and gates"])

    k.exec_summary(
        f"Acme is the #4 US RTE cereal player with a {q.m0(P['fy25_rev'])} FY25 base growing ~5% and "
        "a portfolio weighted three-quarters into segments growing 1% or less. The three-year job is "
        "not to grow the existing mix faster — it is to change the mix. The plan takes net revenue to "
        f"{q.m0(P['fy27_rev'])} in FY27, {q.m0(P['fy28_rev'])} in FY28 and ~$1.02B in FY29, with "
        "nearly a third of that revenue in double-digit-growth segments.",
        tiles=[("$1.02B", "FY29 revenue target"),
               (f"{P['fy28_ebitda']:.0f}%", "EBITDA margin by FY28"),
               ("29%", "FY29 revenue in high-growth segments"),
               ("$150M", "ProteinPeak FY29 target")],
        bullets=[
            f"**The category is not the problem.** RTE Cereal total US grew +1.3% to $8.35B; "
            f"Wellness Protein grew {wp.growth:+.1f}% to ${wp.size:,.0f}M. We are under-weight "
            "in the only pockets that compound.",
            "**Crunchwell is 38% of revenue and flat for six quarters.** Stabilising it — not "
            "reviving it to growth — is the realistic FY27–FY29 commitment (Report 47).",
            f"**Protein is the engine:** ProteinPeak {q.m0(f25['ProteinPeak'])} FY25 → "
            f"{q.m0(P['fy27_brand']['ProteinPeak'])} FY27 → $150M FY29 target, taking Acme's "
            "Wellness Protein share from 7.6% toward the mid-teens.",
            "**Efficiency funds the transition:** trade incrementality 0.52 → 0.65 and retail-media "
            "ratio 0.65 → 1.00 over three years release the money for it.",
            "**All FY27–FY29 figures are targets and commitments**, not forecasts.",
        ], headline="The three-year thesis")

    traj = chart_line("r43_traj.png", ["FY25", "FY26E", "FY27T", "FY28T", "FY29T"],
                      {"Net revenue ($M)": [P['fy25_rev'], P['fy26_rev'], P['fy27_rev'],
                                            P['fy28_rev'], P['fy29_rev']]},
                      title="Net revenue trajectory ($M) — FY27+ are targets", h=2.9)
    marg = chart_line("r43_margin.png", ["FY25", "FY26E", "FY27T", "FY28T", "FY29T"],
                      {"EBITDA margin (%)": [P['fy25_ebitda'], P['fy26_ebitda'], P['fy27_ebitda'],
                                             P['fy28_ebitda'], P['fy29_ebitda']]},
                      title="EBITDA margin path (%) — FY27+ are targets", pct=True, h=2.9)
    k.charts2("FINANCIAL FRAME", "Growth reaccelerates as mix shifts; margin steps to 16% in FY28",
              traj, marg,
              captions=["FY26 is the transition year on the $63.7M/month plan basis. The step-up comes "
                        "with a full year of protein plus the Pack Refresh.",
                        f"The {P['fy28_ebitda']:.0f}% FY28 commitment is unchanged from the board plan; "
                        "FY29 holds it while revenue grows."],
              note="FY25 actual and the FY26 plan basis per FACTS.md; FY27–FY29 are the targets set in "
                   "the FY27 AOP (Report 14) and the long-range plan (Report 15).")

    core25 = f25["Crunchwell"] + f25["HoneyNest"]
    bfy25 = f25["TrailGrove"] + f25["MorningOats"]
    hg25 = f25["ProteinPeak"] + f25["RootDay"]
    core27 = P["fy27_brand"]["Crunchwell"] + P["fy27_brand"]["HoneyNest"]
    bfy27 = P["fy27_brand"]["TrailGrove"] + P["fy27_brand"]["MorningOats"]
    hg27 = P["fy27_brand"]["ProteinPeak"] + P["fy27_brand"]["RootDay"]
    core29, bfy29, hg29 = 400.0, 270.0, 300.0          # FY29 targets
    mix = chart_stacked("r43_mix.png", ["FY25 actual", "FY27 target", "FY29 target"],
                        {"Cereal core (Crunchwell, HoneyNest)": [core25, core27, core29],
                         "Better-for-you (TrailGrove, MorningOats)": [bfy25, bfy27, bfy29],
                         "High-growth (ProteinPeak, RootDay)": [hg25, hg27, hg29],
                         "Other and adjacency":
                             [P['fy25_rev'] - core25 - bfy25 - hg25,
                              P['fy27_rev'] - core27 - bfy27 - hg27,
                              P['fy29_rev'] - core29 - bfy29 - hg29]},
                        title="Revenue mix by portfolio role ($M) — FY27+ are targets", h=3.0)
    k.chart_bullets("PORTFOLIO", "The mix shift is the strategy", mix,
                    [f"**Cereal core holds flat then drifts down** — deliberately, from "
                     f"{q.m0(core25)} to {q.m0(core29)}. We stop funding volume in Kids Sweet "
                     "(−2.8% segment) and reinvest.",
                     f"**High-growth nearly triples** from {q.m0(hg25)} to {q.m0(hg29)}, driven by "
                     "ProteinPeak and RootDay in segments growing +18%.",
                     "**Better-for-you grows modestly** on distribution, not innovation spend.",
                     f"**By FY29, {hg29 / P['fy29_rev'] * 100:.0f}% of revenue** sits in "
                     f"double-digit-growth segments against {hg25 / P['fy25_rev'] * 100:.0f}% today."],
                    note="Planning estimate. FY25 base from seeds/skus.csv brand revenue.")

    seg = cat25.head(8)
    chs = chart_bar("r43_seg.png", [s[:17] for s in seg.subcategory],
                    [float(x) for x in seg.growth],
                    title="Segment growth, FY25 (% YoY)", pct=True, color="teal", h=3.0)
    k.chart_table("BET 1 · PROTEIN", "Win the segment that compounds", chs,
                  ["Metric", "FY25", "FY29 target"],
                  [["Wellness Protein segment size", f"${wp.size:,.0f}M", "$1.45B"],
                   ["Acme share of segment", f"{wp.acme_share:.1f}%", "≈14%"],
                   ["ProteinPeak revenue", q.m0(f25['ProteinPeak']), "$150M"],
                   ["SKUs in market", "6", "12–14"],
                   ["Retailers with full line", "Target, Amazon, WFM", "+Walmart, Kroger, Costco"]],
                  widths=[0.46, 0.27, 0.27],
                  note="Source: seed_category_market_size, seeds/skus.csv. FY29 column is a target.")

    k.two_col("BETS 2 & 3", "Hold the core, extend the adjacency",
              "Bet 2 — stabilise Crunchwell",
              ["Relevance, not Trust: equity work targets Relevance 62.7 → 67 by FY29 (Report 46).",
               "Pack Refresh (Aug 2026, $28M year-1) then Mega Family Pack and Maiz Crunch.",
               "Louisiana back to 4.5%+ share; Birmingham and Memphis defended before they break.",
               "Trade rate down from 25.6% of gross toward 22% without losing base volume."],
              "Bet 3 — better-for-you adjacency",
              ["RootDay rides oat milk +18.8%: single-serve carton and coffee creamer concepts.",
               "TrailGrove granola/bars distribution build — the cheapest volume in the portfolio.",
               "MorningOats single-serve cups (+9.8% segment) as the convenience play.",
               "No new categories outside cereal, oats, granola and plant-based milk through FY29."],
              note="Source: brand_equity_quarterly, seed_innovation_pipeline, seed_category_market_size.")

    k.table("WHAT WE STOP", "Three years of discipline means a stop list",
            ["Stop / exit", "Why", "When", "Freed resource"],
            [["RootDay Coconut Blend, HoneyNest Granola Crunch, HoneyNest Cookie Dough",
              "Sub-scale, low velocity, negative contribution", "Q3 FY26", "≈$1.5M trade + shelf"],
             ["Linear TV as Crunchwell's dominant channel ($24M/yr)",
              "Reach without relevance; CTV and retail media out-perform on modelled incrementality",
              "FY27 planning", "≈$8M to reallocate"],
             ["Amazon Ads at current weight (ratio 0.40)",
              "Lowest incremental return of the four retail-media platforms", "H2 FY26",
              "≈$0.7M immediately, more in FY27"],
             ["Kids Sweet innovation beyond LTOs",
              "Segment is −2.8% and structurally pressured by mom-guilt trend (0.68)",
              "FY27 plan", "R&D capacity to protein"]],
            widths=[0.34, 0.32, 0.14, 0.20], align_right_from=9, size=9.5,
            note="Source: seed_innovation_pipeline (Discontinue), seed_marketing_spend, "
                 "seed_retail_media_spend_q1_2026, seed_macro_trends.")

    k.reco("GATES", "How the executive committee holds this plan to account",
           [(f"Approve the FY27–FY29 frame: {q.m0(P['fy27_rev'])} FY27 → ~$1.02B FY29 at "
             f"{P['fy28_ebitda']:.0f}% margin, and the mix-shift target",
             "Executive committee", "July 2026"),
            ("Gate 1 — Pack Refresh in market and Louisiana above 4.0% share",
             "Cory Whitman", "Q4 FY26"),
            ("Gate 2 — ProteinPeak above $100M run-rate with full Walmart and Kroger distribution",
             "Sage Park / Marcus Boudreaux", "Q4 FY27"),
            ("Gate 3 — portfolio trade incrementality above 0.60 and retail-media ratio above 0.85",
             "RGM Lead / Tasha Brooks", "FY28 planning"),
            ("Annual re-baseline of the LRP against the AOP each July",
             "Strategy / FP&A", "Every July")])

    k.close("Change the mix, or run harder for the same result.",
            ["The cereal core is defended, not grown.",
             "Nearly a third of the company sits in high-growth segments by FY29.",
             f"{q.m0(P['fy27_rev'])} FY27, ~$1.02B FY29 and {P['fy28_ebitda']:.0f}% margin are the "
             "commitments; the mix shift is how they happen."])
    return k.build()


# ================================================= 44 · H2 FY26 reforecast ====
def r44_h2_reforecast():
    k = Deck("44-acme-h2-2026-reforecast-risks-opportunities.pptx",
             kicker="OPERATING PLAN REFORECAST",
             title="Acme Corp H2 FY2026 Reforecast",
             subtitle="Q3 and Q4 rebuilt off the May run-rate, with the risk and opportunity "
                      "ledger behind the number",
             byline="Finance & FP&A · commercial review, July 2026",
             short="H2 FY26 reforecast")

    pm = q.pva_month()
    p1, a1, v1 = q.pva_total(q.Q1)
    p2, a2, v2 = q.pva_total(q.Q2)
    exit_rr = float(pm.act.iloc[-1])

    k.agenda(["Where we are", "How the reforecast is built", "Q3 and Q4 by quarter",
              "Brand-level reforecast", "Risk and opportunity ledger",
              "Cash and trade implications", "What we need decided"])

    k.exec_summary(
        f"May shipped {money(exit_rr)} against a {money(float(pm.plan.iloc[-1]))} monthly plan. "
        f"Holding that run-rate and adding the two known H2 events — the Aug 15 Pack Refresh and a "
        "full quarter of ProteinPeak distribution — gives an H2 landing zone of $379M against $382M "
        "of original plan. We are recommending the reforecast be set there and the full-year "
        "commitment held.",
        tiles=[("$379M", "H2 FY26 reforecast"), ("−0.8%", "reforecast vs original H2 plan"),
               (f"{v2:+.1f}%", "Q2 QTD variance being carried"), ("$14M", "net risk-adjusted exposure")],
        bullets=[
            "**Build method:** May exit run-rate × months, plus Pack Refresh pipeline fill, plus "
            "ProteinPeak distribution gains, less HoneyNest discontinuations.",
            f"**Q1 + Q2 QTD** ran {money(a1 + a2)} against {money(p1 + p2)} of plan.",
            "**The reforecast is not a cut to the full-year commitment.** It reallocates the shortfall "
            "into the two quarters that can carry it.",
            "**All H2 figures are forecast**, built on measured Jan–May actuals.",
        ], headline="The reforecast in four lines")

    ch = chart_bar("r44_quarters.png", ["Q1 actual", "Q2 QTD actual", "Q3 forecast", "Q4 forecast"],
                   [a1, a2, 189.0, 190.0], title="Net revenue by quarter ($M) — Q3/Q4 forecast",
                   color="navy", unit="M", h=2.9)
    k.chart_bullets("THE SHAPE", "H2 carries a modest sequential build", ch,
                    ["**Q3 ($189M forecast)** is the Pack Refresh pipeline quarter — shipment-led, "
                     "with consumption following in Q4.",
                     "**Q4 ($190M forecast)** adds full ProteinPeak distribution and the HoneyNest "
                     "Birthday Cake LTO, less the three discontinued SKUs.",
                     "**Neither quarter assumes** a Louisiana share recovery beyond the ~35 bps "
                     "already measured in Q2.",
                     "**Downside case** is $369M if the Pack Refresh slips a quarter; upside $389M "
                     "if Walmart protein distribution lands early."],
                    note="Source: plan_vs_actual (Q1/Q2 actuals); Q3/Q4 are forecasts built off the "
                         "May run-rate.")

    k.table("LEDGER", "Risks and opportunities behind the H2 number",
            ["Item", "Type", "H2 $ impact", "Probability", "Owner"],
            [["Pack Refresh on-shelf Aug 15 as planned", "Opportunity", "+$6.0M", "High", "Cory Whitman"],
             ["Walmart ProteinPeak full-line authorisation", "Opportunity", "+$4.5M", "Medium",
              "Marcus Boudreaux"],
             ["Retail-media reallocation ($700K, 2.2× LA ROI)", "Opportunity", "+$1.6M", "High",
              "Tasha Brooks"],
             ["Larksfield 14g line takes protein share", "Risk", "−$3.5M", "Medium", "Sage Park"],
             ["Louisiana recovery stalls at 3.0% share", "Risk", "−$2.5M", "Medium", "Marcus Boudreaux"],
             ["Pack Refresh slips to Q4", "Risk", "−$6.0M", "Low", "Cory Whitman"],
             ["H-E-B Cinnamon Twist delist (risk score 0.80)", "Risk", "−$1.8M", "Medium",
              "Marcus Boudreaux"],
             ["Net risk-adjusted position", "Net", "−$1.4M", "—", "Finance"]],
            widths=[0.40, 0.12, 0.15, 0.15, 0.18], total_row=True, align_right_from=2, size=9.5,
            note="Source: seed_innovation_pipeline, seed_competitor_launches, "
                 "seed_heb_cinnamon_twist_delist_risk, seed_retail_media_spend_q1_2026. "
                 "Dollar impacts are planning estimates.")

    tb = q.trade_brand()
    cht = chart_bar("r44_trade.png", list(tb.brand), [float(x) for x in tb.spend_m],
                    title="FY25 trade spend by brand ($M)", color="gold", unit="M", h=2.8)
    k.chart_table("TRADE & CASH", "The H2 trade calendar is where the flexibility sits", cht,
                  ["Lever", "H2 effect"],
                  [["Rebuild Q4 Crunchwell events at lower depth", "≈$2.1M spend, index 0.52 → 0.58"],
                   ["Shift two Kids Sweet events to LTO support", "≈$0.6M reallocated"],
                   ["Fund LA recovery leg from national contingency", "$0.9M, 2.2× ROI"],
                   ["Hold ProteinPeak trade rate at ~12.9%", "Protects launch margin"],
                   ["Net H2 trade spend", "≈$71M, flat to plan"]],
                  widths=[0.5, 0.5], align_right_from=9, total_row=True,
                  note="Source: seed_trade_spend_fy25, seed_trade_promo_events_q1_2026. "
                       "H2 figures are planning estimates.")

    k.reco("DECISIONS", "What the reforecast needs to be real",
           [("Set the H2 reforecast at $379M and hold the FY26 full-year commitment",
             "CFO / Finance", "July 2026"),
            ("Release the $700K retail-media reallocation now, not at the FY27 planning cycle",
             "Tasha Brooks", "By Aug 1"),
            ("Confirm Pack Refresh Aug 15 with a named slip-trigger and a Q4 fallback plan",
             "Cory Whitman", "By Jul 15"),
            ("Take a Cinnamon Twist recovery plan to H-E-B before the Sep 15 review",
             "Marcus Boudreaux", "By Sep 1")])

    k.close("Hold the year. Move the money.",
            ["$379M in H2 is achievable off the May run-rate.",
             "Three opportunities are worth more than the three biggest risks.",
             "Both live decisions are ours, not the market's."])
    return k.build()


# ============================================================ 45 · RGM deck ===
def r45_rgm_price_pack():
    k = Deck("45-acme-fy26-fy27-revenue-growth-management-price-pack.pptx",
             kicker="REVENUE GROWTH MANAGEMENT",
             title="Price, Pack and Promotion Architecture",
             subtitle="Where our net revenue actually leaks, and the FY27 price-pack architecture "
                      "that stops it",
             byline="RGM Lead with Trade Finance · reviewed with the CFO · July 2026",
             short="FY26–27 RGM")

    tb = q.trade_brand()
    ev = q.trade_events("brand")
    el = q.elasticity()

    k.agenda(["The leak, sized", "Trade spend by brand", "Promotion effectiveness",
              "Price elasticity by SKU", "Pack architecture", "The FY27 guardrails",
              "What changes on Monday"])

    k.exec_summary(
        f"Acme spends ${tb.spend_m.sum():.0f}M a year on trade at a portfolio incrementality index of "
        f"{tb.incr.mean():.2f} — meaning roughly half of promoted volume would have happened anyway. "
        "Crunchwell is the concentration: heaviest spend, deepest discounts, most elastic SKUs. The "
        "FY27 architecture trades event frequency for event quality and puts a floor under everyday price.",
        tiles=[(f"${tb.spend_m.sum():.0f}M", "FY25 trade spend"),
               (f"{tb.incr.mean():.2f}", "portfolio incrementality index"),
               (f"{tb.depth.iloc[0]:.1f}%", "Crunchwell average depth"),
               ("0.60", "FY27 index target")],
        bullets=[
            f"**Crunchwell carries ${tb.spend_m.iloc[0]:.1f}M** of the total at "
            f"{tb.depth.iloc[0]:.1f}% average depth and an index of {tb.incr.iloc[0]:.2f} — "
            "better than the portfolio average, but on a base so large that the absolute waste is the "
            "biggest single number in the P&L outside COGS.",
            "**Q1 FY26 ran 43 events, $11.6M of spend, $10.9M incremental** at an average modelled "
            "lift of 14.3% and an index of 0.52.",
            f"**The most elastic SKUs are the Mega packs** — {el.sku_name.iloc[0]} at "
            f"{el.elast.iloc[0]:.2f} at {el.retailer.iloc[0]}. They respond to price, which is exactly "
            "why they get promoted, and exactly why the base erodes.",
            "**FY27 architecture:** fewer, deeper, better-timed events; a defended everyday price "
            "ladder; and one new pack size to reset the value equation without cutting price.",
        ], headline="Where the net revenue goes")

    cht = chart_grouped("r45_trade.png", list(tb.brand),
                        {"Trade spend ($M)": [float(x) for x in tb.spend_m],
                         "Depth (%)": [float(x) for x in tb.depth]},
                        title="FY25 trade spend and average depth, by brand", h=3.0)
    rows = [[r.brand, money(r.spend_m), f"{r.depth:.1f}%", f"{r.incr:.2f}", f"{int(r.events)}"]
            for r in tb.itertuples()]
    rows.append(["Total / average", money(tb.spend_m.sum()), f"{tb.depth.mean():.1f}%",
                 f"{tb.incr.mean():.2f}", f"{int(tb.events.sum())}"])
    k.chart_table("THE SPEND", "Two brands account for three quarters of it", cht,
                  ["Brand", "Spend", "Depth", "Index", "Events"], rows,
                  widths=[0.34, 0.19, 0.16, 0.15, 0.16], total_row=True,
                  note="Source: seed_trade_spend_fy25.")

    erows = [[r.event_type if hasattr(r, "event_type") else r.brand, "", "", ""] for r in []]
    ev2 = q.trade_events("event_type")
    erows = [[r.event_type, f"{int(r.events)}", money(r.spend / 1000, dp=1),
              f"{r.lift:.1f}%", f"{r.idx:.2f}"] for r in ev2.itertuples()]
    k.table("EFFECTIVENESS", "Not all mechanics are worth running",
            ["Event type", "Events", "Spend", "Avg modelled lift", "Index"], erows,
            widths=[0.36, 0.14, 0.16, 0.19, 0.15],
            callout=("The rule we are adopting",
                     "Any mechanic with a modelled incrementality index below 0.45 comes off the "
                     "calendar unless it is defending a distribution commitment. On the Q1 base that "
                     "is roughly $2.4M of spend to redeploy.", "action"),
            note="Source: seed_trade_promo_events_q1_2026, modelled lift and incrementality.")

    che = chart_bar("r45_elast.png", [s.split(" ")[-2] + " " + s.split(" ")[-1] for s in el.sku_name],
                    [float(x) for x in el.elast],
                    title="Price elasticity by SKU × retailer (more negative = more elastic)",
                    color="rust", h=3.0)
    k.chart_bullets("ELASTICITY", "The packs we discount hardest are the ones that erode fastest", che,
                    [f"**{el.sku_name.iloc[0]} at {el.retailer.iloc[0]}** is the most elastic point in "
                     f"the portfolio at {el.elast.iloc[0]:.2f}.",
                     "**Rouses and Walmart** show the steepest curves — the two banners where "
                     "Larksfield has been most aggressive on endcaps in Louisiana.",
                     "**Implication:** deep Mega-pack discounting buys volume at a permanent cost to "
                     "the reference price. It is the mechanism behind the LA base erosion.",
                     "**FY27:** Mega discounting capped at 20% off, with feature-and-display weight "
                     "replacing depth."],
                    note="Source: seed_sku_elasticity_estimates (last recalibrated per row).")

    k.table("ARCHITECTURE", "The FY27 price-pack ladder",
            ["Pack", "Role", "Everyday price", "Promo policy"],
            [["Crunchwell 13oz Multigrain", "Entry / trial", "$4.49", "Max 15% off, 2 events/yr"],
             ["Crunchwell 14oz hero (post-refresh)", "Core volume", "$4.49", "Max 20% off, 4 events/yr"],
             ["Crunchwell 18oz Mega", "Value / pantry", "$5.49", "Max 20% off, 3 events/yr, no stacking"],
             ["Crunchwell 36oz Mega Family (2027-Q1)", "Value ceiling", "$8.99 target",
              "Launch support only, no depth"],
             ["ProteinPeak 12oz", "Premium / growth", "$7.49", "Max 10% off, feature-led"],
             ["ProteinPeak single-serve cup", "Convenience", "$9.99", "No depth; sampling instead"]],
            widths=[0.30, 0.18, 0.18, 0.34], align_right_from=9, size=9.5,
            note="Source: seeds/skus.csv shelf prices, seed_innovation_pipeline (36oz Mega Family, "
                 "2027-Q1). Promo policy is the proposed FY27 guardrail.")

    k.reco("GUARDRAILS", "What changes on Monday",
           [("Adopt the 0.45 incrementality floor for all new events; existing events reviewed at "
             "renewal", "RGM Lead / Trade Finance", "From Aug 1"),
            ("Cap Mega-pack depth at 20% and stop depth stacking with retailer funds",
             "Marcus Boudreaux / NAMs", "FY27 calendar"),
            ("Hold ProteinPeak trade rate at ≤13% of gross through the launch year", "Sage Park", "FY27"),
            ("Bring the 36oz Mega Family Pack forward into the FY27 innovation gate",
             "Innovation / RGM", "Q4 FY26 stage-gate"),
            ("Report portfolio index monthly alongside revenue in the commercial review",
             "Trade Finance", "From August")])

    k.close("Fewer events, better events, defended price.",
            [f"${tb.spend_m.sum():.0f}M at {tb.incr.mean():.2f} is the biggest efficiency pool we own.",
             "0.52 → 0.60 is worth roughly 60 bps of EBITDA.",
             "None of it requires a list-price increase."])
    return k.build()


# ================================================ 46 · Crunchwell FY27 plan ===
def r46_crunchwell_fy27_plan():
    k = Deck("46-crunchwell-fy27-brand-plan-relevance-platform.pptx",
             kicker="ANNUAL BRAND PLAN · FY2027",
             title="Crunchwell FY2027 Brand Plan",
             subtitle="Six flat quarters, one diagnosis: we have a relevance problem, not a trust problem",
             byline="Cory Whitman, Brand Director — Crunchwell · for VP Brand and the CFO · July 2026",
             short="Crunchwell FY27 plan")

    eq = q.equity_delta("Crunchwell", "US-NAT")
    sh = q.share_quarter()
    la = q.share_quarter(la=True)
    coh = q.cohorts()
    mk = q.mkt_spend("Crunchwell")
    sent = q.sentiment()

    k.agenda(["The situation", "Diagnosis: relevance, not trust", "Who is leaving and who is arriving",
              "Where the money goes today", "The creative platform recommendation",
              "The FY27 plan on a page", "Innovation and pack", "Measurement", "The ask"])

    k.exec_summary(
        "Crunchwell has held ~6.0% national value share for six quarters while the category grew and "
        "Larksfield's Field & Honey grew 7.4%. The equity tracker says why: Trust and Quality hold, "
        "Relevance is down 5.9 points and Modernity is soft. Consumers still believe in Crunchwell — "
        "they just do not think it is for them right now. FY27 is a relevance plan, not a value plan.",
        tiles=[(f"{[e for e in eq if e[0]=='Relevance'][0][3]:+.1f} pp", "Relevance, FY25Q1 → FY26Q2"),
               (f"{[e for e in eq if e[0]=='Trust'][0][3]:+.1f} pp", "Trust over the same period"),
               (f"{sh.cw.iloc[-1]:.2f}%", "national value share"),
               (f"{sent[sent.brand=='Crunchwell'].sent.iloc[0]:+.2f}", "social sentiment 2026")],
        bullets=[
            "**The diagnosis is specific.** Relevance 68.6 → 62.7 and Modernity 51.0 → 48.8, while "
            "Trust holds at ~73 and Quality actually improves. That combination is a brand drifting "
            "out of culture, not a brand losing credibility.",
            "**The shopper base is turning over.** Loyal-family penetration is eroding; "
            "cereal-skipper is growing. We are losing occasions, not preference.",
            f"**We spend like a 1990s brand:** ${mk.spend_m.sum():.1f}M behind Crunchwell with Linear "
            f"TV the largest line at ${float(mk[mk.channel.str.contains('TV')].spend_m.sum()):.1f}M.",
            "**The plan:** a relevance platform behind the Aug 2026 Pack Refresh, a media mix shift "
            "from TV to CTV/creator/retail media, and a Louisiana-first execution model.",
        ], headline="Six quarters flat, and the reason is measurable")

    waves = list(q.equity("Crunchwell", "US-NAT").index)
    eqp = q.equity("Crunchwell", "US-NAT")
    cheq = chart_line("r46_equity.png", waves,
                      {a: [float(x) for x in eqp[a]] for a in ["Relevance", "Trust", "Taste",
                                                               "Quality", "Modernity"]},
                      title="Crunchwell brand equity, top-two-box (%) — US National", pct=True, h=3.2)
    k.chart_bullets("DIAGNOSIS", "Trust holds. Relevance is the line that moves.", cheq,
                    [f"**Relevance {eqp['Relevance'].iloc[0]:.1f} → {eqp['Relevance'].iloc[-1]:.1f}** "
                     "across six waves — the steepest decline of any attribute we track.",
                     f"**Trust {eqp['Trust'].iloc[0]:.1f} → {eqp['Trust'].iloc[-1]:.1f}** and "
                     f"**Quality {eqp['Quality'].iloc[0]:.1f} → {eqp['Quality'].iloc[-1]:.1f}** — "
                     "the franchise assets are intact.",
                     f"**Modernity at {eqp['Modernity'].iloc[-1]:.1f}** is the lowest attribute in "
                     "the set and the one the Pack Refresh addresses directly.",
                     "**Social confirms it:** Crunchwell sentiment runs negative at −0.11 on 316 "
                     "mentions, against ProteinPeak at +0.44."],
                    note="Source: brand_equity_quarterly (Kantar-shape), social_mentions 2026.")

    chc = chart_line("r46_cohorts.png", list(coh.index),
                     {c: [float(x) for x in coh[c]] for c in coh.columns},
                     title="Household penetration by cohort (%) — US National", pct=True, h=3.1)
    k.chart_table("THE SHOPPER", "The base is turning over underneath a flat share number", chc,
                  ["Cohort", "FY25Q1", "FY26Q2", "Read"],
                  [["loyal-family", f"{coh['loyal-family'].iloc[0]:.1f}%",
                    f"{coh['loyal-family'].iloc[-1]:.1f}%", "Eroding — the core"],
                   ["cereal-skipper", f"{coh['cereal-skipper'].iloc[0]:.1f}%",
                    f"{coh['cereal-skipper'].iloc[-1]:.1f}%", "Growing — occasions lost"],
                   ["protein-returner", f"{coh['protein-returner'].iloc[0]:.1f}%",
                    f"{coh['protein-returner'].iloc[-1]:.1f}%", "Growing — ProteinPeak's pool"],
                   ["price-shopper", f"{coh['price-shopper'].iloc[0]:.1f}%",
                    f"{coh['price-shopper'].iloc[-1]:.1f}%", "Flat — not a value problem"]],
                  widths=[0.34, 0.2, 0.2, 0.26], align_right_from=1,
                  note="Source: kantar_worldpanel_cohort, US-NAT.")

    chm = chart_donut("r46_mix.png", [c[:20] for c in mk.channel.head(6)],
                      [float(x) for x in mk.spend_m.head(6)],
                      title="Crunchwell A&P by channel ($M)")
    k.chart_bullets("THE MONEY", "A media mix built for a brand that was still relevant", chm,
                    ["**Linear TV is the largest line** — reach against a shrinking cereal occasion.",
                     "**Retail media is second** and is the only line with a modelled ratio above 1.0 "
                     "at Walmart Connect.",
                     "**Creator and CTV are underweight** relative to ProteinPeak, which is the brand "
                     "in the house that is actually growing.",
                     "**FY27 recommendation:** hold total A&P, move roughly a third of the TV line "
                     "into CTV, creator and retail media — with the LA DMA weighted at 2.2× "
                     "national ROI."],
                    note="Source: seed_marketing_spend (Crunchwell), seed_retail_media_spend_q1_2026.")

    k.two_col("PLATFORM", "The creative platform recommendation",
              "\"Made for the morning you actually have\"",
              ["Reframes Crunchwell from a nostalgic family brand to a brand that fits a compressed, "
               "chaotic weekday morning.",
               "Targets Relevance and Modernity directly, without touching Trust or Taste.",
               "Lands with the Pack Refresh (Aug 15 2026) so the visual change and the message change "
               "arrive together.",
               "Executes creator-first in the South, where the share loss is concentrated."],
              "Why not the alternatives",
              ["\"Value\" platform: rejected — price-shopper penetration is flat at ~24%; this is not "
               "a value problem.",
               "\"Heritage\" platform: rejected — Trust is already at 72.9; we would be spending "
               "against an asset we already own.",
               "\"Health\" platform: rejected — that is ProteinPeak's and TrailGrove's ground, and we "
               "would cannibalise the growth brands.",
               "\"Kids\" platform: rejected — the Kids Sweet segment is −2.8% and the mom-guilt trend "
               "runs 0.68."],
              note="Source: brand_equity_quarterly, kantar_worldpanel_cohort, seed_macro_trends, "
                   "seed_category_market_size.")

    k.table("THE PLAN", "Crunchwell FY2027 on a page",
            ["Pillar", "What we do", "Investment", "Success measure"],
            [["Relevance platform", "New creative platform + Pack Refresh launch, creator-first in "
              "the South", "≈$18M A&P", "Relevance 62.7 → 65.5 by FY27Q4"],
             ["Pack Refresh", "Hero SKUs re-skinned, on shelf Aug 15 2026", "$28M year-1 revenue target",
              "Modernity 48.8 → 52"],
             ["Louisiana recovery", "Facing restoration, targeted trade, LA retail-media injection",
              "≈$2.4M", "LA share 3.0% → 4.5%"],
             ["Trade reset", "Depth capped at 20%, event count down, index up", "−$4M net spend",
              "Index 0.57 → 0.62"],
             ["Innovation", "Mega Family 36oz (2027-Q1), Maiz Crunch concept (2027-Q1)",
              "Stage-gate funded", "Two concepts through Stage-4"]],
            widths=[0.19, 0.36, 0.19, 0.26], align_right_from=9, size=9.5,
            note="Source: seed_innovation_pipeline, seed_marketing_spend, seed_geographies. "
                 "FY27 figures are plan targets.")

    k.reco("THE ASK", "What we need signed off",
           [("Approve the relevance platform and kill the value-platform option", "VP Brand", "By Jul 15"),
            ("Approve the A&P mix shift out of Linear TV into CTV, creator and retail media",
             "VP Brand / CFO", "FY27 planning"),
            ("Fund the Louisiana recovery leg at ≈$2.4M inside the existing envelope",
             "CFO", "By Aug 1"),
            ("Hold Pack Refresh at Aug 15 with weekly stage-gate reporting", "Cory Whitman", "From Jul 15"),
            ("Add Relevance and Modernity to the brand scorecard as reported KPIs",
             "Nina Ortega / Insights", "FY27Q1")])

    k.close("Trusted is not the same as wanted.",
            ["Relevance is down 5.9 points; Trust is up 0.6.",
             "The platform, the pack and the media mix all move against relevance.",
             "Louisiana is where we prove it works."])
    return k.build()


# ============================================== 47 · Crunchwell turnaround ====
def r47_crunchwell_turnaround():
    k = Deck("47-crunchwell-fy27-fy29-turnaround-commitment.pptx",
             kicker="THREE-YEAR TURNAROUND · STEERCO COMMITMENT",
             title="Crunchwell FY27–FY29 Turnaround",
             subtitle="What we are committing to, in what order, and the gates at which the "
                      "committee can stop us",
             byline="Cory Whitman with Finance and Supply Chain · SteerCo, July 2026",
             short="Crunchwell turnaround")

    pv = q.pva_brand_month("Crunchwell")
    geo = q.geos()
    la = q.share_quarter(la=True)
    eqp = q.equity("Crunchwell", "US-NAT")

    k.agenda(["The commitment", "Where we are today", "The geography of the problem",
              "Three-year sequence", "Year 1 — stabilise", "Year 2 — rebuild relevance",
              "Year 3 — grow again", "Gates and stop conditions", "The ask"])

    k.exec_summary(
        "Crunchwell is $312M of FY25 revenue running −5.7 to −6.0% to plan every month of FY26, with "
        "a 340 bps hole in Louisiana and a five-point relevance decline nationally. The commitment is "
        "not a return to growth in FY27. It is stabilisation in FY27, relevance recovery in FY28, and "
        "growth in FY29 — with a hard gate at the end of each year.",
        tiles=[(f"{float(pv['var'].mean()):+.1f}%", "FY26 average variance to plan"),
               (f"{la.cw.iloc[-1]:.2f}%", "Louisiana value share"),
               (f"{eqp['Relevance'].iloc[-1]:.1f}", "Relevance top-two-box"),
               (q.m0(q.PLAN['fy27_brand']['Crunchwell']), "FY27 revenue commitment")],
        bullets=[
            "**Year 1 (FY27): stabilise.** Hold revenue at ≈$318M, get Louisiana above 4.5%, land the "
            "Pack Refresh, cap trade depth. No growth commitment.",
            "**Year 2 (FY28): rebuild relevance.** Relevance to 65+, Modernity to 52, Mega Family Pack "
            "in market, Maiz Crunch through Stage-4.",
            "**Year 3 (FY29): grow.** +2% revenue growth with trade rate down from 25.6% to 22% of gross.",
            "**Stop conditions are explicit.** If the Year-1 gate fails, the committee reallocates "
            "Crunchwell A&P to ProteinPeak and TrailGrove rather than funding Year 2.",
        ], headline="A staged commitment, not a promise of growth")

    chv = chart_line("r47_var.png", list(pv.Period),
                     {"Plan ($M/mo)": [float(x) for x in pv.plan],
                      "Actual ($M/mo)": [float(x) for x in pv.act]},
                     title="Crunchwell monthly revenue, plan vs actual ($M)", h=2.9)
    k.chart_bullets("TODAY", "A consistent, structural gap — not a bad month", chv,
                    [f"**Every month of FY26 lands between {pv['var'].min():.1f}% and "
                     f"{pv['var'].max():.1f}%** against a flat $25.19M monthly plan.",
                     "**Consistency is the diagnosis:** this is base erosion, not promotional timing.",
                     "**Louisiana explains roughly a third** of the absolute gap; the rest is national "
                     "relevance decay.",
                     "**The Pack Refresh is the only structural change** landing inside FY26."],
                    note="Source: plan_vs_actual, Crunchwell, 2026-01 to 2026-05.")

    g = geo.head(8)
    chg = chart_bar("r47_geo.png", [n[:18] for n in g.geo_name], [float(x) for x in g.bps],
                    title="Crunchwell share change, FY25 → Q1 FY26 (bps)", color="rust", h=3.0)
    k.chart_table("GEOGRAPHY", "Three battlefields, two leading indicators", chg,
                  ["Market", "FY25", "Q1 FY26", "Δ bps", "Tier"],
                  [[r.geo_name[:22], f"{r.fy25:.1f}%", f"{r.q126:.1f}%", f"{int(r.bps)}",
                    r.priority_tier[:14]] for r in geo.head(7).itertuples()],
                  widths=[0.32, 0.15, 0.16, 0.15, 0.22], size=9.0,
                  note="Source: seed_geographies.")

    k.table("SEQUENCE", "Three years, three different jobs",
            ["Year", "Job", "Revenue commitment", "Lead measures", "Gate"],
            [["FY27", "Stabilise", "$318M (+1.9% on FY25 actual)",
              "LA share ≥4.5%; Pack Refresh 90% ACV; trade index ≥0.60",
              "Q4 FY27 SteerCo"],
             ["FY28", "Rebuild relevance", "$326M (+2.5%)",
              "Relevance ≥65; Modernity ≥52; Mega Family in market", "Q4 FY28 SteerCo"],
             ["FY29", "Grow", "$336M (+3.1%)",
              "Trade rate ≤22% of gross; two new SKUs at scale", "FY30 planning"]],
            widths=[0.09, 0.17, 0.22, 0.36, 0.16], align_right_from=9, size=9.5,
            note="Revenue commitments are targets; FY27 matches the AOP brand build (Report 14). "
                 "Base = FY25 actual from seeds/skus.csv.")

    k.two_col("YEAR 1", "What happens in FY2027",
              "The four workstreams",
              ["**Pack Refresh** — hero SKUs on shelf Aug 15 2026, $28M year-1 revenue target, "
               "confidence 0.82.",
               "**Louisiana** — facing restoration at Walmart (6 → 8 on Mega), targeted Rouses trade, "
               "LA retail-media injection at 2.2× national ROI.",
               "**Relevance platform** — new creative platform launches with the pack.",
               "**Trade reset** — Mega depth capped at 20%, event count down ~15%, index to 0.60."],
              "What we are explicitly not doing",
              ["Not cutting list price. Elasticity on Mega packs (−1.84 to −2.12) means price cuts "
               "buy volume and lose the reference price.",
               "Not adding Kids Sweet innovation — the segment is −2.8%.",
               "Not chasing protein with Crunchwell branding; that is ProteinPeak's job.",
               "Not defending every DMA. Northeast under-indexing stays under-indexed in FY27."],
              note="Source: seed_innovation_pipeline, seed_sku_elasticity_estimates, "
                   "seed_walmart_endcap_audit_la, seed_category_market_size.")

    k.risk("GATES", "The stop conditions, agreed up front",
           [["LA share below 4.0% at Q4 FY27", "Year-1 gate fails",
             "Reallocate LA trade and media to ProteinPeak/TrailGrove; hold Crunchwell at "
             "maintenance A&P", "SteerCo"],
            ["Pack Refresh ACV below 80% by Q4 FY27", "Distribution thesis fails",
             "Renegotiate at Q1 FY28 line reviews before further pack investment",
             "Marcus Boudreaux"],
            ["Relevance still below 63 at Q4 FY28", "Platform fails",
             "Stop the platform, move to a harvest plan on Crunchwell", "VP Brand"],
            ["Trade index below 0.55 at Q4 FY27", "Efficiency thesis fails",
             "Trade Finance takes calendar control from the NAM team", "CFO / RGM Lead"]],
           note="Source: agreed SteerCo stop conditions; measures from syndicated_weekly, "
                "sku_authorization, brand_equity_quarterly, seed_trade_promo_events_q1_2026.")

    k.reco("THE ASK", "What the SteerCo signs today",
           [("Approve the three-year staged commitment with FY27 as a stabilisation year",
             "SteerCo", "July 2026"),
            ("Approve the four Year-1 workstreams and their owners", "Cory Whitman", "July 2026"),
            ("Agree the four stop conditions and the consequence of each", "SteerCo / CFO", "July 2026"),
            ("Report the four Year-1 lead measures monthly, not quarterly", "Cory Whitman", "From August")])

    k.close("Stabilise, then earn the right to grow.",
            ["FY27 is a stabilisation commitment: $318M and Louisiana above 4.5%.",
             "The gates are agreed now, while everyone is calm.",
             "If Year 1 fails, the money moves."])
    return k.build()


# ================================================ 48 · ProteinPeak FY27 plan ==
def r48_proteinpeak_fy27_plan():
    k = Deck("48-proteinpeak-fy27-brand-plan-3yr-roadmap.pptx",
             kicker="ANNUAL BRAND PLAN · FY2027 + THREE-YEAR ROADMAP",
             title="ProteinPeak FY2027 Brand Plan",
             subtitle="The fastest-growing thing we own, in the fastest-growing pocket of the "
                      "category — and what it needs to keep compounding",
             byline="Sage Park, Brand Director — ProteinPeak · July 2026",
             short="ProteinPeak FY27 plan")

    wp25 = q.cat_row("FY2025", "Wellness Protein")
    wpq2 = q.cat_row("Q2-FY2026-MTD", "Wellness Protein")
    tgt = q.cat_row("Q2-FY2026-MTD", "Wellness Protein", "Target Total US")
    wmt = q.cat_row("Q2-FY2026-MTD", "Wellness Protein", "Walmart Total US")
    pv = q.pva_brand_month("ProteinPeak")
    sk = q.skus("ProteinPeak")
    sent = q.sentiment()

    k.agenda(["The opportunity", "Where the launch landed", "Source of volume",
              "The retailer problem", "FY27 plan", "Three-year roadmap",
              "Competitive response", "Measurement", "The ask"])

    k.exec_summary(
        f"Wellness Protein grew {wp25.growth:+.1f}% to ${wp25.size:,.0f}M in FY25 and is running "
        f"{wpq2.growth:+.1f}% in Q2 FY26. Acme's share of it moved {wp25.acme_share:.1f}% → "
        f"{wpq2.acme_share:.1f}% on the April 20 launch. ProteinPeak is the only brand in the house "
        "with a structural tailwind. The FY27 plan is about distribution, not demand — we are "
        "under-distributed at the two largest retailers in America.",
        tiles=[(f"{wpq2.growth:+.1f}%", "Wellness Protein growth, Q2 QTD"),
               (f"{wpq2.acme_share:.1f}%", "Acme share of segment"),
               ("53%", "launch volume new to brand"),
               (f"{sent[sent.brand=='ProteinPeak'].sent.iloc[0]:+.2f}", "social sentiment")],
        bullets=[
            f"**The launch worked.** ProteinPeak went from −25.4% to plan in Q1 (pre-launch) to "
            f"{float(pv['var'].iloc[-1]):+.1f}% in May, with trial at 110–113% of plan at Target.",
            "**53% of volume is new to Acme** — 32% cannibalisation and 15% competitive switching. "
            "That is a healthy launch profile for a line extension.",
            f"**Target over-indexes hard:** Acme holds {tgt.acme_share:.1f}% of Wellness Protein at "
            f"Target versus {wmt.acme_share:.1f}% at Walmart. Same product, same price, "
            "different shelf.",
            "**Larksfield answered on May 12** with a 14g protein line extension. Our response is "
            "Chocolate Almond (64% top-two-box) into the Q4 line reviews, not a price move.",
        ], headline="A brand with a tailwind and a distribution gap")

    chv = chart_line("r48_var.png", list(pv.Period),
                     {"Plan ($M/mo)": [float(x) for x in pv.plan],
                      "Actual ($M/mo)": [float(x) for x in pv.act]},
                     title="ProteinPeak monthly revenue, plan vs actual ($M)", h=2.9)
    k.chart_bullets("THE LAUNCH", "The trough was planned; the recovery is real", chv,
                    ["**Q1 ran ~$4.33M/month against a $5.80M plan** — the pre-launch pipeline "
                     "draw-down, by design.",
                     "**April and May ran ~$5.44M** — a 6% gap to plan, closing.",
                     "**Week-2 repeat is 1.2× the Berry Crunch archive**, the cleanest signal that "
                     "the product delivers on the claim.",
                     "**Velocity tells the retailer story:** 17.5 units/store/week at Target versus "
                     "9.2 at the Walmart pilot."],
                    note="Source: plan_vs_actual (ProteinPeak), seed_proteinpeak_q2_launch.")

    chd = chart_donut("r48_sov.png", ["New to brand", "Cannibalisation", "Competitive switch"],
                      [431, 260, 125], title="Launch source of volume (households)")
    chr_ = chart_bar("r48_retailer.png", ["Target", "Walmart"],
                     [float(tgt.acme_share), float(wmt.acme_share)],
                     title="Acme share of Wellness Protein, Q2 FY26 MTD (%)", pct=True,
                     colors_list=["#2E7D75", "#B24A2E"], h=2.9)
    k.charts2("THE READ", "Healthy volume mix; unhealthy retailer spread", chd, chr_,
              captions=["53% new-to-brand, 32% cannibalisation of PP001–PP003, 15% taken from "
                        "competitors.",
                        f"{tgt.acme_share:.1f}% at Target versus {wmt.acme_share:.1f}% at Walmart — "
                        "a distribution and merchandising gap, not a demand gap."],
              note="Source: household_transactions (PP005/PP006 switch analysis), "
                   "seed_category_market_size retailer cuts.")

    srows = [[r.sku_name.replace("ProteinPeak ", ""), f"${r.price:.2f}", f"{r.acv:.0f}%",
              money(r.rev) if r.rev else "launch", r.status] for r in sk.itertuples()]
    k.table("THE LINE", "Six SKUs, two of them four months old",
            ["SKU", "Shelf price", "National ACV", "FY25 revenue", "Status"], srows,
            widths=[0.36, 0.16, 0.16, 0.16, 0.16],
            callout=("The distribution ask",
                     "Cinnamon Crunch sits at 38% ACV and Cocoa Almond at 28% four months after "
                     "launch. Getting both to 55% — Vanilla Almond's level — is worth more than any "
                     "media dollar we could spend in FY27.", "action"),
            note="Source: seeds/skus.csv.")

    k.table("FY27 PLAN", "ProteinPeak FY2027 on a page",
            ["Pillar", "What we do", "Investment", "Success measure"],
            [["Distribution", "Full-line authorisation at Walmart and Kroger; Costco club pack",
              "Trade + line-review support", "PP005/PP006 ACV ≥55%"],
             ["Innovation", "Chocolate Almond launch (Q4 FY26 line reviews, Q1 FY27 shelf)",
              "Stage-gate funded", "Top-two-box ≥55% held; 8pp substitution gate"],
             ["Creator-led media", "Athlete-anchored creator programme, whitelisted into paid social "
              "and Roundel", "≈$9M A&P", "Sentiment ≥+0.40; earned reach vs protein-curious"],
             ["Retail media", "Weight to Walmart Connect (ratio 1.20) and Kroger Precision (0.77)",
              "≈$6.5M", "Blended modelled ratio ≥1.0"],
             ["Price discipline", "Hold $7.49; max 10% off, feature-led, no depth stacking",
              "−", "Trade rate ≤13% of gross"]],
            widths=[0.17, 0.36, 0.19, 0.28], align_right_from=9, size=9.5,
            note="Source: seed_marketing_spend, seed_retail_media_spend_q1_2026, "
                 "seed_concept_test_chocolate_almond, seed_trade_spend_fy25. FY27 figures are targets.")

    chrm = chart_line("r48_roadmap.png", ["FY25", "FY26E", "FY27T", "FY28T", "FY29T"],
                      {"ProteinPeak revenue ($M)": [48, 62, 100, 125, 150]},
                      title="ProteinPeak revenue roadmap ($M) — FY27+ are targets", h=2.9)
    k.chart_bullets("ROADMAP", "$48M to $150M in four years", chrm,
                    ["**FY26 ($62M est.):** two new SKUs at partial distribution.",
                     "**FY27 ($100M target):** full distribution at Walmart and Kroger, Chocolate "
                     "Almond in market. This is the AOP commitment (Report 14).",
                     "**FY28 ($125M target):** ProteinPeak Bars 12g (Stage-1, 2028-Q2) opens the "
                     "$2.96B granola-bar segment.",
                     "**FY29 ($150M target):** 12–14 SKUs, mid-teens share of a $1.45B segment."],
                    note="Source: seed_innovation_pipeline (PP bars, Stage-1), "
                         "seed_category_market_size. FY27–FY29 are targets.")

    k.reco("THE ASK", "What ProteinPeak needs from the business",
           [("Put ProteinPeak full-line authorisation on the Walmart August line-review agenda",
             "Marcus Boudreaux", "Aug line review"),
            ("Approve Chocolate Almond for the Q4 FY26 Walmart and Target line reviews",
             "Innovation SteerCo", "Aug 5"),
            ("Weight FY27 retail media to Walmart Connect and Kroger Precision, away from Amazon",
             "Tasha Brooks / Hugo Lin", "FY27 planning"),
            ("Hold the $7.49 price and the 10% depth cap through the launch year", "Sage Park", "FY27"),
            ("Add velocity by retailer to the monthly brand scorecard", "Sage Park", "From August")])

    k.close("The demand is proven. The shelf is the constraint.",
            ["53% of launch volume is new to Acme.",
             f"{tgt.acme_share:.1f}% share at Target versus {wmt.acme_share:.1f}% at Walmart.",
             "FY27 is a distribution plan with a media programme attached."])
    return k.build()


# ============================================ 49 · Chocolate Almond gate ======
def r49_chocolate_almond_gate():
    k = Deck("49-proteinpeak-q3-chocolate-almond-steerco-gate.pptx",
             kicker="INNOVATION STEERCO · STAGE GATE",
             title="ProteinPeak Chocolate Almond — Concept Test Read",
             subtitle="Does the Q3 line extension clear the action standard and the "
                      "cannibalisation gate?",
             byline="Maya Chen, Senior Insights Analyst · for the innovation SteerCo, Aug 5 2026",
             short="Choc Almond gate")

    ct = q.concept_test()

    def v(metric, default=None):
        r = ct[ct.metric == metric]
        return r.value.iloc[0] if len(r) else default

    k.agenda(["The decision", "Method and sample", "Topline result",
              "Cohort read", "Cannibalisation gate", "Competitive context",
              "Recommendation and next steps"])

    k.exec_summary(
        f"Chocolate Almond scores {v('top_two_box_pct')}% top-two-box against a "
        f"{v('action_standard_threshold_pct')}% action standard — "
        f"{v('delta_vs_launch_sku_pretest_pp')}pp above the launch-SKU pretest and "
        f"{v('delta_vs_cereal_innovation_benchmark_pp')}pp above the five-year cereal-innovation "
        "benchmark. Substitutional cannibalisation against the launch SKUs is 8pp against a 12pp "
        "SteerCo gate. Both gates clear. The recommendation is to take it to the Q4 Walmart and "
        "Target line reviews.",
        tiles=[(f"{v('top_two_box_pct')}%", "top-two-box"),
               (f"{v('action_standard_threshold_pct')}%", "action standard"),
               ("8pp", "substitutional cannibalisation"),
               ("12pp", "SteerCo gate")],
        bullets=[
            f"**Sample:** n={v('n_total')}, fielded {v('field_period_start')} to "
            f"{v('field_period_close')}, standard Acme cereal-innovation monadic design.",
            "**Cohort strength is where the news is:** protein-curious at 71% top-two-box with a "
            "3.06/5 purchase-intent mean; lapsed-cereal at 66%.",
            "**Current-Crunchwell buyers score 52%** — below the standard, which is the right answer: "
            "this SKU is not built to convert the family-cereal base.",
            "**Cannibalisation splits cleanly:** 22% overlap with the launch SKUs, 14pp additive, "
            "8pp substitutional. Against Crunchwell it is negligible at 2pp.",
        ], headline="Both gates clear")

    cht = chart_bar("r49_topline.png",
                    ["Chocolate Almond", "Action standard", "Launch-SKU pretest",
                     "Innovation benchmark"],
                    [float(v('top_two_box_pct')), float(v('action_standard_threshold_pct')),
                     float(v('top_two_box_pct')) - float(v('delta_vs_launch_sku_pretest_pp')),
                     float(v('top_two_box_pct')) - float(v('delta_vs_cereal_innovation_benchmark_pp'))],
                    title="Top-two-box purchase intent (%)", pct=True,
                    colors_list=["#2E7D75", "#5B6472", "#3E6DA8", "#B98A2E"], h=2.9)
    k.chart_bullets("TOPLINE", "Clears the standard with room", cht,
                    [f"**{v('top_two_box_pct')}% top-two-box** against a "
                     f"{v('action_standard_threshold_pct')}% standard.",
                     f"**{v('delta_vs_launch_sku_pretest_pp')}pp better than the SKUs that just "
                     "launched** — and those are performing at 110–113% of trial plan at Target.",
                     f"**{v('delta_vs_cereal_innovation_benchmark_pp')}pp above the five-year "
                     "innovation benchmark** puts this in the top quartile of concepts we have tested.",
                     "**Chocolate as a breakfast preference runs +14pp** in the protein-curious "
                     "cohort (U&A, April 2026) — the concept is riding a real preference, not a "
                     "novelty score."],
                    note="Source: seed_concept_test_chocolate_almond, seed_ua_study_2026q2_reference.")

    coh = ct[ct.section.str.contains("cohort", case=False, na=False)]
    crows = [[str(r.metric).replace("_", " "), f"{r.value}{'' if str(r.unit)=='nan' else ''}",
              str(r.unit), str(r.scope) if str(r.scope) != "nan" else "—"]
             for r in coh.itertuples()]
    if crows:
        k.table("COHORTS", "The concept works hardest where we need it to",
                ["Metric", "Value", "Unit", "Scope"], crows[:9],
                widths=[0.44, 0.14, 0.14, 0.28], align_right_from=1, size=9.5,
                note="Source: seed_concept_test_chocolate_almond, cohort section.")

    chc = chart_bar("r49_cohort.png", ["Protein-curious", "Lapsed-cereal", "Current-Crunchwell",
                                       "Action standard"],
                    [71, 66, 52, 55], title="Top-two-box by cohort (%)", pct=True,
                    colors_list=["#2E7D75", "#2E7D75", "#B98A2E", "#5B6472"], h=2.9)
    chn = chart_bar("r49_cannib.png", ["Additive", "Substitutional", "SteerCo gate"],
                    [14, 8, 12], title="Cannibalisation vs ProteinPeak launch SKUs (pp)",
                    colors_list=["#2E7D75", "#3E6DA8", "#B24A2E"], h=2.9)
    k.charts2("THE GATES", "Cohort strength and a cannibalisation result inside the gate", chc, chn,
              captions=["Protein-curious 71% and lapsed-cereal 66% both clear; "
                        "current-Crunchwell 52% does not, and should not.",
                        "22% overlap decomposes to 14pp additive and 8pp substitutional against a "
                        "12pp gate. Versus Crunchwell: 6% overlap, 2pp substitutional."],
              note="Source: seed_concept_test_chocolate_almond.")

    comp = q.comp_launches("2025-08-01")
    crows2 = [[r.brand, r.sku_new, str(r.launch_date), str(r.claim)[:44], f"{r.buzz:.2f}"]
              for r in comp.head(6).itertuples()]
    k.table("CONTEXT", "The competitive window is open now",
            ["Brand", "SKU", "Launch", "Claim", "Buzz d30"], crows2,
            widths=[0.18, 0.18, 0.14, 0.36, 0.14], align_right_from=4,
            callout=("Why the timing matters",
                     "Larksfield launched a 14g protein extension on May 12 2026 and is escalating on "
                     "both the protein and Louisiana fronts. A Q1 FY27 Chocolate Almond shelf date "
                     "requires the Q4 FY26 line reviews. Missing them costs us two quarters.", "risk"),
            note="Source: seed_competitor_launches.")

    k.reco("RECOMMENDATION", "Take it forward",
           [("Approve Chocolate Almond to Stage-4 Pre-Launch", "Innovation SteerCo", "Aug 5 2026"),
            ("Include Chocolate Almond in the Q4 FY26 Walmart and Target line reviews",
             "Marcus Boudreaux / Soo-jin Lee", "Q4 FY26"),
            ("Hold the 12pp substitution gate as a post-launch measure, re-read at week 13",
             "Maya Chen", "Q1 FY27 + 13 weeks"),
            ("Brief creator and retail-media plans off the protein-curious cohort, not the "
             "general population", "Sage Park / Hugo Lin", "By Sep 15")])

    k.close("Clears the standard, clears the gate, and the window is open.",
            [f"{v('top_two_box_pct')}% top-two-box against a {v('action_standard_threshold_pct')}% standard.",
             "8pp substitutional against a 12pp gate.",
             "Q4 line reviews are the decision point, not the concept."])
    return k.build()


# ================================================ 50 · HoneyNest portfolio ====
def r50_honeynest_portfolio():
    k = Deck("50-honeynest-kids-sweet-portfolio-decision.pptx",
             kicker="PORTFOLIO DECISION",
             title="HoneyNest and the Kids Sweet Question",
             subtitle="A well-run brand inside a structurally declining segment — harvest, "
                      "reposition, or invest?",
             byline="HoneyNest Brand Manager with Insights and Finance · July 2026",
             short="HoneyNest decision")

    ks24 = q.cat_row("FY2024", "Kids Sweet")
    ks25 = q.cat_row("FY2025", "Kids Sweet")
    pv = q.pva_brand_month("HoneyNest")
    tb = q.trade_brand()
    hn_trade = tb[tb.brand == "HoneyNest"].iloc[0]
    mac = q.macro()
    pipe = q.pipeline()
    hn_pipe = pipe[pipe.brand == "HoneyNest"]

    k.agenda(["The question", "Brand performance", "Segment reality",
              "Where the trade money goes", "Three options",
              "The recommendation", "What it means for the pipeline", "The ask"])

    k.exec_summary(
        f"HoneyNest is running {float(pv['var'].mean()):+.1f}% to plan — one of the best-executed "
        f"brands in the portfolio — inside a segment that shrank from ${ks24.size:,.0f}M to "
        f"${ks25.size:,.0f}M ({ks25.growth:+.1f}%). Good brand management inside a bad segment "
        "produces exactly this: on-plan performance and no future. The recommendation is a managed "
        "harvest with one repositioning bet, not continued investment at current levels.",
        tiles=[(f"{float(pv['var'].mean()):+.1f}%", "FY26 variance to plan"),
               (f"{ks25.growth:+.1f}%", "Kids Sweet segment growth"),
               (f"${hn_trade.spend_m:.1f}M", "FY25 trade spend"),
               (f"{hn_trade.incr:.2f}", "trade incrementality index")],
        bullets=[
            f"**HoneyNest delivers.** {float(pv['var'].mean()):+.1f}% average variance to plan across "
            "FY26 — better than every brand except RootDay.",
            f"**The segment does not.** Kids Sweet is ${ks25.size:,.0f}M and "
            f"{ks25.growth:+.1f}% YoY, with the mom-guilt trend running at 0.68 strength and "
            "trending down for kids' cereal.",
            f"**We spend ${hn_trade.spend_m:.1f}M of trade at {hn_trade.depth:.1f}% depth** for an "
            f"index of {hn_trade.incr:.2f} — buying volume in a segment that is leaving.",
            "**Three SKUs are already on the FY26 discontinue list** (Granola Crunch, Cookie Dough) "
            "and the pipeline holds only an LTO.",
        ], headline="A well-run brand in the wrong room")

    chs = chart_bar("r50_segment.png", ["Kids Sweet FY24", "Kids Sweet FY25", "Family Sweet FY25",
                                        "Wellness Protein FY25"],
                    [float(ks24.growth), float(ks25.growth), 1.4, 18.3],
                    title="Segment growth comparison (% YoY)", pct=True,
                    colors_list=["#B24A2E", "#B24A2E", "#B98A2E", "#2E7D75"], h=2.9)
    k.chart_bullets("THE SEGMENT", "This is not a cycle — it is a structural decline", chs,
                    [f"**Kids Sweet: ${ks24.size:,.0f}M → ${ks25.size:,.0f}M.** Two consecutive years "
                     "of decline.",
                     f"**Mom-guilt trend at {float(mac[mac.topic.str.contains('mom-guilt')].strength.iloc[0]) if len(mac[mac.topic.str.contains('mom-guilt')]) else 0.68} strength**, "
                     "direction down for kids' cereal — a permissioning problem, not a taste problem.",
                     "**Low-sugar pressure at 0.72** compounds it: the segment's core benefit is the "
                     "thing parents are trying to avoid.",
                     "**Meanwhile Wellness Protein grew +18.3%.** The same shelf space and the same "
                     "trade dollars are worth far more one segment over."],
                    note="Source: seed_category_market_size, seed_macro_trends.")

    chp = chart_line("r50_pva.png", list(pv.Period),
                     {"Plan ($M/mo)": [float(x) for x in pv.plan],
                      "Actual ($M/mo)": [float(x) for x in pv.act]},
                     title="HoneyNest monthly revenue, plan vs actual ($M)", h=2.9)
    k.chart_table("THE BRAND", "Execution is not the problem", chp,
                  ["Measure", "HoneyNest", "Portfolio"],
                  [["FY26 variance to plan", f"{float(pv['var'].mean()):+.1f}%", "−5.3% (Q1 total)"],
                   ["Trade spend", f"${hn_trade.spend_m:.1f}M", f"${tb.spend_m.sum():.0f}M"],
                   ["Trade depth", f"{hn_trade.depth:.1f}%", f"{tb.depth.mean():.1f}%"],
                   ["Incrementality index", f"{hn_trade.incr:.2f}", f"{tb.incr.mean():.2f}"],
                   ["Segment growth", f"{ks25.growth:+.1f}%", "+1.3% (RTE total)"]],
                  widths=[0.44, 0.28, 0.28],
                  note="Source: plan_vs_actual, seed_trade_spend_fy25, seed_category_market_size.")

    k.table("OPTIONS", "Three ways to play it",
            ["Option", "What it means", "FY27–FY29 revenue", "Investment", "Verdict"],
            [["A · Invest", "Fund a kids-cereal relaunch with new mascot and media",
              "$92M → $96M → $99M", "≈$12M incremental A&P", "Reject"],
             ["B · Harvest", "Hold distribution, cut A&P to maintenance, run LTOs only, "
              "cut trade depth", "$92M → $88M → $84M", "≈$1M A&P", "Recommend"],
             ["C · Reposition", "Move HoneyNest into Family Wholegrain with a whole-grain-plus line",
              "$92M → $94M → $97M", "≈$5M + R&D", "Recommend as a bet inside B"]],
            widths=[0.14, 0.34, 0.20, 0.18, 0.14], align_right_from=9, size=9.5, status_col=4,
            callout=("Why not Option A",
                     "Funding a relaunch into a −2.8% segment against a 0.68-strength mom-guilt "
                     "trend spends FY27 growth money on the least favourable structural position in "
                     "the portfolio. The same $12M behind ProteinPeak distribution returns more.",
                     "risk"),
            note="Revenue paths are planning estimates. Source: seed_category_market_size, "
                 "seed_innovation_pipeline, seed_macro_trends.")

    prows = [[r.concept_name[:38], r.stage_gate, str(r.planned_launch_date),
              q.musd(r.projected_revenue_year1_musd), q.dash(r.status)]
             for r in hn_pipe.itertuples()]
    k.table("PIPELINE", "What HoneyNest has in the tank",
            ["Concept", "Stage", "Planned launch", "Year-1 revenue", "Status"], prows,
            widths=[0.34, 0.20, 0.16, 0.16, 0.14], align_right_from=2, size=9.5,
            note="Source: seeds/innovation_pipeline.csv.")

    k.reco("THE ASK", "Decide the role, then fund it",
           [("Adopt Option B — managed harvest — as HoneyNest's portfolio role from FY27",
             "VP Brand / CFO", "FY27 planning"),
            ("Fund the Option C whole-grain repositioning as a single Stage-2 concept, not a relaunch",
             "Innovation SteerCo", "Q4 FY26 gate"),
            ("Confirm the Q3 FY26 discontinuation of Granola Crunch and Cookie Dough",
             "HoneyNest BM / Supply Chain", "Q3 FY26"),
            ("Redirect ≈$8M of HoneyNest trade and A&P to ProteinPeak distribution and TrailGrove",
             "CFO / RGM Lead", "FY27 planning"),
            ("Keep the Birthday Cake LTO as the one active innovation in FY27", "HoneyNest BM", "Q4 FY26")])

    k.close("Manage it well, but stop paying for growth it cannot deliver.",
            ["HoneyNest is executing at −1.1% to plan in a −2.8% segment.",
             "Harvest, with one repositioning bet.",
             "$8M moves to where the category is growing."])
    return k.build()


# ============================================ 51 · TrailGrove + RootDay =======
def r51_bfy_growth():
    k = Deck("51-trailgrove-rootday-fy27-better-for-you-growth.pptx",
             kicker="PORTFOLIO GROWTH PLAN · FY2027",
             title="TrailGrove and RootDay — The Under-Funded Upside",
             subtitle="Two brands sitting in double-digit-growth segments with single-digit "
                      "investment behind them",
             byline="TrailGrove and RootDay brand teams with Category Insights · July 2026",
             short="BFY growth FY27")

    gran = q.cat_row("FY2025", "Total", "US National")
    oat = q.cat_row("FY2025", "Oat")
    ssc = q.cat_row("FY2025", "Single-Serve Cups")
    tg = q.pva_brand_month("TrailGrove")
    rd = q.pva_brand_month("RootDay")
    mkb = q.mkt_by_brand()
    pipe = q.pipeline()
    sent = q.sentiment()

    k.agenda(["The under-funded case", "TrailGrove today", "RootDay today",
              "Segment tailwinds", "Investment gap", "FY27 plan for both",
              "Innovation pipeline", "The ask"])

    k.exec_summary(
        f"TrailGrove ({float(tg['var'].mean()):+.1f}% to plan) and RootDay "
        f"({float(rd['var'].mean()):+.1f}% to plan) are the two most on-plan brands in the house. "
        f"They sit in granola (+3.3%) and oat milk ({oat.growth:+.1f}%) — and together they receive "
        f"less A&P than Crunchwell spends on Linear TV alone. The FY27 recommendation is a modest, "
        "distribution-weighted investment increase funded from HoneyNest and Crunchwell TV.",
        tiles=[(f"{oat.growth:+.1f}%", "oat milk segment growth"),
               (f"{float(rd['var'].mean()):+.1f}%", "RootDay variance to plan"),
               (f"{float(tg['var'].mean()):+.1f}%", "TrailGrove variance to plan"),
               (f"{ssc.growth:+.1f}%", "single-serve cups growth")],
        bullets=[
            f"**RootDay is the best-performing brand in the portfolio** at "
            f"{float(rd['var'].mean()):+.1f}% to plan, in a ${oat.size:,.0f}M segment growing "
            f"{oat.growth:+.1f}%. Acme holds {oat.acme_share:.1f}% of it.",
            f"**TrailGrove is $152M and {float(tg['var'].mean()):+.1f}% to plan** in granola, an "
            f"${gran.size:,.0f}M segment growing {gran.growth:+.1f}% where we already hold "
            f"{gran.acme_share:.1f}% share.",
            "**Neither has an investment problem we created deliberately** — they were simply never "
            "the priority. That is the cheapest thing to fix in the FY27 plan.",
            "**Sentiment is with us:** Oatly runs +0.20 and MorningOats +0.10, while Crunchwell sits "
            "at −0.11. Better-for-you is where consumer conversation is positive.",
        ], headline="Two brands doing more with less")

    chg = chart_bar("r51_segments.png",
                    ["Oat milk", "Granola", "Single-serve cups", "Family Sweet", "Kids Sweet"],
                    [float(oat.growth), float(gran.growth), float(ssc.growth), 1.4, -2.8],
                    title="Segment growth, FY25 (% YoY)", pct=True,
                    colors_list=["#2E7D75", "#2E7D75", "#2E7D75", "#B98A2E", "#B24A2E"], h=2.9)
    chm = chart_bar("r51_spend.png", list(mkb.brand), [float(x) for x in mkb.spend_m],
                    title="A&P spend by brand ($M, seed period)", color="sky", unit="M", h=2.9)
    k.charts2("THE GAP", "The growth is in one chart; the money is in the other", chg, chm,
              captions=["Oat milk, granola and single-serve cups all grow mid-to-high single digits "
                        "or better.",
                        "Crunchwell and ProteinPeak take the overwhelming majority of A&P. "
                        "TrailGrove and RootDay are rounding errors."],
              note="Source: seed_category_market_size, seed_marketing_spend.")

    k.table("TODAY", "Where the two brands actually are",
            ["Measure", "TrailGrove", "RootDay"],
            [["FY25 revenue", "$152.0M", "$62.0M"],
             ["SKUs", "10", "8"],
             ["FY26 variance to plan", f"{float(tg['var'].mean()):+.1f}%",
              f"{float(rd['var'].mean()):+.1f}%"],
             ["Home segment", f"Granola (${gran.size:,.0f}M, {gran.growth:+.1f}%)",
              f"Oat milk (${oat.size:,.0f}M, {oat.growth:+.1f}%)"],
             ["Acme share of segment", f"{gran.acme_share:.1f}%", f"{oat.acme_share:.1f}%"],
             ["Trade spend FY25", "$10.8M", "$4.7M"],
             ["Trade depth", "13.5%", "9.5%"]],
            widths=[0.32, 0.34, 0.34], align_right_from=1,
            callout=("The structural point",
                     "RootDay holds 3.8% of a segment growing 18.8%, on 9.5% trade depth. That is the "
                     "most efficient share position in the portfolio and the one with the most "
                     "headroom. It is also the least funded.", "info"),
            note="Source: seeds/skus.csv, plan_vs_actual, seed_trade_spend_fy25, "
                 "seed_category_market_size.")

    prows = [[r.concept_name[:40], r.brand, r.stage_gate, str(r.planned_launch_date),
              q.musd(r.projected_revenue_year1_musd)]
             for r in pipe[pipe.brand.isin(["TrailGrove", "RootDay"])].itertuples()]
    k.table("PIPELINE", "What is already in the tank for both brands",
            ["Concept", "Brand", "Stage", "Planned launch", "Year-1"], prows,
            widths=[0.34, 0.14, 0.20, 0.16, 0.16], align_right_from=3, size=9.5,
            note="Source: seeds/innovation_pipeline.csv.")

    k.two_col("FY27 PLAN", "Distribution first, innovation second",
              "TrailGrove FY27",
              ["Distribution build in granola and bars — the cheapest incremental volume in the house.",
               "Bites Yogurt-Coated (Stage-2) into the Q4 FY26 gate for a FY28 launch.",
               "Social-led media at ≈$4M, no linear TV.",
               "Hold trade depth at 13.5%; grow on distribution, not discount.",
               "FY27 target: $162M (+6.6% on FY25)."],
              "RootDay FY27",
              ["Single-Serve Carton (Stage-3, on-hold) reactivated for the gym-bag occasion.",
               "Coffee Creamer (Stage-2) — oat creamer is genuine whitespace against Califia and Silk.",
               "Barista positioning behind the oat-milk barista trend (0.84 strength).",
               "Discontinue Coconut Blend in Q3 FY26 as planned.",
               "FY27 target: $74M (+19.4% on FY25)."],
              note="Source: seeds/innovation_pipeline.csv, seed_macro_trends. FY27 targets are plan.")

    k.reco("THE ASK", "A small amount of money, in the right place",
           [("Approve ≈$6M incremental FY27 investment across TrailGrove and RootDay, funded from "
             "HoneyNest harvest and Crunchwell TV", "CFO / VP Brand", "FY27 planning"),
            ("Reactivate the RootDay Single-Serve Carton concept from On-Hold", "Innovation SteerCo",
             "Q4 FY26 gate"),
            ("Take TrailGrove granola and bar distribution gaps into the Q4 line reviews",
             "Marcus Boudreaux / Priya Raman", "Q4 FY26"),
            ("Report both brands' segment share monthly — today neither is on the scorecard",
             "Category Insights", "From August")])

    k.close("The cheapest growth in the portfolio is the growth we are not funding.",
            ["Two brands, two double-digit-growth segments, minimal investment.",
             "≈$6M redirected, not new money.",
             "$236M FY27 combined target between them."])
    return k.build()


if __name__ == "__main__":
    for fn in [r41_company_q2_qbr, r42_fy27_aop_board_preread, r43_long_range_plan,
               r44_h2_reforecast, r45_rgm_price_pack, r46_crunchwell_fy27_plan,
               r47_crunchwell_turnaround, r48_proteinpeak_fy27_plan,
               r49_chocolate_almond_gate, r50_honeynest_portfolio, r51_bfy_growth]:
        print("built", os.path.basename(fn()))
