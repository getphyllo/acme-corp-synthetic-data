"""Brand-level reports 22-24: RootDay, ProteinPeak, Crunchwell.

Run from repo root:
    .venv/bin/python reports/generators/brands2.py

Every headline number traces to acme.duckdb, seeds/*.csv, or FACTS.md.
Forward numbers (FY27+ targets, next-quarter forecasts) are labelled
"target" / "plan" / "planning estimate" in-document. No invented history.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import (Doc, df, seed_csv, money, palette,
                 chart_line, chart_bar, chart_grouped, chart_stacked,
                 chart_waterfall, chart_donut)


# ---------------------------------------------------------------- helpers ----
def _brand_q2fy26(brand):
    """Q2 FY26 partial actuals (Apr–May) vs plan for a brand, from plan_vs_actual."""
    r = df(f"""SELECT SUM(Plan_Revenue_USD)/1e6 p, SUM(Actual_Revenue_USD)/1e6 a
               FROM plan_vs_actual
               WHERE Brand='{brand}' AND Period IN ('2026-04','2026-05')""").iloc[0]
    p, a = float(r.p), float(r.a)
    return p, a, (a - p) / p * 100


def _brand_monthly(brand, periods):
    ps = ",".join(f"'{x}'" for x in periods)
    return df(f"""SELECT Period,
                    ROUND(SUM(Plan_Revenue_USD)/1e6,2) plan,
                    ROUND(SUM(Actual_Revenue_USD)/1e6,2) act,
                    ROUND((SUM(Actual_Revenue_USD)-SUM(Plan_Revenue_USD))
                          /SUM(Plan_Revenue_USD)*100,1) var
                  FROM plan_vs_actual WHERE Brand='{brand}' AND Period IN ({ps})
                  GROUP BY Period ORDER BY Period""")


# ============================================================== REPORT 22 ====
def r22_rootday_brand_review():
    d = Doc("22-rootday-q2-2026-brand-review-fy27-outlook.pdf",
            kicker="BRAND REVIEW · Q2 FY2026",
            title="RootDay — Q2 FY2026 Brand Review & FY27 Outlook",
            subtitle="A $62M oat-milk franchise riding the category's fastest adjacency",
            owner="Brand Manager — RootDay (Lillian Park, Innovation lead, contributor)",
            period="Q2 FY2026 · FY27 outlook", short="RootDay Q2 + FY27",
            doc_type="Internal brand review", date_str="July 2026")

    p, a, var = _brand_q2fy26("RootDay")   # Apr–May FY26 actuals vs plan
    d.cover_facts([
        ("FY25 net revenue", "$62M (acquired 2023; ~12.3M units)"),
        ("Q2 FY26 vs plan (Apr–May)", f"{money(a)} actual vs {money(p)} plan · {var:+.1f}%"),
        ("Category tailwind", "Oat plant-based milk +18.8% (fastest adjacency)"),
        ("Barista trend strength", "0.84 — the volume engine of oat milk"),
        ("FY27 headline call", "Grow with the category; land Coffee Creamer, hold Single-Serve"),
    ])

    d.exec_summary(
        "RootDay is a small brand in a fast lane. Oat-milk — the plant-based-milk pocket where RootDay "
        "lives — grew +18.8% in FY25 to $1.64B while almond declined and coconut stalled, and the "
        "barista/foodservice use-case (trend strength 0.84) is the volume engine underneath that growth. "
        "The brand is on plan: Q2 FY26 is running "
        f"{var:+.1f}% to plan (essentially flat), the steadiest read in the Acme portfolio. The FY27 job is "
        "simple to state and disciplined to execute — grow with the category, not against it: extend into "
        "the barista/creamer occasion, prune the tail, and avoid over-investing ahead of demand.",
        bullets=[
            "<b>On plan.</b> RootDay ran &minus;0.3% to plan in Jan–Mar and "
            f"{var:+.1f}% in Apr–May FY26 — the tightest plan adherence of any Acme brand (plan_vs_actual).",
            "<b>The tailwind is real and specific.</b> Oat is the only growing plant-based-milk segment "
            "(+18.8% FY25); almond is in structural decline (&minus;2.4%) and the barista occasion (0.84) "
            "is where the incremental volume sits.",
            "<b>FY27 innovation is a two-item agenda:</b> advance <i>RootDay Coffee Creamer 16oz</i> "
            "(Stage-2 concept, $3.8M yr-1 planning estimate, target 2027-Q3) into the barista/creamer "
            "occasion; hold <i>Single-Serve Carton 8oz</i> (Stage-3, On-Hold).",
            "<b>Prune the tail.</b> Coconut Blend is slated to discontinue in Q3 FY26 — a low-velocity SKU "
            "in a low-growth segment (coconut+other +4.2% vs oat +18.8%).",
        ])

    # --- 1 · category context
    d.h1("1 · The category is doing the heavy lifting")
    d.kpis([
        ("Oat milk $ growth", "+18.8%", "FY25, $1.64B"),
        ("Almond (mature)", "−2.4%", "structural decline"),
        ("Barista trend", "0.84", "oat-milk volume engine"),
        ("RootDay vs plan", f"{var:+.1f}%", "Q2 FY26, on plan"),
    ])
    d.body(
        "RootDay's entire strategic advantage is <i>where it plays</i>. Within plant-based milk, oat is the "
        "growth engine — up +18.8% in FY25 to $1.64B — while almond, the legacy volume leader, is shrinking "
        "(&minus;2.4%) and coconut-and-other is flat-to-modest (+4.2%). This is the mirror image of "
        "Crunchwell's problem: RootDay does not have to fight its category to grow, it has to keep pace with "
        "it. The pull is concentrated in the barista/foodservice occasion — the macro trend Acme tracks at "
        "0.84 strength and labels 'the volume engine of oat milk' — which is exactly the whitespace the FY27 "
        "concept slate targets.")

    ch_cat = chart_bar("r22_oatmilk_vs_peers.png",
                       ["Oat", "Coconut + other", "Almond"],
                       [18.8, 4.2, -2.4],
                       title="Plant-based milk — value growth by segment (%)", pct=True,
                       colors_list=[palette["teal"], palette["gold"], palette["rust"]],
                       h=2.7)
    d.image(ch_cat, "Oat is the only segment growing double-digit; almond is in structural decline. "
                    "Oat FY25 vs prior year; almond/coconut FY24 latest full-year comparators "
                    "(seed_category_market_size).")
    d.source("seed_category_market_size (NielsenIQ Total US xAOC), Plant-Based Milk; "
             "seed_macro_trends MT002 (oat-milk barista 0.84).")

    # --- 2 · revenue vs plan
    d.h1("2 · Performance — steady, and on plan")
    m = _brand_monthly("RootDay", ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05"])
    lbl = {"2026-01": "Jan", "2026-02": "Feb", "2026-03": "Mar", "2026-04": "Apr", "2026-05": "May"}
    rows = [[lbl[r.Period], f"${r.plan:.2f}M", f"${r.act:.2f}M", f"{r.var:+.1f}%",
             "On plan"] for r in m.itertuples()]
    tp = float(m.plan.sum()); ta = float(m.act.sum())
    rows.append(["FY26 YTD (Jan–May)", f"${tp:.2f}M", f"${ta:.2f}M",
                 f"{(ta-tp)/tp*100:+.1f}%", "On plan"])
    d.h2("2.1 · RootDay net revenue vs plan — FY26 YTD")
    d.table(["Month", "Plan", "Actual", "Var %", "Status"], rows,
            widths=[0.30, 0.18, 0.18, 0.16, 0.18], total_row=True)
    d.source("plan_vs_actual (Acme ERP shape), RootDay, 2026-01 through 2026-05.")

    ch_rev = chart_line("r22_rev_vs_plan.png",
                        [lbl[p] for p in m.Period],
                        {"Plan": [float(x) for x in m.plan],
                         "Actual": [float(x) for x in m.act]},
                        title="RootDay net revenue — actual vs plan ($M/mo)", h=2.7)
    d.image(ch_rev, "Actuals track plan within a few tenths of a point every month — the steadiest line "
                    "in the portfolio.")
    d.callout("On plan is the right answer here",
              "RootDay is not the brand where Acme needs a heroic number. At &minus;0.3% to plan in Q1 and "
              f"{var:+.1f}% in Q2-to-date, it is doing its job: holding a profitable, growing niche while the "
              "portfolio's discretionary innovation dollars flow to ProteinPeak (growth engine) and "
              "Crunchwell (flagship turnaround). The FY27 plan protects that discipline.", "win")

    d.pagebreak()
    # --- 3 · FY27 outlook / innovation
    d.h1("3 · FY27 outlook — grow with the category, land the barista occasion")
    d.body(
        "FY27 is a growth-with-the-category plan, not a step-change. The single most important move is to "
        "convert the barista/creamer occasion — the 0.84-strength trend where oat-milk volume actually sits — "
        "into a RootDay SKU. Two concepts are in the pipeline and one legacy SKU is being retired. All FY27 "
        "revenue figures below are planning estimates carried at the pipeline's stated year-1 potential and "
        "confidence, not booked demand.")

    pipe = seed_csv("innovation_pipeline.csv")
    rd = pipe[pipe["brand"] == "RootDay"].copy()

    def _rev(x):
        try:
            return f"${float(x):.1f}M"
        except (ValueError, TypeError):
            return "—"

    order = {"INV006": 0, "INV005": 1, "INV023": 2, "INV013": 3, "INV018": 4}
    rd["ord"] = rd["concept_id"].map(order).fillna(9)
    rd = rd.sort_values("ord")
    prows = []
    for r in rd.itertuples():
        conf = "" if r.confidence_score_0to1 != r.confidence_score_0to1 else f"{r.confidence_score_0to1:.2f}"
        prows.append([r.concept_name.replace("RootDay ", ""), r.stage_gate.replace("Stage-", "S"),
                      str(r.planned_launch_date), _rev(r.projected_revenue_year1_musd),
                      conf if conf else "—", r.status])
    d.h2("3.1 · RootDay FY27 concept pipeline")
    d.table(["Concept", "Stage", "Planned", "Yr-1 (est.)", "Conf.", "Status"], prows,
            widths=[0.30, 0.14, 0.15, 0.14, 0.11, 0.16],
            align=["LEFT", "LEFT", "LEFT", "RIGHT", "RIGHT", "LEFT"])
    d.source("seeds/innovation_pipeline.csv (RootDay). Yr-1 revenue = planning estimate; confidence 0–1.")

    ch_pipe = chart_bar("r22_pipeline.png",
                        ["Coffee Creamer\n16oz (S2)", "Single-Serve\nCarton (S3, hold)",
                         "Yogurt Smoothie\n(S1 idea)", "Half-Gallon\n(S1 idea)"],
                        [3.8, 4.5, 6.0, 5.5],
                        title="RootDay pipeline — year-1 revenue potential ($M, planning estimate)",
                        colors_list=[palette["teal"], palette["slate"], palette["gold"], palette["gold"]],
                        unit="", h=2.7)
    d.image(ch_pipe, "Coffee Creamer (teal) is the FY27 priority — nearest-stage, on-trend. Single-Serve "
                     "Carton (grey) is larger but On-Hold. Ideas (gold) are FY28+.")

    d.h2("3.2 · Advance: RootDay Coffee Creamer 16oz")
    d.body(
        "<b>Stage-2 concept · $3.8M year-1 planning estimate · confidence 0.42 · target 2027-Q3 · "
        "owner Lillian Park.</b> This is the FY27 priority. The barista occasion is where oat-milk volume "
        "concentrates (trend 0.84), and a shelf-stable 16oz creamer extends RootDay from the pour-over-cereal "
        "and latte occasion into everyday coffee — a foodservice-adjacent, higher-frequency use. The "
        "confidence score (0.42) reflects that this is early-stage; the recommendation is to fund concept "
        "validation and a barista/foodservice channel test in FY27, not to over-commit spend ahead of the "
        "read.")

    d.h2("3.3 · Hold: RootDay Single-Serve Carton 8oz")
    d.callout("Single-Serve Carton is On-Hold — keep it there for now",
              "INV005 (Stage-3 prototype, $4.5M year-1 planning estimate, confidence 0.58, target 2027-Q2) "
              "is the larger single-serve bet, but its status is On-Hold. Single-serve is a real format trend, "
              "but with Coffee Creamer the priority barista play and RootDay's innovation budget deliberately "
              "modest, the discipline is to hold the carton until Creamer reads and capex/co-man capacity is "
              "confirmed. Do not re-activate this quarter.", "risk")

    d.h2("3.4 · Prune: discontinue Coconut Blend (Q3 FY26)")
    d.body(
        "RootDay Coconut Blend is slated for discontinuation in Q3 FY26 (INV023, Discontinue-Plan). The "
        "rationale is portfolio hygiene: coconut-and-other grows only +4.2% against oat's +18.8%, the SKU is "
        "a low-velocity niche, and retiring it frees shelf argument and working capital for the on-trend oat "
        "and creamer line. Manage the transition with retailers to protect total RootDay distribution.")

    # --- 4 · risks + recs
    d.h1("4 · Risks & the FY27 ask")
    d.callout("Watch-items into FY27",
              "(1) Oat-milk is a magnet for entrants — Califia (barista), Silk and Oatly all launched oat SKUs "
              "in 2025; RootDay must earn the barista occasion before larger players lock it. "
              "(2) The GLP-1/appetite-shift trend (0.81, volume-down) is a low-grade headwind on beverage "
              "volume broadly. (3) Coffee Creamer is confidence 0.42 — treat FY27 as a validate-and-test year, "
              "not a full-scale launch commitment.", "risk")
    d.recommendations([
        ("Advance RootDay Coffee Creamer 16oz through concept validation + a barista/foodservice channel "
         "test; gate a FY27-Q3 launch decision on the read.", "Brand Manager / Lillian Park", "FY27 H1"),
        ("Keep Single-Serve Carton 8oz On-Hold; re-evaluate only after Creamer reads and co-man capacity "
         "is confirmed.", "Lillian Park", "FY27 H2 review"),
        ("Execute the Coconut Blend discontinuation with retailer transition management to protect total "
         "distribution.", "Brand Manager", "Q3 FY26"),
        ("Hold the FY27 plan to grow with the oat category (~+15–18% segment); do not over-invest ahead of "
         "demand.", "Brand Manager / Finance", "FY27 plan"),
    ])
    return d.build()


# ============================================================== REPORT 23 ====
def r23_proteinpeak_brand_plan():
    d = Doc("23-proteinpeak-fy27-brand-plan-3yr-roadmap.pdf",
            kicker="BRAND PLAN & 3-YEAR ROADMAP",
            title="ProteinPeak — FY27 Brand Plan & 3-Year Growth Roadmap",
            subtitle="Acme's growth engine in the category's fastest-growing pocket",
            owner="Sage Park, Brand Lead — ProteinPeak",
            period="FY27 plan · FY27–FY29 roadmap", short="ProteinPeak FY27+",
            doc_type="Internal brand plan (3-year)", date_str="July 2026")

    p, a, var = _brand_q2fy26("ProteinPeak")   # Apr–May post-launch
    d.cover_facts([
        ("Trajectory", "$48M FY25 → $80M FY26 plan → ~$110M FY28 / ~$140M FY29 (targets)"),
        ("Category", "Wellness Protein +18.3% ($840M); Acme share 7.6→8.4%"),
        ("Launch read (Apr 20)", "Trial 110% plan at Target vs 77% Walmart-pilot"),
        ("Source of volume", "53% new-to-brand · 32% cannibalization · 15% switch"),
        ("Q2 FY26 vs plan (post-launch)", f"{money(a)} vs {money(p)} plan · {var:+.1f}%"),
    ])

    d.exec_summary(
        "ProteinPeak is Acme's growth engine, and it is pointed at the right target. Wellness Protein is the "
        "fastest-growing pocket in RTE cereal — +18.3% in FY25 to $840M — and Acme's share is climbing "
        "(7.6% FY25 to 8.4% Q2-FY26 MTD) on the back of the April 20 Cinnamon Crunch (PP005) and Cocoa Almond "
        "(PP006) launch. The launch read is strong where it matters: trial at 110%+ of plan at Target, a "
        "healthy 53% new-to-brand source of volume, W2 repeat ~1.2x the Berry Crunch benchmark, and the "
        "best social sentiment in the portfolio (+0.44). The three-year plan builds from $80M FY26 to "
        "planning targets of ~$110M FY28 and ~$140M FY29 — a roadmap of Target-first distribution expansion, "
        "a validated Chocolate Almond gate-pass for Q3, and a form-factor pipeline (Mini Cups, Bars). The "
        "principal threat is Larksfield's Field & Honey 14g protein extension.",
        bullets=[
            "<b>Right category, gaining share.</b> Wellness Protein +18.3% to $840M; Acme share 7.6% → 8.4% "
            "(Q2-FY26 MTD). This is where the portfolio grows (seed_category_market_size).",
            "<b>Launch is working.</b> Trial 110%+ of plan at Target vs 77% Walmart-pilot; 53% of volume is "
            "new-to-brand; W2 repeat ~1.2x Berry Crunch; sentiment +0.44 on ~496 mentions.",
            "<b>Target over-indexes hard.</b> Acme Wellness Protein share is 18.4% at Target vs 5.2% at "
            "Walmart — the roadmap is Target-anchored and channels-out.",
            "<b>Pipeline is gated and real.</b> Chocolate Almond cleared the concept-test gate (64% top-2-box "
            "vs 55% standard; 8pp substitutional < 12pp SteerCo gate) for a Q3 launch; Mini Cups (2027-Q4) "
            "and Bars 12g (2028) extend form factors.",
            "<b>The threat:</b> Field &amp; Honey 14g protein (LCH00032, May 12) narrows our protein delta "
            "from 11g to 6g — we defend on sugar, cinnamon and repeat, not on grams.",
        ])

    # --- 1 · category & share
    d.h1("1 · The category — and why ProteinPeak wins by playing here")
    d.kpis([
        ("Wellness Protein $", "$840M", "FY25, +18.3%"),
        ("Acme share", "8.4%", "Q2-FY26 (was 7.6%)"),
        ("Target share", "18.4%", "vs 5.2% Walmart"),
        ("Social sentiment", "+0.44", "best in portfolio"),
    ])
    d.body(
        "Wellness Protein is the single best place to be in RTE cereal. It grew +18.3% in FY25 to $840M — "
        "an order of magnitude faster than Family Sweet (+1.4%) or the total category (+1.3%) — and the "
        "high-protein-cereal macro trend reads 0.92, the strongest signal Acme tracks. ProteinPeak is not "
        "just riding the category; it is taking share within it: Acme's Wellness Protein value share moved "
        "from 7.1% (FY24) to 7.6% (FY25) to 8.4% (Q2-FY26 MTD). The strategic implication is that a dollar "
        "of ProteinPeak investment compounds twice — category growth plus share gain — which is precisely "
        "why it earns the portfolio's discretionary innovation spend (cross-ref the LRP, Report 15, and the "
        "innovation portfolio, Report 33).")

    ch_share = chart_line("r23_wp_share.png",
                          ["FY24", "FY25", "Q1-FY26", "Q2-FY26"],
                          {"Acme Wellness Protein share": [7.1, 7.6, 7.8, 8.4]},
                          title="Acme value share of Wellness Protein (%)", pct=True, h=2.6)
    d.image(ch_share, "Share climbing through the launch. seed_category_market_size, Wellness Protein, "
                      "US National (Q2-FY26 is month-to-date).")
    d.source("seed_category_market_size (NielsenIQ Total US xAOC), Wellness Protein; "
             "seed_macro_trends MT001 (high-protein cereal 0.92).")

    # --- 2 · revenue roadmap
    d.h1("2 · The three-year revenue roadmap")
    d.body(
        "ProteinPeak more than doubled from FY24 to the FY26 plan on the strength of the launch build. FY25 "
        "closed at $48M; the FY26 plan is $80M, loaded onto PP005 + PP006 shipping from April 20. The "
        "roadmap extends to planning targets of ~$110M in FY28 and ~$140M in FY29 — <b>these FY27–FY29 "
        "figures are planning targets, not booked demand</b> — carried by distribution build-out (Target-first, "
        "then Kroger/Walmart), the Chocolate Almond Q3 addition, and a form-factor pipeline.")

    ch_road = chart_bar("r23_roadmap.png",
                        ["FY24", "FY25", "FY26 plan", "FY27 tgt", "FY28 tgt", "FY29 tgt"],
                        [39, 48, 80, 95, 110, 140],
                        title="ProteinPeak net revenue — actual & planning targets ($M)",
                        colors_list=[palette["navy"], palette["navy"], palette["teal"],
                                     palette["gold"], palette["gold"], palette["gold"]],
                        unit="", h=2.9)
    d.image(ch_road, "Navy = actual; teal = FY26 plan; gold = FY27–FY29 planning targets. FY24 $39M / FY25 "
                     "$48M are actuals (skus.csv, +24.6% YoY); FY26 $80M is plan; FY27+ are planning targets.")
    d.callout("Read the colors literally",
              "FY24–FY25 ($39M → $48M, +24.6% YoY) are measured actuals. FY26 ($80M) is the committed plan. "
              "FY27 (~$95M), FY28 (~$110M) and FY29 (~$140M) are planning targets that assume distribution "
              "build-out, Chocolate Almond, and the form-factor pipeline all land — they are a roadmap to "
              "steer against, not a forecast to bank.", "info")

    d.pagebreak()
    # --- 3 · launch read
    d.h1("3 · Launch read — strong at Target, soft at Walmart-pilot")
    d.h2("3.1 · Trial vs plan by retailer")
    d.body(
        "The April 20 launch read splits cleanly by retailer. At Target — where the endcap and Roundel media "
        "ran and where Acme over-indexes — trial hit 110–113% of plan and velocity ~17.5 units/store/week. "
        "The Walmart pilot ran soft at 77–78% of plan (~9.2 u/store/wk). This is a distribution-and-context "
        "story, not a demand story: Acme's Wellness Protein share is 18.4% at Target versus 5.2% at Walmart, "
        "so Target is both the stronger launchpad and the more representative read of true demand.")

    ch_trial = chart_bar("r23_trial.png",
                         ["Target", "Walmart-pilot"],
                         [110, 77],
                         title="Launch trial vs plan by retailer (% of plan, Week-4)", pct=True,
                         colors_list=[palette["teal"], palette["rust"]], h=2.5)
    d.image(ch_trial, "Target clears plan; the Walmart pilot runs soft. proteinpeak_q2_launch + "
                      "seed_category_market_size (Target/Walmart Wellness Protein share).")

    d.h2("3.2 · Source of volume — the launch is additive")
    d.body(
        "Of the households ProteinPeak pulled in, 53% were new-to-brand, 32% cannibalized existing ProteinPeak "
        "SKUs, and 15% switched from a competitor. A majority-new-to-brand mix is the signal a healthy launch "
        "should send: the brand is growing the franchise, not just reshuffling its own shelf. Week-2 repeat "
        "runs ~1.2x the Berry Crunch (PP003) benchmark and social sentiment is +0.44 on ~496 mentions — the "
        "strongest sentiment in the Acme portfolio.")
    ch_sov = chart_donut("r23_sov.png",
                         ["New-to-brand", "Cannibalization", "Competitor switch"],
                         [53, 32, 15],
                         title="ProteinPeak launch — source of volume (%)")
    d.image(ch_sov, "Majority new-to-brand — the launch is expanding the franchise. household_transactions "
                    "(PP005/PP006), of qualified switches.")
    d.source("proteinpeak_q2_launch, household_transactions (PP005/PP006), social_mentions (2026).")

    # --- 4 · pipeline
    d.h1("4 · Innovation pipeline — gated, sequenced, form-factor led")
    d.body(
        "The pipeline is disciplined: one validated near-term add (Chocolate Almond, Q3), then two "
        "form-factor extensions that widen the occasion base. Chocolate Almond cleared its gate — 64% "
        "top-two-box against the 55% action standard (+11pp vs the innovation benchmark), with only 8pp "
        "substitutional cannibalization against the 12pp SteerCo threshold, so it passes on both purchase "
        "intent and additivity (concept_tests). Chocolate as a breakfast flavor over-indexes +14pp among "
        "protein-curious shoppers, the exact cohort ProteinPeak is recruiting.")

    pipe = seed_csv("innovation_pipeline.csv")
    pp = pipe[pipe["brand"] == "ProteinPeak"].copy()

    def _rev(x):
        try:
            return f"${float(x):.1f}M"
        except (ValueError, TypeError):
            return "—"

    prows = [["Chocolate Almond (Q3)", "Concept-test gate passed", "2026-Q3", "—", "64% top-2-box"]]
    order = {"INV020": 0, "INV012": 1}
    pp["ord"] = pp["concept_id"].map(order).fillna(9)
    pp = pp[pp["concept_id"].isin(order.keys())].sort_values("ord")
    for r in pp.itertuples():
        prows.append([r.concept_name.replace("ProteinPeak ", ""), r.stage_gate,
                      str(r.planned_launch_date), _rev(r.projected_revenue_year1_musd),
                      f"conf {r.confidence_score_0to1:.2f}"])
    d.h2("4.1 · ProteinPeak pipeline")
    d.table(["Concept", "Stage / status", "Planned", "Yr-1 (est.)", "Read"], prows,
            widths=[0.24, 0.28, 0.13, 0.14, 0.21],
            align=["LEFT", "LEFT", "LEFT", "RIGHT", "LEFT"])
    d.source("seeds/innovation_pipeline.csv (ProteinPeak); seed_concept_test_chocolate_almond "
             "(Chocolate Almond gate). Yr-1 = planning estimate.")
    d.callout("Chocolate Almond passes the gate — advance to Q3 launch",
              "n=1,000; 64% top-two-box clears the 55% action standard (+6pp vs launch-SKU pretest, +11pp vs "
              "the 5-year innovation benchmark). Protein-curious cohort 71% top-two-box. Cannibalization vs "
              "ProteinPeak launch SKUs is 8pp substitutional — under the 12pp SteerCo gate — and only 2pp vs "
              "Crunchwell. Field of Jun 22–Jul 11. See the concept-test read, Report 33.", "win")

    d.pagebreak()
    # --- 5 · retailer & threat
    d.h1("5 · Where to win — and what to defend against")
    d.h2("5.1 · Target-first, channels-out")
    d.body(
        "Target is the anchor. Acme's Wellness Protein value share is 18.4% at Target versus 5.2% at "
        "Walmart, and the launch read confirms it converts there. The FY27 distribution plan is Target-first "
        "(protect and expand the endcap and everyday facings), then a disciplined Kroger build (Cocoa Almond "
        "new-item TPR is already live), then a re-scoped Walmart re-entry once the pilot learnings are worked "
        "in. The Target Joint Business Plan, Report 37, carries the account-level detail; this plan sets the "
        "brand priority behind it.")
    ch_ret = chart_bar("r23_retailer_share.png",
                       ["Target", "Walmart"],
                       [18.4, 5.2],
                       title="Acme Wellness Protein value share by retailer (%)", pct=True,
                       colors_list=[palette["teal"], palette["slate"], ], h=2.4)
    d.image(ch_ret, "Target over-indexes 3.5x on Wellness Protein share. seed_category_market_size, "
                    "Q2-FY26 MTD.")

    d.h2("5.2 · The competitive threat — Field & Honey 14g")
    d.callout("Field & Honey 14g protein narrows our headline claim",
              "Larksfield launched Field & Honey Protein 14g (LCH00032) on May 12, 2026, at $4.79/12oz — "
              "narrowing ProteinPeak's protein delta from 11g to 6g. A trademark on 'Field & Honey Chocolate "
              "Crunch' was filed April 22, signalling a likely Q4 chocolate entry. The defense is not a "
              "grams arms-race: ProteinPeak wins on the sugar leg (8g), real-cinnamon taste, +0.44 sentiment, "
              "and W2 repeat. Land Chocolate Almond in Q3 to occupy the chocolate-protein space before "
              "Larksfield does.", "risk")

    d.h1("6 · Risks & the FY27–FY29 ask")
    d.callout("Watch-items across the roadmap",
              "(1) Walmart-pilot execution gap must close before Walmart scale is committed. "
              "(2) Field &amp; Honey 14g (and a likely Q4 chocolate) pressures the claim and the chocolate "
              "whitespace simultaneously. (3) The FY27–FY29 targets assume the pipeline lands on cadence — "
              "slippage on Chocolate Almond or Mini Cups pulls the curve down. (4) Cannibalization discipline: "
              "hold new-SKU substitutional overlap under the 12pp SteerCo gate as the line extends.", "risk")
    d.recommendations([
        ("Advance Chocolate Almond to a Q3 FY26 launch on the passed gate; occupy chocolate-protein before "
         "Field & Honey's likely Q4 entry.", "Sage Park", "Q3 FY26"),
        ("Run the Target-first distribution plan; protect endcap + everyday facings and expand ahead of "
         "the FY27 build (see Target JBP, Report 37).", "Sage Park / NAM", "FY27 H1"),
        ("Close the Walmart-pilot execution gap before committing Walmart scale; re-scope on pilot learnings.",
         "Sage Park / Tom Reilly (NAM)", "FY27 H1"),
        ("Sequence the form-factor pipeline: Mini Cups Six-Pack (2027-Q4), Bars 12g (2028) — gate each on "
         "concept test and <12pp substitutional overlap.", "Sage Park / Lillian Park", "FY27–FY28"),
        ("Defend the claim on sugar/taste/repeat, not grams; hold the FY26 $80M and steer FY27–FY29 targets "
         "(~$95M / ~$110M / ~$140M) as the pipeline lands.", "Sage Park / Finance", "FY27 plan"),
    ])
    return d.build()


# ============================================================== REPORT 24 ====
def r24_crunchwell_turnaround():
    d = Doc("24-crunchwell-fy27-fy29-turnaround-plan.pdf",
            kicker="3-YEAR TURNAROUND PLAN · FY27–FY29",
            title="Crunchwell — FY27–FY29 Turnaround Plan",
            subtitle="Rebuilding relevance for the flagship — a three-year strategic commitment",
            owner="Cory Whitman, Brand Director; VP Marketing (sponsor)",
            period="FY27–FY29", short="Crunchwell Turnaround",
            doc_type="Strategic commitment (3-year)", date_str="July 2026")

    d.cover_facts([
        ("The problem", "Relevance, not Trust — Relevance 68.6→62.7 (−5.9pp, 6 waves)"),
        ("Trust", "Holds ~72 (72.3→72.9) — the franchise is not broken"),
        ("National share", "6.0% flat, slipping at the edges"),
        ("Louisiana battlefield", "6.4% → 3.0% (−340 bps)"),
        ("3-year commitment", "Arrest decline FY27, return to growth FY28–FY29 (targets)"),
    ])

    d.exec_summary(
        "Crunchwell is Acme's flagship and its diagnosis is precise: this is a <i>relevance</i> problem, not "
        "a trust problem. Over six quarters, brand Relevance fell 5.9 points (68.6 → 62.7) while Trust held "
        "steady at ~72 and Taste and Quality barely moved. The brand is still trusted; it is drifting out of "
        "cultural relevance. National value share is flat at 6.0% but slipping at the edges — Louisiana has "
        "collapsed −340 bps (6.4% → 3.0%), leading-indicator DMAs Birmingham and Memphis are softening, and "
        "the price gap to Field &amp; Honey has widened from 8% to 14%. This plan is a three-year commitment "
        "built on four pillars — rebuild relevance, restore an innovation cadence, close the price gap through "
        "RGM, and recover Louisiana and the leading indicators — with a phased goal: arrest the share decline "
        "in FY27, then return to growth in FY28–FY29 (planning targets).",
        bullets=[
            "<b>Relevance, not Trust.</b> Relevance 68.6 → 62.7 (&minus;5.9pp over 6 waves); Trust 72.3 → 72.9 "
            "(holds); Taste and Quality flat (brand_equity_quarterly). The equity signal is unambiguous.",
            "<b>Share is flat nationally, failing regionally.</b> National ~6.0% flat; Louisiana &minus;340 bps "
            "(6.4→3.0); Birmingham 5.7→5.4 and Memphis 5.4→5.1 softening (early LA pattern).",
            "<b>Price gap widening.</b> The gap to Field &amp; Honey has moved from ~8% to ~14% — a real RGM "
            "problem behind the relevance one.",
            "<b>Social sentiment is negative.</b> Crunchwell reads &minus;0.11 on 316 mentions in 2026 — the "
            "relevance gap made visible in culture.",
            "<b>The commitment:</b> four pillars, three years — arrest the decline in FY27, return to growth "
            "in FY28–FY29 (planning targets).",
        ])

    # --- 1 · the diagnosis
    d.h1("1 · The diagnosis — relevance, not trust")
    d.kpis([
        ("Relevance", "62.7", "−5.9pp over 6 waves"),
        ("Trust", "72.9", "holds (was 72.3)"),
        ("National share", "6.0%", "flat, edges slipping"),
        ("Social sentiment", "−0.11", "316 mentions, 2026"),
    ])
    d.body(
        "The single most important slide in this plan is the equity trend. Kantar tracks five attributes for "
        "Crunchwell; over six quarters (FY25Q1 → FY26Q2), four are essentially flat and one is falling. "
        "Relevance — Cory's lead-indicator attribute — dropped 5.9 points, from 68.6 to 62.7. Trust rose "
        "slightly (72.3 → 72.9). Taste (74.4 → 73.2) and Quality (69.3 → 70.3) held; Modernity is soft "
        "(51.0 → 48.8) and moves with Relevance. The read is decisive: consumers still trust Crunchwell and "
        "still rate its taste, but it is fading from their consideration set. You do not fix a relevance "
        "problem with a trust message — you fix it with modern positioning, cultural presence, and a reason "
        "to re-consider.")

    eq = df("""SELECT Wave, Attribute, Top_Two_Box_Pct FROM brand_equity_quarterly
               WHERE Brand='Crunchwell' AND DMA='US-NAT'""")
    waves = ["FY25Q1", "FY25Q2", "FY25Q3", "FY25Q4", "FY26Q1", "FY26Q2"]
    piv = eq.pivot(index="Wave", columns="Attribute", values="Top_Two_Box_Pct").reindex(waves)
    series = {attr: [round(float(piv.loc[w, attr]), 1) for w in waves]
              for attr in ["Trust", "Taste", "Quality", "Relevance", "Modernity"]}
    ch_eq = chart_line("r24_equity.png", waves, series,
                       title="Crunchwell brand equity — Top-2-box % by attribute (6 waves)", h=3.1)
    d.image(ch_eq, "Trust, Taste and Quality hold; Relevance falls 5.9pp and Modernity softens. "
                   "brand_equity_quarterly (Kantar Brand Equity Tracker, US-NAT).")
    d.source("brand_equity_quarterly (Kantar), Crunchwell US-NAT, FY25Q1–FY26Q2; "
             "social_mentions (2026, Crunchwell −0.11 on 316 mentions).")

    d.callout("Why this reframes the whole plan",
              "If the problem were Trust, the answer would be reassurance and heritage. Because the problem is "
              "Relevance, the answer is modern positioning, creators and social presence, and an innovation "
              "cadence that gives shoppers a reason to look again. Every pillar below flows from this one "
              "diagnosis.", "info")

    d.pagebreak()
    # --- 2 · the edges are slipping
    d.h1("2 · National flat, but the edges are slipping")
    d.body(
        "The national number reassures and misleads. Crunchwell's national value share has held at ~6.0% for "
        "six quarters (6.00 in 2025Q1, 5.97 in 2026Q2). But share is being lost at the geographic edges, and "
        "the pattern is spreading. Louisiana is the acute case — a &minus;340 bps collapse from 6.4% to 3.0% "
        "(New Orleans 5.1→3.0, Baton Rouge 5.8→4.2). More concerning strategically, the two leading-indicator "
        "DMAs Acme flagged — Birmingham (5.7→5.4) and Memphis (5.4→5.1) — are now showing the early LA "
        "pattern: Field &amp; Honey endcap presence up, Crunchwell Mega velocity softening. A flat national "
        "average is what a slow regional bleed looks like before it reaches the headline.")

    geo = seed_csv("geographies.csv")
    picks = ["LA-DMA", "NOLA", "BTR", "BIR-DMA", "MEM-DMA"]
    gsub = geo[geo["geo_id"].isin(picks)].set_index("geo_id").reindex(picks)
    grows = [[r.geo_name, f"{r.crunchwell_share_fy25_pct:.1f}%",
              f"{r.crunchwell_share_q12026_pct:.1f}%",
              f"{(r.crunchwell_share_q12026_pct - r.crunchwell_share_fy25_pct)*100:+.0f} bps",
              r.priority_tier] for r in gsub.itertuples()]
    d.h2("2.1 · Battlefields and leading indicators — Crunchwell share (FY25 → Q1 FY26)")
    d.table(["Geography", "FY25", "Q1 FY26", "Δ", "Tier"], grows,
            widths=[0.34, 0.13, 0.13, 0.15, 0.25],
            align=["LEFT", "RIGHT", "RIGHT", "RIGHT", "LEFT"])
    d.source("seeds/geographies.csv (Crunchwell share by geography). Canonical LA headline "
             "6.4%→3.0% / −340 bps (docs/louisiana-decline.md).")

    ch_share = chart_line("r24_share_traj.png",
                          ["2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2",
                           "FY27 tgt", "FY28 tgt", "FY29 tgt"],
                          {"National share": [6.00, 6.06, 6.02, 6.02, 6.01, 5.97, 6.0, 6.2, 6.4]},
                          title="Crunchwell national value share — actual & FY27–FY29 targets (%)",
                          pct=True, h=2.8)
    d.image(ch_share, "History is flat at ~6.0% (syndicated_weekly, ex-LA). The FY27–FY29 points are "
                      "planning targets: arrest in FY27, growth FY28–FY29.")

    d.h2("2.2 · The price gap is widening")
    d.body(
        "Underneath the relevance problem is a real revenue-growth-management one. The price gap between "
        "Crunchwell and Field &amp; Honey has widened from roughly 8% to 14% as Larksfield holds sharper "
        "everyday and promoted prices. A widening gap makes every relevance and innovation dollar work harder "
        "than it should; closing it is Pillar 3.")
    ch_gap = chart_bar("r24_price_gap.png",
                       ["Prior", "Current"],
                       [8, 14],
                       title="Crunchwell price gap to Field & Honey (%)", pct=True,
                       colors_list=[palette["gold"], palette["rust"]], h=2.3)
    d.image(ch_gap, "The gap has widened ~6 points. Price-gap figures per the FY27 plan grounding "
                    "(Reports 18 / 39).")

    d.pagebreak()
    # --- 3 · four-pillar plan
    d.h1("3 · The four-pillar turnaround plan")
    d.lede(
        "Four pillars, sequenced so relevance and innovation lead, RGM funds, and the regional recovery "
        "proves the model in-market. All revenue outcomes are FY27–FY29 planning targets.")

    d.h2("Pillar 1 · Rebuild relevance and brand")
    d.body(
        "The lead pillar attacks the diagnosis directly: modern positioning, a creator and social program, "
        "and a shift of message away from heritage-trust toward cultural relevance. Crunchwell's 2026 social "
        "sentiment is &minus;0.11 across 316 mentions — the relevance gap made visible. The mandate is to move "
        "that number positive and to arrest the Relevance decline, then reverse it, over the three years. "
        "This is where the plan's center of gravity sits.")

    d.h2("Pillar 2 · Restore an innovation cadence")
    inv = seed_csv("innovation_pipeline.csv")
    cw = inv[inv["brand"] == "Crunchwell"].copy()

    def _rev(x):
        try:
            return f"${float(x):.1f}M"
        except (ValueError, TypeError):
            return "Recovery"

    show = ["INV001", "INV002", "INV019", "INV022"]
    cw["ord"] = cw["concept_id"].map({c: i for i, c in enumerate(show)}).fillna(9)
    cw = cw[cw["concept_id"].isin(show)].sort_values("ord")
    irows = []
    for r in cw.itertuples():
        conf = "" if r.confidence_score_0to1 != r.confidence_score_0to1 else f"{r.confidence_score_0to1:.2f}"
        irows.append([r.concept_name.replace("Crunchwell ", ""), r.stage_gate.replace("Stage-", "S"),
                      str(r.planned_launch_date), _rev(r.projected_revenue_year1_musd),
                      conf if conf else "—"])
    d.table(["Initiative", "Stage", "Planned", "Yr-1 (est.)", "Conf."], irows,
            widths=[0.34, 0.20, 0.15, 0.16, 0.13],
            align=["LEFT", "LEFT", "LEFT", "RIGHT", "RIGHT"])
    d.source("seeds/innovation_pipeline.csv (Crunchwell). Yr-1 revenue = planning estimate.")
    d.body(
        "The cadence is anchored by the <b>Pack Refresh — Hero SKUs</b> (Stage-5 Launch Prep, $28M year-1 "
        "planning estimate, confidence 0.82, launching 2026-08-15) — the biggest near-term bet and the visible "
        "signal that Crunchwell is modernizing. Behind it: <b>Hispanic 'Maiz Crunch'</b> ($12M, Stage-2, "
        "target 2027-Q1) to recruit a growing shopper base, <b>Mega Family Pack 36oz</b> ($8.5M, Stage-3, "
        "target 2027-Q1) for value/pantry-load, and the <b>Cinnamon Twist reformulation</b> (Stage-3, 2026-Q4) "
        "to fix a known underperformer. See the innovation portfolio, Report 33.")

    d.h2("Pillar 3 · RGM — close the price gap")
    d.body(
        "Pillar 3 funds the plan and removes the RGM drag. Close the price gap to Field &amp; Honey (from ~14% "
        "back toward ~8%) through architecture and pack-price-architecture work, not blunt promotion — "
        "Crunchwell already carries a heavy ~25.6%-of-gross trade rate at low incrementality. The goal is a "
        "healthier price-pack ladder that improves realized price while narrowing the shelf gap that hands "
        "Larksfield an everyday-value story.")

    d.h2("Pillar 4 · Louisiana + leading-indicator recovery")
    d.body(
        "Pillar 4 proves the model in-market. Louisiana (&minus;340 bps) has a funded recovery plan — facing "
        "recovery, targeted trade, and a LA retail-media injection at ~2.2x portfolio ROI — and the Pack "
        "Refresh (Leg 3) is tied to it. Extend the same playbook pre-emptively to the leading-indicator DMAs "
        "Birmingham and Memphis before they follow Louisiana's path; Tasha's Q3 Walmart Connect reroute "
        "already targets these markets. See the Louisiana diagnostic, Report 17.")

    d.pagebreak()
    # --- 4 · commitment table
    d.h1("4 · The three-year commitment")
    d.body(
        "The commitment is phased and explicit. FY27 is about arresting the decline — stabilizing Relevance "
        "and national share and closing the acute Louisiana gap. FY28–FY29 return the flagship to growth. "
        "<b>All FY27–FY29 outcomes are planning targets, not forecasts.</b>")
    d.table(
        ["Horizon", "Commitment", "Lead metric", "Target (planning)"],
        [["FY27", "Arrest the decline", "Relevance / national share",
          "Relevance stops falling; share holds ~6.0%"],
         ["FY27", "Close the acute gap", "Louisiana share",
          "Recover LA off the 3.0% trough"],
         ["FY28", "Return to growth", "National share",
          "Share up to ~6.2% (target)"],
         ["FY29", "Compound the recovery", "National share / Relevance",
          "Share ~6.4%; Relevance rebuilding (target)"]],
        widths=[0.12, 0.28, 0.28, 0.32], align=["LEFT", "LEFT", "LEFT", "LEFT"])
    d.source("Planning targets set against brand_equity_quarterly and syndicated_weekly baselines. "
             "FY27–FY29 figures are commitments/targets, not measured or forecast history.")

    d.callout("Risks to the commitment",
              "(1) Relevance is a slow-moving metric — a positioning reset takes several waves to read, so "
              "FY27 progress may look like stabilization before improvement. (2) Field &amp; Honey keeps "
              "escalating (Family Sweet stealth, 14g protein, likely Q4 chocolate) on both the price and "
              "innovation fronts. (3) The Pack Refresh (2026-08-15) is the biggest single bet — execution "
              "risk on it is execution risk on the whole FY27 arrest. (4) The heavy trade rate must come down "
              "as RGM works, or Pillar 3 self-funds too slowly.", "risk")

    d.recommendations([
        ("Stand up the Pillar 1 relevance program — modern positioning + creator/social — and set a "
         "quarterly Relevance and sentiment tracker as the lead KPI.", "Cory Whitman / VP Marketing", "FY27 H1"),
        ("Land the Pack Refresh (2026-08-15) as the visible modernization signal; protect the launch.",
         "Cory Whitman / Audrey Kim", "Aug 2026"),
        ("Sequence Maiz Crunch, Mega 36oz and the Cinnamon Twist reformulation to sustain the FY27–FY28 "
         "innovation cadence.", "Lillian Park", "FY27–FY28"),
        ("Run the RGM price-pack-architecture work to close the Field & Honey gap from ~14% toward ~8% "
         "without deepening trade.", "RGM / Finance", "FY27"),
        ("Execute the Louisiana recovery and extend the playbook to Birmingham/Memphis before they follow "
         "(see Report 17).", "Marcus Boudreaux / Tasha Brooks", "FY27 H1"),
    ])
    return d.build()


if __name__ == "__main__":
    for fn in (r22_rootday_brand_review, r23_proteinpeak_brand_plan, r24_crunchwell_turnaround):
        print(fn())
