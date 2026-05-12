# Hypothesis Tree — ProteinPeak Q2 2026 Launch Week-4 Read

Sage's email asks four questions. This file is the evidence map for each — what we expect to find when we query the data.

---

## H1 — Trial is mixed by channel: Target hot, Walmart cold

**Hypothesis:** Cinnamon Crunch + Cocoa Almond are tracking **113% of plan in Target** (endcap-supported) and **78% of plan in Walmart** (pilot, no endcap). Amazon roughly on plan. WFM/Sprouts slightly above plan.

**Why this matters:** Determines whether the launch is a "Target-only success" (lean Q3 budget into Roundel + push for endcap renewal) or a "broad win" (lean into Walmart-pilot expansion at the August line review).

**Evidence to pull:**

```sql
-- Trial velocity by retailer, post-launch
SELECT Banner,
       AVG(Sales_Units) AS avg_velocity,
       COUNT(*) AS n_observations
FROM perfect_store
WHERE SKU IN ('PP005','PP006')
  AND Date >= '2026-04-20'
GROUP BY Banner
ORDER BY avg_velocity DESC;
```

**Plan-vs-actual cut:**

```sql
SELECT Retailer, Period,
       ROUND(AVG(Variance_Pct)*100, 1) AS variance_pct
FROM plan_vs_actual
WHERE Brand = 'ProteinPeak'
  AND Period IN ('2026-04','2026-05')
GROUP BY Retailer, Period
ORDER BY Period, variance_pct DESC;
```

**Expected signal:** Target ≈ +13% over plan, Walmart ≈ -22% under plan.

---

## H2 — Repeat curve is strong: Week-2 repeat for PP005 ≈ 1.2x Berry Crunch

**Hypothesis:** Households who purchase PP005/PP006 in Week 1 return to purchase it again in Weeks 2–4 at a rate **1.2× ProteinPeak Berry Crunch (PP003)** at the same week-since-launch.

**Why this matters:** Trial without repeat is a launch that pulls forward demand and decays. A 1.2× repeat lift vs the most-recent flavor success says this is a **product fit**, not just a buzz launch.

**Evidence to pull:**

```sql
-- Households with 2+ PP005/PP006 purchases within 4 weeks of first-buy
WITH first_buys AS (
  SELECT Household_ID,
         MIN(Week_Start) AS first_buy_wk,
         Product_SKU
  FROM household_transactions
  WHERE Product_SKU IN ('PP003','PP005','PP006')
  GROUP BY Household_ID, Product_SKU
),
repeats AS (
  SELECT h.Household_ID, h.Product_SKU,
         COUNT(*) FILTER (WHERE t.Week_Start > h.first_buy_wk
                          AND t.Week_Start <= DATE_ADD(h.first_buy_wk, INTERVAL 28 DAY)) AS n_repeat
  FROM first_buys h
  LEFT JOIN household_transactions t
    ON h.Household_ID = t.Household_ID AND h.Product_SKU = t.Product_SKU
  GROUP BY h.Household_ID, h.Product_SKU
)
SELECT Product_SKU,
       AVG(CASE WHEN n_repeat >= 1 THEN 1 ELSE 0 END) AS repeat_rate
FROM repeats GROUP BY Product_SKU;
```

**Cross-check:** `product_reviews.Rating_1to5` for PP005/PP006 launch period vs PP003 first-90-days. PP005/PP006 should rate ≈ 4.6 vs PP003 ≈ 4.4.

---

## H3 — Cannibalization of PP001 is real but bounded (~6% steady-state)

**Hypothesis:** ProteinPeak Vanilla Almond Original (PP001) velocity dips **~11% in Week 1** at launch retailers, then settles at **~6% below pre-launch baseline** in Weeks 2–4. The other ~94% of PP005/PP006 volume is incremental (new-to-brand + competitor switch).

**Why this matters:** A 6% steady-state cannibalization rate on a $25M franchise SKU is ~$1.5M of pulled-forward demand — bounded enough that the net incremental from PP005/PP006 ($14M + $10M plan) still drives the +$32M FY26 ProteinPeak growth.

