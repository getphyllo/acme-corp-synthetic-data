"""Brand-level reports (18-21): Crunchwell Q2 BR + three FY27 annual brand plans.

Run from repo root:
    .venv/bin/python reports/generators/brands.py

Every headline number traces to FACTS.md, acme.duckdb, or seeds/*.csv. Forward
FY27+ figures are labelled target/plan/planning estimate in-document.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import (Doc, df, seed_csv, money, chart_line, chart_bar, chart_grouped,
                 chart_stacked, chart_waterfall, chart_donut)


# ---------------------------------------------------------------- helpers ----
def _brand_var(brand, periods):
    """Return (plan_$M, actual_$M, var%) for a brand across a list of Periods."""
    ps = ",".join(f"'{p}'" for p in periods)
    r = df(f"SELECT SUM(Plan_Revenue_USD)/1e6 p, SUM(Actual_Revenue_USD)/1e6 a "
           f"FROM plan_vs_actual WHERE Brand='{brand}' AND Period IN ({ps})").iloc[0]
    p, a = float(r.p), float(r.a)
    return p, a, (a - p) / p * 100


def _cat(period, subcat, category="RTE Cereal"):
    """Single category_market_size row → (size_$M, yoy%, acme_share%)."""
    cm = seed_csv("category_market_size.csv")
    row = cm[(cm.period == period) & (cm.subcategory == subcat) &
             (cm.category == category)].iloc[0]
    return float(row.market_size_usd_mm), float(row.yoy_growth_pct), float(row.acme_share_pct)


# =========================================================== REPORT 18 =======
def r18_crunchwell_q2_brand_review():
    d = Doc("18-crunchwell-q2-2026-brand-business-review.pdf",
            kicker="BRAND BUSINESS REVIEW · Q2 FY2026",
            title="Crunchwell — Q2 FY2026 Brand Business Review",
            subtitle="The $312M flagship: share held, revenue behind plan, and the equity signal driving both",
            owner="Cory Whitman, Brand Director — Crunchwell",
            period="Q2 FY2026", short="Crunchwell Q2 BR",
            doc_type="Brand quarterly business review", date_str="July 2026")

    # --- grounded numbers
    p_q2, a_q2, var_q2 = _brand_var("Crunchwell", ["2026-04", "2026-05"])  # Q2 actuals through May
    # national share Crunchwell, ex-LA, by quarter
    sh = df("""SELECT SUBSTR(Week,1,4)||'-Q'||CAST(CEIL(CAST(SUBSTR(Week,7,2) AS INT)/13.0) AS INT) q,
                 ROUND(AVG(Crunchwell_Value_Share)*100,2) cw,
                 ROUND(AVG(Larksfield_Value_Share)*100,2) lf,
                 ROUND(AVG(PL_Value_Share)*100,2) pl
               FROM syndicated_weekly WHERE Category='RTE Cereal' AND DMA<>'LA-DMA'
                 AND Week>='2025-W01' GROUP BY 1 ORDER BY 1""")
    # equity waves FY25Q1 vs FY26Q2 (US-NAT)
    eq = df("""SELECT Attribute, Wave, ROUND(Top_Two_Box_Pct,1) ttb
               FROM brand_equity_quarterly WHERE Brand='Crunchwell' AND DMA='US-NAT'
                 AND Wave IN ('FY25Q1','FY26Q2') ORDER BY Attribute, Wave""")
    eqd = {a: {w: t for _, a2, w, t in eq.itertuples() if a2 == a}
           for a in eq.Attribute.unique()}
    rel25, rel26 = eqd["Relevance"]["FY25Q1"], eqd["Relevance"]["FY26Q2"]
    # social sentiment
    ss = df("""SELECT ROUND(AVG("Sentiment_-1to1"),2) s, COUNT(*) n
               FROM social_mentions WHERE Brand_Mentioned='Crunchwell' AND Date>='2026-01-01'""").iloc[0]

    d.cover_facts([
        ("National value share", "6.0% — held flat (Acme #4 RTE)"),
        ("Q2 net revenue vs plan", f"{money(a_q2)} vs {money(p_q2)} plan · {var_q2:+.1f}%"),
        ("Louisiana DMA share", "6.4% → 3.0% (−340 bps, peak-to-trough)"),
        ("Brand equity — Relevance", f"{rel25:.1f} → {rel26:.1f} T2B (−{rel25-rel26:.1f} pp)"),
        ("Near-term bet", "Pack Refresh — Hero SKUs, launches 2026-08-15 ($28M yr1)"),
    ])

    d.exec_summary(
        "Crunchwell held its national footprint in Q2 FY2026 — value share sits at 6.0%, flat across six "
        "quarters — but ran " + f"{var_q2:.1f}% behind a ${p_q2:,.0f}M plan, the same "
        "5.7&ndash;6.0% gap the brand has carried every month of the fiscal year. The revenue miss is not a broad "
        "demand collapse; it is two things stacked. First, a regional wound: Louisiana share has fallen from a "
        "6.4% Mass/Grocery peak to 3.0%, &minus;340 bps. Second, and more strategic, a slow erosion of brand "
        "<b>Relevance</b> — down " + f"{rel25-rel26:.1f} points of top-two-box while Trust and Quality hold. "
        "Crunchwell is still trusted; it is drifting from cultural relevance. The Q2 job is to stabilise the "
        "number while the Pack Refresh and a targeted innovation slate re-earn relevance.",
        bullets=[
            f"<b>Share held, revenue didn't:</b> national value share 6.0% (flat); Q2 net revenue {money(a_q2)} "
            f"vs {money(p_q2)} plan ({var_q2:+.1f}%). The gap is structural to FY26, not a new deterioration.",
            "<b>Louisiana is the acute problem:</b> &minus;340 bps of local share (6.4% → 3.0%). Recovery is scoped and "
            "funded — see the turnaround plan, Report 24, and the South-region read, Report 39.",
            f"<b>Relevance is the lead diagnostic:</b> {rel25:.1f} → {rel26:.1f} T2B (&minus;{rel25-rel26:.1f} pp). "
            f"Trust holds at ~73. Social sentiment runs {ss.s:+.2f} on {int(ss.n)} 2026 mentions — a soft-negative signal.",
            "<b>The forward bet:</b> the Pack Refresh (Hero SKUs, $28M yr-1, launches 2026-08-15) is the biggest "
            "near-term innovation and the anchor of both the relevance rebuild and the LA recovery.",
        ])

    d.h1("1 · Brand scorecard")
    d.kpis([
        ("Net revenue (Q2)", money(a_q2), f"{var_q2:+.1f}% vs plan"),
        ("Natl value share", "6.0%", "flat, 6 qtrs"),
        ("Relevance (T2B)", f"{rel26:.1f}", f"−{rel25-rel26:.1f} pp vs FY25Q1"),
        ("Louisiana share", "3.0%", "−340 bps p-to-t"),
        ("Social sentiment", f"{ss.s:+.2f}", f"{int(ss.n)} mentions '26"),
    ])
    d.body(
        "The scorecard is amber. The franchise is intact at the national level — share, distribution and Trust are "
        "stable — but two indicators are red: Louisiana share and brand Relevance. Both point at the same underlying "
        "issue, a brand that is respected but no longer feels current to the shopper. Everything downstream of that — "
        "the revenue gap, the sentiment reading, the LA erosion accelerating where a modern challenger (Larksfield / "
        "Field &amp; Honey) presses hardest — is a symptom of it.")

    # national share trend chart
    ch_share = chart_line("r18_share.png", list(sh.q),
                          {"Crunchwell": [round(x, 2) for x in sh.cw],
                           "Larksfield": [round(x, 2) for x in sh.lf],
                           "Private label": [round(x, 2) for x in sh.pl]},
                          title="National RTE-cereal value share, ex-Louisiana (%)", pct=True, h=2.8)
    d.h2("1.1 · National share is stable — the problem is not the base")
    d.body(
        "Across six quarters Crunchwell's national value share holds at 6.0%, with Larksfield the share gainer at "
        "~14.0% and private label steady near 10.0%. Read plainly: this is not a national franchise in decline. "
        "The base is holding. That is exactly why the revenue gap and the Louisiana collapse deserve a surgical "
        "response rather than a wholesale relaunch — we are defending a stable, profitable core, not rescuing a "
        "franchise in free-fall.")
    d.image(ch_share, "National value share, ex-LA. Crunchwell flat at 6.0%; Larksfield the national gainer.")
    d.source("syndicated_weekly (RTE Cereal, ex LA-DMA), quarterly averages 2025-W01 → 2026 partial.")

    d.pagebreak()
    d.h1("2 · The revenue gap, sized")
    rows = [["2026-01", "$25.19M", "$23.75M", "−5.7%"],
            ["2026-02", "$25.19M", "$23.66M", "−6.0%"],
            ["2026-03", "$25.19M", "$23.69M", "−5.9%"],
            ["2026-04", "$25.19M", "$23.70M", "−5.9%"],
            ["2026-05", "$25.19M", "$23.75M", "−5.7%"]]
    d.h2("2.1 · Net revenue vs plan — FY26 monthly")
    d.table(["Month", "Plan", "Actual", "Var %"], rows,
            widths=[0.28, 0.24, 0.24, 0.24])
    d.source("plan_vs_actual (Acme ERP shape), Crunchwell brand, FY26 periods through May.")
    d.body(
        "The gap is remarkably consistent — 5.7 to 6.0% behind plan, every month. Consistency matters: it says "
        "the miss is structural (a plan set above where the brand is actually running, compounded by the Louisiana "
        "hole) rather than a fresh deterioration or an execution wobble. The absolute drag is roughly $1.5M/month, "
        "~$18M annualised, and a material fraction of that traces to a single DMA.")

    d.h1("3 · Louisiana — −340 bps of local share")
    la = df("""SELECT SUBSTR(Week,1,4)||'-Q'||CAST(CEIL(CAST(SUBSTR(Week,7,2) AS INT)/13.0) AS INT) q,
                 ROUND(AVG(Crunchwell_Value_Share)*100,2) cw
               FROM syndicated_weekly WHERE Category='RTE Cereal' AND DMA='LA-DMA'
                 AND Week>='2025-W01' GROUP BY 1 ORDER BY 1""")
    d.body(
        "Louisiana is the acute wound inside a stable body. The canonical headline (Mass/Grocery, peak-to-trough) "
        "is 6.4% → 3.0%, &minus;340 bps; the value-weighted all-channel cut is milder — Crunchwell LA-DMA value share "
        f"ran {la.cw.iloc[1]:.1f}% in early FY25 and troughed at {la.cw.min():.1f}% in Q1 FY26 before a partial "
        f"bounce to {la.cw.iloc[-1]:.1f}% in Q2 — but the direction is identical. New Orleans (5.1 → 3.0) and "
        "Baton Rouge (5.8 → 4.2) are the sharpest metros. The root cause is multi-factor: a Walmart modular reset "
        "that cut facings, Larksfield promo intensity, residual Hurricane Tonya supply disruption, private-label "
        "pressure, and a Hispanic-shopper mix the brand under-serves. The scoped, funded three-leg recovery lives in "
        "the turnaround plan (Report 24); the South-region operating detail is in Report 39.")
    ch_la = chart_line("r18_la.png", list(la.q), {"Crunchwell (LA-DMA)": [round(x, 2) for x in la.cw]},
                       title="Crunchwell Louisiana DMA value share (%)", pct=True, h=2.5)
    d.image(ch_la, "LA-DMA all-channel value share: trough in Q1 FY26, early Q2 stabilisation. Headline "
                   "peak-to-trough (Mass/Grocery) is 6.4% → 3.0%.")
    d.callout("Louisiana is where the relevance gap gets exploited",
              "The category itself is shrinking in Louisiana (RTE total ~$38M/qtr, −2.8%). Into that softness, a "
              "modern challenger presses on facings and promo. A trusted-but-dated brand is most exposed exactly "
              "where an aggressor is most active. LA is the national relevance problem, playing out fast in one DMA.", "risk")

    d.pagebreak()
    d.h1("4 · Brand equity — Relevance, not Trust")
    attrs = ["Relevance", "Trust", "Taste", "Quality", "Modernity"]
    fy25 = [eqd[a]["FY25Q1"] for a in attrs]
    fy26 = [eqd[a]["FY26Q2"] for a in attrs]
    d.body(
        f"The single most important diagnostic on this brand: <b>Relevance</b> has fallen {rel25:.1f} → {rel26:.1f} "
        f"top-two-box (&minus;{rel25-rel26:.1f} pp) over five waves, while <b>Trust</b> is flat-to-up "
        f"({eqd['Trust']['FY25Q1']:.1f} → {eqd['Trust']['FY26Q2']:.1f}) and <b>Quality</b> holds "
        f"({eqd['Quality']['FY25Q1']:.1f} → {eqd['Quality']['FY26Q2']:.1f}). Taste is essentially stable; "
        f"Modernity is soft ({eqd['Modernity']['FY25Q1']:.1f} → {eqd['Modernity']['FY26Q2']:.1f}). "
        "The pattern is unambiguous. Consumers still trust Crunchwell and rate its quality — they are simply "
        "deciding it matters less to them. That is a relevance problem, and it is fixable with modernization "
        "(pack, format, cultural fit) rather than a trust rebuild, which would be far slower and costlier.")
    ch_eq = chart_grouped("r18_equity.png", attrs,
                          {"FY25 Q1": fy25, "FY26 Q2": fy26},
                          title="Crunchwell brand equity, top-two-box % (US-NAT)", h=3.0)
    d.image(ch_eq, "Relevance and Modernity slip; Trust, Quality and Taste hold. The gap to close is relevance.")
    d.source("brand_equity_quarterly (Kantar-shape, US-NAT), waves FY25Q1 and FY26Q2; social_mentions 2026.")

    d.h1("5 · The innovation response")
    d.h2("5.1 · Pack Refresh — the anchor bet (launch 2026-08-15)")
    d.body(
        "The Crunchwell Pack Refresh (Hero SKUs) is in Stage-5 Launch Prep at $28M year-one and confidence 0.82 — "
        "the biggest near-term innovation in the company and the anchor of both the relevance rebuild and the "
        "Louisiana recovery (it is Leg 3 of the LA plan). Visual modernization directly targets the Relevance and "
        "Modernity gap without touching the Trust/Quality equity we want to protect. Launch is 2026-08-15.")
    d.h2("5.2 · The relevance-and-reach slate behind it")
    d.body(
        "Two concepts extend the thesis. The Hispanic <b>Maiz Crunch</b> format (Stage-2 Concept, $12M year-one, "
        "confidence 0.46, planned 2027-Q1) addresses a real gap — Crunchwell penetration in Hispanic households runs "
        "~4.1% vs ~11.7% non-Hispanic — and is directly tied to the Louisiana Hispanic-shopper hypothesis. The "
        "<b>Cinnamon Twist reformulation</b> (Stage-3, recovery track) rescues an underperforming SKU (CR006, launched "
        "2025 at ~41% ACV) flagged on negative review themes — reformulate or delist by Q3. FY27+ revenue figures "
        "here are planning estimates, not booked volume.")
    d.h2("Innovation slate — near-term")
    d.table(["Concept", "Stage", "Yr-1 (plan)", "Launch", "Role"],
            [["Pack Refresh — Hero SKUs", "Stage-5 Launch Prep", "$28.0M", "2026-08-15", "Relevance + LA anchor"],
             ["Hispanic Maiz Crunch", "Stage-2 Concept", "$12.0M", "2027-Q1 (plan)", "Reach / LA Hispanic"],
             ["Cinnamon Twist reformulation", "Stage-3 Prototype", "Recovery", "2026-Q4 (plan)", "SKU rescue"]],
            widths=[0.32, 0.24, 0.15, 0.15, 0.14])
    d.source("innovation_pipeline.csv (INV001, INV002, INV022). Year-1 revenue = planning estimate for FY27+ items.")

    d.callout("Watch-items into Q3",
              "(1) Pack Refresh execution — an $28M launch on 2026-08-15 must land clean; it is carrying two "
              "strategic jobs. (2) Louisiana stabilisation must hold and extend beyond the Q2 partial bounce. "
              "(3) Relevance is a slow-moving metric; expect the pack change to show in shipment and velocity before "
              "it shows in the tracker.", "risk")
    d.recommendations([
        ("Land the Pack Refresh on 2026-08-15 with full retail support; treat it as the relevance-rebuild anchor.",
         "Cory Whitman / Audrey Kim", "Aug — now"),
        ("Execute the funded Louisiana three-leg recovery (facings, targeted trade, LA retail media). See Report 24 / 39.",
         "Marcus Boudreaux", "Q3 — now"),
        ("Advance Maiz Crunch through Stage-2 to close the Hispanic-HH penetration gap tied to LA.",
         "Lillian Park", "FY27 planning"),
        ("Resolve Cinnamon Twist: reformulate on review-driven fixes or delist by Q3.",
         "Lillian Park", "Q3 gate"),
        ("Hold the FY26 Crunchwell number; report the relevance tracker monthly against pack-change milestones.",
         "Cory Whitman / Finance", "Monthly MBR"),
    ])
    return d.build()


# =========================================================== REPORT 19 =======
def r19_honeynest_fy27_plan():
    d = Doc("19-honeynest-fy27-annual-brand-plan.pdf",
            kicker="ANNUAL BRAND PLAN · FY27",
            title="HoneyNest — FY27 Annual Brand Plan",
            subtitle="Defending a $94M kids-sweet brand in a declining segment: hold share, cull the tail, lift margin",
            owner="Brand Manager — HoneyNest",
            period="FY2027", short="HoneyNest FY27 Plan",
            doc_type="Annual brand plan", date_str="July 2026")

    p_q1, a_q1, var_q1 = _brand_var("HoneyNest", ["2026-01", "2026-02", "2026-03"])
    ks24, g24, s24 = _cat("FY2024", "Kids Sweet")
    ks25, g25, s25 = _cat("FY2025", "Kids Sweet")

    d.cover_facts([
        ("Brand net revenue (FY25)", "$94M — Acme's kids-sweet franchise"),
        ("Segment (Kids Sweet)", f"${ks25/1000:.2f}B, {g25:+.1f}% YoY — declining"),
        ("FY26 run-rate vs plan", f"{var_q1:+.1f}% (on plan)"),
        ("Macro headwind", "'Kid-cereal mom-guilt' 0.68, Down"),
        ("FY27 posture", "Defend core · SKU cull · better-for-you reposition"),
    ])

    d.exec_summary(
        "HoneyNest is a $94M kids-sweet brand doing a hard job well: holding its position in a structurally declining "
        f"segment. Kids Sweet fell {g25:.1f}% in FY25 to ${ks25/1000:.2f}B and is pressured by a durable "
        "consumer shift — 'kid-cereal mom-guilt' (macro strength 0.68, trending down). Against that, HoneyNest is "
        f"running on plan ({var_q1:+.1f}% in Q1 FY26). The FY27 plan is therefore not a growth story; it is a "
        "disciplined defence — protect the core equity SKUs, rationalise a long tail of low-ACV products, run a "
        "single high-return LTO, and begin a credible better-for-you reposition that gives the brand a reason to "
        "exist as the segment shrinks. The FY27 target is roughly flat-to-slightly-down net revenue, share held, "
        "with margin improved by the SKU cull.",
        bullets=[
            f"<b>The market is the story:</b> Kids Sweet ${ks24/1000:.2f}B → ${ks25/1000:.2f}B "
            f"({g25:+.1f}%), a worsening decline (FY24 was {g24:+.1f}%). This is a defend-and-optimise segment, not a grow one.",
            f"<b>On plan today:</b> Q1 FY26 net revenue {money(a_q1)} vs {money(p_q1)} plan ({var_q1:+.1f}%). "
            "The brand is executing; the constraint is the category.",
            "<b>Cut the tail:</b> discontinue HoneyNest Granola Crunch (HN011, 18% ACV) and Cookie Dough "
            "(HN012, 12% ACV) in Q3 FY26 — both confirmed. Redirect the shelf and A&amp;P to the core.",
            "<b>Earn a future:</b> Birthday Cake LTO in Q4 ($2.4M, planning estimate) for buzz, and a Stage-1 "
            "better-for-you concept — HoneyNest Plus Whole Grain ($4M) — to test a mom-guilt answer.",
        ])

    d.h1("1 · Where HoneyNest plays — a declining segment")
    d.kpis([
        ("Brand net revenue", "$94M", "FY25, 12 SKUs"),
        ("Segment size", f"${ks25/1000:.2f}B", f"{g25:+.1f}% YoY"),
        ("Acme segment share", f"{s25:.1f}%", "Kids Sweet"),
        ("FY26 vs plan", f"{var_q1:+.1f}%", "on plan"),
        ("Mom-guilt macro", "0.68", "Down (kids)"),
    ])
    d.body(
        "The strategic frame is simple and it is set by the category, not the brand. Kids Sweet is in a durable "
        f"dollar decline — {g24:+.1f}% in FY24, worsening to {g25:+.1f}% in FY25 — driven by fewer kids at the "
        "breakfast table for sugary cereal and by parents' guilt about serving it. HoneyNest holds "
        f"{s25:.1f}% of that shrinking segment. A brand in this position wins by taking share of a smaller pie "
        "profitably and by finding an adjacent reason to exist, not by out-spending a secular decline.")
    seg = chart_bar("r19_segment.png",
                    ["Kids Sweet FY24", "Kids Sweet FY25"],
                    [ks24 / 1000, ks25 / 1000],
                    title="Kids Sweet segment size, $B (declining)", color="rust", unit="B", h=2.6)
    d.image(seg, "Kids Sweet dollars: FY24 → FY25 down −2.8%, worsening from −1.2% the prior year. The segment "
                 "is in secular decline, not a cyclical dip.")
    d.source("category_market_size.csv (NielsenIQ-shape), RTE Cereal / Kids Sweet, FY24–Q1FY26.")

    d.pagebreak()
    d.h1("2 · FY27 strategy — defend, cull, reposition")
    d.lede("Three moves: protect the equity core, rationalise the tail for margin, and plant a better-for-you flag.")
    d.h2("2.1 · Defend the core")
    d.body(
        "Nine of HoneyNest's twelve SKUs are genuine equity assets — Original (HN001, 72% ACV), Chocolate, Mega, "
        "Strawberry — carrying the brand's ~82% aided awareness. The FY27 plan protects them: hold distribution, "
        "keep the modest A&amp;P behind the hero SKUs, and defend facings against private label. No heroics; steady "
        "execution to hold share as the segment contracts.")
    d.h2("2.2 · SKU rationalisation — cut the tail")
    d.table(["SKU", "FY25 rev", "ACV", "Action", "Timing"],
            [["HoneyNest Granola Crunch (HN011)", "$1.4M", "18%", "Discontinue", "Q3 FY26"],
             ["HoneyNest Cookie Dough (HN012)", "$1.0M", "12%", "Discontinue", "Q3 FY26"]],
            widths=[0.40, 0.15, 0.12, 0.18, 0.15])
    d.source("skus.csv (HN011/HN012, status 'Delist Q3 2026'); innovation_pipeline.csv (INV024, INV025, confirmed).")
    d.body(
        "Both delist SKUs are confirmed for Q3 FY26. Together they are ~$2.4M of low-velocity, low-ACV revenue that "
        "consumes shelf, complexity and trade dollars out of proportion to their contribution. Culling them lifts "
        "portfolio margin, frees facings for the core, and simplifies the trade calendar — the primary FY27 margin "
        "lever. The revenue is small enough that share is defensible without it.")
    # before/after SKU count
    cull = chart_bar("r19_cull.png", ["SKUs before cull", "SKUs after cull (FY27)"],
                     [12, 10], title="HoneyNest SKU count — before / after rationalisation",
                     color="navy", unit="", h=2.3)
    d.image(cull, "12 → 10 active SKUs. Fewer, healthier lines; margin and shelf redirected to the core.")

    d.h2("2.3 · Reposition — a better-for-you flag")
    d.body(
        "The only durable answer to mom-guilt is a better-for-you proposition. FY27 plants two seeds. The "
        "<b>Birthday Cake LTO</b> (HN008 line, Stage-4 Pre-Launch, $2.4M year-one planning estimate, Q4 FY26) buys "
        "near-term buzz and nostalgia at low risk. More strategically, <b>HoneyNest Plus Whole Grain</b> — a "
        "heart-health kid range (Stage-1 Idea, $4M planning estimate, confidence 0.31) — tests whether the brand can "
        "credibly carry a whole-grain, mom-permission message. It is early and unproven; FY27 funds concept and "
        "screening, not a launch. Treated as an option on the brand's future, not a bet.")

    d.pagebreak()
    d.h1("3 · The FY27 plan — numbers & phasing")
    d.body(
        "The FY27 target is deliberately modest and honest: roughly flat-to-slightly-down net revenue against FY26, "
        "share held in Kids Sweet, and improved brand margin from the SKU cull and a leaner trade calendar. In a "
        f"segment declining ~{abs(g25):.0f}% a year, holding share while lifting margin is the win. All FY27 "
        "figures below are targets / planning estimates.")
    d.table(["Metric", "FY26 (est. actual)", "FY27 (target)", "Note"],
            [["Net revenue", "~$92M", "~$90–92M", "Flat-to-slightly-down; defend"],
             ["Kids Sweet share", "~5.0%", "Hold ~5.0%", "Share of a shrinking segment"],
             ["Active SKUs", "12", "10", "HN011 + HN012 delisted Q3 FY26"],
             ["Brand margin", "Baseline", "+ (tail cull)", "Primary FY27 lever"]],
            widths=[0.26, 0.24, 0.24, 0.26])
    d.source("plan_vs_actual (FY26 run-rate); skus.csv; category_market_size.csv. FY27 column = targets/plan.")

    d.h2("Plan phasing — FY27")
    d.table(["Quarter", "Focus"],
            [["Q3 FY26 (pre-FY27 setup)", "Execute HN011 + HN012 delist; redirect shelf & trade to core"],
             ["Q4 FY26 → FY27 Q1", "Birthday Cake LTO in market; measure buzz & incremental lift"],
             ["FY27 H1", "Defend core distribution & facings; hold share; lean trade calendar"],
             ["FY27 H2", "Advance HoneyNest Plus Whole Grain concept & screening; go/no-go gate"]],
            widths=[0.30, 0.70], align=["LEFT", "LEFT"])

    d.callout("The risk is over-investing behind a declining segment",
              "The wrong move is to chase kids-sweet growth with spend. The category is in secular decline (mom-guilt "
              "0.68, Down); Great Value private label presses on price. FY27 discipline is to defend efficiently, cull "
              "aggressively, and treat the better-for-you reposition as a low-cost option — not to spend our way "
              "against a shrinking pie.", "risk")
    d.recommendations([
        ("Execute the HN011 + HN012 delist in Q3 FY26; redirect shelf, trade and A&P to the core nine SKUs.",
         "Brand Manager — HoneyNest", "Q3 FY26"),
        ("Run the Birthday Cake LTO in Q4; measure incremental lift as a template for future LTOs.",
         "Lillian Park", "Q4 FY26"),
        ("Hold Kids Sweet share and lift brand margin via the tail cull and a leaner trade calendar.",
         "Brand Manager / Finance", "FY27"),
        ("Advance HoneyNest Plus Whole Grain to a Stage-2 go/no-go on the mom-guilt / whole-grain thesis.",
         "Lillian Park", "FY27 H2"),
    ])
    return d.build()


# =========================================================== REPORT 20 =======
def r20_morningoats_fy27_plan():
    d = Doc("20-morningoats-fy27-annual-brand-plan.pdf",
            kicker="ANNUAL BRAND PLAN · FY27",
            title="MorningOats — FY27 Annual Brand Plan",
            subtitle="A flat hot-cereal brand with a fast-growing pocket: play where single-serve and on-the-go win",
            owner="Brand Manager — MorningOats",
            period="FY2027", short="MorningOats FY27",
            doc_type="Annual brand plan", date_str="July 2026")

    p_q1, a_q1, var_q1 = _brand_var("MorningOats", ["2026-01", "2026-02", "2026-03"])
    tot24, gtot24, stot24 = _cat("FY2024", "Total", "Hot Cereal")
    inst24, ginst24, _ = _cat("FY2024", "Instant", "Hot Cereal")
    sc24, gsc24, ssc24 = _cat("FY2024", "Single-Serve Cups", "Hot Cereal")
    sc25, gsc25, ssc25 = _cat("FY2025", "Single-Serve Cups", "Hot Cereal")
    stl24, gstl24, _ = _cat("FY2024", "Steel-Cut", "Hot Cereal")
    ovn24, govn24, _ = _cat("FY2024", "Overnight", "Hot Cereal")

    d.cover_facts([
        ("Brand net revenue (FY25)", "~$93M — Acme's hot-cereal brand"),
        ("Hot Cereal total", f"${tot24/1000:.2f}B, {gtot24:+.1f}% — flat/declining"),
        ("The growth pocket", f"Single-Serve Cups {gsc25:+.1f}% YoY"),
        ("FY26 run-rate vs plan", f"{var_q1:+.1f}% (on plan)"),
        ("FY27 posture", "Grow single-serve / on-the-go; hold instant base"),
    ])

    d.exec_summary(
        "MorningOats is a ~$93M hot-cereal brand in a category that is going nowhere in aggregate — Hot Cereal total "
        f"grew {gtot24:+.1f}% and Instant, the largest sub-segment, is in decline ({ginst24:+.1f}%). But underneath "
        f"that flat headline is a real growth pocket: Single-Serve Cups grew {gsc25:+.1f}% in FY25, where Acme "
        f"already holds {ssc25:.0f}% share, and Overnight is the fastest emerging format ({govn24:+.1f}% off a small "
        "base). The consumer trend behind it — on-the-go single-serve breakfast (macro strength 0.72, Up) — is "
        f"durable. MorningOats is on plan today ({var_q1:+.1f}% in Q1 FY26). The FY27 plan is a deliberate mix shift: "
        "hold the instant base efficiently, and put innovation and A&amp;P behind cups and on-the-go formats where "
        "the category is actually growing.",
        bullets=[
            f"<b>Category is flat, but the pocket is hot:</b> Hot Cereal total {gtot24:+.1f}%, Instant "
            f"{ginst24:+.1f}%; Single-Serve Cups {gsc25:+.1f}% and Overnight {govn24:+.1f}%. Play where it grows.",
            f"<b>On plan:</b> Q1 FY26 net revenue {money(a_q1)} vs {money(p_q1)} plan ({var_q1:+.1f}%). "
            "Execution is sound; the opportunity is mix, not fixing a miss.",
            "<b>Grow single-serve:</b> Pumpkin Spice Cup LTO (Stage-4, $1.8M, Q3 FY26) is a near-term, high-confidence "
            "(0.72) seasonal win in the growth format.",
            "<b>Extend on-the-go:</b> Overnight Banana prototype (Stage-3, $2.1M, 2027-Q1 planning estimate) "
            "extends the emerging overnight format if MO008 Vanilla validates the occasion.",
        ])

    d.h1("1 · The category picture — flat total, a growing pocket")
    d.kpis([
        ("Brand net revenue", "~$93M", "FY25, 8 SKUs"),
        ("Hot Cereal total", f"${tot24/1000:.2f}B", f"{gtot24:+.1f}%"),
        ("Single-Serve Cups", f"{gsc25:+.0f}%", f"{ssc25:.0f}% Acme share"),
        ("FY26 vs plan", f"{var_q1:+.1f}%", "on plan"),
        ("On-the-go macro", "0.72", "Up"),
    ])
    d.body(
        "The single most important slide in this plan is the sub-segment growth split. Reading Hot Cereal as one flat "
        "number hides the opportunity. Instant — the biggest slice — is declining and dominated by Quaker; steel-cut "
        "is a premium niche. But Single-Serve Cups and Overnight are growing double-digit, and they map directly to "
        "the on-the-go breakfast occasion where MorningOats' Cup line already over-indexes. FY27 is about deliberately "
        "shifting weight into that pocket.")
    sub = chart_bar("r20_subseg.png",
                    ["Instant", "Steel-Cut", "Single-Serve Cups", "Overnight"],
                    [ginst24, gstl24, gsc25, govn24],
                    title="Hot Cereal sub-segment YoY growth (%)", pct=True,
                    colors_list=["#B24A2E", "#5B6472", "#2E7D75", "#2E7D75"], h=2.7)
    d.image(sub, "Instant declines; cups (+9.8% FY25) and overnight (+18.6%) grow. The growth is in single-serve / "
                 "on-the-go, where MorningOats already plays.")
    d.source("category_market_size.csv (NielsenIQ-shape), Hot Cereal sub-segments; Instant/Steel-Cut/Overnight FY24, "
             "Single-Serve Cups FY25.")

    d.pagebreak()
    d.h1("2 · The single-serve opportunity, sized")
    d.body(
        f"Single-Serve Cups is a ${sc25/1000:.2f}B sub-segment growing {gsc25:+.1f}%, and Acme holds ~{ssc25:.0f}% of "
        "it — well above the ~4% share MorningOats holds in Hot Cereal overall. Three of the brand's eight SKUs are "
        "already cups (Maple, Apple Cinnamon, Cinnamon Roll), carrying strong unit velocity at a premium $2.49 price. "
        "This is the brand's right to win: a growing format, a demonstrated share advantage, and a proven consumer "
        "occasion. The Overnight sub-segment is smaller and earlier but grows fastest of all; MO008 Overnight Vanilla "
        "is the brand's toe-hold there.")
    cups = chart_bar("r20_cups.png",
                     ["Instant", "Single-Serve Cups", "Steel-Cut", "Overnight"],
                     [inst24, sc25, stl24, ovn24],
                     title="Hot Cereal sub-segment size, $M (where the growth pocket sits)",
                     color="navy", unit="M", h=2.7)
    d.image(cups, "Cups are a ~$560M pocket growing +9.8%; overnight is small but +18.6%. Instant is large but "
                  "declining. MorningOats over-indexes in the growth formats.")
    d.callout("The strategic read: mix, not miracles",
              "MorningOats does not need to reverse a category decline; it needs to shift its own mix toward the "
              "growing pocket. Every incremental A&P and innovation dollar should favour cups and on-the-go over "
              "defending instant, which is a share-hold job at best.", "info")

    d.h1("3 · FY27 innovation plan — grow the growth pocket")
    d.h2("3.1 · Pumpkin Spice Cup LTO — the near-term win")
    d.body(
        "The Pumpkin Spice Cup LTO (Stage-4 Pre-Launch, $1.8M year-one planning estimate, confidence 0.72, Q3 FY26) "
        "is the highest-confidence near-term move: a seasonal LTO in the growing cup format, repeating the proven "
        "success of the Cinnamon Roll cup. Low risk, on-trend, in the right pocket.")
    d.h2("3.2 · Overnight Banana — extend the emerging format")
    d.body(
        "Overnight Banana (Stage-3 Prototype, $2.1M year-one planning estimate, confidence 0.54, planned 2027-Q1) "
        "extends MorningOats into the fastest-growing hot-cereal format. It is explicitly contingent: it advances "
        "only if MO008 Overnight Vanilla validates the refrigerator-ready overnight occasion. FY27 funds the "
        "prototype and the read on Vanilla, not an unconditional launch. FY27+ revenue is a planning estimate.")
    d.h2("Innovation slate — FY27")
    d.table(["Concept", "Stage", "Yr-1 (plan)", "Conf.", "Launch"],
            [["MorningOats Cup Pumpkin Spice LTO", "Stage-4 Pre-Launch", "$1.8M", "0.72", "Q3 FY26"],
             ["MorningOats Overnight Banana", "Stage-3 Prototype", "$2.1M", "0.54", "2027-Q1 (plan)"]],
            widths=[0.38, 0.24, 0.13, 0.10, 0.15])
    d.source("innovation_pipeline.csv (INV016, INV008). Year-1 revenue & FY27 launch = planning estimates.")

    d.pagebreak()
    d.h1("4 · The FY27 plan — targets & phasing")
    d.body(
        "FY27 targets modest net-revenue growth driven entirely by mix — cups and on-the-go up, instant held flat — "
        "with share gains concentrated in the Single-Serve Cups pocket. The instant base is a defend-and-harvest job. "
        "All FY27 figures are targets / planning estimates.")
    d.table(["Metric", "FY26 (est. actual)", "FY27 (target)", "Note"],
            [["Net revenue", "~$92M", "~$93–95M", "Modest growth via mix shift"],
             ["Single-Serve Cups share", f"~{ssc25:.0f}%", "Grow", "The right-to-win pocket"],
             ["Instant base", "Declining category", "Hold", "Defend / harvest efficiently"],
             ["Innovation live", "—", "2 (Pumpkin LTO, Overnight Banana)", "Both in the growth pocket"]],
            widths=[0.26, 0.24, 0.26, 0.24])
    d.source("plan_vs_actual (FY26 run-rate); category_market_size.csv; innovation_pipeline.csv. FY27 = targets/plan.")

    d.h2("Plan phasing — FY27")
    d.table(["Quarter", "Focus"],
            [["Q3 FY26", "Pumpkin Spice Cup LTO in market; read seasonal cup lift"],
             ["Q4 FY26 → FY27 Q1", "Confirm MO008 Overnight Vanilla occasion; go/no-go on Overnight Banana"],
             ["FY27 H1", "Overnight Banana launch (if validated); grow cup distribution & velocity"],
             ["FY27 H2", "Hold instant base; shift A&P weight toward on-the-go formats"]],
            widths=[0.30, 0.70], align=["LEFT", "LEFT"])

    d.callout("Watch-item — don't over-fund a niche too early",
              "Overnight is the fastest-growing format but a small absolute pool; Overnight Banana is gated on the "
              "MO008 Vanilla read for good reason. The near-term, dependable value is the cup LTO in a proven "
              "$560M+ pocket. Sequence spend accordingly.", "risk")
    d.recommendations([
        ("Launch the Pumpkin Spice Cup LTO in Q3 FY26; treat cups as the priority growth format.",
         "Brand Manager — MorningOats", "Q3 FY26"),
        ("Confirm the MO008 Overnight Vanilla occasion read; gate Overnight Banana on the result.",
         "Lillian Park", "Q4 FY26"),
        ("Shift FY27 A&P and shelf weight from instant toward single-serve / on-the-go.",
         "Brand Manager", "FY27 planning"),
        ("Grow Single-Serve Cups share; hold the instant base efficiently as a harvest segment.",
         "Brand Manager / Finance", "FY27"),
    ])
    return d.build()


# =========================================================== REPORT 21 =======
def r21_trailgrove_fy27_plan():
    d = Doc("21-trailgrove-fy27-annual-brand-plan.pdf",
            kicker="ANNUAL BRAND PLAN · FY27",
            title="TrailGrove — FY27 Annual Brand Plan",
            subtitle="Acme's healthy portfolio anchor: extend a $152M granola/bars franchise into the growth pockets",
            owner="Brand Manager — TrailGrove",
            period="FY2027", short="TrailGrove FY27",
            doc_type="Annual brand plan", date_str="July 2026")

    p_q1, a_q1, var_q1 = _brand_var("TrailGrove", ["2026-01", "2026-02", "2026-03"])
    gtot24, ggro24, sgro24 = _cat("FY2024", "Total", "Granola")
    gtot25, ggro25, sgro25 = _cat("FY2025", "Total", "Granola")
    bar24, gbar24, sbar24 = _cat("FY2024", "Granola Bar", "Bar")
    gss24, gss_g24, gss_s24 = _cat("FY2024", "Single-Serve", "Granola")

    d.cover_facts([
        ("Brand net revenue (FY25)", "$152M — Acme's #2 brand"),
        ("Granola segment", f"${gtot25/1000:.2f}B, {ggro25:+.1f}% — healthy grower"),
        ("Bar segment", f"${bar24/1000:.2f}B, {gbar24:+.1f}% — steady"),
        ("FY26 run-rate vs plan", f"{var_q1:+.1f}% (on plan)"),
        ("FY27 posture", "Extend into growth: bites, Hispanic, single-serve"),
    ])

    d.exec_summary(
        "TrailGrove is Acme's second-largest brand ($152M FY25) and its healthiest — a granola and bars franchise "
        f"sitting in growing, on-trend segments. Granola grew {ggro25:+.1f}% in FY25 to ${gtot25/1000:.2f}B, where "
        f"Acme holds a category-leading ~{sgro25:.1f}% share; Granola Bars are a large, steady ${bar24/1000:.2f}B "
        f"segment ({gbar24:+.1f}%). TrailGrove is on plan ({var_q1:+.1f}% in Q1 FY26). Unlike the defend-oriented "
        "plans elsewhere in the portfolio, TrailGrove's FY27 job is offence: extend the franchise into the growth "
        "pockets — yogurt-coated snacking bites, a Hispanic trail-mix format, and single-serve granola cups — and "
        "position the brand explicitly as Acme's healthy / active-lifestyle portfolio anchor.",
        bullets=[
            f"<b>Healthy, growing segments:</b> Granola {ggro25:+.1f}% (${gtot25/1000:.2f}B, ~{sgro25:.1f}% Acme "
            f"share); Granola Bars steady at {gbar24:+.1f}%. This is a brand that gets to play offence.",
            f"<b>On plan:</b> Q1 FY26 net revenue {money(a_q1)} vs {money(p_q1)} plan ({var_q1:+.1f}%). Solid base to build on.",
            "<b>Extend into snacking:</b> TrailGrove Bites Yogurt-Coated (Stage-2, $3.6M, 2027-Q2 planning estimate) "
            "enters the kid-lunchbox snacking occasion KIND owns with Bites.",
            "<b>Reach & convenience:</b> a Hispanic Trail Mix Mango-Chile format ($2.4M, companion to the portfolio "
            "Hispanic strategy) plus single-serve granola cups extend the franchise into growing formats.",
        ])

    d.h1("1 · A healthy brand in growing segments")
    d.kpis([
        ("Brand net revenue", "$152M", "FY25, #2 brand"),
        ("Granola segment", f"{ggro25:+.1f}%", f"~{sgro25:.1f}% Acme share"),
        ("Granola Bars", f"{gbar24:+.1f}%", f"${bar24/1000:.2f}B, steady"),
        ("FY26 vs plan", f"{var_q1:+.1f}%", "on plan"),
        ("Active-lifestyle fit", "Anchor", "healthy portfolio"),
    ])
    d.body(
        f"TrailGrove's position is enviable: it leads a growing category. Acme holds ~{sgro25:.1f}% of Granola — its "
        "highest share in any segment — and granola is growing steadily on the back of a clean-ingredient, "
        "real-food consumer trend. Granola Bars add a large, stable base. That combination means the FY27 plan can "
        "be built around extension and reach rather than defence. The brand's role in the portfolio is to be the "
        "healthy / active anchor — the credible answer to a wellness-oriented shopper across granola, bars and "
        "snacking formats.")
    seg = chart_bar("r21_segment.png",
                    ["Granola (FY25)", "Granola Bars (FY24)", "Granola single-serve (FY24)"],
                    [ggro25, gbar24, gss_g24],
                    title="TrailGrove's segments — YoY growth (%)", pct=True,
                    colors_list=["#2E7D75", "#2E7D75", "#2E7D75"], h=2.6)
    d.image(seg, "Granola +3.3%, bars +2.1% steady, granola single-serve +8.4% — all growing. TrailGrove plays in "
                 "healthy, on-trend pockets.")
    d.source("category_market_size.csv (NielsenIQ-shape), Granola & Bar segments, FY24–FY25.")

    d.pagebreak()
    d.h1("2 · Franchise health & the case for offence")
    d.body(
        "TrailGrove's ten SKUs span three formats — granola pouches (the core, led by Honey Almond at 68% ACV), "
        "granola bars (Honey Almond, PB Chocolate, Mixed Berry), and a trail-mix entry. The portfolio is broad, "
        f"premium-priced, and healthy in a market that increasingly rewards exactly that. Sitting on-plan "
        f"({var_q1:+.1f}%) in growing segments is the strongest position in the brand book — it earns the right to "
        "invest for extension. The FY27 thesis: take the brand's healthy credibility into three adjacent growth "
        "pockets rather than deepen an already-strong core.")
    grow = chart_bar("r21_size.png",
                     ["Granola total", "Granola bars", "Granola clusters", "Granola single-serve"],
                     [gtot25, bar24, _cat("FY2024", "Clusters", "Granola")[0], gss24],
                     title="TrailGrove-adjacent segment size, $M", color="navy", unit="M", h=2.7)
    d.image(grow, "The addressable pools: a ~$1.9B granola segment and a ~$3.0B granola-bar segment, with growing "
                  "clusters and single-serve pockets to extend into.")
    d.callout("Position: the healthy / active portfolio anchor",
              "Where Crunchwell is the trusted flagship and ProteinPeak the wellness-protein growth engine, TrailGrove "
              "is the everyday healthy anchor — granola, bars, and snacking for the active, clean-label shopper. "
              "FY27 investment should reinforce that role, not dilute it.", "info")

    d.h1("3 · FY27 innovation plan — extend into growth")
    d.h2("3.1 · TrailGrove Bites Yogurt-Coated — the snacking extension")
    d.body(
        "TrailGrove Bites Yogurt-Coated (Stage-2 Concept, $3.6M year-one planning estimate, confidence 0.48, planned "
        "2027-Q2) is the headline FY27 extension: entering the kid-lunchbox snacking occasion that KIND currently owns "
        "with its Bites line. It carries TrailGrove's healthy credibility into a high-frequency snacking format and is "
        "the largest new-revenue opportunity in the FY27 slate.")
    d.h2("3.2 · Hispanic Mango-Chile & single-serve cups — reach and convenience")
    d.body(
        "Two further moves extend reach and format. The Hispanic <b>Trail Mix Mango-Chile</b> format (Stage-2 Concept, "
        "$2.4M year-one planning estimate, confidence 0.34, 2027-Q2) is the companion to the portfolio's Hispanic "
        "strategy (alongside Crunchwell Maiz Crunch). <b>Single-serve granola cups</b> (Stage-2 Concept, $2.9M "
        "planning estimate) take the granola franchise into the growing convenience format. Both are early-stage "
        "concepts; FY27 funds concept validation and screening, not committed launches. FY27+ revenue figures are "
        "planning estimates.")
    d.h2("Innovation slate — FY27")
    d.table(["Concept", "Stage", "Yr-1 (plan)", "Conf.", "Launch"],
            [["TrailGrove Bites — Yogurt-Coated", "Stage-2 Concept", "$3.6M", "0.48", "2027-Q2 (plan)"],
             ["Trail Mix Mango-Chile (Hispanic)", "Stage-2 Concept", "$2.4M", "0.34", "2027-Q2 (plan)"],
             ["Granola Single-Serve Cups", "Stage-2 Concept", "$2.9M", "0.36", "2027-Q4 (plan)"]],
            widths=[0.38, 0.22, 0.14, 0.10, 0.16])
    d.source("innovation_pipeline.csv (INV009, INV014, INV021). Year-1 revenue & FY27 launch = planning estimates.")

    d.pagebreak()
    d.h1("4 · The FY27 plan — targets & phasing")
    d.body(
        "TrailGrove is the one brand in this planning cycle with an unambiguous growth target. FY27 aims for "
        "low-single-digit net-revenue growth, share held-to-gained in Granola, and three extension concepts advanced "
        "through their stage gates. All FY27 figures are targets / planning estimates.")
    d.table(["Metric", "FY26 (est. actual)", "FY27 (target)", "Note"],
            [["Net revenue", "~$150M", "~$155–158M", "Low-single-digit growth"],
             ["Granola share", f"~{sgro25:.1f}%", "Hold / gain", "Category-leading position"],
             ["Extension concepts live/advancing", "—", "3", "Bites, Hispanic, SS cups"],
             ["Portfolio role", "Healthy anchor", "Reinforce", "Active-lifestyle positioning"]],
            widths=[0.30, 0.22, 0.22, 0.26])
    d.source("plan_vs_actual (FY26 run-rate); category_market_size.csv; innovation_pipeline.csv. FY27 = targets/plan.")

    d.h2("Plan phasing — FY27")
    d.table(["Quarter", "Focus"],
            [["Q4 FY26 → FY27 Q1", "Advance Bites Yogurt-Coated & Mango-Chile through Stage-2 validation"],
             ["FY27 H1", "Bites launch prep; grow core granola & bar distribution"],
             ["FY27 Q2", "TrailGrove Bites + Mango-Chile launch (planning target)"],
             ["FY27 H2", "Single-serve granola cups screening; reinforce healthy-anchor positioning"]],
            widths=[0.30, 0.70], align=["LEFT", "LEFT"])

    d.callout("Watch-item — concept confidence is still low",
              "The FY27 extensions are Stage-2 with modest confidence scores (0.34–0.48). They are options to be "
              "validated, not committed launches. Gate spend on stage-gate reads; protect the healthy, on-plan core "
              "regardless of how the extensions test.", "risk")
    d.recommendations([
        ("Advance TrailGrove Bites Yogurt-Coated through Stage-2; treat it as the priority FY27 extension.",
         "Brand Manager — TrailGrove", "FY27 H1"),
        ("Progress the Hispanic Mango-Chile format as the companion to the portfolio Hispanic strategy.",
         "Lillian Park", "FY27 H1"),
        ("Validate single-serve granola cups; extend the franchise into the growing convenience format.",
         "Lillian Park", "FY27 H2"),
        ("Deliver low-single-digit growth and reinforce TrailGrove as the healthy / active portfolio anchor.",
         "Brand Manager / Finance", "FY27"),
    ])
    return d.build()


if __name__ == "__main__":
    for fn in (r18_crunchwell_q2_brand_review,
               r19_honeynest_fy27_plan,
               r20_morningoats_fy27_plan,
               r21_trailgrove_fy27_plan):
        print(fn())
