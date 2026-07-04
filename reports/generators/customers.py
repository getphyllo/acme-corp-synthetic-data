"""Customer / retailer JBPs, regional review, and CFO reforecast (reports 35-40).

Six builders:
  35 — Walmart FY27 Joint Business Plan
  36 — Kroger FY27 Joint Business Plan
  37 — Target FY27 JBP + Back-to-School 2026 wrap
  38 — Costco / Club Channel FY27 Line Review & JBP
  39 — South Region H1 FY26 Commercial Review + Louisiana Recovery Tracker
  40 — Q2 FY26 Financial Performance & H2 Reforecast (CFO read)

Every headline number traces to FACTS.md, acme.duckdb, or seeds/*.csv. Forward
FY27+/reforecast numbers are labelled as target / plan / planning estimate.
Run from repo root:  .venv/bin/python reports/generators/customers.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import (Doc, df, seed_csv, money, palette,
                 chart_line, chart_bar, chart_grouped, chart_stacked,
                 chart_waterfall, chart_donut)


# --------------------------------------------------------------- helpers ----
def _num(s):
    """Coerce a possibly-'N/A' seed column to float, NaN otherwise."""
    import pandas as pd
    return pd.to_numeric(s, errors="coerce")


# ============================================================ REPORT 35 =====
def r35_walmart_jbp():
    d = Doc("35-walmart-fy27-joint-business-plan.pdf",
            kicker="JOINT BUSINESS PLAN · FY27",
            title="Walmart — FY27 Joint Business Plan",
            subtitle="Acme Corp × Walmart · recovering facings, closing the endcap gap, winning protein",
            owner="Marcus Boudreaux, Sales; Walmart team (Tom Reilly, NAM)",
            period="FY2027 (built H2 FY26)", short="Walmart JBP FY27",
            doc_type="Retailer joint business plan", date_str="June 2026")

    d.cover_facts([
        ("Acme sales at Walmart (FY25)", "$184M · 21.4% of Acme ACV"),
        ("Account status", "#1 customer · Tier 1 cornerstone"),
        ("Live issue — LA endcaps", "23 of 41 Supercenters: 3 Larksfield, 0 Acme"),
        ("Live issue — protein", "Acme Wellness Protein share 5.2% (vs 18.4% at Target)"),
        ("Best-in-class lever", "Walmart Connect retail media — 1.20 incrementality"),
        ("FY27 joint theme", "Facing recovery · Pack Refresh · protein · retail media"),
    ])

    d.exec_summary(
        "Walmart is Acme's largest customer at $184M in FY25 net revenue — 21.4% of the "
        "company's ACV-weighted distribution and the single account that most moves the enterprise "
        "number. The relationship is fundamentally healthy, but three specific, fixable problems are "
        "costing both partners growth: the September 2025 modular reset cut Crunchwell Mega from 8 to 6 "
        "facings and became the primary driver of Louisiana's share collapse; a Louisiana endcap deficit "
        "now runs 3 Larksfield to 0 Acme in 23 of 41 audited Supercenters; and the ProteinPeak "
        "Walmart-pilot is underperforming at 78% of trial plan while the same brand over-indexes at Target. "
        "The FY27 plan is built to fix all three and to scale the one lever that is working best of any "
        "retailer — Walmart Connect.",
        bullets=[
            "<b>Recover the base.</b> The Louisiana driver is a Walmart execution issue we can jointly "
            "reverse — facing recovery on Crunchwell Mega and endcap parity against Larksfield.",
            "<b>Land the Pack Refresh.</b> Crunchwell's Hero-SKU Pack Refresh (a $28M year-one plan, "
            "on-shelf 15 Aug 2026) is the biggest near-term innovation; Walmart distribution timing is the ask.",
            "<b>Fix protein.</b> Acme holds only 5.2% Wellness Protein share at Walmart against a $840M, "
            "+18% category — the assortment gap, not demand, is the constraint.",
            "<b>Scale what works.</b> Walmart Connect returned $1.20 incremental per $1 in Q1 — the best of "
            "any platform — and is the funded engine for FY27 (see the CFO read, Report 40).",
        ])

    # --- section 1: account scorecard
    d.h1("1 · Account scorecard")
    d.kpis([
        ("Acme sales (FY25)", "$184M", "21.4% of Acme ACV"),
        ("Priority tier", "Tier 1", "cornerstone account"),
        ("Retail-media incr.", "1.20", "Walmart Connect, best-in-class"),
        ("LA protein share", "5.2%", "vs 18.4% at Target"),
    ])
    d.body(
        "Walmart is a cornerstone account and the largest line in Acme's customer book. The joint task "
        "for FY27 is not to reinvent the relationship but to remove three drags on a base that is otherwise "
        "sound: a shelf-set that has moved against Crunchwell in the South, a protein assortment that "
        "under-serves the fastest-growing pocket in the category, and a media investment that — uniquely at "
        "Walmart — is already paying back above 1.0.")

    rev = chart_bar("r35_rev.png", ["Walmart", "Kroger", "Target", "Costco", "Amazon"],
                    [184.0, 93.0, 68.0, 52.0, 44.0],
                    title="Acme net revenue by top customer, FY25 ($M)", color="navy",
                    unit="M", h=2.5)
    d.image(rev, "Walmart alone is roughly the sum of the next two accounts. Source: seed_retailers.")
    d.source("seed_retailers (Acme FY25 net revenue by customer).")

    # --- section 2: the September reset & endcap deficit
    d.pagebreak()
    d.h1("2 · The Louisiana shelf: reset & endcap deficit")
    d.body(
        "The September 2025 modular reset cut Crunchwell Mega from 8 facings to 6 in Louisiana "
        "Supercenters. That single change is the largest identified driver of Crunchwell's Louisiana share "
        "collapse — from ~6.4% to 3.0%, a −340 bps move detailed in the South Region review (Report 39). "
        "The situation has since worsened at the endcap. In the May 2026 audit of 41 Louisiana "
        "Supercenters, 23 carried three Larksfield (Field & Honey) endcaps and zero Acme endcaps; across "
        "all 47 doors audited, Acme held zero secondary displays against 111 for Larksfield.")

    ec = seed_csv("walmart_endcap_audit_la.csv")
    ec_may = ec[ec.audit_date == "2026-05-11"]
    sc = ec_may[ec_may.supercenter_format == "Supercenter"]
    three_lf = int(((sc.larksfield_endcap_count == 3) & (sc.acme_endcap_count == 0)).sum())
    d.h2("2.1 · Walmart LA endcap audit — May 2026")
    d.table(
        ["Metric", "Larksfield (Field & Honey)", "Acme (Crunchwell)"],
        [["Supercenters audited", f"{len(sc)}", f"{len(sc)}"],
         ["Total endcaps held", f"{int(sc.larksfield_endcap_count.sum())}", f"{int(sc.acme_endcap_count.sum())}"],
         ["Stores with 3 endcaps / 0 endcaps", f"{three_lf} with 3", f"{three_lf} with 0"],
         ["Crunchwell Mega facings (avg)", "—", f"{sc.facing_count_crunchwell_mega.mean():.0f} (was 8 pre-reset)"]],
        widths=[0.40, 0.30, 0.30])
    d.source("walmart_endcap_audit_la (store-level audit, 2026-05-11).")

    ecc = chart_grouped("r35_endcap.png", ["Sept 2025", "Oct 2025", "Nov 2025", "May 2026"],
                        {"Larksfield endcaps (per store)": [1.0, 2.0, 3.0, 105/41],
                         "Acme endcaps (per store)": [0.67, 0.33, 0.0, 0.0]},
                        title="Walmart LA endcaps per Supercenter — Larksfield vs Acme",
                        h=2.7)
    d.image(ecc, "Acme has been progressively displaced at the Walmart LA endcap since the September reset. "
                 "May 2026 figures are per-Supercenter averages across 41 stores. Source: walmart_endcap_audit_la.")
    d.callout("The endcap deficit is the recovery lever",
              "Rouses OOS and Larksfield promo intensity matter, but the Walmart endcap is where the "
              "share is being lost fastest. FY27 Leg 1 is a joint commitment to Crunchwell Mega facing "
              "recovery (6→8) and at least one Acme endcap in every LA Supercenter through the key windows.",
              "action")

    # --- section 3: protein gap
    d.h1("3 · The protein gap: Walmart vs Target")
    d.body(
        "Wellness Protein is the category's fastest-growing pocket — $710M in FY24 to $840M in FY25 "
        "(+18.3%), tracking +18.6% MTD in Q2 FY26. Acme's national share is building fast behind "
        "ProteinPeak, but the retailer split is stark: Acme holds 18.4% Wellness Protein share at Target "
        "and just 5.2% at Walmart. The ProteinPeak Walmart-pilot (Cinnamon Crunch, launched 27 Apr 2026) "
        "is running at 78% of trial plan against 113% at Target. This is an assortment and execution gap, "
        "not a demand problem — Walmart shoppers buy protein cereal, they just do not find Acme's on shelf.")

    pg = chart_bar("r35_protein.png", ["Target", "Walmart"], [18.4, 5.2],
                   title="Acme Wellness Protein value share by retailer (%)", pct=True,
                   colors_list=[palette["teal"], palette["rust"]], h=2.5)
    d.image(pg, "A 13.2-point retailer gap on the fastest-growing pocket in cereal. "
                "Source: seed_category_market_size (Q2-FY2026-MTD).")
    d.source("seed_category_market_size (Wellness Protein, Target/Walmart Total US); "
             "seed_proteinpeak_q2_launch (Walmart-pilot trial).")

    # --- section 4: retail media
    d.h1("4 · Retail media — Walmart Connect is the portfolio leader")
    rm = seed_csv("retail_media_spend_q1_2026.csv")
    rmg = rm.groupby("platform").agg(spend=("spend_kusd", "sum"),
                                     inc=("incremental_revenue_kusd", "sum"),
                                     ratio=("modeled_incrementality_ratio", "mean")).reset_index()
    rmg = rmg.sort_values("ratio", ascending=False)
    rows = [[r.platform, money(r.spend/1000), money(r.inc/1000, dp=2), f"{r.ratio:.2f}",
             "Scale" if r.ratio >= 1 else ("Hold" if r.ratio >= 0.75 else "Reallocate")]
            for r in rmg.itertuples()]
    d.table(["Platform", "Spend (Q1)", "Incremental", "Incr. ratio", "FY27 call"], rows,
            widths=[0.34, 0.16, 0.18, 0.16, 0.16])
    d.body(
        "Walmart Connect returned $1.21M incremental on $1.0M of Q1 spend — a 1.20 ratio, the best of any "
        "platform and the only one above break-even at scale. The FY27 plan reallocates media out of "
        "Amazon Ads (0.40, a drag) and into Walmart Connect, targeting the Louisiana recovery and the "
        "Pack Refresh launch window (see the CFO read, Report 40, for the H2 reallocation of ~$700K).")
    d.source("retail_media_spend_q1_2026 (Q1 FY26 modeled incrementality).")

    # --- section 5: FY27 joint targets
    d.h1("5 · FY27 joint targets & the ask")
    d.body(
        "The FY27 joint business plan is built on four commitments. The revenue figures below are "
        "planning targets, not booked business, and are contingent on the shelf and media actions landing "
        "in-window.")
    d.table(
        ["FY27 joint workstream", "Commitment", "Owner"],
        [["Facing recovery", "Crunchwell Mega 6→8 facings, LA Supercenters", "Boudreaux / Reilly"],
         ["Endcap parity", "≥1 Acme endcap per LA Supercenter, key windows", "Boudreaux / Reilly"],
         ["Pack Refresh distribution", "Hero-SKU Pack Refresh on-shelf 15 Aug 2026 ($28M yr-1 plan)", "Audrey Kim"],
         ["Protein assortment", "Close the 5.2%→Target-benchmark gap; ProteinPeak items", "Sage Park"],
         ["Retail media", "Scale Walmart Connect; fund LA recovery at 2.2× ROI", "Tasha Brooks"]],
        widths=[0.26, 0.52, 0.22])
    d.callout("FY27 risk — Larksfield is escalating on two fronts",
              "Field & Honey launched a 14g-protein line extension (LCH00032) on 12 May 2026, pressing the "
              "protein and Louisiana battles simultaneously. If the September 2026 reset does not restore "
              "Crunchwell facings and grant Acme endcaps, the Louisiana base does not recover and the "
              "protein gap widens. Reset timing is the single highest-leverage joint decision for FY27.",
              "risk")
    d.recommendations([
        ("Restore Crunchwell Mega to 8 facings and secure ≥1 Acme endcap per LA Supercenter at the Sept 2026 reset.",
         "Marcus Boudreaux / Tom Reilly", "Sept 2026 reset"),
        ("Confirm Pack Refresh Hero-SKU distribution and timing to hold the 15 Aug 2026 on-shelf date.",
         "Audrey Kim / Walmart team", "Aug 2026"),
        ("Build a ProteinPeak Walmart assortment plan to close the 5.2%→18.4% share gap vs Target.",
         "Sage Park", "FY27 line review"),
        ("Scale Walmart Connect and direct the H2 media reallocation into LA recovery (2.2× ROI).",
         "Tasha Brooks", "H2 FY26 → FY27"),
    ])
    return d.build()


# ============================================================ REPORT 36 =====
def r36_kroger_jbp():
    d = Doc("36-kroger-fy27-joint-business-plan.pdf",
            kicker="JOINT BUSINESS PLAN · FY27",
            title="Kroger — FY27 Joint Business Plan",
            subtitle="Acme Corp × Kroger · category captaincy, defending against Simple Truth, winning protein",
            owner="Priya Raman, Category Manager; Kroger team (Jasmine Watkins, NAM)",
            period="FY2027", short="Kroger JBP FY27",
            doc_type="Retailer joint business plan", date_str="June 2026")

    d.cover_facts([
        ("Acme sales at Kroger (FY25)", "$93M · Tier 1"),
        ("Acme role", "Category captain — RTE cereal"),
        ("Live threat", "Simple Truth private-label protein switching"),
        ("Crunchwell → Simple Truth switch", "14.3% national (Kroger HH panel)"),
        ("Larksfield share gain", "+1.4 pts national · +2.1 pts Kroger-South"),
        ("Retail-media incrementality", "0.77 (Kroger Precision Marketing)"),
    ])

    d.exec_summary(
        "Kroger is Acme's #2 customer at $93M in FY25 net revenue and the account where Acme holds the "
        "category-captain seat. That captaincy is now being tested from inside the store: Kroger's own "
        "Simple Truth private label is pulling protein-forward shoppers out of Crunchwell at a 14.3% "
        "national switch rate, and Larksfield's Field & Honey is gaining shelf momentum, up +1.4 points "
        "nationally and +2.1 points in Kroger-South. Neither threat is Kroger acting against Acme — both "
        "are the category evolving toward protein and value. The FY27 plan uses the captain's chair to "
        "grow the total category while defending Crunchwell and accelerating ProteinPeak into the "
        "protein pocket Simple Truth is currently capturing.",
        bullets=[
            "<b>Defend the base.</b> Crunchwell is switching to Simple Truth at 14.3% nationally; the loss "
            "is concentrated in protein-forward and sugar-reduced occasions, exactly where ProteinPeak plays.",
            "<b>Convert the threat.</b> The protein-forward segment is pulling ~2.3% per quarter out of "
            "traditional family cereal — captaincy should route that demand to ProteinPeak, not Simple Truth.",
            "<b>Watch the South.</b> Larksfield gained +2.1 points at Kroger-South, the same battlefield as "
            "the Louisiana decline (see Report 39).",
            "<b>Improve media efficiency.</b> Kroger Precision Marketing returned $0.77 per $1 in Q1 — "
            "solid but below break-even; FY27 optimizes toward it.",
        ])

    # --- section 1: scorecard
    d.h1("1 · Account & captaincy scorecard")
    d.kpis([
        ("Acme sales (FY25)", "$93M", "#2 customer · Tier 1"),
        ("Acme role", "Cat captain", "RTE cereal"),
        ("Crunchwell switch", "14.3%", "to Simple Truth (natl)"),
        ("Retail-media incr.", "0.77", "Kroger Precision"),
    ])
    d.body(
        "Acme's category-captaincy at Kroger is an asset and a responsibility: it gives Acme the shelf and "
        "assortment influence to steer category growth, and it obliges Acme to grow the total category, "
        "not just its own brands. The FY27 plan is written in that frame — defend Crunchwell against "
        "private-label switching while routing the category's protein migration into ProteinPeak "
        "distribution rather than ceding it to Simple Truth.")

    # --- section 2: Simple Truth switching
    d.h1("2 · Simple Truth private-label switching")
    st = seed_csv("kroger_simple_truth_switching.csv")
    st_div = st[(st.segment == "Protein") & (st.kroger_division.str.startswith("Kroger-"))].copy()
    st_div["switch_rate_pct"] = _num(st_div["switch_rate_pct"])
    st_div["from_hh_count"] = _num(st_div["from_hh_count"])
    st_div = st_div.sort_values("switch_rate_pct", ascending=False)
    d.body(
        "A Numerator household-panel study across Kroger divisions shows Crunchwell lapsed buyers switching "
        "into Simple Truth protein items at a 14.3% national rate — the anchor number for this plan. The "
        "switch is heaviest in the protein and wholegrain segments (12.4%–20.0% by division and item "
        "group) and is where Simple Truth has gained +0.8 points of protein-segment share. Larksfield's "
        "Field & Honey is the other gainer, up +1.4 points nationally and +2.1 points at Kroger-South.")

    sf = chart_bar("r36_switch.png",
                   [r.kroger_division.replace("Kroger-", "") for r in st_div.itertuples()],
                   list(st_div.switch_rate_pct),
                   title="Crunchwell → Simple Truth protein switch rate, by Kroger division (%)",
                   pct=True, color="rust", horizontal=True, h=2.9)
    d.image(sf, "Protein-segment switching runs 12.9%–15.3% across divisions; the aggregated national rate "
                "is 14.3%. Source: kroger_simple_truth_switching (Numerator HH panel, 2026-Q1).")

    d.h2("2.1 · Where the share is going")
    d.table(
        ["Share movement (2026-Q1, Kroger)", "Shift", "Read"],
        [["Simple Truth — protein segment", "+0.8 pts", "PL capturing protein demand"],
         ["Larksfield Field & Honey — national", "+1.4 pts", "branded protein challenger"],
         ["Larksfield Field & Honey — Kroger-South", "+2.1 pts", "same front as Louisiana decline"],
         ["Protein-forward vs traditional family", "−2.3%/qtr", "segment migration, category-wide"],
         ["Crunchwell — national", "flat", "holding, but leaking to protein"]],
        widths=[0.52, 0.18, 0.30])
    d.source("kroger_simple_truth_switching (anchor rows: national 14.3%, Simple Truth +0.8 pts, "
             "Larksfield +1.4 natl / +2.1 South).")
    d.callout("The switch is a protein story, not a price story",
              "Crunchwell is losing protein-forward and sugar-reduced occasions, each pulling ~2.3% per "
              "quarter out of traditional family cereal. The defensible move is not deeper Crunchwell "
              "promotion — it is putting ProteinPeak on the Kroger protein shelf so the migrating shopper "
              "stays in an Acme brand rather than switching to Simple Truth.", "info")

    # --- section 3: category leadership / share by segment
    d.pagebreak()
    d.h1("3 · Category leadership — growing the whole aisle")
    cat = seed_csv("category_market_size.csv")
    fy25 = cat[(cat.period == "FY2025") & (cat.geography == "US National")]
    seg_rows = []
    for name, sub in [("Family Sweet", "Family Sweet"), ("Family Oat", "Family Oat"),
                      ("Wellness Protein", "Wellness Protein"), ("Kids Sweet", "Kids Sweet")]:
        row = cat[(cat.subcategory == sub) & (cat.geography == "US National") & (cat.period == "FY2025")]
        if len(row):
            r = row.iloc[0]
            seg_rows.append([name, money(r.market_size_usd_mm/1000, dp=2, unit="B") if r.market_size_usd_mm > 1000
                             else money(r.market_size_usd_mm, dp=0), f"{r.yoy_growth_pct:+.1f}%", f"{r.acme_share_pct:.1f}%"])
    d.body(
        "As category captain, Acme's FY27 plan for Kroger is to grow the total aisle by leaning into the "
        "pockets that are growing and managing the ones that are declining. Wellness Protein (+18.3%) and "
        "Family Oat (+0.4–2.4%) are where the plan invests distribution and shelf; Kids Sweet (−2.8%) is "
        "managed for margin, not volume.")
    d.table(["RTE segment (FY25, US)", "Size", "YoY growth", "Acme share"], seg_rows,
            widths=[0.40, 0.20, 0.20, 0.20])
    d.source("category_market_size (NielsenIQ-shape, FY2025 US National).")

    seg_ch = chart_bar("r36_segments.png",
                       ["Wellness\nProtein", "Family\nOat", "Family\nSweet", "Kids\nSweet"],
                       [18.3, 2.4, 1.4, -2.8],
                       title="RTE segment dollar growth, FY25 (%) — where captaincy should lean",
                       pct=True,
                       colors_list=[palette["teal"], palette["teal"], palette["gold"], palette["rust"]],
                       h=2.5)
    d.image(seg_ch, "Route category growth to protein and oat; manage kids-sweet decline. "
                    "Family Oat +2.4% per FACTS; total-oat framing. Source: category_market_size.")

    # --- section 4: retail media & trade
    d.h1("4 · Kroger Precision Marketing & trade")
    d.body(
        "Kroger Precision Marketing returned $0.32M incremental on $0.4M of Q1 spend — a 0.77 ratio, "
        "second only to Walmart Connect in the portfolio and clearly worth scaling in FY27 with tighter "
        "targeting. Crunchwell's Kroger trade line ran $18.2M in FY25 at a 0.60 incrementality index, "
        "leveraged by the captaincy relationship; the FY27 promo plan rationalizes depth toward "
        "higher-incrementality mechanics rather than blanket price-off.")
    ts = seed_csv("trade_spend_fy25.csv")
    kr = ts[ts.retailer == "Kroger"].sort_values("trade_spend_kusd", ascending=False)
    trows = [[r.brand, money(r.trade_spend_kusd/1000, dp=1), f"{r.trade_depth_pct:.1f}%",
              f"{r.incrementality_index:.2f}"] for r in kr.itertuples()]
    d.table(["Brand (Kroger trade, FY25)", "Spend", "Depth", "Incr. index"], trows,
            widths=[0.40, 0.20, 0.20, 0.20])
    d.source("trade_spend_fy25 (Kroger); retail_media_spend_q1_2026 (Kroger Precision).")

    # --- section 5: FY27 targets
    d.h1("5 · FY27 joint targets & the ask")
    d.table(
        ["FY27 joint workstream", "Commitment", "Owner"],
        [["Defend Crunchwell", "Cut the 14.3% Simple Truth switch; protein/sugar-reduced offense", "Priya Raman"],
         ["Protein assortment", "ProteinPeak distribution on the Kroger protein shelf", "Sage Park"],
         ["Category leadership", "Grow the aisle: protein + oat in, manage kids-sweet", "Priya Raman"],
         ["Promo optimization", "Rationalize Crunchwell depth toward higher-incrementality mechanics", "Priya Raman"],
         ["Retail media", "Scale Kroger Precision (0.77) with tighter targeting", "Tasha Brooks"]],
        widths=[0.26, 0.52, 0.22])
    d.callout("FY27 risk — the captain must convert the protein migration",
              "If ProteinPeak does not win Kroger protein-shelf distribution in FY27, the category's "
              "protein migration continues to flow to Simple Truth and Field & Honey — and the captaincy "
              "narrative erodes with it. Defending Crunchwell on price alone loses money and does not "
              "address the underlying segment shift. See the pre-read, Report 03, and the LA read, Report 32.",
              "risk")
    d.recommendations([
        ("Stand up a Crunchwell defense plan targeting protein-forward and sugar-reduced switching to Simple Truth.",
         "Priya Raman", "FY27 JBP"),
        ("Win ProteinPeak protein-shelf distribution at Kroger to intercept the protein migration.",
         "Sage Park / Jasmine Watkins", "FY27 line review"),
        ("Use captaincy to grow the total aisle: protein and oat distribution up, kids-sweet managed.",
         "Priya Raman", "FY27"),
        ("Scale Kroger Precision Marketing (0.77) and rationalize Crunchwell trade depth.",
         "Tasha Brooks", "H2 FY26 → FY27"),
    ])
    return d.build()


# ============================================================ REPORT 37 =====
def r37_target_jbp_bts():
    d = Doc("37-target-fy27-jbp-back-to-school-2026-wrap.pdf",
            kicker="JOINT BUSINESS PLAN · FY27 + BTS WRAP",
            title="Target — FY27 Joint Business Plan & Back-to-School 2026 Wrap",
            subtitle="Acme Corp × Target · extending the ProteinPeak lead, the BTS occasion, Roundel efficiency",
            owner="Wes Okafor, Shopper Marketing; Target team (Soo-jin Lee, NAM)",
            period="FY2027 · BTS 2026", short="Target JBP + BTS",
            doc_type="Retailer joint business plan", date_str="June 2026")

    d.cover_facts([
        ("Acme sales at Target (FY25)", "$68M · Tier 1"),
        ("ProteinPeak fit", "18.4% Wellness Protein share (vs 5.2% at Walmart)"),
        ("Launch performance", "Trial 113% of plan (vs 78% at Walmart-pilot)"),
        ("BTS 2025 benchmark", "$14.4M incremental category $ (Target)"),
        ("BTS cohort overlap", "~65% protein-curious · ~69% Circle members"),
        ("Retail-media incrementality", "0.50 (Target Roundel)"),
    ])

    d.exec_summary(
        "Target is Acme's #3 customer at $68M and the account where the future of the portfolio shows up "
        "first. ProteinPeak over-indexes here — 18.4% Wellness Protein value share against 5.2% at Walmart "
        "— and the Q2 2026 launch cleared 113% of trial plan at Target versus 78% at the Walmart-pilot. "
        "The Target shopper is protein-curious, Circle-connected, and skews toward exactly the households "
        "Acme wants. The 2025 Back-to-School occasion delivered $14.4M in incremental category dollars at "
        "Target across a seven-week window, with roughly two-thirds protein-curious cohort overlap. The "
        "FY27 plan extends the ProteinPeak lead, builds a repeatable BTS program, and pushes Roundel "
        "toward payback.",
        bullets=[
            "<b>Extend the protein lead.</b> Target is Acme's protein stronghold; the FY27 plan protects "
            "and widens the 18.4% share while Walmart catches up.",
            "<b>Own Back-to-School.</b> BTS 2025 was worth $14.4M in incremental category dollars at Target; "
            "FY27 builds a shopper-marketing program around the occasion.",
            "<b>Land Chocolate Almond.</b> The ProteinPeak Q3 Chocolate Almond concept cleared 64% top-2-box "
            "(action standard 55%) and indexes to the Target protein-curious shopper (see Report 06 / 23).",
            "<b>Fix Roundel.</b> Target Roundel returned $0.50 per $1 in Q1 — the lowest of the four retail "
            "media platforms; FY27 rebuilds it around the BTS and launch windows.",
        ])

    # --- section 1: scorecard + protein over-index
    d.h1("1 · Account scorecard — the protein stronghold")
    d.kpis([
        ("Acme sales (FY25)", "$68M", "#3 customer · Tier 1"),
        ("Protein share", "18.4%", "vs 5.2% at Walmart"),
        ("Launch trial", "113%", "of plan (Wk-4)"),
        ("Roundel incr.", "0.50", "lowest of 4 platforms"),
    ])
    d.body(
        "Target is where Acme's wellness-protein bet is already working. ProteinPeak holds 18.4% Wellness "
        "Protein value share at Target — more than three times its 5.2% share at Walmart — and the April "
        "2026 launch of Cinnamon Crunch and Cocoa Almond cleared 113% of trial plan in the first four "
        "weeks, supported by a national endcap and Roundel. The Target shopper profile explains it: "
        "protein-curious, premium-leaning, and Circle-connected.")

    pg = chart_bar("r37_protein.png", ["Target", "Walmart"], [18.4, 5.2],
                   title="Acme Wellness Protein value share, Target vs Walmart (%)", pct=True,
                   colors_list=[palette["teal"], palette["slate"]], h=2.4)
    d.image(pg, "Target over-indexes for ProteinPeak by 13.2 points. Source: category_market_size (Q2-FY2026-MTD).")

    # --- section 2: BTS wrap
    d.h1("2 · Back-to-School 2026 wrap (2025 benchmark)")
    bts = seed_csv("numerator_bts_occasion_2025.csv")
    tb = bts[bts.retailer == "Target"].sort_values("iso_week")
    bts_total = tb.incremental_category_dollars_kusd.sum() / 1000
    d.body(
        "The Back-to-School occasion is a distinct, high-value cereal window at Target. The 2025 benchmark "
        f"(seven weeks, W28–W34) delivered {money(bts_total)} in incremental category dollars at Target — "
        "the largest single-retailer BTS pull in the Numerator occasion frame. The occasion concentrates "
        "exactly the households Acme wants: cereal-buying households with kids 5–14, ~65% protein-curious "
        "cohort overlap, and ~69% Target Circle membership overlap. That overlap makes BTS the natural "
        "moment to introduce protein-forward cereal to family shoppers.")

    bts_ch = chart_line("r37_bts.png",
                        [w.replace("2025-", "") for w in tb.iso_week],
                        {"Incremental category $ (M)": [round(x/1000, 2) for x in tb.incremental_category_dollars_kusd]},
                        title="Target BTS occasion — incremental category dollars by week ($M, 2025)",
                        h=2.7)
    d.image(bts_ch, f"The BTS window peaks in mid-August (W32–W33). Seven-week total {money(bts_total)}. "
                    "Source: numerator_bts_occasion_2025 (Target).")
    d.h2("2.1 · Who the BTS shopper is")
    d.table(
        ["BTS occasion overlap (Target, 2025)", "Value", "Why it matters"],
        [["HH with kids 5–14 buying cereal", f"~{tb.hh_kids_5_14_buying_cereal_share.mean()*100:.0f}% share", "family occasion core"],
         ["Protein-curious cohort overlap", f"~{tb.protein_curious_cohort_overlap.mean()*100:.0f}%", "ProteinPeak intro window"],
         ["Target Circle membership overlap", f"~{tb.target_circle_membership_overlap.mean()*100:.0f}%", "addressable via Roundel"],
         ["Incremental category dollars", f"{money(bts_total)}", "the size of the prize"]],
        widths=[0.44, 0.22, 0.34])
    d.source("numerator_bts_occasion_2025 (Target, W28–W34 2025 benchmark).")

    # --- section 3: Chocolate Almond
    d.pagebreak()
    d.h1("3 · ProteinPeak Chocolate Almond — Q3 fit for the Target shopper")
    ca = seed_csv("concept_test_chocolate_almond.csv")
    def caval(sec, met):
        r = ca[(ca.section == sec) & (ca.metric == met)]
        return r.value.iloc[0] if len(r) else None
    ttb = caval("topline", "top_two_box_pct")
    thr = caval("topline", "action_standard_threshold_pct")
    pc_ttb = caval("protein-curious", "top_two_box_pct")
    choc_pref = caval("overlay", "chocolate_breakfast_preference_protein_curious_vs_cereal_avg_pp")
    d.body(
        f"The ProteinPeak Chocolate Almond concept (Q3 innovation) cleared {ttb}% top-two-box against a "
        f"{thr}% action standard — +6 points versus the launch-SKU pretest and +11 points versus the "
        "five-year cereal-innovation benchmark. Critically for Target, it over-indexes on precisely the "
        f"shopper Target concentrates: the protein-curious cohort scored {pc_ttb}% top-two-box, and "
        f"chocolate-as-a-breakfast-flavor preference runs +{choc_pref} points higher among protein-curious "
        "shoppers than the cereal average. It also passes the cannibalization gate (8pp substitutional < "
        "12pp SteerCo threshold). Chocolate Almond is the right FY27 innovation to lead at Target.")
    ca_ch = chart_bar("r37_choc.png",
                      ["Protein-\ncurious", "All\ncells", "Lapsed-\ncereal", "Action\nstandard", "Current\nCrunchwell"],
                      [float(pc_ttb), float(ttb), float(caval("lapsed-cereal", "top_two_box_pct")),
                       float(thr), float(caval("current-Crunchwell", "top_two_box_pct"))],
                      title="Chocolate Almond purchase intent — top-2-box by cohort (%)", pct=True,
                      colors_list=[palette["teal"], palette["teal"], palette["sky"], palette["gold"], palette["slate"]],
                      h=2.5)
    d.image(ca_ch, "Protein-curious 71% and all-cells 64% both clear the 55% action standard. "
                   "Source: concept_test_chocolate_almond (field 2026-06-22 → 2026-07-11).")

    # --- section 4: Roundel
    d.h1("4 · Target Roundel — the efficiency fix")
    d.body(
        "Roundel is the FY27 efficiency project. It returned $0.22M incremental on $0.4M of Q1 spend — a "
        "0.50 ratio, the lowest of the four retail-media platforms. The Target shopper is highly "
        "addressable (Circle overlap ~69% in the BTS window), so the gap is targeting and creative "
        "discipline, not audience quality. FY27 rebuilds Roundel around two owned moments — the ProteinPeak "
        "launch/relaunch windows and the BTS occasion — rather than always-on spend.")
    d.callout("Roundel is under-earning a premium audience",
              "A 0.50 incrementality ratio on the account with the strongest protein shopper and 69% Circle "
              "overlap is a self-inflicted inefficiency. Concentrating Roundel into the BTS and launch "
              "windows — where intent and addressability peak — is the fastest path to payback.", "info")

    # --- section 5: FY27 targets
    d.h1("5 · FY27 joint targets & the ask")
    d.table(
        ["FY27 joint workstream", "Commitment", "Owner"],
        [["Extend ProteinPeak lead", "Protect/widen 18.4% protein share; lead Chocolate Almond Q3", "Sage Park"],
         ["Back-to-School program", "Build a repeatable BTS shopper program on the $14.4M occasion", "Wes Okafor"],
         ["Roundel efficiency", "Rebuild around BTS + launch windows; target payback > 0.50", "Tasha Brooks"],
         ["Circle activation", "Use ~69% Circle overlap for protein-curious intro at BTS", "Wes Okafor"]],
        widths=[0.28, 0.50, 0.22])
    d.callout("FY27 risk — the protein lead is contestable",
              "Target is Acme's protein stronghold, but Larksfield's 14g-protein line extension (12 May "
              "2026) and the premium-protein challengers (Magic Spoon, Three Wishes) all court the same "
              "protein-curious shopper. Leading Chocolate Almond at Target and owning the BTS occasion is "
              "how the lead is defended rather than assumed. See Reports 23 and 31.", "risk")
    d.recommendations([
        ("Lead the ProteinPeak Q3 Chocolate Almond launch at Target, indexed to the protein-curious shopper.",
         "Sage Park / Soo-jin Lee", "Q3 FY26 → FY27"),
        ("Stand up a repeatable Back-to-School shopper-marketing program on the $14.4M Target occasion.",
         "Wes Okafor", "BTS 2026"),
        ("Rebuild Roundel around BTS and launch windows to move the 0.50 incrementality toward payback.",
         "Tasha Brooks", "H2 FY26"),
        ("Activate the ~69% Circle overlap for protein-curious introduction during BTS.",
         "Wes Okafor", "BTS 2026"),
    ])
    return d.build()


# ============================================================ REPORT 38 =====
def r38_club_line_review():
    d = Doc("38-costco-club-fy27-line-review-jbp.pdf",
            kicker="CLUB CHANNEL LINE REVIEW · FY27",
            title="Costco / Club Channel — FY27 Line Review & Joint Business Plan",
            subtitle="Costco, Sam's Club & club channel · pack architecture, item count, the value equation",
            owner="Club Channel Sales (Frank Calabrese, NAM)",
            period="FY2027", short="Club JBP FY27",
            doc_type="Club channel line review", date_str="June 2026")

    d.cover_facts([
        ("Costco (FY25)", "$52M · Tier 1 (Club)"),
        ("Sam's Club (FY25)", "$28M · Tier 2 (Club)"),
        ("Club channel total", "~$80M Acme (Costco + Sam's)"),
        ("Club dynamics", "Limited SKU count · big-pack value · treasure-hunt · membership"),
        ("Pack architecture bet", "Crunchwell Mega Family Pack 36oz ($8.5M yr-1 plan, 2027-Q1)"),
        ("Data caveat", "Club-level splits are planning estimates — see §4"),
    ])

    d.exec_summary(
        "The club channel — Costco at $52M and Sam's Club at $28M in FY25, roughly $80M of Acme net "
        "revenue combined — plays by different rules than mass and grocery: a deliberately limited item "
        "count, a big-pack value equation, treasure-hunt merchandising, and a membership base that rewards "
        "trip-worthy value. Acme wins in club where it brings a distinct pack architecture (MorningOats "
        "Cup is the current hero) and loses where it simply ships mass SKUs into a club box. The FY27 line "
        "review is a pack-architecture argument: a Crunchwell Mega Family Pack 36oz built for the club "
        "value equation, TrailGrove and RootDay multipacks, and a ProteinPeak club variety pack to carry "
        "the fastest-growing pocket into the channel. Club-level financial splits in this document are "
        "planning estimates; the dataset carries limited club-granular history and we flag it explicitly.",
        bullets=[
            "<b>Club is a pack-architecture channel.</b> Item count is scarce; each SKU must earn its slot "
            "on pack size, value-per-ounce, and trip appeal — not brand breadth.",
            "<b>The headline bet.</b> Crunchwell Mega Family Pack 36oz ($8.5M year-one plan, 2027-Q1 "
            "prototype) is purpose-built for the club value equation.",
            "<b>Carry protein into club.</b> A ProteinPeak club variety pack brings the +18% Wellness "
            "Protein pocket into the channel; TrailGrove/RootDay multipacks extend the same logic.",
            "<b>Planning-estimate flag.</b> Costco and Sam's are $52M/$28M in the retailer master, but "
            "club-level brand/pack splits below are modelled planning estimates, not measured club POS.",
        ])

    # --- section 1: channel scorecard
    d.h1("1 · Club channel scorecard")
    d.kpis([
        ("Costco (FY25)", "$52M", "Tier 1 · Club"),
        ("Sam's Club (FY25)", "$28M", "Tier 2 · Club"),
        ("Club total", "~$80M", "Costco + Sam's"),
        ("Current hero", "MorningOats Cup", "club value SKU"),
    ])
    d.body(
        "Costco and Sam's Club together carry roughly $80M of Acme net revenue. Both are club-format "
        "accounts: a curated item count in the low single digits per category, a big-pack/value merchandising "
        "model, and treasure-hunt discovery that rewards genuinely differentiated pack architecture. "
        "MorningOats Cup is Acme's current club hero; the FY27 line review is about earning more of the "
        "scarce club slots with packs designed for the channel rather than adapted from mass.")

    clubrev = chart_bar("r38_clubrev.png", ["Costco", "Sam's Club", "BJ's"],
                        [52.0, 28.0, 9.0],
                        title="Acme net revenue by club account, FY25 ($M)", color="navy",
                        unit="M", h=2.4)
    d.image(clubrev, "Costco leads the channel; Sam's is the growth seat. Source: seed_retailers.")
    d.source("seed_retailers (Costco, Sam's Club, BJ's — Acme FY25 net revenue).")

    # --- section 2: pack architecture
    d.h1("2 · Pack architecture — the FY27 argument")
    d.body(
        "Club rewards value-per-ounce and pack distinctiveness. Acme's mass architecture tops out at 18oz "
        "(Crunchwell Mega); club buyers reward a bigger, better-value pack. The FY27 line review leads "
        "with the Crunchwell Mega Family Pack 36oz — a Stage-3 prototype carrying an $8.5M year-one plan "
        "and a 2027-Q1 target — doubling the current Mega pack size into the club value equation. Multipack "
        "formats (TrailGrove bars, RootDay cartons) and a ProteinPeak variety pack complete the argument.")
    sk = seed_csv("skus.csv")
    biggest = sk[sk.status == "Active"].sort_values("pack_size_oz", ascending=False).head(6)
    prows = [[r.sku_name, f"{r.pack_size_oz:.0f} oz", money(r.avg_shelf_price_usd, unit="", dp=2),
              r.price_tier] for r in biggest.itertuples()]
    d.h2("2.1 · Current largest packs vs the club opportunity")
    d.table(["Largest active packs today", "Pack size", "Shelf price", "Tier"], prows,
            widths=[0.44, 0.18, 0.18, 0.20])
    d.body(
        "Today's largest single-pack in the branded cereal line is 18oz. The proposed Crunchwell Mega "
        "Family Pack 36oz is a purpose-built club doubling; RootDay already ships a 32oz carton that "
        "multipacks cleanly, and TrailGrove/ProteinPeak run 6-count formats that lend themselves to "
        "club variety packs.")
    d.source("skus (active SKU pack architecture); innovation_pipeline (Mega Family Pack 36oz, Stage-3).")

    pk = chart_bar("r38_pack.png",
                   ["Crunchwell\nMega (today)", "Mega Family\nPack 36oz (plan)", "RootDay\ncarton", "MorningOats\nSteel Cut"],
                   [18, 36, 32, 30],
                   title="Pack-size architecture — the club value ladder (oz)", color="teal",
                   unit="oz", h=2.5)
    d.image(pk, "The 36oz Family Pack is the missing rung on the club value ladder. "
                "36oz figure is a planning-estimate concept spec. Source: skus, innovation_pipeline.")
    d.callout("Innovation status — planning, not booked",
              "Crunchwell Mega Family Pack 36oz is a Stage-3 prototype with a $8.5M year-one revenue plan "
              "and a 2027-Q1 target (confidence 0.62). It is a plan, not committed distribution. See the "
              "RGM / price-pack architecture read, Report 17.", "info")

    # --- section 3: item plan
    d.pagebreak()
    d.h1("3 · FY27 club item plan")
    d.body(
        "The FY27 club item plan concentrates Acme's scarce slots against the value equation and the "
        "growing pockets. Revenue figures are club-level planning estimates, not measured club POS.")
    d.table(
        ["FY27 club item candidate", "Format", "Club rationale", "Status"],
        [["Crunchwell Mega Family Pack 36oz", "Big-pack single", "Value-per-oz; treasure-hunt", "Plan ($8.5M yr-1)"],
         ["ProteinPeak club variety pack", "Multipack", "Carry +18% protein into club", "Concept"],
         ["TrailGrove bars multipack", "6-ct+ multipack", "Snacking value; current variety-pack pull", "Extend"],
         ["RootDay oat-milk multipack", "Carton multipack", "32oz cartons multipack cleanly", "Extend"],
         ["MorningOats Cup club pack", "Cup multipack", "Current club hero; single-serve +9.8%", "Grow"]],
        widths=[0.34, 0.18, 0.30, 0.18])
    d.source("innovation_pipeline, skus, category_market_size (single-serve cups +9.8%). "
             "Item-level club economics are planning estimates.")
    d.body(
        "The value equation is the club buyer's decision rule: does this pack deliver enough value-per-"
        "ounce and trip appeal to earn one of a handful of slots? Acme's FY27 answer is bigger packs on "
        "Crunchwell, variety packs on protein and snacking, and a defended MorningOats Cup position.")

    # --- section 4: data caveat + line-review asks
    d.h1("4 · Data caveat & FY27 line-review asks")
    d.callout("Club-level data is limited — treat splits as planning estimates",
              "The Acme dataset carries robust account totals (Costco $52M, Sam's $28M from the retailer "
              "master) but limited club-granular POS. Brand-by-pack club splits, the 36oz pack economics, "
              "and item-level club revenue in this review are modelled planning estimates for line-review "
              "discussion, not measured club-channel history. Any FY27 commitment should be conditioned on "
              "a club-specific data build.", "risk")
    d.recommendations([
        ("Lead the FY27 club line review with Crunchwell Mega Family Pack 36oz built for the club value equation.",
         "Club Channel Sales / Frank Calabrese", "FY27 line review"),
        ("Propose a ProteinPeak club variety pack to carry the +18% protein pocket into the channel.",
         "Sage Park", "FY27 line review"),
        ("Extend TrailGrove and RootDay multipacks; defend and grow the MorningOats Cup club position.",
         "Club Channel Sales", "FY27"),
        ("Commission a club-specific POS/data build before booking any FY27 club revenue plan.",
         "Insights / Finance", "H2 FY26"),
    ])
    return d.build()


# ============================================================ REPORT 39 =====
def r39_south_region():
    d = Doc("39-south-region-h1-2026-commercial-review.pdf",
            kicker="REGIONAL COMMERCIAL REVIEW · SOUTH",
            title="South Region — H1 FY2026 Commercial Review",
            subtitle="Louisiana recovery tracker · the −340 bps story, root cause, and the three-leg plan",
            owner="Marcus Boudreaux, Director Sales — South Region",
            period="H1 FY2026", short="South Region H1",
            doc_type="Regional commercial review", date_str="June 2026")

    d.cover_facts([
        ("Louisiana Crunchwell share", "6.4% → 3.0% (−340 bps, peak-to-trough)"),
        ("Primary driver", "Walmart Sept 2025 reset (~55%)"),
        ("Endcap deficit (Walmart LA)", "23 of 41 Supercenters: 3 Larksfield, 0 Acme"),
        ("Recovery leg 3", "LA retail media at 2.2× portfolio ROI"),
        ("Leading-indicator watch", "Birmingham 5.7→5.4 · Memphis 5.4→5.1"),
        ("Q2 FY26 signal", "LA Crunchwell 3.97→4.16 (value share, early stabilization)"),
    ])

    d.exec_summary(
        "Louisiana is the South Region's defining story and the single largest regional drag on Acme's "
        "enterprise number. Crunchwell's Louisiana share fell from ~6.4% to 3.0% — a −340 bps "
        "peak-to-trough collapse — driven predominantly by a Walmart shelf change rather than a demand "
        "shift. The root cause is now attributed across five hypotheses, dominated by the September 2025 "
        "Walmart modular reset. A three-leg recovery is funded and in-market: facing recovery, targeted "
        "trade, and a Louisiana retail-media injection running at 2.2× the portfolio ROI. Early Q2 signals "
        "show stabilization — LA Crunchwell value share ticked from 3.97% (Q1) to 4.16% (Q2 MTD) — but two "
        "leading-indicator DMAs, Birmingham and Memphis, are softening as Field & Honey spreads. This "
        "review sizes the decline, decomposes it, and tracks the recovery.",
        bullets=[
            "<b>Size:</b> −340 bps of Louisiana Crunchwell share (6.4% → 3.0%), the canonical Mass/Grocery "
            "peak-to-trough headline; the all-channel value cut is milder (~6.1 → 4.0) but same-direction.",
            "<b>Cause:</b> five hypotheses — Walmart reset ~55%, Larksfield promo ~20%, Hurricane Tonya "
            "supply ~12%, Walmart private label ~8%, Hispanic-shopper shift ~5%.",
            "<b>Recovery:</b> three legs — facing recovery, targeted trade, and LA retail media at 2.2× ROI "
            "— with Walmart endcap parity as the highest-leverage single action.",
            "<b>Watch:</b> Birmingham (5.7→5.4) and Memphis (5.4→5.1) are the early-warning DMAs for "
            "Field & Honey spread beyond Louisiana.",
        ])

    # --- section 1: the decline, sized
    d.h1("1 · Louisiana — the decline, sized")
    d.kpis([
        ("LA Crunchwell share", "3.0%", "from 6.4% peak"),
        ("Decline", "−340 bps", "peak-to-trough"),
        ("Primary driver", "~55%", "Walmart Sept reset"),
        ("Q2 signal", "4.16%", "value share, stabilizing"),
    ])
    d.body(
        "The canonical Louisiana headline is a −340 bps fall in Crunchwell share, from ~6.4% at the Q4 "
        "FY24 Mass/Grocery peak to 3.0% in Q1 FY26 (per the geographies master and the LA decline "
        "analysis). The value-weighted, all-channel syndicated cut is milder — Crunchwell LA value share "
        "moved from ~6.1% to a 3.97% Q1 trough — but points the same direction. Both cuts now show early "
        "Q2 stabilization as the recovery lands.")

    la = df("""SELECT SUBSTR(Week,1,4)||'-Q'||CAST(CEIL(CAST(SUBSTR(Week,7,2) AS INT)/13.0) AS INT) q,
                 ROUND(AVG(Crunchwell_Value_Share)*100,2) cw, ROUND(AVG(Acme_Value_Share)*100,2) acme,
                 ROUND(AVG(Larksfield_Value_Share)*100,2) lf
               FROM syndicated_weekly WHERE Category='RTE Cereal' AND DMA='LA-DMA'
                 AND Week>='2025-W01' GROUP BY 1 ORDER BY 1""")
    la_ch = chart_line("r39_la_share.png", list(la.q),
                       {"Crunchwell (LA)": [round(x, 2) for x in la.cw],
                        "Acme all-brand (LA)": [round(x, 2) for x in la.acme],
                        "Larksfield (LA)": [round(x, 2) for x in la.lf]},
                       title="Louisiana DMA value share (%) — the Crunchwell decline & early recovery",
                       pct=True, h=2.9)
    d.image(la_ch, "Crunchwell LA value share troughed at 3.97% in Q1 FY26 and ticked up to 4.16% in Q2 MTD "
                   "while Larksfield held ~14%. Source: syndicated_weekly (LA-DMA, RTE Cereal).")

    # --- section 2: root cause decomposition
    d.h1("2 · Root-cause decomposition — five hypotheses")
    d.body(
        "The −340 bps decline decomposes across five hypotheses. The dominant driver is the September 2025 "
        "Walmart modular reset that cut Crunchwell Mega from 8 to 6 facings and progressively removed Acme "
        "endcaps; the remainder is Larksfield promo intensity at Rouses, the Hurricane Tonya supply "
        "collapse, Walmart private-label pressure, and a Hispanic-shopper mix shift. The shares below are "
        "the working attribution estimates from the LA diagnostic.")
    d.table(
        ["Hypothesis", "Est. share of decline", "Evidence"],
        [["H1 — Walmart Sept 2025 reset", "~55%", "Crunchwell Mega 8→6 facings; endcap loss (audit)"],
         ["H2 — Larksfield promo intensity", "~20%", "Field & Honey endcaps at Rouses; 21% depth"],
         ["H3 — Hurricane Tonya supply", "~12%", "Houston/Thibodaux DC fill dropped to ~52%"],
         ["H4 — Walmart private label", "~8%", "Great Value picking up secondary displays"],
         ["H5 — Hispanic-shopper mix shift", "~5%", "LA Hispanic pop +9%; Crunchwell under-indexes"]],
        widths=[0.34, 0.20, 0.46])
    d.source("LA diagnostic (five-hypothesis attribution); walmart_endcap_audit_la; "
             "promo_events_louisiana; shipments (Hurricane Tonya).")

    wf = chart_waterfall("r39_hyp.png",
                         ["H1 Walmart\nreset", "H2 Larksfield\npromo", "H3 Tonya\nsupply",
                          "H4 Walmart\nPL", "H5 Hispanic\nshift"],
                         [-1.87, -0.68, -0.41, -0.27, -0.17],
                         title="Attributing the −340 bps Crunchwell LA decline (bps, illustrative split)",
                         unit="")
    d.image(wf, "The −340 bps decline apportioned to the five hypotheses (bps; shares per the LA diagnostic). "
                "Walmart reset dominates. Source: LA diagnostic attribution.")

    # --- section 3: the three-leg recovery + door-level evidence
    d.pagebreak()
    d.h1("3 · The three-leg recovery")
    d.body(
        "The recovery is scoped, funded, and in-market on three legs. Leg 1 (facings) is the joint Walmart "
        "ask carried in the FY27 JBP (Report 35): restore Crunchwell Mega to 8 facings and secure at least "
        "one Acme endcap per Louisiana Supercenter. Leg 2 (trade) is a targeted recovery-promo cadence to "
        "answer Larksfield's intensity. Leg 3 (retail media) is a Louisiana injection running at 2.2× the "
        "portfolio ROI — the most efficient marginal dollar available to the region.")
    d.h2("3.1 · Door-level evidence — Walmart, Rouses, H-E-B")
    ec = seed_csv("walmart_endcap_audit_la.csv")
    ecm = ec[(ec.audit_date == "2026-05-11") & (ec.supercenter_format == "Supercenter")]
    three_lf = int(((ecm.larksfield_endcap_count == 3) & (ecm.acme_endcap_count == 0)).sum())
    ro = seed_csv("rouses_oos_by_door.csv")
    heb = seed_csv("heb_cinnamon_twist_delist_risk.csv")
    d.table(
        ["Door-level signal (H1 FY26)", "Reading", "Source"],
        [["Walmart LA endcaps", f"{three_lf} of {len(ecm)} Supercenters: 3 Larksfield, 0 Acme", "walmart_endcap_audit_la"],
         ["Rouses on-shelf availability", f"avg {ro.osa_pct.mean():.0f}% OSA across {len(ro)} doors (Crunchwell Mega)", "rouses_oos_by_door"],
         ["Rouses OOS", f"avg {ro.oos_days_q1_2026.mean():.0f} OOS-days in Q1; all {len(ro)} doors have Larksfield endcaps", "rouses_oos_by_door"],
         ["H-E-B Cinnamon Twist", f"delist-risk {heb.delist_risk_score_0to1.mean():.2f} avg; Sept 2026 review", "heb_cinnamon_twist_delist_risk"]],
        widths=[0.30, 0.48, 0.22])
    d.source("walmart_endcap_audit_la; rouses_oos_by_door; heb_cinnamon_twist_delist_risk.")
    d.callout("Recovery leg with the highest leverage: the Walmart endcap",
              "Louisiana share is lost fastest at the Walmart endcap (0 Acme vs 3 Larksfield in 23 of 41 "
              "Supercenters) and at Rouses shelf (avg ~74% OSA, all doors carrying Larksfield endcaps). "
              "Facing recovery at the September 2026 reset is the single action that most moves the "
              "recovery. See the Walmart FY27 JBP, Report 35.", "action")

    # --- section 4: leading indicators + projection
    d.h1("4 · Leading-indicator DMA watch & recovery projection")
    d.body(
        "Louisiana is stabilizing, but the same Field & Honey playbook is beginning to appear in two "
        "adjacent DMAs. Birmingham Crunchwell share slipped from 5.7% to 5.4% and Memphis from 5.4% to "
        "5.1% (geographies master, FY25 → Q1 FY26) — early spread signals, not yet a decline, but the "
        "region's watch-items. Containing Field & Honey in Louisiana is also how the region prevents a "
        "second front opening.")
    li = chart_grouped("r39_leading.png", ["Birmingham", "Memphis"],
                       {"FY25": [5.7, 5.4], "Q1 FY26": [5.4, 5.1]},
                       title="Leading-indicator DMAs — Crunchwell share (%), early F&H spread",
                       pct=True)
    d.image(li, "Both DMAs down ~0.3 points — early-warning, not yet decline. Source: seed_geographies.")
    d.body(
        "Recovery projection (planning estimate): with the three legs landing at the September 2026 reset, "
        "the region targets restoring Louisiana Crunchwell share toward the mid-4s through H2 FY26, "
        "building on the Q2 uptick to 4.16% value share. This is a plan contingent on facing recovery, "
        "not a booked forecast.")
    d.callout("Regional risk — the second front",
              "Field & Honey's 14g-protein line extension (12 May 2026) and its early spread into "
              "Birmingham/Memphis mean the Louisiana recovery must hold while a protein-and-adjacency "
              "threat builds. If the September reset does not restore facings, Louisiana does not recover "
              "and the leading-indicator DMAs tip from watch into decline. See Reports 18, 24, 35.", "risk")
    d.recommendations([
        ("Land recovery Leg 1 at the Sept 2026 Walmart reset: Crunchwell Mega 6→8 facings, ≥1 Acme LA endcap.",
         "Marcus Boudreaux", "Sept 2026 reset"),
        ("Run the Leg 2 targeted recovery-trade cadence to answer Larksfield promo intensity at Rouses.",
         "Marcus Boudreaux", "H1–H2 FY26"),
        ("Sustain the Leg 3 Louisiana retail-media injection at 2.2× ROI through the recovery window.",
         "Tasha Brooks", "H2 FY26"),
        ("Stand up active monitoring of Birmingham and Memphis for Field & Honey spread.",
         "Jordan Hsu / Insights", "Ongoing"),
    ])
    return d.build()


# ============================================================ REPORT 40 =====
def r40_cfo_reforecast():
    d = Doc("40-q2-2026-financial-performance-h2-reforecast.pdf",
            kicker="FINANCIAL PERFORMANCE & REFORECAST",
            title="Q2 FY2026 Financial Performance & H2 Reforecast",
            subtitle="CFO read · plan-vs-actual trajectory, spend efficiency, the EBITDA bridge to 16%",
            owner="CFO office; Finance",
            period="Q2 FY2026 · H2 reforecast", short="CFO Q2 + Reforecast",
            doc_type="CFO financial performance read", date_str="June 2026")

    # live monthly plan/actual
    mo = df("""SELECT Period, ROUND(SUM(Plan_Revenue_USD)/1e6,1) plan, ROUND(SUM(Actual_Revenue_USD)/1e6,1) act,
                 ROUND((SUM(Actual_Revenue_USD)-SUM(Plan_Revenue_USD))/SUM(Plan_Revenue_USD)*100,1) var
               FROM plan_vs_actual WHERE Period>='2025-10' AND Period<='2026-05' GROUP BY 1 ORDER BY 1""")
    q1 = df("""SELECT ROUND(SUM(Plan_Revenue_USD)/1e6,1) p, ROUND(SUM(Actual_Revenue_USD)/1e6,1) a
               FROM plan_vs_actual WHERE Period IN ('2026-01','2026-02','2026-03')""").iloc[0]
    var_q1 = (q1.a - q1.p) / q1.p * 100

    d.cover_facts([
        ("Q1 FY26 net revenue", f"{money(q1.a)} actual vs {money(q1.p)} plan · {var_q1:+.1f}%"),
        ("Trajectory", "−5.2% (Q1) improving to −3.4% (May)"),
        ("Retail-media efficiency", "$0.65 incremental per $1 (Amazon 0.40 drag)"),
        ("Trade", "~$146M FY25 · 0.52 Q1 incrementality index"),
        ("EBITDA margin", "14.2% today → 16% target FY28"),
        ("H2 ask", "Reallocate ~$700K retail media; trade rationalization"),
    ])

    d.exec_summary(
        f"Acme's revenue gap to plan is narrowing. The company ran {var_q1:.1f}% behind plan in Q1 FY26 "
        f"({money(q1.a)} vs {money(q1.p)}), improved to −3.5% in April and −3.4% in May as the ProteinPeak "
        "launch pipe filled. The miss is concentrated, not broad: Crunchwell runs a steady −6% to plan and "
        "ProteinPeak has closed from −25% pre-launch to −6% post-launch. The CFO watch-item is spend "
        "efficiency — retail media returns $0.65 incremental per $1 with Amazon Ads (0.40) the drag, and "
        "trade sits at a 0.52 incrementality index on roughly $146M of FY25 spend. The path to the 16% "
        "EBITDA target (from 14.2% today) runs through mix, RGM, trade efficiency, and SG&A. This read "
        "sets the H2 reforecast and proposes two reallocations: ~$700K of retail media out of Amazon, and "
        "trade rationalization toward higher-incrementality mechanics.",
        bullets=[
            f"<b>Trajectory:</b> monthly variance improved from −5.2% (Jan) to −3.4% (May) — the launch is "
            "closing the gap on schedule.",
            "<b>Gap composition:</b> Crunchwell −6% (steady) and ProteinPeak (−25% → −6% post-launch) are "
            "the two brands carrying the miss; four brands are within ~1.6% of plan.",
            "<b>Efficiency:</b> retail media $0.65/$1 (Amazon 0.40 drag); trade 0.52 incrementality — both "
            "are the levers for the H2 reallocation.",
            "<b>EBITDA:</b> 14.2% today to a 16% FY28 target via a mix / RGM / trade-efficiency / SG&A "
            "bridge (planning targets).",
        ])

    # --- section 1: plan vs actual trajectory
    d.h1("1 · Plan-vs-actual — the trajectory is improving")
    d.kpis([
        ("Q1 variance", f"{var_q1:+.1f}%", f"{money(q1.a)} vs {money(q1.p)}"),
        ("May variance", f"{mo[mo.Period=='2026-05'].iloc[0]['var']:+.1f}%", "improving"),
        ("Monthly plan", "$63.7M", "FY26 run-rate"),
        ("Improvement", "+1.8 pts", "Jan → May"),
    ])
    d.body(
        "The company's monthly variance to plan improved through the first five months of FY26, from −5.2% "
        "in January to −3.4% in May, as the April 20 ProteinPeak launch began contributing revenue against "
        "a $63.7M monthly plan. The trajectory — not the absolute Q1 miss — is the number that matters for "
        "the H2 reforecast: the gap is closing on schedule as the innovation pipe fills.")
    mo_ch = chart_line("r40_pva.png",
                       [p.replace("2025-", "'25-").replace("2026-", "'26-") for p in mo.Period],
                       {"Plan ($M/mo)": [round(x, 1) for x in mo.plan],
                        "Actual ($M/mo)": [round(x, 1) for x in mo.act]},
                       title="Monthly net revenue — plan vs actual ($M), Oct 2025 → May 2026",
                       h=2.9)
    d.image(mo_ch, "The actual line steps up in April–May as the ProteinPeak launch contributes. "
                   "Source: plan_vs_actual (company-level, monthly).")
    d.source("plan_vs_actual (SAP/Acme ERP shape), 2025-10 → 2026-05.")

    # --- section 2: brand contribution to the gap
    d.h1("2 · Brand contribution to the gap")
    bd = df("""SELECT Brand,
                 ROUND(AVG(CASE WHEN Period IN ('2026-01','2026-02','2026-03')
                    THEN (Actual_Revenue_USD-Plan_Revenue_USD)/Plan_Revenue_USD*100 END),1) q1var,
                 ROUND(AVG(CASE WHEN Period IN ('2026-04','2026-05')
                    THEN (Actual_Revenue_USD-Plan_Revenue_USD)/Plan_Revenue_USD*100 END),1) aprmay
               FROM plan_vs_actual WHERE Period>='2026-01' GROUP BY 1
               ORDER BY q1var""")
    brows = [[r.Brand, f"{r.q1var:+.1f}%", f"{r.aprmay:+.1f}%",
              "Improving (launch)" if r.Brand == "ProteinPeak" else
              ("The steady drag" if r.Brand == "Crunchwell" else "On track")]
             for r in bd.itertuples()]
    d.table(["Brand", "Q1 var", "Apr–May var", "Read"], brows,
            widths=[0.28, 0.18, 0.18, 0.36])
    d.body(
        "The gap has two owners. Crunchwell runs a steady −5.7% to −6.0% every month — the structural drag, "
        "tied to the Louisiana decline and category headwinds. ProteinPeak was −25% in Q1 by design (a "
        "pre-launch pipeline draw-down) and has closed to −6% post-launch. The other four brands run within "
        "~1.6% of plan. The reforecast therefore hinges on two questions: does ProteinPeak keep closing, "
        "and does the Louisiana recovery stem the Crunchwell drag?")
    d.source("plan_vs_actual (brand-level, Q1 and Apr–May FY26).")

    # --- section 3: spend efficiency
    d.pagebreak()
    d.h1("3 · Spend efficiency — the CFO's core question")
    d.body(
        "The working question is simple: is the marginal spend dollar working? On retail media, the "
        "blended Q1 answer is $0.65 incremental per $1 — carried by Walmart Connect (1.20) and Kroger "
        "Precision (0.77) and dragged by Amazon Ads (0.40). On trade, the Q1 incrementality index is 0.52 "
        "across 43 events and $11.6M of spend, against roughly $146M of FY25 trade — a heavy investment "
        "with a modest marginal return, concentrated in Crunchwell's ~25.6%-of-gross trade rate.")
    rm = seed_csv("retail_media_spend_q1_2026.csv")
    rmg = rm.groupby("platform").agg(spend=("spend_kusd", "sum"),
                                     inc=("incremental_revenue_kusd", "sum"),
                                     ratio=("modeled_incrementality_ratio", "mean")).reset_index()
    rmg = rmg.sort_values("ratio", ascending=False)
    eff_ch = chart_bar("r40_eff.png",
                       [p.replace(" Marketing", "").replace(" Ads", "").replace(" Connect", "\nConnect").replace(" Precision", "\nPrecision") for p in rmg.platform],
                       [round(x, 2) for x in rmg.ratio],
                       title="Retail-media incrementality by lever (incremental per $1 spent)",
                       colors_list=[palette["teal"] if r >= 1 else (palette["gold"] if r >= 0.75 else palette["rust"]) for r in rmg.ratio],
                       h=2.5)
    d.image(eff_ch, "Only Walmart Connect clears break-even; Amazon Ads is the drag. Blended $0.65/$1. "
                    "Source: retail_media_spend_q1_2026.")
    d.table(
        ["Spend lever (Q1 FY26)", "Efficiency", "Read"],
        [["Retail media — blended", "$0.65 / $1", "$2.73M incr. on $4.2M"],
         ["Walmart Connect", "1.20", "scale it"],
         ["Kroger Precision", "0.77", "hold / optimize"],
         ["Target Roundel", "0.50", "rebuild around windows"],
         ["Amazon Ads", "0.40", "the drag — reallocate"],
         ["Trade promotion", "0.52 index", "43 events, $11.6M; rationalize depth"]],
        widths=[0.40, 0.22, 0.38])
    d.source("retail_media_spend_q1_2026; trade_promo_events_q1_2026; trade_spend_fy25 (~$146M total).")

    # --- section 4: EBITDA bridge
    d.h1("4 · The EBITDA bridge — 14.2% to 16%")
    d.body(
        "Acme runs a 14.2% EBITDA margin today against a 16% target by FY28. The bridge is built from four "
        "planning levers: favorable mix (protein and premium growing faster than kids-sweet decline), "
        "revenue-growth management, trade efficiency (lifting the 0.52 incrementality index), and SG&A "
        "discipline. The bridge below is a planning target, not a booked forecast — each leg is a "
        "commitment to be earned through FY27–FY28.")
    eb = chart_waterfall("r40_ebitda.png",
                         ["FY26\n14.2%", "Mix", "RGM", "Trade\nefficiency", "SG&A", "FY28\n16.0%"],
                         [14.2, 0.6, 0.5, 0.4, 0.3, 0.0],
                         title="EBITDA-margin bridge, 14.2% → 16.0% (pts, planning target)", unit="")
    d.image(eb, "The 1.8-point EBITDA build to the FY28 target, apportioned across four levers "
                "(planning estimate). Source: FACTS (EBITDA 14.2% today, 16% FY28 target).")
    d.callout("The bridge is a plan, not a forecast",
              "The 14.2% → 16% build and its four-lever split are planning targets for FY27–FY28, not "
              "booked results. Trade efficiency alone (0.52 index on ~$146M) is the largest single "
              "opportunity; see the RGM read, Report 17, and the H2 plan, Report 16.", "info")

    # --- section 5: H2 reforecast + reallocations
    d.h1("5 · H2 reforecast & proposed reallocations")
    d.body(
        "The H2 reforecast lands FY26 on the improving trajectory: hold the ProteinPeak build, stem the "
        "Crunchwell drag via the Louisiana recovery, and reallocate spend toward the levers that work. Two "
        "reallocations are proposed for H2 (planning estimates, pending the Week-13 launch read).")
    d.table(
        ["Proposed H2 reallocation", "Amount / action", "Rationale"],
        [["Retail media — out of Amazon Ads", "~$700K", "0.40 drag → Walmart Connect (1.20), Kroger, LA (2.2×)"],
         ["Trade rationalization", "Depth → mechanics", "Lift the 0.52 incrementality index; Crunchwell depth"],
         ["Louisiana recovery funding", "Sustain Leg 3", "LA retail media at 2.2× portfolio ROI"],
         ["Hold ProteinPeak build", "No cut", "Launch closing −25% → −6%; the FY26 growth engine"]],
        widths=[0.34, 0.24, 0.42])
    d.source("retail_media_spend_q1_2026; trade_promo_events_q1_2026; plan_vs_actual. Reallocations are planning estimates.")
    d.callout("Reforecast risk — the gap closes on two contingencies",
              "The improving trajectory assumes ProteinPeak keeps closing (Walmart-pilot at 78% of plan is "
              "the risk) and the Louisiana recovery stems the Crunchwell drag. If either slips, the H2 "
              "reforecast tightens. Spend efficiency must improve before further H2 budget is committed. "
              "See the H2 plan (Report 16), the RGM read (Report 17), and Report 27.", "risk")
    d.recommendations([
        ("Reallocate ~$700K H2 retail media out of Amazon Ads into Walmart Connect, Kroger, and the LA recovery.",
         "Tasha Brooks / Finance", "H2 FY26"),
        ("Rationalize Crunchwell trade depth toward higher-incrementality mechanics to lift the 0.52 index.",
         "RGM / Finance", "H2 FY26"),
        ("Hold the ProteinPeak FY26 build; reaffirm contingent on the Week-13 launch read.",
         "Finance / Sage Park", "Week-13 read"),
        ("Set the H2 reforecast on the improving −3.4% trajectory; gate further budget on spend efficiency.",
         "CFO office", "H2 planning"),
    ])
    return d.build()


# ------------------------------------------------------------------- main ---
if __name__ == "__main__":
    for fn in (r35_walmart_jbp, r36_kroger_jbp, r37_target_jbp_bts,
               r38_club_line_review, r39_south_region, r40_cfo_reforecast):
        print(fn())