**Evidence to pull:**

```sql
-- PP001 velocity dip post-launch at launch retailers
WITH pre AS (
  SELECT AVG(Sales_Units) AS pre_velocity
  FROM perfect_store
  WHERE SKU = 'PP001'
    AND Banner IN ('Target','Amazon','Whole Foods','Sprouts','Kroger')
    AND Date BETWEEN '2026-01-01' AND '2026-04-19'
),
post AS (
  SELECT AVG(Sales_Units) AS post_velocity
  FROM perfect_store
  WHERE SKU = 'PP001'
    AND Banner IN ('Target','Amazon','Whole Foods','Sprouts','Kroger')
    AND Date >= '2026-04-20'
)
SELECT pre.pre_velocity, post.post_velocity,
       (post.post_velocity - pre.pre_velocity) / pre.pre_velocity AS pct_change
FROM pre, post;
```

**Source-of-volume waterfall:**

```sql
SELECT Switching_Flag, COUNT(*) AS n_buys,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
FROM household_transactions
WHERE Product_SKU IN ('PP005','PP006')
GROUP BY Switching_Flag
ORDER BY n_buys DESC;
```

**Expected distribution:** New_To_Brand ≈ 53%, Cannibalization ≈ 32%, Competitor_Switch ≈ 15%.

---

## H4 — Creator + retail-media response curve favors Target endcap + Sage cohort

**Hypothesis:** The launch's strongest response comes from the **Target endcap + Sage Park athlete cohort** combination. The Amazon push (creator-supported, no endcap) is on plan. The Walmart-pilot is soft because Walmart's shopper doesn't show up for premium-price ($7.49) wellness cereal without the endcap signal.

**Why this matters:** Tells Hugo Lin (and Tasha Brooks on Pacvue) where to lean the remaining Q2 retail-media budget. Recommended action: hold Amazon, lean into Target endcap renewal, deprioritize Walmart-pilot.

**Evidence to pull:**

```sql
-- Creator attribution by partnership status
SELECT cr.creator_id, cr.handle, cr.acme_partnership_status,
       COUNT(*) AS n_posts,
       SUM(cp.Attributed_Sales_Lift_72hr_USD) AS total_attributed_usd
FROM creator_posts cp
JOIN seed_creators cr ON cp.Creator_ID = cr.creator_id
WHERE cp.Brand_Mentioned = 'ProteinPeak'
  AND cp.Date >= '2026-04-20'
GROUP BY cr.creator_id, cr.handle, cr.acme_partnership_status
ORDER BY total_attributed_usd DESC NULLS LAST
LIMIT 10;
```

**Retail media x velocity check:**

```sql
-- Retail-media spend pace by retailer vs Sales_Value lift
SELECT pe.Retailer,
       SUM(pe.Trade_Spend_USD) AS retail_media_spend,
       AVG(ps.Sales_Value) AS avg_sales_value
FROM promo_events pe
LEFT JOIN perfect_store ps
  ON ps.Banner = pe.Retailer AND ps.SKU = pe.SKU
WHERE pe.SKU IN ('PP005','PP006')
GROUP BY pe.Retailer
ORDER BY retail_media_spend DESC;
```

**Expected signal:** Top attributed creators are Sage Park cohort (CR-0012 anchor + CR-0007/0021/0040/0042/0013). Target Roundel spend has the highest revenue-per-dollar; Walmart Connect lowest.

---

## Hypothesis attribution to the Week-4 narrative

```
                Estimated contribution to the +$3M [sample] PP005+PP006 W4 revenue
              ┌──────────────────────────────────────────┐
H1  Target endcap channel mix         ████████████████  ~42%
H4  Creator + retail-media stack      ██████████        ~28%
H2  Repeat strength (vs Berry Crunch) ██████            ~18%
H3  Net incremental over PP001 cann.  ████              ~12%
              └──────────────────────────────────────────┘
```

This is the bar Maya defends on Tuesday May 26 in Whitfield's room.
