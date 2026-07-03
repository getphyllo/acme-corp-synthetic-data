"""Category / consumer-insights reports (30-34). Run: python generators/insights.py

Grounding: every headline number traces to reports/generators/FACTS.md, to
acme.duckdb, or to seeds/*.csv. Forward numbers (H2 reallocations, FY27 pipeline
revenue, launch targets) are worded as plan / target / planning estimate.
Note: seed_innovation_pipeline reads oddly from duckdb — use seed_csv().
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import (Doc, df, seed_csv, money, palette,
                 chart_line, chart_bar, chart_grouped, chart_stacked,
                 chart_waterfall, chart_donut)


# ============================================================== helpers ======
def _hex(name):
    """Resolve a palette colour name to its hex code (chart colors_list needs hex)."""
    return palette[name]


def _pos_neg(vals, pos="green", neg="rust"):
    """Hex colour per value: green if >=0 else rust."""
    return [_hex(pos) if v >= 0 else _hex(neg) for v in vals]


# ================================================ 30 · Category SOB Q2 ======
def r30_category_state_of_business():
    d = Doc("30-q2-2026-category-state-of-business.pdf",
            kicker="CATEGORY STATE-OF-THE-BUSINESS",
            title="Acme Corp — Q2 FY2026 Category State-of-the-Business",
            subtitle="RTE Cereal and adjacencies: where the category is growing and where Acme should play",
            owner="Nina Ortega, Category Insights",
            period="Q2 FY2026", short="Category SOB Q2",
            doc_type="Category insights review", date_str="July 2026")

    d.cover_facts([
        ("RTE Cereal, Total US (FY25)", "$8.35B · +1.3% YoY"),
        ("Fastest pocket", "Wellness Protein $840M · +18.3%"),
        ("Acme RTE share", "5.7% total · 8.4% Wellness Protein (Q2 MTD)"),
        ("Shrinking pocket", "Kids Sweet $1.41B · −2.8%"),
        ("Where-to-play call", "Fund the protein and single-serve pockets; defend Family Sweet"),
    ])

    d.exec_summary(
        "RTE Cereal is a low-growth category (+1.3% in dollars to $8.35B in FY25) hiding a wide "
        "spread between pockets. Wellness Protein grew +18.3% to $840M and is still accelerating "
        "(+18.6% Q2-FY26 MTD); Kids Sweet fell −2.8% and Family Sweet — Crunchwell's home — grew "
        "only +1.4%. Acme holds 5.7% of the total category but 8.4% of Wellness Protein and rising, "
        "which is where the ProteinPeak build is deliberately concentrated. The strategic read is a "
        "where-to-play question, not a demand crisis: the category is fine, the mix is what matters.",
        bullets=[
            "<b>The category:</b> $8.35B FY25, +1.3%. Growth is pocket-specific — protein and "
            "single-serve up double digits, kids and wholegrain in decline.",
            "<b>Acme's advantaged pocket:</b> Wellness Protein $840M (+18.3%), Acme share "
            "7.6% FY25 climbing to 8.4% Q2 MTD behind the ProteinPeak Cinnamon Crunch / Cocoa "
            "Almond launch. Target over-indexes at 18.4% share of the pocket.",
            "<b>Adjacencies confirm the thesis:</b> oat milk +18.8%, single-serve hot-cereal cups "
            "+9.8%, granola +3.3% — all consumer shifts toward protein, convenience and permissibility.",
            "<b>Macro backdrop:</b> high-protein demand (strength 0.92) and cinnamon (0.81) are "
            "tailwinds; GLP-1 appetite shift (0.81, down-volume) and low-sugar pressure (0.72) are "
            "the structural headwinds on legacy sweet cereal.",
        ])

    # --- 1 · Category size & growth
    d.h1("1 · The category, sized")
    d.kpis([
        ("RTE Cereal (FY25)", "$8.35B", "+1.3% YoY"),
        ("Acme share", "5.7%", "of total RTE"),
        ("Wellness Protein", "$840M", "+18.3%, fastest"),
        ("Kids Sweet", "$1.41B", "−2.8%, declining"),
    ])
    d.body(
        "RTE Cereal in the US is a $8.35B category that grew +1.3% in FY25 ($8.24B → $8.35B), a "
        "modest step up from +0.9% the prior year. The Q1-FY26 read (+1.1%) and the Q2 MTD read "
        "(+1.4%) both track in that same low-single-digit band. Acme all-brand dollar share of the "
        "total category sits at 5.7%. Nothing at the top line is broken; the story is entirely in "
        "how the category divides.")
    ctrend = chart_bar(
        "r30_category_size.png",
        ["FY24", "FY25"], [8.24, 8.35],
        title="RTE Cereal dollar size, Total US ($B, full fiscal years)",
        color="navy", unit="B", h=2.6)
    d.image(ctrend, "Full-year category size: $8.24B → $8.35B (+1.3%). FY26 quarters track the same +1.1% to +1.4% band.")

    # --- 2 · Segment growth
    d.pagebreak()
    d.h1("2 · Segment growth — the real story")
    seg = df("""SELECT subcategory, market_size_usd_mm sz, yoy_growth_pct g, acme_share_pct sh
                FROM seed_category_market_size
                WHERE category='RTE Cereal' AND period='FY2025'
                ORDER BY g DESC""")
    seg_rows = [[r.subcategory, f"${r.sz/1000:.2f}B" if r.sz >= 1000 else f"${r.sz:.0f}M",
                 f"{r.g:+.1f}%", f"{r.sh:.1f}%"] for r in seg.itertuples()]
    d.h2("2.1 · RTE Cereal segment scorecard — FY2025")
    d.table(["Segment", "Size", "$ Growth YoY", "Acme share"], seg_rows,
            widths=[0.36, 0.20, 0.22, 0.22])
    d.source("seed_category_market_size (NielsenIQ Total US xAOC), FY2025.")
    segbar = chart_bar(
        "r30_segment_growth.png",
        list(seg.subcategory), [round(float(g), 1) for g in seg.g],
        title="RTE Cereal segment dollar growth, FY2025 (%)", pct=True,
        colors_list=_pos_neg(list(seg.g)), horizontal=True, h=2.9)
    d.image(segbar, "Wellness Protein (+18.3%) is the outlier; Kids Sweet is the only shrinking pocket.")
    d.body(
        "Wellness Protein grew +18.3% to $840M — five times the growth rate of Family Sweet (+1.4%, "
        "$2.86B, Crunchwell's home) and in stark contrast to Kids Sweet (−2.8%, $1.41B, HoneyNest's "
        "home). Family Oat grew +2.4% on the back of the Cheerios Oat Crunch launch. The pattern is "
        "unambiguous: dollars are migrating toward protein and permissibility and away from "
        "traditional kid-sweet cereal.")

    # --- 3 · Acme share by segment
    d.h1("3 · Where Acme wins by segment")
    d.body(
        "Acme's 5.7% total-category share masks a strong position in the pocket that matters most. "
        "In Wellness Protein, Acme share climbed from 7.1% (FY24) to 7.6% (FY25) and to 8.4% in the "
        "Q2-FY26 month-to-date read as ProteinPeak's two new hero SKUs shipped. At Target specifically "
        "— the launch's lead account — Acme holds 18.4% of the Wellness Protein pocket versus 5.2% at "
        "Walmart, an index that reflects both the Roundel endcap support and a Target shopper who "
        "over-indexes for premium protein.")
    sh_seg = df("""SELECT subcategory, acme_share_pct sh
                   FROM seed_category_market_size
                   WHERE category='RTE Cereal' AND period='FY2025'
                     AND subcategory IN ('Family Sweet','Family Oat','Kids Sweet','Wellness Protein')
                   ORDER BY sh DESC""")
    shbar = chart_bar(
        "r30_acme_share.png",
        list(sh_seg.subcategory) + ["Wellness Protein (Q2 MTD)"],
        [round(float(s), 1) for s in sh_seg.sh] + [8.4],
        title="Acme share by RTE Cereal segment (%)", pct=True,
        colors_list=[_hex("slate")] * len(sh_seg) + [_hex("teal")], h=2.7)
    d.image(shbar, "Acme over-indexes in the pockets it has funded (Family Oat, Wellness Protein).")
    d.callout("Where-to-play read",
              "Acme's advantaged position is Wellness Protein, where it holds ~8% share of an +18% "
              "pocket and is still gaining. Family Sweet is a defend-and-hold job (slow-growth, high "
              "Acme dependence via Crunchwell). Kids Sweet is a managed decline. The portfolio bet — "
              "concentrate innovation dollars in protein and single-serve, defend the Crunchwell base "
              "— is directionally correct; see the LRP (Report 15) and the ProteinPeak read (Report 23).",
              "info")

    # --- 4 · Adjacencies
    d.h1("4 · Adjacencies — the same shifts, one aisle over")
    adj = df("""SELECT category, subcategory, market_size_usd_mm sz, yoy_growth_pct g
                FROM seed_category_market_size
                WHERE period='FY2025' AND category<>'RTE Cereal'
                ORDER BY g DESC""")
    adj_rows = [[f"{r.category} — {r.subcategory}",
                 f"${r.sz/1000:.2f}B" if r.sz >= 1000 else f"${r.sz:.0f}M",
                 f"{r.g:+.1f}%"] for r in adj.itertuples()]
    d.h2("4.1 · Adjacent-category growth — FY2025")
    d.table(["Adjacency", "Size", "$ Growth YoY"], adj_rows,
            widths=[0.50, 0.24, 0.26])
    d.source("seed_category_market_size, FY2025 (Plant-Based Milk, Granola, Hot Cereal).")
    d.body(
        "The adjacencies rhyme with the RTE read. Oat milk grew +18.8% ($1.64B) — the same "
        "plant-forward, functional shopper that drives Wellness Protein — and is where RootDay plays. "
        "Single-serve hot-cereal cups grew +9.8%, confirming the convenience shift that MorningOats "
        "Cup rides. Granola grew +3.3% ($1.88B), TrailGrove's pocket. Wherever the shopper is trading "
        "toward protein, oats, and single-serve convenience, the category is growing; wherever the "
        "proposition is legacy sweet, it is flat to down.")

    # --- 5 · Macro & reconciliation
    d.h1("5 · Macro forces & source reconciliation")
    d.h2("5.1 · Tailwinds and headwinds")
    d.body(
        "The demand-side forces sort cleanly. Tailwinds: high-protein cereal demand (strength 0.92, "
        "growth) and the cinnamon flavour renaissance (0.81) — both squarely under ProteinPeak and "
        "the Crunchwell Cinnamon Twist range. Headwinds: the GLP-1 / Ozempic appetite shift (0.81, "
        "flagged down-volume) is a structural drag on breakfast portion size, and low-sugar "
        "reformulation pressure (0.72) weighs on legacy sweet cereal. The net effect concentrates "
        "growth in exactly the pockets Acme has been funding.")
    macro = df("""SELECT trend_topic t, strength_0to1 s, direction dir
                  FROM seed_macro_trends
                  WHERE trend_topic IN ('High-protein cereal','Cinnamon flavor renaissance',
                    'On-the-go single-serve breakfast','GLP-1 / Ozempic appetite shift',
                    'Low-sugar reformulation pressure','Kid-cereal mom guilt')
                  ORDER BY s DESC""")
    macro_rows = [[r.t, f"{r.s:.2f}", r.dir] for r in macro.itertuples()]
    d.table(["Macro force", "Strength", "Direction"], macro_rows,
            widths=[0.52, 0.18, 0.30])
    d.source("seed_macro_trends (strength 0–1). Positive-direction forces favour protein/single-serve; down-forces drag legacy sweet.")
    d.h2("5.2 · NielsenIQ ↔ Kantar reconciliation")
    d.callout("Read the two panels together, not against each other",
              "This report is built on NielsenIQ Total US xAOC (retail dollar movement — what sold "
              "through the register). The shopper-panel view (Kantar Worldpanel, Report 31) measures "
              "who bought and how often. They will not tie out to the decimal: NielsenIQ captures "
              "dollars including price and promo, Kantar captures household penetration and frequency. "
              "The directional agreement is what matters — both show Wellness Protein gaining buyers "
              "and dollars, both show legacy sweet cereal losing occasions. Where a specific number is "
              "quoted, its source is named.", "info")

    d.callout("Category risks into H2",
              "(1) GLP-1 down-volume compounds on the largest, sweetest, most mature SKUs — the "
              "Crunchwell base. (2) Larksfield's Field & Honey has escalated into the protein pocket "
              "(14g line extension, Report 32), directly contesting Acme's one advantaged position. "
              "(3) Kids Sweet decline (−2.8%) is structural, not cyclical — HoneyNest needs a "
              "portfolio answer, not more promotion.", "risk")
    d.recommendations([
        ("Concentrate FY27 innovation and A&P behind Wellness Protein and single-serve — the only "
         "double-digit pockets Acme can win.", "Nina Ortega / VP Innovation", "FY27 planning"),
        ("Defend Family Sweet share with the Crunchwell Pack Refresh; treat it as hold, not grow.",
         "Cory Whitman", "Q3 launch"),
        ("Build a HoneyNest portfolio answer to structural Kids-Sweet decline rather than defending "
         "with trade depth.", "Category Insights", "FY27 planning"),
        ("Track the protein pocket weekly now that Larksfield has entered it (Report 32).",
         "Nina Ortega", "Ongoing"),
    ])
    return d.build()


# =============================================== 31 · Shopper Panel H1 ======
def r31_shopper_household_panel():
    d = Doc("31-h1-2026-shopper-household-panel-insights.pdf",
            kicker="SHOPPER & PANEL INSIGHTS",
            title="Acme Corp — H1 FY2026 Shopper & Household Panel Insights Review",
            subtitle="Kantar cohort penetration, source of volume, and the demographics behind the ProteinPeak launch",
            owner="Consumer Insights; Panel Analytics",
            period="H1 FY2026", short="Shopper Panel H1",
            doc_type="Shopper & panel insights review", date_str="July 2026")

    d.cover_facts([
        ("Panel frame", "Kantar Worldpanel, FY25Q1 → FY26Q2 (US-NAT)"),
        ("Eroding cohort", "loyal-family 47.9% → 46.6% penetration"),
        ("Growing (good)", "protein-returner 11.5% → 13.1%"),
        ("Growing (risk)", "cereal-skipper 18.3% → 20.8%"),
        ("Launch source of volume", "53% new-to-brand · 32% cannibalization · 15% competitor"),
    ])

    d.exec_summary(
        "The household panel tells a two-speed story. The buyer base for legacy family cereal is "
        "slowly eroding — the loyal-family cohort's penetration slipped from 47.9% to 46.6% over six "
        "quarters, and the cereal-skipper cohort grew from 18.3% to 20.8%, the single most important "
        "risk signal in the frame. Against that, the protein-returner cohort grew from 11.5% to 13.1% "
        "and buys ~4.6 times a quarter, and the ProteinPeak launch drew 53% of its real volume from "
        "genuinely new-to-brand households. The franchise is not collapsing; it is being slowly "
        "re-based toward protein and convenience while the sweet-cereal occasion thins out.",
        bullets=[
            "<b>Cohorts (US-NAT, FY25Q1 → FY26Q2):</b> loyal-family 47.9 → 46.6 (eroding); "
            "protein-returner 11.5 → 13.1 (growing, valuable); cereal-skipper 18.3 → 20.8 "
            "(growing — the risk); price-shopper 22.2 → 22.8 (stable).",
            "<b>Source of volume:</b> of ProteinPeak's real switching households, 53% were "
            "new-to-brand (431), 32% cannibalization from other Acme (260), 15% competitor "
            "switch (125) — a healthy, franchise-accretive split.",
            "<b>The occasion risk:</b> the cereal-skipper cohort growing to one in five households, "
            "amplified by the GLP-1 appetite shift, is a slow structural drain on the breakfast "
            "occasion that no single launch reverses.",
            "<b>Who bought the launch:</b> ProteinPeak buyers skew high-income (150K+ the largest "
            "bracket) but with a broad income spread, and over-index on multi-brand switchers — the "
            "profile you want for a franchise-building launch.",
        ])

    # --- 1 · Cohort penetration
    d.h1("1 · Cohort penetration — who is in the category")
    coh = df("""SELECT Cohort, Quarter, HH_Penetration_Pct p
                FROM kantar_worldpanel_cohort WHERE DMA='US-NAT'
                ORDER BY Cohort, Quarter""")
    quarters = ["FY25Q1", "FY25Q2", "FY25Q3", "FY25Q4", "FY26Q1", "FY26Q2"]
    series = {}
    for c in ["loyal-family", "protein-returner", "cereal-skipper", "price-shopper"]:
        sub = coh[coh.Cohort == c].set_index("Quarter")["p"]
        series[c] = [round(float(sub[q]), 1) for q in quarters]
    d.kpis([
        ("loyal-family", "46.6%", "↓ from 47.9%"),
        ("protein-returner", "13.1%", "↑ from 11.5%"),
        ("cereal-skipper", "20.8%", "↑ from 18.3% (risk)"),
        ("price-shopper", "22.8%", "≈ flat"),
    ])
    cline = chart_line(
        "r31_cohort_penetration.png", quarters, series,
        title="Kantar cohort household penetration, US-NAT (%)", pct=True, h=3.0)
    d.image(cline, "Four cohorts, six quarters. Loyal-family drifts down; protein-returner and cereal-skipper both climb.")
    d.body(
        "Read the lines as competing pulls on the same households. The loyal-family cohort — the "
        "spine of Crunchwell and HoneyNest volume — has lost ~1.3 points of penetration in six "
        "quarters. That volume is not vanishing so much as splitting two ways: some of it into the "
        "protein-returner cohort (up +1.6 points, and a heavy buyer at 4.6 trips/quarter), which "
        "ProteinPeak is built to capture, and some of it out of the category entirely into the "
        "cereal-skipper cohort (up +2.5 points). The cereal-skipper line is the one to watch — it is "
        "the panel signature of the GLP-1 appetite shift and the broader breakfast-occasion decline.")
    d.callout("The cereal-skipper cohort is the structural risk",
              "One in five US households is now a cereal-skipper (20.8%, up from 18.3%). These are "
              "lapsing occasions, not lapsing brands — no promotion or pack refresh wins them back "
              "because they are leaving the breakfast-cereal aisle, not switching within it. The "
              "portfolio answer is convenience and protein formats that fit a smaller-portion, "
              "on-the-go occasion, not deeper trade on legacy sweet cereal.", "risk")

    # --- 2 · Source of volume
    d.pagebreak()
    d.h1("2 · Source of volume — where ProteinPeak's launch volume came from")
    sov = df("""SELECT Switching_Flag f, COUNT(*) n
                FROM household_transactions
                WHERE Product_SKU IN ('PP005','PP006')
                  AND Switching_Flag IN ('New_To_Brand','Cannibalization','Competitor_Switch')
                GROUP BY 1""")
    sov_map = {r.f: int(r.n) for r in sov.itertuples()}
    ntb, cann, comp = sov_map["New_To_Brand"], sov_map["Cannibalization"], sov_map["Competitor_Switch"]
    tot = ntb + cann + comp
    d.body(
        f"The household-transaction panel resolves the launch into three kinds of switch. Of the "
        f"{tot} households whose ProteinPeak purchase was a genuine switch, {ntb} ({ntb/tot*100:.0f}%) "
        f"were new-to-brand, {cann} ({cann/tot*100:.0f}%) came from another Acme brand "
        f"(cannibalization), and {comp} ({comp/tot*100:.0f}%) switched in from a competitor. A launch "
        f"that is majority new-to-brand with only ~a third cannibalization is franchise-accretive — "
        f"it is growing the Acme buyer base, not just reshuffling it (see the Week-4 read, Report 23).")
    donut = chart_donut(
        "r31_source_of_volume.png",
        ["New-to-brand", "Cannibalization", "Competitor switch"],
        [ntb, cann, comp],
        title="ProteinPeak source of volume (real switches, PP005+PP006)")
    d.image(donut, "53% new-to-brand is the headline: this launch expands the franchise more than it shifts it.")

    # --- switching by loyalty segment
    d.h2("2.1 · Switching by brand-loyalty segment")
    seg = df("""SELECT Brand_Loyalty_Segment s,
                  SUM(CASE WHEN Switching_Flag='New_To_Brand' THEN 1 ELSE 0 END) ntb,
                  SUM(CASE WHEN Switching_Flag='Cannibalization' THEN 1 ELSE 0 END) can,
                  SUM(CASE WHEN Switching_Flag='Competitor_Switch' THEN 1 ELSE 0 END) comp
                FROM household_transactions
                WHERE Product_SKU IN ('PP005','PP006')
                  AND Switching_Flag IN ('New_To_Brand','Cannibalization','Competitor_Switch')
                GROUP BY 1 ORDER BY ntb DESC""")
    seg_rows = [[r.s, str(int(r.ntb)), str(int(r.can)), str(int(r.comp))] for r in seg.itertuples()]
    d.table(["Loyalty segment", "New-to-brand", "Cannibalization", "Competitor switch"], seg_rows,
            widths=[0.34, 0.22, 0.24, 0.20])
    d.source("household_transactions, Switching_Flag, PP005 + PP006 (ProteinPeak launch SKUs).")
    d.body(
        "Multi-brand switchers supplied the largest block of new-to-brand households, which is exactly "
        "the profile a protein launch should attract — mobile shoppers with no fixed cereal loyalty. "
        "Encouragingly, a meaningful share of new-to-brand volume also came from competitor-loyal and "
        "light-buyer households, evidence the launch is pulling genuinely incremental buyers rather "
        "than only churning within the Acme base.")

    # --- 3 · Demographics
    d.h1("3 · Who the launch buyer is")
    inc = df("""SELECT Income_Bracket b, COUNT(DISTINCT Household_ID) n
                FROM household_transactions WHERE Product_SKU IN ('PP005','PP006')
                GROUP BY 1""")
    eth = df("""SELECT Ethnicity e, COUNT(DISTINCT Household_ID) n
                FROM household_transactions WHERE Product_SKU IN ('PP005','PP006')
                GROUP BY 1 ORDER BY n DESC""")
    inc_order = ["<30K", "30-50K", "50-75K", "75-100K", "100-150K", "150K+"]
    inc_map = {r.b: int(r.n) for r in inc.itertuples()}
    incbar = chart_bar(
        "r31_income.png", inc_order, [inc_map.get(b, 0) for b in inc_order],
        title="ProteinPeak buyer households by income bracket (count)", color="teal", h=2.6)
    d.image(incbar, "Buyer income skews to the 150K+ bracket but spreads broadly — a premium proposition with mass reach.")
    d.body(
        "ProteinPeak's launch buyers skew premium — the 150K+ bracket is the single largest — but the "
        "distribution is broad rather than concentrated, so the proposition is not confined to a "
        "high-income niche. By ethnicity, the buyer base broadly mirrors the household panel, with a "
        "meaningful Hispanic sub-base that connects to the Hispanic-format innovation thesis "
        "(Crunchwell Maiz Crunch, Report 33). The households table also confirms a category-wide skew "
        "toward multi-brand switchers over single-brand loyalists — a category where habit is loosening "
        "and a well-positioned launch can take share.")
    eth_rows = [[r.e, str(int(r.n))] for r in eth.itertuples()]
    d.h2("3.1 · Launch-buyer ethnicity mix")
    d.table(["Ethnicity", "Buyer households"], eth_rows, widths=[0.6, 0.4])
    d.source("household_transactions + households (Kantar-shape panel), PP005 + PP006 buyers.")

    # --- 4 · Occasion / GLP-1
    d.h1("4 · The breakfast occasion under GLP-1")
    d.body(
        "The single biggest medium-term threat in the panel is not a competitor — it is the shrinking "
        "breakfast-cereal occasion. The GLP-1 / Ozempic appetite shift (macro strength 0.81, flagged "
        "as a down-volume force) reduces portion size and eating frequency, and it lands hardest on "
        "the largest, sweetest bowls. The panel signature is the cereal-skipper cohort's climb to "
        "20.8% penetration. This is why the portfolio's forward bet is weighted toward protein "
        "(satiety, permissibility) and single-serve (portion-controlled, on-the-go) rather than "
        "toward defending legacy family-sweet volume.")
    d.callout("Panel-to-shelf reconciliation",
              "These are Kantar-shape household-panel measures (who bought, how often). They will not "
              "tie to the NielsenIQ retail-dollar view in the category report (Report 30) to the "
              "decimal — different instruments, same direction. Both show protein gaining and legacy "
              "sweet losing. Cohort penetration here is the US-NAT panel cut; regional cuts (LA-DMA, "
              "Southeast) move faster and are tracked separately.", "info")
    d.recommendations([
        ("Weight portfolio and media behind protein and single-serve to meet the GLP-1 / cereal-skipper "
         "occasion shift, not deeper trade on legacy sweet.", "Consumer Insights", "FY27 planning"),
        ("Protect the ProteinPeak launch's new-to-brand momentum with sustained repeat-driving media, "
         "not just trial support.", "Sage Park", "H2 FY26"),
        ("Size the Hispanic sub-base opportunity to inform the Crunchwell Maiz Crunch concept "
         "(Report 33).", "Panel Analytics", "FY27 planning"),
        ("Instrument a quarterly cereal-skipper win-back test focused on convenience formats.",
         "Consumer Insights", "H2 FY26"),
    ])
    return d.build()


# ==================================== 32 · Competitive Intelligence Q2 ======
def r32_competitive_intelligence():
    d = Doc("32-q2-2026-competitive-intelligence-innovation-watch.pdf",
            kicker="COMPETITIVE INTELLIGENCE",
            title="Acme Corp — Q2 FY2026 Competitive Intelligence & Innovation Watch",
            subtitle="Field & Honey escalates on two fronts; the protein challengers and private label",
            owner="Competitive Intelligence; Category Insights",
            period="Q2 FY2026", short="Comp Intel Q2",
            doc_type="Competitive intelligence review", date_str="July 2026")

    d.cover_facts([
        ("Primary aggressor", "Field & Honey (Larksfield) — ~14% national share"),
        ("The escalation", "14g-protein line ext LCH00032, launched 2026-05-12"),
        ("Second front", "Field & Honey Almond (2025-09-08), Louisiana stealth"),
        ("Private-label pressure", "Great Value Honey Almond/Nut — 84–86% ACV at launch"),
        ("Threat call", "Larksfield now contests protein AND Louisiana simultaneously"),
    ])

    d.exec_summary(
        "The competitive picture in Q2 has a clear protagonist: Larksfield's Field & Honey brand. "
        "Already the national share leader among branded competitors (~14%) and the aggressor behind "
        "Crunchwell's Louisiana decline via its September 2025 Almond stealth launch, Field & Honey "
        "escalated on 2026-05-12 with a 14g-protein line extension (LCH00032) — a direct strike on "
        "ProteinPeak's one advantaged pocket. The move narrows ProteinPeak's protein delta from 11g "
        "to 6g while opening a second front in the Southeast. Behind Larksfield sit the usual "
        "protein/keto challengers (Magic Spoon, RXBAR, Catalina Crunch) driving high launch buzz but "
        "low velocity, General Mills extending Cheerios, and a high-ACV private-label wall.",
        bullets=[
            "<b>Field & Honey is the aggressor:</b> Almond launch 2025-09-08 (LA-priority, took "
            "Crunchwell facings) and the 14g-protein line extension LCH00032 on 2026-05-12 "
            "(Southeast-priority) — two fronts, one competitor.",
            "<b>The protein escalation matters most:</b> LCH00032 pitches 14g protein against "
            "ProteinPeak's 12g, narrowing the delta to 6g. A trademark for a Field & Honey chocolate "
            "variant was filed 2026-04-22, signalling a likely Q4 chocolate launch.",
            "<b>Buzz vs velocity:</b> launch buzz is highest for the niche protein/keto DTC brands "
            "(Magic Spoon 0.92) but their in-market velocity is low; the real shelf threats are the "
            "high-ACV mass launches (Great Value 0.16–0.18 buzz but 84–86% ACV).",
            "<b>Cheerios stays busy:</b> Choco Crunch (2026-01-15) and Peanut Butter (2026-04-06) "
            "extend into Crunchwell's Family Sweet adjacency with national TV support.",
        ])

    # --- 1 · Larksfield / Field & Honey
    d.h1("1 · Field & Honey — the two-front aggressor")
    fh = df("""SELECT sku_new, product_description, launch_date, launch_dmas, launch_price_usd,
                 claim_headline, buzz_index_day30, acv_at_launch_pct, status
               FROM seed_competitor_launches
               WHERE brand='Field & Honey' ORDER BY launch_date""")
    fh_rows = [[str(r.launch_date), r.product_description.replace("Field & Honey ", ""),
                f"${r.launch_price_usd:.2f}", str(r.buzz_index_day30),
                str(r.acv_at_launch_pct), r.status] for r in fh.itertuples()]
    d.table(["Launch date", "Product", "Price", "Buzz d30", "ACV %", "Status"], fh_rows,
            widths=[0.16, 0.34, 0.12, 0.13, 0.12, 0.13])
    d.source("seed_competitor_launches, brand = Field & Honey (Larksfield). ACV 'N/A' where pre-launch.")
    d.body(
        "Field & Honey opened its Louisiana campaign quietly. The Almond Crunch launch on 2025-09-08 "
        "carried an explicit LA-DMA priority and 4-week endcap plus feature support; it is one of the "
        "five attributed causes of Crunchwell's Louisiana share decline (see Report 24). Then on "
        "2026-05-12 Larksfield escalated with the Field & Honey Protein 14g line extension "
        "(LCH00032), flagged Southeast-priority and backed by a Walmart paid-sampling and influencer "
        "push. This is the strategically important move: it takes the fight into Wellness Protein, the "
        "one pocket where Acme has a defensible share position, while keeping pressure on Louisiana.")
    d.callout("The protein delta just narrowed from 11g to 6g",
              "ProteinPeak's competitive story leaned on a protein advantage. Field & Honey's 14g "
              "line extension narrows that delta to 6g versus ProteinPeak's 12g — the sugar leg still "
              "favours ProteinPeak (8g, low), but the headline protein claim is now contested. A "
              "trademark filing for 'Field & Honey Chocolate Crunch' on 2026-04-22 points to a Q4 "
              "chocolate launch that would directly counter ProteinPeak Cocoa Almond and the "
              "Chocolate Almond concept in test (Report 33).", "risk")

    # --- 2 · Share trend
    d.pagebreak()
    d.h1("2 · National share — Larksfield leads, Crunchwell holds")
    sh = df("""SELECT SUBSTR(Week,1,4)||'-Q'||CAST(CEIL(CAST(SUBSTR(Week,7,2) AS INT)/13.0) AS INT) q,
                 ROUND(AVG(Larksfield_Value_Share)*100,2) lf,
                 ROUND(AVG(Crunchwell_Value_Share)*100,2) cw,
                 ROUND(AVG(Acme_Value_Share)*100,2) acme
               FROM syndicated_weekly
               WHERE Category='RTE Cereal' AND DMA<>'LA-DMA' AND Week>='2025-W01'
               GROUP BY 1 ORDER BY 1""")
    shline = chart_line(
        "r32_share_trend.png", list(sh.q),
        {"Field & Honey (Larksfield)": [float(x) for x in sh.lf],
         "Crunchwell": [float(x) for x in sh.cw],
         "Acme (all brands)": [float(x) for x in sh.acme]},
        title="National RTE-cereal value share (%, ex-LA)", pct=True, h=2.9)
    d.image(shline, "Larksfield holds a ~14% national lead over Crunchwell's ~6%; both are broadly stable nationally.")
    d.body(
        "Nationally, Field & Honey (Larksfield) holds ~14.1% value share against Crunchwell's ~6.0% "
        "and Acme all-brand ~7.9–8.1%. The national picture is stable — this is not a broad-based "
        "share war. The danger is regional and segment-specific: Larksfield is willing to spend "
        "aggressively in targeted DMAs (Louisiana) and is now extending into the protein pocket, so "
        "the national-share calm understates the pressure in the two places that matter to Acme's "
        "growth algorithm.")

    # --- 3 · Buzz index at launch
    d.h1("3 · Launch buzz vs shelf reality")
    buzz = df("""SELECT brand, sku_new, product_description, subcategory,
                   TRY_CAST(buzz_index_day30 AS DOUBLE) b
                 FROM seed_competitor_launches
                 WHERE TRY_CAST(buzz_index_day30 AS DOUBLE) IS NOT NULL
                   AND launch_date >= '2025-05-01' AND manufacturer <> 'Acme Corp'
                 ORDER BY b DESC LIMIT 12""")
    blabels = [r.product_description[:26] for r in buzz.itertuples()]
    bvals = [round(float(r.b), 2) for r in buzz.itertuples()]
    buzzbar = chart_bar(
        "r32_buzz.png", blabels, bvals,
        title="Day-30 launch buzz index, competitor launches (0–1)",
        color="gold", horizontal=True, h=3.4)
    d.image(buzzbar, "Buzz peaks for niche protein/keto DTC launches; it does not equal shelf velocity or ACV.")
    d.body(
        "Day-30 buzz is highest for the small protein/keto brands — Magic Spoon Peanut Butter (0.92), "
        "Off Limits (0.62), Three Wishes (0.66) — but their in-market velocity is a fraction of the "
        "mass launches, because buzz concentrates in narrow, highly-online audiences. The launches "
        "that actually move shelf are the high-ACV mass entries: Great Value Honey Almond / Nut carry "
        "almost no buzz (0.16–0.18) but launched at 84–86% ACV and are among the highest-velocity new "
        "items, having absorbed Crunchwell's lost Walmart facings in the September 2025 reset. Read "
        "buzz and distribution together: buzz tells you where the cultural energy is, ACV tells you "
        "what is actually taking the shelf.")

    # --- 4 · The rest of the field
    d.h1("4 · The rest of the competitive field")
    d.h2("4.1 · General Mills — Cheerios extensions")
    d.body(
        "General Mills continues to extend Cheerios into Acme adjacencies with heavy national support. "
        "Choco Crunch (2026-01-15) and Peanut Butter (2026-04-06) both push into the Family Sweet / "
        "Family Oat space adjacent to Crunchwell, each backed by national TV plus endcap. Cheerios Oat "
        "Crunch (2026-01-15, buzz 0.86, 69% ACV by day 90) is a direct shelf-adjacency threat to "
        "Crunchwell Original Family.")
    d.h2("4.2 · Protein / keto challengers")
    d.body(
        "Magic Spoon, RXBAR, Catalina Crunch, Three Wishes and Off Limits crowd the Wellness Protein "
        "pocket from the premium DTC end (price points $6.99–$9.99). Individually they are low-ACV, "
        "low-velocity and creator-dependent, but collectively they establish the protein-cereal "
        "occasion that both ProteinPeak and now Field & Honey are scaling into mass distribution. "
        "They are the leading indicator, not the direct threat.")
    d.h2("4.3 · Private label")
    d.body(
        "Great Value (Walmart PL) Honey Almond and Honey Nut Toasted Oats launched August 2025 at "
        "$2.79 and reached 84–86% ACV almost immediately inside Walmart's modular. They are a "
        "structural price-floor pressure and a documented contributor to Crunchwell's Louisiana "
        "facing loss. Whole Foods' 365 PL move (2025-09-22) was an explicit response to Field & "
        "Honey Almond — private label reacts to branded aggression fast.")

    d.callout("Threat assessment & Acme response",
              "Priority 1: Field & Honey's protein escalation (LCH00032) contests Acme's one growth "
              "engine — respond by holding the ProteinPeak sugar/taste story, defending the 12g claim, "
              "and pre-empting the likely Q4 chocolate launch with the Chocolate Almond concept "
              "(Report 33). Priority 2: continue the Louisiana recovery against Field & Honey Almond "
              "and Great Value (Report 24). Priority 3: monitor — the DTC protein challengers and "
              "Cheerios extensions are watch-items, not fire-drills.", "action")
    d.recommendations([
        ("Defend the ProteinPeak protein/sugar/taste claim against Field & Honey 14g; brief sales on "
         "the 6g-delta narrowing.", "Sage Park / Competitive Intel", "Q3 FY26"),
        ("Accelerate the Chocolate Almond concept decision (Report 33) to pre-empt Larksfield's "
         "trademarked Q4 chocolate launch.", "VP Innovation", "Now"),
        ("Sustain the Louisiana recovery vs Field & Honey Almond + Great Value (Report 24).",
         "Marcus Boudreaux", "Ongoing"),
        ("Stand up a monthly protein-pocket competitive tracker now that mass players have entered "
         "(cross-ref Report 39).", "Competitive Intelligence", "Monthly"),
    ])
    return d.build()


# ================================ 33 · Innovation Portfolio Stage-Gate ======
def r33_innovation_stage_gate():
    d = Doc("33-fy27-innovation-portfolio-stage-gate-review.pdf",
            kicker="INNOVATION PORTFOLIO · STAGE-GATE",
            title="Acme Corp — FY27 Innovation Portfolio & Stage-Gate Review",
            subtitle="The full pipeline from idea to in-market, with gate decisions and the discontinue slate",
            owner="VP Innovation; R&D; Insights",
            period="FY27 planning", short="Innovation Stage-Gate",
            doc_type="Innovation portfolio & stage-gate review", date_str="July 2026")

    ip = seed_csv("innovation_pipeline.csv")
    # numeric coercion (revenue col contains 'Recovery' and blanks)
    import pandas as pd
    ip["rev"] = pd.to_numeric(ip["projected_revenue_year1_musd"], errors="coerce")
    ip["conf"] = pd.to_numeric(ip["confidence_score_0to1"], errors="coerce")

    d.cover_facts([
        ("Pipeline size", "25 concepts across 6 stage-gates"),
        ("Live now (Q2 FY26)", "ProteinPeak Cinnamon Crunch + Cocoa Almond"),
        ("Biggest near-term bet", "Crunchwell Pack Refresh — $28M yr1, launch 2026-08-15"),
        ("Gate passed", "ProteinPeak Chocolate Almond — 64% top-2-box, cannibalization clears"),
        ("Discontinue slate (Q3)", "RootDay Coconut, HoneyNest Granola Crunch + Cookie Dough"),
    ])

    total_rev = ip["rev"].sum()
    d.exec_summary(
        f"The innovation pipeline holds 25 concepts spanning six stage-gates, with a combined "
        f"projected year-1 revenue of ${total_rev:,.0f}M across the fundable concepts. Two "
        f"ProteinPeak SKUs are live (Cinnamon Crunch, Cocoa Almond, launched 2026-04-20); the "
        f"Crunchwell Pack Refresh is the single biggest near-term bet at $28M year-1 revenue and a "
        f"2026-08-15 launch; and the ProteinPeak Chocolate Almond concept has cleared its stage-gate "
        f"on a 64% top-two-box score with cannibalization inside the SteerCo threshold. Against those "
        f"advances, the portfolio is also pruning: three low-return SKUs are confirmed for "
        f"discontinuation in Q3. The governance question for FY27 is whether the funnel is "
        f"appropriately weighted toward the two pockets that are actually growing — protein and "
        f"single-serve — versus legacy line extensions.",
        bullets=[
            "<b>Live (Stage-6):</b> ProteinPeak Cinnamon Crunch ($14M yr1, conf 0.74) and Cocoa "
            "Almond ($10M, 0.68) — the Q2 growth engine, launched 2026-04-20.",
            "<b>Biggest bet (Stage-5):</b> Crunchwell Pack Refresh, Hero SKUs — $28M yr1, conf 0.82, "
            "launch 2026-08-15, tied to the Louisiana recovery (Leg 3).",
            "<b>Gate passed:</b> ProteinPeak Chocolate Almond cleared its action standard — 64% "
            "top-two-box (>55% gate) and 8pp substitutional cannibalization (<12pp SteerCo gate).",
            "<b>Pre-launch LTOs:</b> HoneyNest Birthday Cake ($2.4M, Q4) and MorningOats Cup Pumpkin "
            "Spice ($1.8M, Q3). <b>Discontinue Q3:</b> RootDay Coconut Blend, HoneyNest Granola "
            "Crunch, HoneyNest Cookie Dough.",
        ])

    # --- 1 · Funnel
    d.h1("1 · The pipeline funnel")
    stage_order = ["Stage-1 Idea", "Stage-2 Concept", "Stage-3 Prototype",
                   "Stage-4 Pre-Launch", "Stage-5 Launch Prep", "Stage-6 In-Market",
                   "Stage-Final Discontinue"]
    counts = ip.groupby("stage_gate").size()
    stage_labels = [s.replace("Stage-", "S").replace(" ", "\n", 1) for s in stage_order]
    stage_counts = [int(counts.get(s, 0)) for s in stage_order]
    d.kpis([
        ("Total concepts", "25", "6 stage-gates"),
        ("Live in-market", "2", "ProteinPeak Q2"),
        ("Launch-ready", "3", "S4 + S5"),
        ("Discontinuing", "3", "Q3 FY26"),
    ])
    funnel = chart_bar(
        "r33_funnel.png",
        [s.replace("Stage-", "").replace("Final ", "") for s in stage_order],
        stage_counts,
        title="Innovation pipeline — concept count by stage-gate", color="navy",
        horizontal=True, h=2.9)
    d.image(funnel, "A wide idea/concept base narrowing to two live SKUs — a healthy funnel shape, discontinues aside.")
    d.body(
        "The funnel is broad at the front (13 concepts across Stage-1 Idea and Stage-2 Concept) and "
        "appropriately narrow at the back (two live SKUs, one in launch prep, two pre-launch). Three "
        "concepts sit in the final discontinue gate. The shape is right; the composition is the "
        "question — the early stages lean toward Crunchwell and RootDay line extensions where the "
        "confidence scores are lowest (0.22–0.46), while the highest-confidence bets are the protein "
        "and pack-refresh moves already deep in the pipe.")

    # top concepts by projected year-1 revenue
    top = ip[ip["rev"].notna()].sort_values("rev", ascending=False).head(8)
    revbar = chart_bar(
        "r33_projected_revenue.png",
        [n[:30] for n in top.concept_name],
        [round(float(r), 1) for r in top.rev],
        title="Projected year-1 revenue by concept — top 8 ($M, planning projection)",
        color="teal", horizontal=True, unit="M", h=3.0)
    d.image(revbar, "The Crunchwell Pack Refresh ($28M) dwarfs the field; the two live ProteinPeak SKUs follow.")

    # --- 2 · Stage-by-stage
    d.pagebreak()
    d.h1("2 · Stage-by-stage detail")
    for stg, hdr in [("Stage-6 In-Market", "2.1 · Stage-6 · In-market (live now)"),
                     ("Stage-5 Launch Prep", "2.2 · Stage-5 · Launch prep"),
                     ("Stage-4 Pre-Launch", "2.3 · Stage-4 · Pre-launch")]:
        sub = ip[ip.stage_gate == stg]
        d.h2(hdr)
        rows = [[r.concept_name, r.brand,
                 f"${r.rev:,.1f}M" if pd.notna(r.rev) else "—",
                 f"{r.conf:.2f}" if pd.notna(r.conf) else "—",
                 str(r.planned_launch_date)] for r in sub.itertuples()]
        d.table(["Concept", "Brand", "Yr1 rev (proj.)", "Conf.", "Launch"], rows,
                widths=[0.34, 0.18, 0.18, 0.12, 0.18])
    d.source("seed_csv('innovation_pipeline.csv'). Year-1 revenue is a planning projection, not booked revenue.")
    d.callout("The $28M Crunchwell Pack Refresh is the biggest single bet",
              "At $28M projected year-1 revenue and confidence 0.82, the Crunchwell Pack Refresh "
              "(Hero SKUs, launch 2026-08-15) dwarfs every other near-term concept and doubles as "
              "Leg 3 of the Louisiana recovery, carrying $1.4M of LA-targeted media. Its scale means "
              "it is also the biggest execution risk in the portfolio — a base-defence move, not a "
              "growth-pocket move, so its job is to hold Family Sweet share, not add to it.", "info")

    # --- 3 · Chocolate Almond gate
    d.h1("3 · Gate decision — ProteinPeak Chocolate Almond")
    ct = seed_csv("concept_test_chocolate_almond.csv")

    def _ct(section, metric):
        r = ct[(ct.section == section) & (ct.metric == metric)]
        return r["value"].iloc[0] if len(r) else None

    d.body(
        "The ProteinPeak Chocolate Almond concept (ProteinPeak Q3 candidate) cleared its stage-gate. "
        "On a monadic test of n=1,000, it scored 64% top-two-box purchase intent against Acme's 55% "
        "cereal-innovation action standard — +6pp versus the ProteinPeak launch-SKU pretest and +11pp "
        "versus the five-year innovation benchmark. Purchase intent is strongest exactly where the "
        "brand needs it: 71% top-two-box in the protein-curious cohort (3.06 mean intent) and 66% in "
        "lapsed-cereal, versus 52% in current-Crunchwell buyers.")
    d.h2("3.1 · Concept-test scorecard")
    ct_rows = [
        ["Top-two-box purchase intent", "64%", "≥55% action standard → clears"],
        ["vs launch-SKU pretest", "+6pp", "improving on the prior launch"],
        ["vs 5-yr innovation benchmark", "+11pp", "top-decile concept"],
        ["Protein-curious cohort TTB", "71%", "the target cohort"],
        ["Cannibalization (substitutional, vs launch SKUs)", "8pp", "<12pp SteerCo gate → clears"],
        ["Cannibalization (substitutional, vs Crunchwell)", "2pp", "negligible"],
    ]
    d.table(["Metric", "Result", "Read"], ct_rows, widths=[0.44, 0.16, 0.40])
    d.source("seed_concept_test_chocolate_almond (n=1000, field 2026-06-22 → 2026-07-11).")
    d.callout("Gate PASSED — but time-critical",
              "The concept clears both gates: 64% top-two-box (>55%) and 8pp substitutional "
              "cannibalization against the ProteinPeak launch SKUs (<12pp SteerCo threshold), with a "
              "further +14pp chocolate-breakfast preference among protein-curious households (U&A "
              "Apr 2026). With Larksfield's chocolate variant trademarked (Report 32), this concept "
              "should be fast-tracked, not parked.", "win")

    # --- 4 · Discontinues + governance
    d.h1("4 · Discontinue slate & governance")
    disc = ip[ip.stage_gate == "Stage-Final Discontinue"]
    disc_rows = [[r.concept_name.replace(" - Discontinue", ""), r.brand,
                  str(r.planned_launch_date), r.status] for r in disc.itertuples()]
    d.h2("4.1 · Confirmed discontinuations — Q3 FY2026")
    d.table(["SKU", "Brand", "Timing", "Status"], disc_rows,
            widths=[0.38, 0.20, 0.18, 0.24])
    d.source("innovation_pipeline.csv, Stage-Final Discontinue.")
    d.body(
        "Three SKUs are confirmed or planned for discontinuation in Q3 FY26: RootDay Coconut Blend "
        "(niche, sub-scale distribution), HoneyNest Granola Crunch and HoneyNest Cookie Dough (both "
        "in the structurally-declining Kids Sweet pocket, per Report 30). Pruning these frees shelf, "
        "supply-chain complexity and marketing focus for the protein and pack-refresh bets. A fourth "
        "SKU — RootDay Single-Serve Carton — sits on-hold at Stage-3.")
    d.h2("4.2 · Stage-gate governance")
    d.body(
        "The stage-gate discipline is working where it is applied: the Chocolate Almond concept was "
        "held to a quantified 55% action standard and a 12pp cannibalization ceiling, and passed on "
        "evidence rather than advocacy. The FY27 governance priorities are (1) apply the same "
        "quantified gates to the eight Stage-2 concepts, several of which carry sub-0.45 confidence "
        "and no clear whitespace thesis; (2) rebalance the early funnel toward the growing pockets; "
        "and (3) protect the two funded winners — the ProteinPeak line and the Crunchwell Pack "
        "Refresh — from resource dilution by lower-confidence line extensions.")
    d.callout("Portfolio risk",
              "The early funnel over-indexes on legacy line extensions (Crunchwell, RootDay) at low "
              "confidence, while the category's growth is in protein and single-serve (Report 30). "
              "Without a deliberate rebalance, the pipeline will keep generating low-return concepts "
              "in shrinking pockets and starve the pockets that are actually winning.", "risk")
    d.recommendations([
        ("Fast-track ProteinPeak Chocolate Almond to launch to pre-empt Larksfield's Q4 chocolate "
         "(Report 32).", "VP Innovation / Sage Park", "Now"),
        ("Protect the Crunchwell Pack Refresh launch (2026-08-15) as the biggest bet and Louisiana "
         "recovery Leg 3.", "Cory Whitman", "Q3 FY26"),
        ("Execute the Q3 discontinue slate; reallocate freed shelf/supply to protein and single-serve.",
         "R&D / Supply", "Q3 FY26"),
        ("Apply quantified stage-gates to the Stage-2 concepts; kill or advance on evidence "
         "(cross-ref LRP, Report 15).", "VP Innovation", "FY27 planning"),
    ])
    return d.build()


# ============================== 34 · eCommerce & Retail Media Q2 ============
def r34_ecommerce_retail_media():
    d = Doc("34-q2-2026-ecommerce-retail-media-performance.pdf",
            kicker="eCOMMERCE & RETAIL MEDIA",
            title="Acme Corp — Q2 FY2026 eCommerce & Retail Media Performance Review",
            subtitle="Retail-media incrementality by platform, digital shelf, and the H2 reallocation",
            owner="Tasha Brooks, eCommerce & Retail Media",
            period="Q2 FY2026 (Q1 detail)", short="eComm & RM Q2",
            doc_type="eCommerce & retail-media review", date_str="July 2026")

    rm = seed_csv("retail_media_spend_q1_2026.csv")
    rmg = rm.groupby("platform").agg(
        spend=("spend_kusd", "sum"),
        inc=("incremental_revenue_kusd", "sum"),
        ratio=("modeled_incrementality_ratio", "mean"),
        roas=("platform_reported_roas", "mean")).reset_index()
    rmg = rmg.sort_values("spend", ascending=False)
    tot_sp = rmg.spend.sum() / 1000
    tot_inc = rmg.inc.sum() / 1000

    d.cover_facts([
        ("Amazon Acme revenue (FY25)", "$44M (5.4% of net)"),
        ("Retail-media spend (Q1)", f"${tot_sp:.1f}M → ${tot_inc:.2f}M incremental"),
        ("Blended incrementality", f"${tot_inc/tot_sp:.2f} per $1 spent"),
        ("Best platform", "Walmart Connect — 1.20 modeled incrementality"),
        ("The drag", "Amazon Ads — 0.40 modeled incrementality"),
    ])

    d.exec_summary(
        f"The retail-media portfolio returned ${tot_inc:.2f}M of modeled incremental revenue on "
        f"${tot_sp:.1f}M of Q1 spend — a blended ${tot_inc/tot_sp:.2f} of incremental sales per "
        f"dollar. That blended number hides a 3x spread by platform: Walmart Connect returns 1.20 "
        f"and Kroger 0.77, while Amazon Ads — the largest single line at $2.4M — returns only 0.40 "
        f"because platform-reported ROAS double-counts a subscribe-and-save base that would have "
        f"converted anyway. The gap between what platforms report and what is genuinely incremental "
        f"is the central finding. The H2 recommendation is to reallocate ~$700K out of Amazon Ads "
        f"into Walmart, Kroger and Louisiana, where the incremental dollar works nearly 3x harder.",
        bullets=[
            f"<b>The portfolio:</b> ${tot_sp:.1f}M Q1 spend → ${tot_inc:.2f}M incremental "
            f"(${tot_inc/tot_sp:.2f} per $1). Amazon is the largest and the least efficient line.",
            "<b>Platform spread:</b> Walmart Connect 1.20 (best) and Kroger 0.77 carry the portfolio; "
            "Amazon Ads 0.40 and Target Roundel 0.50 lag on modeled incrementality.",
            "<b>Reported vs modeled:</b> Amazon's platform-reported ROAS (~1.1x) overstates true "
            "incrementality (0.40) because it credits an already-loyal subscribe-and-save base — the "
            "single biggest measurement gap in the portfolio.",
            "<b>H2 plan (planning estimate):</b> reallocate ~$700K out of Amazon Ads into Walmart "
            "Connect, Kroger and Louisiana at an estimated ~2.2x the current Amazon return; TikTok "
            "Shop grocery (macro strength 0.86) is the emerging test.",
        ])

    # --- 1 · Portfolio & platform
    d.h1("1 · Retail-media incrementality by platform")
    d.kpis([
        ("Q1 spend", f"${tot_sp:.1f}M", "4 platforms"),
        ("Incremental", f"${tot_inc:.2f}M", f"${tot_inc/tot_sp:.2f} per $1"),
        ("Best: Walmart", "1.20", "reinvest"),
        ("Drag: Amazon", "0.40", "reallocate"),
    ])
    order = ["Amazon Ads", "Walmart Connect", "Target Roundel", "Kroger Precision Marketing"]
    rmg["ord"] = rmg.platform.apply(lambda p: order.index(p) if p in order else 99)
    rmg = rmg.sort_values("ord")
    rows = [[r.platform, f"${r.spend/1000:.1f}M", f"${r.inc/1000:.2f}M",
             f"{r.roas:.2f}x", f"{r.ratio:.2f}",
             "Reinvest" if r.ratio >= 1 else "Reallocate"] for r in rmg.itertuples()]
    rows.append(["Total retail media", f"${tot_sp:.1f}M", f"${tot_inc:.2f}M", "—",
                 f"{tot_inc/tot_sp:.2f}", "Rebalance H2"])
    d.table(["Platform", "Spend", "Incremental", "Reported ROAS", "Modeled incr.", "Call"], rows,
            widths=[0.30, 0.13, 0.15, 0.15, 0.15, 0.12], total_row=True)
    d.source("seed_retail_media_spend_q1_2026 (Pacvue + modeled incrementality), Q1 FY2026.")

    grp = chart_grouped(
        "r34_spend_vs_incremental.png",
        [p.replace(" Precision Marketing", "") for p in rmg.platform],
        {"Spend $M": [round(float(r.spend) / 1000, 2) for r in rmg.itertuples()],
         "Incremental $M": [round(float(r.inc) / 1000, 2) for r in rmg.itertuples()]},
        title="Retail-media spend vs modeled incremental revenue by platform ($M)", unit="$M", h=2.9)
    d.image(grp, "Amazon spends the most and returns the least incremental; Walmart returns more than it costs.")

    # --- 2 · Incrementality ratio
    d.pagebreak()
    d.h1("2 · The incrementality ratio — where the dollar works")
    ratbar = chart_bar(
        "r34_incrementality_ratio.png",
        [p.replace(" Precision Marketing", "") for p in rmg.platform],
        [round(float(r.ratio), 2) for r in rmg.itertuples()],
        title="Modeled incrementality ratio by platform ($ incremental per $ spent)",
        colors_list=[_hex("green") if r.ratio >= 1 else (_hex("gold") if r.ratio >= 0.7 else _hex("rust"))
                     for r in rmg.itertuples()], h=2.7)
    d.image(ratbar, "Above 1.0 (Walmart) the media pays for itself; below ~0.5 (Amazon, Target) it is subsidising base sales.")
    d.body(
        "The incrementality ratio is the decision metric — dollars of genuinely incremental sales per "
        "dollar of media. Walmart Connect at 1.20 is the only platform where the media more than pays "
        "for itself; Kroger Precision at 0.77 is defensible, particularly given Acme's category "
        "captaincy there. Amazon Ads at 0.40 and Target Roundel at 0.50 are subsidising sales that "
        "would largely have happened anyway. The blended portfolio return of "
        f"${tot_inc/tot_sp:.2f} per dollar is dragged down almost entirely by the size of the Amazon line.")
    d.h2("2.1 · The reported-vs-modeled gap")
    d.callout("Amazon's reported ROAS is not incrementality",
              "Amazon platform-reported ROAS runs ~1.1x, which looks acceptable — but the modeled "
              "incrementality is 0.40, because Amazon's attribution credits a subscribe-and-save base "
              "that reorders regardless of the ad. The measurement gap (reported ~1.1x vs modeled "
              "0.40) is the single most important thing for the CFO to understand (see Report 40): "
              "the platform is reporting sales it did not cause. Where ProteinPeak runs on Amazon it "
              "does out-perform Crunchwell at the SKU level, so the fix is selective, not a full exit.",
              "info")

    # --- 3 · Search & digital shelf
    d.h1("3 · Search trends & the digital shelf")
    st = df("""SELECT Date d, ROUND(AVG(Volume_Index_0to100),1) v
               FROM search_trends
               WHERE Keyword IN ('proteinpeak','proteinpeak cinnamon crunch','proteinpeak cocoa almond','proteinpeak target')
                 AND Date >= '2025-06-01'
               GROUP BY 1 ORDER BY 1""")
    st_labels = [str(r.d)[:7] for r in st.itertuples()]
    stline = chart_line(
        "r34_search_trend.png", st_labels,
        {"ProteinPeak search (avg index)": [float(r.v) for r in st.itertuples()]},
        title="ProteinPeak search-volume index across keywords (0–100)", h=2.7)
    d.image(stline, "ProteinPeak search steps up sharply at the April 2026 launch — the launch-SKU keywords went from ~1 to 100.")
    d.body(
        "The digital shelf did its job at launch. Aggregate ProteinPeak search volume steps up sharply "
        "from April 2026, driven by the launch-SKU keywords: 'proteinpeak cinnamon crunch' ran near "
        "index 1 for two years and hit 100 at launch, and 'proteinpeak cocoa almond' spiked from under "
        "1 to the 60–85 range. The parent 'proteinpeak' term and 'proteinpeak target' also lifted, "
        "confirming that the Roundel endcap and creator activity converted into genuine search "
        "demand rather than just impressions. Digital-shelf availability held through the spike, so "
        "the demand converted rather than leaking to substitutes.")

    # --- 4 · Emerging & reallocation
    d.h1("4 · Emerging channels & the H2 reallocation")
    d.h2("4.1 · TikTok Shop grocery — the emerging test")
    d.body(
        "TikTok Shop for grocery carries a macro-trend strength of 0.86 (emerging, up) — the "
        "second-strongest signal in the trend frame after high-protein cereal. It is not yet a "
        "meaningful revenue line, but it is where the protein-curious, creator-led ProteinPeak "
        "audience already lives. The recommendation is a contained H2 test rather than a scaled "
        "commitment, funded from the Amazon reallocation.")
    d.h2("4.2 · Proposed H2 reallocation (planning estimate)")
    d.callout("Move ~$700K out of Amazon Ads",
              "The H2 plan is a planning estimate, contingent on a mid-H1 read: reallocate ~$700K of "
              "Amazon Ads spend (the TrailGrove and MorningOats lines that are near-fully cannibalized "
              "are the first defund candidates) into Walmart Connect, Kroger Precision and a Louisiana "
              "retail-media layer. At current platform ratios the reallocated dollar is estimated to "
              "work ~2.2x harder than it does on Amazon. ProteinPeak's Amazon spend, which out-performs "
              "at SKU level, is protected. Full CFO framing is in Report 40; the omnichannel plan "
              "cross-references Report 28.", "action")
    d.body(
        "The reallocation is not an Amazon exit — Amazon is a $44M Acme account and ProteinPeak's "
        "Amazon SKUs out-perform Crunchwell's. It is a surgical move out of the lines where Amazon's "
        "attribution most overstates incrementality (the defund candidates flagged in the Q1 data) "
        "and into the platforms and the region where the incremental dollar is proven to work harder.")
    d.recommendations([
        ("Reallocate ~$700K H2 out of Amazon Ads (defund near-cannibalized TrailGrove/MorningOats "
         "lines) into Walmart Connect, Kroger, and Louisiana.", "Tasha Brooks", "H2 planning"),
        ("Take the reported-vs-modeled incrementality gap to the CFO; standardise on modeled "
         "incrementality, not platform ROAS (Report 40).", "Tasha Brooks / Finance", "H2 MBR"),
        ("Protect ProteinPeak's Amazon spend — it out-performs at SKU level — while pruning the rest.",
         "eCommerce team", "Ongoing"),
        ("Stand up a contained TikTok Shop grocery test funded from the Amazon reallocation "
         "(cross-ref Report 28).", "Tasha Brooks", "H2 FY26"),
    ])
    return d.build()


if __name__ == "__main__":
    for fn in (r30_category_state_of_business,
               r31_shopper_household_panel,
               r32_competitive_intelligence,
               r33_innovation_stage_gate,
               r34_ecommerce_retail_media):
        print(fn())
