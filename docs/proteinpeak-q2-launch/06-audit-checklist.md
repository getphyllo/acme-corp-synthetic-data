# Audit Checklist — ProteinPeak Q2 Launch + Louisiana Decline Coexistence

Before sharing a prototype that depends on either scenario, run this checklist against `acme.duckdb`. Every query below should return the expected order of magnitude. If anything drifts, regenerate (`python3 generator/generate.py`) and re-run.

The first ten checks validate the **ProteinPeak Q2 launch** (Scenario 2). The last six re-confirm the **Louisiana decline** (Scenario 1) so the two scenarios remain compatible.

---

## Quick start

```bash
duckdb acme.duckdb < docs/proteinpeak-q2-launch/06-audit-checklist.md
# Or copy/paste individual SELECTs into duckdb -c "..."
```

---

## ProteinPeak Q2 Launch checks

### PP-1: New SKUs exist in seed and parquet

```sql
SELECT sku_id, sku_name, status, launch_year
FROM seed_skus
WHERE sku_id IN ('PP005','PP006');
-- Expect: two rows, status='Active-Launch-Q2', launch_year=2026
```

### PP-2: PP005/PP006 only appear on/after 2026-04-20 in epos

```sql
SELECT MIN(Date_Time) AS first_appearance, COUNT(*) AS n_tx
FROM epos
WHERE Product_SKU IN ('PP005','PP006');
-- Expect: first_appearance >= '2026-04-20', n_tx > 50
```

### PP-3: Trial-velocity gap between Target and Walmart

```sql
SELECT Banner, ROUND(AVG(Sales_Units), 2) AS avg_velocity, COUNT(*) AS n
FROM perfect_store
WHERE SKU IN ('PP005','PP006') AND Date >= '2026-04-20'
GROUP BY Banner ORDER BY avg_velocity DESC;
-- Expect: Target velocity > Walmart velocity (Target ~17, Walmart ~9)
```

### PP-4: Plan-vs-actual channel split

```sql
SELECT Retailer, ROUND(AVG(Variance_Pct)*100, 1) AS variance_pct
FROM plan_vs_actual
WHERE Brand = 'ProteinPeak' AND Period IN ('2026-04','2026-05')
  AND Retailer IN ('Target','Walmart','Amazon')
GROUP BY Retailer ORDER BY variance_pct DESC;
-- Expect: Target ≈ +13%, Walmart ≈ -22%, Amazon ≈ 0% (±6)
```

### PP-5: PP001 cannibalization

```sql
WITH pre AS (
  SELECT AVG(Sales_Units) AS v
  FROM perfect_store
  WHERE SKU='PP001' AND Banner IN ('Target','Amazon','Whole Foods','Sprouts','Kroger')
    AND Date BETWEEN '2026-01-01' AND '2026-04-19'
), post AS (
  SELECT AVG(Sales_Units) AS v
  FROM perfect_store
  WHERE SKU='PP001' AND Banner IN ('Target','Amazon','Whole Foods','Sprouts','Kroger')
    AND Date >= '2026-04-20'
)
SELECT pre.v AS pre_velocity, post.v AS post_velocity,
       ROUND((post.v - pre.v) / pre.v * 100, 1) AS pct_change
FROM pre, post;
-- Expect: pct_change between -4% and -10%
```

### PP-6: Source-of-volume distribution

```sql
SELECT Switching_Flag, COUNT(*) AS n,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
FROM household_transactions
WHERE Product_SKU IN ('PP005','PP006')
GROUP BY Switching_Flag ORDER BY n DESC;
-- Expect: New_To_Brand ~53%, Cannibalization ~32%, Competitor_Switch ~15%
```

### PP-7: Authorization gating

```sql
SELECT Snapshot_Date,
       SUM(CASE WHEN Auth_Status='Authorized' THEN 1 ELSE 0 END) AS authorized,
       SUM(CASE WHEN Auth_Status='Not_Authorized' THEN 1 ELSE 0 END) AS not_authorized
FROM sku_authorization
WHERE SKU IN ('PP005','PP006')
GROUP BY Snapshot_Date ORDER BY Snapshot_Date;
-- Expect: 0 authorized before 2026-04-30; rising after
```

### PP-8: Social mention positive sentiment post-launch

```sql
SELECT ROUND(AVG("Sentiment_-1to1"), 3) AS avg_sentiment, COUNT(*) AS n_mentions
FROM social_mentions
WHERE Brand_Mentioned = 'ProteinPeak' AND Date >= '2026-04-20';
-- Expect: avg_sentiment > 0.30, n_mentions > 300
```

### PP-9: Sage Park cohort creator attribution

