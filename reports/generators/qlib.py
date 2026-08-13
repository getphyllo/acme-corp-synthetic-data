"""Grounded query helpers shared by the PPTX decks (41-60) and DOCX docs (61-80).

Every function here is a thin, named wrapper over acme.duckdb / seeds so the same
number is computed the same way in a deck and in a memo. Nothing is hardcoded
except the labels; the values come from the data product.

Import from a builder module as:
    from qlib import pva_brand, pva_total, share_quarter, ...
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from lib import df, seed_csv

Q1 = ["2026-01", "2026-02", "2026-03"]
Q2 = ["2026-04", "2026-05"]              # Q2 FY26 actuals stop at May
H1 = Q1 + Q2
FY25 = [f"2025-{m:02d}" for m in range(1, 13)]

# ---------------------------------------------------------- canonical plan ---
# The forward plan is already fixed by Reports 14 (FY27 AOP) and 15 (FY27-29 LRP).
# Anything in reports 41-80 that quotes a forward total must read it from here so
# the PDF, the deck and the memo cannot drift apart. All values are TARGETS.
PLAN = {
    "fy25_rev": 812.0,          # FY25 actual net revenue (measured)
    "fy26_rev": 764.0,          # FY26 basis = $63.7M/mo plan run-rate
    "fy27_rev": 880.0, "fy28_rev": 950.0, "fy29_rev": 1020.0,
    "fy25_ebitda": 14.2, "fy26_ebitda": 14.2,
    "fy27_ebitda": 15.0, "fy28_ebitda": 16.0, "fy29_ebitda": 16.0,
    "trade_envelope": 150.0,    # FY27 trade envelope, rationalised
    "ap_envelope": 95.0,        # FY27 A&P envelope
    # FY27 bottom-up brand targets (Report 14). Sum reconciles to ~$880M with
    # non-brand / adjacency revenue.
    "fy27_brand": {"Crunchwell": 318, "ProteinPeak": 100, "TrailGrove": 162,
                   "MorningOats": 92, "HoneyNest": 92, "RootDay": 74},
}


def brand_fy25():
    """FY25 revenue by brand from seeds/skus.csv — the base every build starts from."""
    s = seed_csv("skus.csv").groupby("brand")["fy25_revenue_musd"].sum()
    return {b: float(v) for b, v in s.items()}


def fy27_build():
    """Derived FY25 -> FY27 bridge: (brand deltas, adjacency/mix residual).

    The residual is computed, never asserted, so the bridge always ties to
    PLAN['fy27_rev'].
    """
    f25, f27 = brand_fy25(), PLAN["fy27_brand"]
    deltas = {b: f27[b] - f25.get(b, 0.0) for b in f27}
    residual = PLAN["fy27_rev"] - PLAN["fy25_rev"] - sum(deltas.values())
    return deltas, residual


def _in(periods):
    return ",".join(f"'{p}'" for p in periods)


def m0(x):
    """'$880M' — whole-million money, for plan totals."""
    return f"${x:,.0f}M"


def musd(v, dp=1):
    """'$28.0M' — or an em dash where the source has no figure (e.g. discontinuations)."""
    try:
        if v is None or (isinstance(v, str) and not v.strip()) or pd.isna(float(v)):
            return "—"
        return f"${float(v):,.{dp}f}M"
    except (TypeError, ValueError):
        return "—"


def dash(v):
    """Source values that are legitimately absent ('N/A', NaN) render as an em dash."""
    s = "" if v is None else str(v).strip()
    return "—" if s.lower() in ("", "n/a", "na", "nan", "none") else s


def roll_up(d, label_col, n, sum_cols=(), mean_cols=(), other="All other"):
    """Keep the top n rows and collapse the tail into one labelled row.

    Slides hold about a dozen table rows; long tails get rolled up rather than
    truncated so the totals still reconcile.
    """
    if len(d) <= n:
        return d
    head, tail = d.head(n).copy(), d.tail(len(d) - n)
    row = {label_col: f"{other} ({len(tail)})"}
    for c in sum_cols:
        row[c] = tail[c].sum()
    for c in mean_cols:
        row[c] = tail[c].mean()
    for c in d.columns:
        row.setdefault(c, "")
    return pd.concat([head, pd.DataFrame([row])[d.columns]], ignore_index=True)


# ------------------------------------------------------------ plan vs actual --
def pva_brand(periods=Q1):
    return df(f"""SELECT Brand,
                    ROUND(SUM(Plan_Revenue_USD)/1e6,1)   AS plan,
                    ROUND(SUM(Actual_Revenue_USD)/1e6,1) AS act,
                    ROUND((SUM(Actual_Revenue_USD)-SUM(Plan_Revenue_USD))
                          /SUM(Plan_Revenue_USD)*100,1)  AS var
                  FROM plan_vs_actual WHERE Period IN ({_in(periods)})
                  GROUP BY 1 ORDER BY plan DESC""")


def pva_total(periods=Q1):
    r = df(f"""SELECT SUM(Plan_Revenue_USD)/1e6 p, SUM(Actual_Revenue_USD)/1e6 a
               FROM plan_vs_actual WHERE Period IN ({_in(periods)})""").iloc[0]
    p, a = float(r.p), float(r.a)
    return p, a, (a - p) / p * 100


def pva_month(periods=H1):
    return df(f"""SELECT Period,
                    ROUND(SUM(Plan_Revenue_USD)/1e6,1)   AS plan,
                    ROUND(SUM(Actual_Revenue_USD)/1e6,1) AS act,
                    ROUND((SUM(Actual_Revenue_USD)-SUM(Plan_Revenue_USD))
                          /SUM(Plan_Revenue_USD)*100,1)  AS var
                  FROM plan_vs_actual WHERE Period IN ({_in(periods)})
                  GROUP BY 1 ORDER BY 1""")


def pva_retailer(periods=Q1, top=8):
    return df(f"""SELECT Retailer,
                    ROUND(SUM(Plan_Revenue_USD)/1e6,1)   AS plan,
                    ROUND(SUM(Actual_Revenue_USD)/1e6,1) AS act,
                    ROUND((SUM(Actual_Revenue_USD)-SUM(Plan_Revenue_USD))
                          /SUM(Plan_Revenue_USD)*100,1)  AS var
                  FROM plan_vs_actual WHERE Period IN ({_in(periods)})
                  GROUP BY 1 ORDER BY plan DESC LIMIT {top}""")


def pva_brand_month(brand, periods=H1):
    return df(f"""SELECT Period,
                    ROUND(SUM(Plan_Revenue_USD)/1e6,2)   AS plan,
                    ROUND(SUM(Actual_Revenue_USD)/1e6,2) AS act,
                    ROUND((SUM(Actual_Revenue_USD)-SUM(Plan_Revenue_USD))
                          /SUM(Plan_Revenue_USD)*100,1)  AS var
                  FROM plan_vs_actual
                  WHERE Brand='{brand}' AND Period IN ({_in(periods)})
                  GROUP BY 1 ORDER BY 1""")


# -------------------------------------------------------------------- share ---
_QEXPR = ("SUBSTR(Week,1,4)||'-Q'||CAST(CEIL(CAST(SUBSTR(Week,7,2) AS INT)/13.0) AS INT)")


def share_quarter(la=False, since="2025-W01"):
    """Quarterly average value share, RTE Cereal. la=True -> Louisiana DMA only."""
    where = "DMA='LA-DMA'" if la else "DMA<>'LA-DMA'"
    return df(f"""SELECT {_QEXPR} AS q,
                    ROUND(AVG(Acme_Value_Share)*100,2)        AS acme,
                    ROUND(AVG(Crunchwell_Value_Share)*100,2)  AS cw,
                    ROUND(AVG(Larksfield_Value_Share)*100,2)  AS lf,
                    ROUND(AVG(PL_Value_Share)*100,2)          AS pl
                  FROM syndicated_weekly
                  WHERE Category='RTE Cereal' AND {where} AND Week>='{since}'
                  GROUP BY 1 ORDER BY 1""")


def share_channel(la=True, since="2025-W27"):
    where = "DMA='LA-DMA'" if la else "DMA<>'LA-DMA'"
    return df(f"""SELECT Channel,
                    ROUND(AVG(CASE WHEN Week<'2026-W01' THEN Crunchwell_Value_Share END)*100,2) AS before,
                    ROUND(AVG(CASE WHEN Week>='2026-W01' THEN Crunchwell_Value_Share END)*100,2) AS after
                  FROM syndicated_weekly
                  WHERE Category='RTE Cereal' AND {where} AND Week>='{since}'
                  GROUP BY 1 ORDER BY 1""")


def distribution(la=True, since="2025-W27"):
    where = "DMA='LA-DMA'" if la else "DMA<>'LA-DMA'"
    return df(f"""SELECT {_QEXPR} AS q,
                    ROUND(AVG(ACV_Distribution_Pct),1) AS acv,
                    ROUND(AVG(TDP),0)                  AS tdp,
                    ROUND(AVG(Avg_Facings),2)          AS facings,
                    ROUND(AVG(Promo_Share)*100,1)      AS promo
                  FROM syndicated_weekly
                  WHERE Category='RTE Cereal' AND {where} AND Week>='{since}'
                  GROUP BY 1 ORDER BY 1""")


# ----------------------------------------------------------------- category ---
def catgrowth(period="FY2025"):
    return df(f"""SELECT subcategory, category, market_size_usd_mm AS size,
                    yoy_growth_pct AS growth, acme_share_pct AS share
                  FROM seed_category_market_size
                  WHERE period='{period}' AND geography='US National'
                  ORDER BY growth DESC""")


def cat_row(period, subcat, geo="US National"):
    r = df(f"""SELECT market_size_usd_mm AS size, yoy_growth_pct AS growth,
                 acme_share_pct AS acme_share
               FROM seed_category_market_size
               WHERE period='{period}' AND subcategory='{subcat}' AND geography='{geo}'
               LIMIT 1""")
    return None if r.empty else r.iloc[0]


# ------------------------------------------------------------- retail media ---
def retail_media():
    rm = seed_csv("retail_media_spend_q1_2026.csv")
    g = (rm.groupby("platform")
           .agg(spend=("spend_kusd", "sum"), inc=("incremental_revenue_kusd", "sum"),
                cann=("cannibalized_base_kusd", "sum"),
                ratio=("modeled_incrementality_ratio", "mean"),
                rroas=("platform_reported_roas", "mean"))
           .reset_index().sort_values("spend", ascending=False))
    g["spend_m"] = g.spend / 1000
    g["inc_m"] = g.inc / 1000
    return g


def retail_media_brand():
    rm = seed_csv("retail_media_spend_q1_2026.csv")
    return (rm.groupby("brand")
              .agg(spend=("spend_kusd", "sum"), inc=("incremental_revenue_kusd", "sum"),
                   ratio=("modeled_incrementality_ratio", "mean"))
              .reset_index().sort_values("spend", ascending=False))


# ---------------------------------------------------------------- trade -------
def trade_brand():
    t = seed_csv("trade_spend_fy25.csv")
    # promo_count_fy25 carries "Always-on" for e-comm lines -> numeric only
    t["promo_count_fy25"] = pd.to_numeric(t["promo_count_fy25"], errors="coerce").fillna(0)
    g = (t.groupby("brand")
          .agg(spend=("trade_spend_kusd", "sum"), depth=("trade_depth_pct", "mean"),
               incr=("incrementality_index", "mean"), events=("promo_count_fy25", "sum"))
          .reset_index().sort_values("spend", ascending=False))
    g["spend_m"] = g.spend / 1000
    return g


def trade_events(by="retailer"):
    e = seed_csv("trade_promo_events_q1_2026.csv")
    g = (e.groupby(by)
          .agg(events=("event_id", "count"), spend=("spend_kusd", "sum"),
               inc=("incremental_revenue_kusd", "sum"), lift=("modeled_lift_pct", "mean"),
               idx=("modeled_incrementality_index", "mean"))
          .reset_index().sort_values("spend", ascending=False))
    return g


def trade_events_raw():
    return seed_csv("trade_promo_events_q1_2026.csv")


# ------------------------------------------------------------------ media -----
def mkt_spend(brand=None, periods=None):
    w = []
    if brand:
        w.append(f"brand='{brand}'")
    if periods:
        w.append(f"period IN ({_in(periods)})")
    where = ("WHERE " + " AND ".join(w)) if w else ""
    return df(f"""SELECT channel, ROUND(SUM(spend_kusd)/1000,2) AS spend_m,
                    ROUND(SUM(TRY_CAST(impressions_mln AS DOUBLE)),1) AS imps
                  FROM seed_marketing_spend {where}
                  GROUP BY 1 ORDER BY spend_m DESC""")


def mkt_by_period():
    return df("""SELECT period, ROUND(SUM(spend_kusd)/1000,1) AS spend_m
                 FROM seed_marketing_spend GROUP BY 1 ORDER BY 1""")


def mkt_by_brand():
    return df("""SELECT brand, ROUND(SUM(spend_kusd)/1000,2) AS spend_m
                 FROM seed_marketing_spend GROUP BY 1 ORDER BY spend_m DESC""")


# ----------------------------------------------------------------- equity -----
def equity(brand="Crunchwell", dma="US-NAT"):
    """Wave x Attribute top-two-box matrix."""
    d = df(f"""SELECT Wave, Attribute, ROUND(AVG(Top_Two_Box_Pct),1) AS ttb
               FROM brand_equity_quarterly
               WHERE Brand='{brand}' AND DMA='{dma}'
               GROUP BY 1,2 ORDER BY 1""")
    return d.pivot(index="Wave", columns="Attribute", values="ttb")


def equity_delta(brand="Crunchwell", dma="US-NAT"):
    p = equity(brand, dma)
    first, last = p.index[0], p.index[-1]
    return [(a, float(p.loc[first, a]), float(p.loc[last, a]),
             float(p.loc[last, a]) - float(p.loc[first, a]))
            for a in p.columns]


def nps():
    return df("""SELECT wave, ROUND(AVG(nps_0to10),2) AS nps,
                   ROUND(AVG(aided_aw_crunchwell)*100,1) AS aided,
                   ROUND(AVG(taste),2) AS taste,
                   ROUND(AVG(price_sensitivity_1to5),2) AS price_sens
                 FROM brand_health GROUP BY 1 ORDER BY 1""")


# ------------------------------------------------------------ supply chain ----
def fill_month(since="2025-09-01"):
    return df(f"""SELECT SUBSTR(Week_Start,1,7) AS mo,
                    ROUND(AVG(Fill_Rate_Pct)*100,1) AS fill,
                    ROUND(AVG(On_Time_Pct)*100,1)   AS otif
                  FROM shipments WHERE Week_Start>='{since}'
                  GROUP BY 1 ORDER BY 1""")


def cut_reasons(since="2025-10-01"):
    # uncut lines carry the literal string 'None' in the parquet, not SQL NULL
    return df(f"""SELECT CASE WHEN Cut_Reason IS NULL OR Cut_Reason='None'
                              THEN 'No cut' ELSE Cut_Reason END AS reason,
                    ROUND(SUM(Ordered_Units-Shipped_Units)/1000.0,1) AS cut_k,
                    ROUND(AVG(Fill_Rate_Pct)*100,1) AS fill,
                    COUNT(*) AS lines
                  FROM shipments WHERE Week_Start>='{since}'
                  GROUP BY 1 ORDER BY cut_k DESC""")


def fill_dc(since="2026-01-01", top=8):
    return df(f"""SELECT Retailer_DC AS dc,
                    ROUND(AVG(Fill_Rate_Pct)*100,1) AS fill,
                    ROUND(AVG(On_Time_Pct)*100,1)   AS otif,
                    COUNT(*) AS lines
                  FROM shipments WHERE Week_Start>='{since}'
                  GROUP BY 1 ORDER BY fill ASC LIMIT {top}""")


# ------------------------------------------------------------- innovation -----
def pipeline():
    p = seed_csv("innovation_pipeline.csv")
    p.columns = [c.strip() for c in p.columns]
    return p


def pipeline_stage():
    p = pipeline()
    g = (p.groupby("stage_gate")
          .agg(n=("concept_id", "count"),
               rev=("projected_revenue_year1_musd", "sum"),
               conf=("confidence_score_0to1", "mean"))
          .reset_index().sort_values("stage_gate", ascending=False))
    return g


def concept_test():
    """Chocolate Almond concept test as {(section, metric): (value, unit, scope)}."""
    d = df("SELECT section, metric, value, unit, scope, notes FROM seed_concept_test_chocolate_almond")
    return d


# ------------------------------------------------------------- geo / shopper --
def geos():
    return df("""SELECT geo_name, geo_type, region, priority_tier,
                   crunchwell_share_fy25_pct AS fy25,
                   crunchwell_share_q12026_pct AS q126,
                   ROUND((crunchwell_share_q12026_pct-crunchwell_share_fy25_pct)*100,0) AS bps,
                   acme_bdi AS bdi, population_mln AS pop
                 FROM seed_geographies ORDER BY bps ASC""")


def cohorts(dma="US-NAT"):
    d = df(f"""SELECT Cohort, Quarter, ROUND(AVG(HH_Penetration_Pct),1) AS pen,
                 ROUND(AVG(Purchases_Per_Buyer_Per_Qtr),2) AS ppb
               FROM kantar_worldpanel_cohort WHERE DMA='{dma}'
               GROUP BY 1,2 ORDER BY 2""")
    return d.pivot(index="Quarter", columns="Cohort", values="pen")


def sentiment(year="2026"):
    return df(f"""SELECT Brand_Mentioned AS brand, COUNT(*) AS mentions,
                    ROUND(AVG("Sentiment_-1to1"),2) AS sent,
                    ROUND(SUM(Reach)/1e6,1) AS reach_m
                  FROM social_mentions WHERE SUBSTR(Date,1,4)='{year}'
                  GROUP BY 1 HAVING COUNT(*)>50 ORDER BY mentions DESC""")


# ---------------------------------------------------------------- retail ------
def retailers(top=10):
    return df(f"""SELECT retailer_name AS retailer, channel, acv_weight_pct AS acv,
                    acme_revenue_fy25_musd AS rev, acme_nam AS nam, priority_tier AS tier
                  FROM seed_retailers ORDER BY rev DESC LIMIT {top}""")


def skus(brand=None):
    where = f"WHERE brand='{brand}'" if brand else ""
    return df(f"""SELECT sku_id, sku_name, brand, subcategory, pack_size_oz AS oz,
                    avg_shelf_price_usd AS price, fy25_revenue_musd AS rev,
                    national_acv_pct AS acv, status
                  FROM seed_skus {where} ORDER BY rev DESC""")


def comp_launches(since="2025-06-01"):
    return df(f"""SELECT brand, manufacturer, sku_new, product_description AS descr,
                    launch_date, claim_headline AS claim, pack_oz, launch_price_usd AS price,
                    acv_day_90_pct AS acv90, buzz_index_day30 AS buzz,
                    year1_velocity_units_per_store_per_wk AS velocity, status
                  FROM seed_competitor_launches WHERE launch_date>='{since}'
                  ORDER BY launch_date DESC""")


def macro(top=10):
    return df(f"""SELECT trend_topic AS topic, strength_0to1 AS strength, phase, direction,
                    affected_categories AS cats
                  FROM seed_macro_trends ORDER BY strength DESC LIMIT {top}""")


def pos(brand=None, dma=None):
    w = []
    if brand:
        w.append(f"brand='{brand}'")
    if dma:
        w.append(f"dma='{dma}'")
    where = ("WHERE " + " AND ".join(w)) if w else ""
    return df(f"""SELECT period, brand, dma, channel,
                    ROUND(gross_revenue_kusd/1000,2) AS gross_m,
                    ROUND(trade_spend_kusd/1000,2)   AS trade_m,
                    ROUND(net_revenue_kusd/1000,2)   AS net_m,
                    acv_dist_pct AS acv, share_pct AS share
                  FROM seed_monthly_pos_fy25_q12026 {where} ORDER BY period""")


def endcap_la():
    return df("""SELECT store_city AS city, COUNT(*) AS stores,
                   ROUND(AVG(larksfield_endcap_count),2) AS lf_endcaps,
                   ROUND(AVG(acme_endcap_count),2)       AS acme_endcaps,
                   ROUND(AVG(private_label_endcap_count),2) AS pl_endcaps,
                   ROUND(AVG(facing_count_crunchwell_mega),2) AS cw_mega_facings,
                   ROUND(AVG(facing_count_field_and_honey),2) AS fh_facings,
                   ROUND(AVG(CASE WHEN oos_flag_crunchwell_mega THEN 1.0 ELSE 0 END)*100,0) AS oos_pct
                 FROM seed_walmart_endcap_audit_la GROUP BY 1 ORDER BY stores DESC""")


def osa_banner(since="2026-01-01", top=8):
    return df(f"""SELECT Banner AS banner,
                    ROUND(AVG(OSA_Pct),1) AS osa,
                    ROUND(AVG(Planogram_Compliance_Pct),1) AS pog,
                    ROUND(AVG(Facings),2) AS facings
                  FROM perfect_store WHERE Date>='{since}'
                  GROUP BY 1 ORDER BY osa ASC LIMIT {top}""")


def bts():
    return df("""SELECT retailer, ROUND(AVG(hh_kids_5_14_buying_cereal_share)*100,1) AS kids_share,
                   ROUND(AVG(protein_curious_cohort_overlap)*100,1) AS protein_overlap,
                   ROUND(SUM(incremental_category_dollars_kusd)/1000,2) AS inc_m
                 FROM seed_numerator_bts_occasion_2025 GROUP BY 1 ORDER BY inc_m DESC""")


def elasticity(brand=None, top=10):
    where = f"WHERE brand='{brand}'" if brand else ""
    return df(f"""SELECT sku_name, brand, retailer, price_elasticity AS elast,
                    baseline_price_usd AS price, confidence_0to1 AS conf
                  FROM seed_sku_elasticity_estimates {where}
                  ORDER BY elast ASC LIMIT {top}""")


def pp_launch():
    return df("""SELECT sku, sku_name, retailer, dma, event_type,
                   promo_depth_pct_off AS depth, unit_price_promo AS price,
                   start_date, end_date, notes
                 FROM seed_proteinpeak_q2_launch ORDER BY start_date""")


def rouses_oos():
    return df("""SELECT sku_name, store_city AS city, osa_pct AS osa,
                   oos_days_q1_2026 AS oos_days, promo_response_lift_pct AS lift,
                   larksfield_endcap_flag AS lf_endcap
                 FROM seed_rouses_oos_by_door ORDER BY osa ASC""")


def kroger_switching():
    return df("""SELECT segment, from_brand, to_brand, switch_rate_pct AS rate,
                   share_pt_shift AS shift_pt, kroger_division AS division,
                   confidence_0to1 AS conf
                 FROM seed_kroger_simple_truth_switching ORDER BY shift_pt DESC""")


def heb_delist_risk():
    return df("""SELECT sku_name, heb_region AS region, store_count AS stores,
                   acv_authorization_pct AS acv, velocity_units_per_store_per_week AS velocity,
                   oos_rate_q1_pct AS oos, delist_risk_score_0to1 AS risk,
                   delist_risk_band AS band, next_review_date AS review
                 FROM seed_heb_cinnamon_twist_delist_risk ORDER BY risk DESC""")