```sql
SELECT Creator_ID, COUNT(*) AS posts,
       ROUND(SUM(Attributed_Sales_Lift_72hr_USD)) AS total_attributed
FROM creator_posts
WHERE Brand_Mentioned = 'ProteinPeak' AND Date >= '2026-04-20'
  AND Creator_ID IN ('CR-0012','CR-0007','CR-0021','CR-0040','CR-0042','CR-0013','CR-0027')
GROUP BY Creator_ID ORDER BY total_attributed DESC;
-- Expect: 7 rows; CR-0012 (Sage Park anchor) typically tops the list
```

### PP-10: Search trends spike post-launch

```sql
SELECT Keyword, MIN(Date) AS first_appearance,
       ROUND(MAX(Volume_Index_0to100), 1) AS peak_volume
FROM search_trends
WHERE Keyword IN ('proteinpeak cinnamon crunch','proteinpeak cocoa almond','proteinpeak target')
GROUP BY Keyword ORDER BY Keyword;
-- Expect: launch-period peak >= 20 on each launch keyword
```

---

## Louisiana Decline regression checks (Scenario 1 still intact)

### LA-1: LA-DMA Crunchwell share Q1 2026

```sql
SELECT ROUND(AVG(Crunchwell_Value_Share)*100, 2) AS la_share_pct
FROM syndicated_weekly
WHERE DMA = 'LA-DMA' AND Category = 'RTE Cereal' AND Week LIKE '2026%';
-- Expect: ~3.0% (-340 bps vs FY25)
```

### LA-2: Hurricane Tonya fill-rate dip

```sql
SELECT ROUND(AVG(Fill_Rate_Pct)*100, 1) AS avg_fill_pct
FROM shipments
WHERE Week_Start BETWEEN '2025-11-08' AND '2025-12-10'
  AND Retailer_DC LIKE '%Houston%';
-- Expect: avg_fill_pct < 75%
```

### LA-3: LA Crunchwell plan vs actual

```sql
SELECT ROUND(AVG(Variance_Pct)*100, 1) AS la_variance_pct
FROM plan_vs_actual
WHERE Brand = 'Crunchwell' AND DMA = 'LA-DMA' AND Period LIKE '2026-%';
-- Expect: la_variance_pct < -30%
```

### LA-4: Crunchwell Mega facings cut at Walmart South (pre-reset vs post-reset within Walmart South)

```sql
SELECT
  CASE WHEN Date < '2025-09-15' THEN 'pre-reset' ELSE 'post-reset' END AS period,
  ROUND(AVG(Facings), 2) AS avg_facings, COUNT(*) AS n
FROM perfect_store
WHERE SKU IN ('CR002','CR004','CR005') AND Banner = 'Walmart'
  AND Banner_Region = 'Walmart South'
GROUP BY period;
-- Expect: post-reset avg_facings noticeably lower than pre-reset
-- (cross-region comparison is noisy because store size mix differs by region)
```

### LA-5: Cinnamon Twist (CR006) authorization

```sql
SELECT ROUND(AVG(CASE WHEN Auth_Status='Authorized' THEN 1.0 ELSE 0 END), 2) AS auth_rate
FROM sku_authorization WHERE SKU = 'CR006';
-- Expect: 0.35 to 0.50
```

### LA-6: LA Crunchwell social sentiment dip Q4'25-Q1'26

```sql
SELECT ROUND(AVG("Sentiment_-1to1"), 3) AS avg_sentiment, COUNT(*) AS n
FROM social_mentions
WHERE Brand_Mentioned = 'Crunchwell' AND DMA_Region = 'LA-DMA'
  AND Date >= '2025-10-01' AND Date < '2026-04-01';
-- Expect: avg_sentiment < -0.10, n > 100
```

---

## Coexistence checks (both stories intact)

### CO-1: Both scenarios contribute to Acme's headline numbers

```sql
-- ProteinPeak FY26 plan growth should be roughly +50% to +70% nationally
SELECT ROUND(SUM(Actual_Revenue_USD) / SUM(Plan_Revenue_USD) - 1, 3) AS pp_var
FROM plan_vs_actual WHERE Brand='ProteinPeak' AND Period LIKE '2026-%';

-- Crunchwell FY26 should be soft because of LA
SELECT ROUND(SUM(Actual_Revenue_USD) / SUM(Plan_Revenue_USD) - 1, 3) AS cr_var
FROM plan_vs_actual WHERE Brand='Crunchwell' AND Period LIKE '2026-%';
```

### CO-2: Switching_Flag uses three taxonomies

```sql
SELECT Switching_Flag, COUNT(*) AS n
FROM household_transactions
GROUP BY Switching_Flag ORDER BY n DESC;
-- Expect: No (dominant) + Yes (LA decline) + New_To_Brand + Cannibalization + Competitor_Switch
```

### CO-3: Both scenarios' event logs survive

```sql
SELECT COUNT(*) AS la_events FROM seed_promo_events_louisiana;
SELECT COUNT(*) AS pp_events FROM seed_proteinpeak_q2_launch;
-- Expect: la_events = 17, pp_events = 15
```
