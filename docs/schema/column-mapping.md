# Kellogg → Acme — Column-by-column mapping

This document maps every column in the Kellogg ME reference files to the Acme equivalent. Use it when reasoning about whether a synthetic-data field is preserved, renamed, or added.

A ✓ means the column exists in the Acme file. A ✗ means it was deliberately dropped (with reason). A ★ means the column is **new in Acme** and not in Kellogg.

---

## 1. EPOS — `acme-epos-30k.csv` ↔ `kellogg_me_epos_100k.csv`

| Kellogg column | Acme column | Status | Notes |
|---|---|---|---|
| Transaction_ID | Transaction_ID | ✓ | TXN0000001 format preserved |
| Date_Time | Date_Time | ✓ | YYYY-MM-DD HH:MM:SS preserved |
| Country | Country | ✓ | "United States" |
| Country_Code | Country_Code | ✓ | "USA" |
| — | State | ★ | Two-letter US state code |
| — | DMA | ★ | DMA id (e.g., `LA-DMA`) — joins to `acme-geographies.csv` |
| City | City | ✓ | US city in DMA |
| Retail_Chain | Retail_Chain | ✓ | Walmart, Target, Kroger, Rouses etc. |
| Store_Type | Store_Type | ✓ | Hypermarket / Supermarket / Convenience / Online |
| Store_ID | Store_ID | ✓ | 3-letter chain prefix + 4-digit number |
| Customer_ID | Customer_ID | ✓ | C###### format preserved |
| Product_SKU | Product_SKU | ✓ | Acme SKU id (CR001 etc.) |
| Product_Name | Product_Name | ✓ | Full SKU description |
| — | Brand | ★ | Brand name (Crunchwell, HoneyNest, Honey Bunches Oats, etc.) — for Acme-vs-competitor pivots |
| — | Manufacturer | ★ | "Acme Corp" / "Post Foods" / "General Mills" / "Walmart PL" / etc. |
| Product_Category | Product_Category | ✓ | RTE Cereal / Hot Cereal / Granola / Plant-Based Milk / Bar |
| Quantity_Sold | Quantity_Sold | ✓ | |
| Currency | Currency | ✓ | "USD" |
| Unit_Price_Local | Unit_Price_Local | ✓ | Base unit price USD |
| Total_Sale_Amount | Total_Sale_Amount | ✓ | Base × Qty |
| Discount_Percent | Discount_Percent | ✓ | 0.00–0.30 typical |
| Final_Sale_Amount | Final_Sale_Amount | ✓ | After discount × Qty |
| Promotion_Type | Promotion_Type | ✓ | None / Price Off / Multi-Buy / Bundle / Loyalty |
| Promotion_Flag | Promotion_Flag | ✓ | Yes / No |
| Payment_Method | Payment_Method | ✓ | + EBT (American context) |
| Weekday | Weekday | ✓ | |
| Month | Month | ✓ | |
| Hour | Hour | ✓ | |
| Seasonality_Flag | Seasonality_Flag | ✓ | None / BackToSchool / Holiday / Easter / SuperBowl (replaces `Ramadan`) |

---

## 2. Perfect Store — `acme-perfect-store-50k.csv` ↔ `Kellogg_ME_PerfectStore_150k.csv`

| Kellogg column | Acme column | Status | Notes |
|---|---|---|---|
| Date | Date | ✓ | |
| Store_ID | Store_ID | ✓ | |
| Country | Country | ✓ | |
| Country_Code | Country_Code | ✓ | |
| — | State | ★ | |
| — | DMA | ★ | |
| City | City | ✓ | |
| Cluster | Cluster | ✓ | Renamed concept: now Mass / Grocery / Club / E-commerce / Drug / Convenience |
| Banner | Banner | ✓ | US retailer name |
| Size_Tier | Size_Tier | ✓ | S / M / L preserved |
| SKU | SKU | ✓ | |
| Product_Description | Product_Description | ✓ | |
| — | Brand | ★ | |
| — | Manufacturer | ★ | |
| Category | Category | ✓ | |
| Unit_Price_Local_Proxy | Unit_Price_Local_Proxy | ✓ | |
| Promotion_Flag | Promotion_Flag | ✓ | |
| Promotion_Type | Promotion_Type | ✓ | |
| Promotion_Depth_% | Promotion_Depth_Pct | ✓ | renamed (no `%` in column name) |
| Opening_Inventory_Units | Opening_Inventory_Units | ✓ | |
| Received_Units | Received_Units | ✓ | |
| Sales_Units | Sales_Units | ✓ | |
| Sales_Value | Sales_Value | ✓ | |
| Closing_Inventory_Units | Closing_Inventory_Units | ✓ | |
| OSA_% | OSA_Pct | ✓ | renamed; encodes Hurricane Tonya OOS spike |
| Planogram_Compliance_% | Planogram_Compliance_Pct | ✓ | renamed |
| Facings | Facings | ✓ | encodes the Walmart Sept 2025 reset (Crunchwell Mega 8→6) |

---

## 3. Syndicated Weekly — `acme-syndicated-weekly-niq.csv` ↔ `NielsenIQ_ME_100k_SQLReady.csv`

| Kellogg column | Acme column | Status | Notes |
|---|---|---|---|
| Country | Country | ✓ | |
| — | DMA | ★ | The grain is now DMA, not country |
| — | Region | ★ | Census region |
| Category | Category | ✓ | |
| Channel | Channel | ✓ | Mass / Grocery / Club / E-commerce / Drug & Conv |
| Week | Week | ✓ | ISO YYYY-Wnn |
| Value_USD_MM | Value_USD_MM | ✓ | Category $ in millions |
| Volume_Tons | Volume_Units_K | ✓ (renamed) | Acme reports volume in K units, not tons |
| Kellogg_Value_Share | Acme_Value_Share | ✓ (renamed) | Total Acme share |
| — | Crunchwell_Value_Share | ★ | The brand the Louisiana decline lives in |
| — | Post_Value_Share | ★ | Competitor — Honey Bunches story |
| — | GeneralMills_Value_Share | ★ | Cheerios |
| — | Kellanova_Value_Share | ★ | |
| — | PL_Value_Share | ★ | Private label |
| Promo_Share | Promo_Share | ✓ | |
| Avg_Price_USD | Avg_Price_USD | ✓ | |
| — | ACV_Distribution_Pct | ★ | so distribution analysis is possible without Perfect Store join |
| — | TDP | ★ | Total Distribution Points |
| — | Avg_Facings | ★ | |

---

## 4. Brand Health — `acme-brand-health-15k.csv` ↔ `kellogg_ME_brand_health_2024_2025_100k.csv`

| Kellogg column | Acme column | Status | Notes |
|---|---|---|---|
| response_id | response_id | ✓ | R_######## format preserved |
| wave | wave | ✓ | YYYYQq, extended through 2026Q1 |
| response_date | response_date | ✓ | |
| country | country | ✓ | |
| — | state | ★ | |
| — | dma | ★ | Encodes the LA softening |
| city_tier | city_tier | ✓ | |
| age_band | age_band | ✓ | |
| gender | gender | ✓ | |
| household_size | household_size | ✓ | |
| children_present | children_present | ✓ | |
| — | ethnicity | ★ | Hispanic / Non-Hisp White / Non-Hisp Black / Asian / Other |
| income_bracket | income_bracket | ✓ | US bands (<30K → 150K+) |
| education_level | education_level | ✓ | US ladder |
| marital_status | marital_status | ✓ | |
| primary_category | primary_category | ✓ | |
| channel_preference | channel_preference | ✓ | |
| retailer_type | retailer_type | ✓ | |
| ramadan_period | holiday_season_flag | ✓ (renamed) | Equivalent calendar concept |
| unaided_aw_kellogg | unaided_aw_crunchwell | ✓ (renamed) | |
| aided_aw_kellogg | aided_aw_crunchwell | ✓ (renamed) | |
| considers_kellogg | considers_crunchwell | ✓ (renamed) | |
| consideration_set_size | consideration_set_size | ✓ | |
| purchase_frequency_qtr | purchase_frequency_qtr | ✓ | |
| price_sensitivity_1to5 | price_sensitivity_1to5 | ✓ | |
| promo_propensity_0to1 | promo_propensity_0to1 | ✓ | |
| usage_primary | usage_primary | ✓ | |
| taste, quality, health, value, family_friendly, innovation, trust | (same) | ✓ | 1–5 scales preserved |
| likelihood_repurchase_1to5 | likelihood_repurchase_1to5 | ✓ | |
| nps_0to10 | nps_0to10 | ✓ | |
| top_competitor | top_competitor | ✓ | US competitor set |
| price_paid_usd_equiv | price_paid_usd | ✓ (renamed) | |
| respondent_weight | respondent_weight | ✓ | |
| aided_aw_nestle | — | ✗ | Replaced by US-relevant brands |
| aided_aw_general_mills | aided_aw_cheerios | ✓ (refined) | Brand-level, not manufacturer |
| aided_aw_weetabix | — | ✗ | Removed (not US-relevant) |
| aided_aw_quaker | aided_aw_quaker | ✓ | |
| aided_aw_local_brand | aided_aw_great_value_pl | ✓ (refined) | Walmart Great Value PL |
| — | aided_aw_honeynest | ★ | Acme kid brand |
| — | aided_aw_proteinpeak | ★ | |
| — | aided_aw_morningoats | ★ | |
| — | aided_aw_trailgrove | ★ | |
| — | aided_aw_rootday | ★ | |
| — | aided_aw_honey_bunches | ★ | The LA-relevant competitor |
| — | aided_aw_frosted_flakes | ★ | |

---

## 5. Households — `acme-households-5k.csv` ↔ `households.csv`

| Kellogg column | Acme column | Status | Notes |
|---|---|---|---|
| Household_ID | Household_ID | ✓ | HH###### |
| Country | Country | ✓ | |
| Country_Code | Country_Code | ✓ | |
| — | State | ★ | |
| — | DMA | ★ | |
| City | City | ✓ | |
| Urban | Urbanicity | ✓ (renamed) | Urban / Suburban / Rural |
| Currency | Currency | ✓ | |
| HH_Size | HH_Size | ✓ | |
| Income_Bracket | Income_Bracket | ✓ | US bands |
| Head_Age | HOH_Age | ✓ (renamed) | Head-of-household age |
| — | HOH_Gender | ★ | |
| Education_Level | Education_Level | ✓ | |
| — | Marital_Status | ★ | |
| — | Ethnicity | ★ | |
| Children_Flag | Children_Flag | ✓ | |
| Children_Age_Band | Children_Age_Band | ✓ | 0-5 / 6-11 / 12-17 / Mixed / None |
| — | Number_Of_Children | ★ | |
| Loyalty_Score | Loyalty_Score | ✓ | 0–1 |
| Brand_Loyalty_Segment | Brand_Loyalty_Segment | ✓ | "Acme Loyal" / "Multi-Brand Switcher" / "Competitor Loyal" / "Light Buyer" |
| Price_Sensitivity_Segment | Price_Sensitivity_Segment | ✓ | |
| Adopter_Type | Adopter_Type | ✓ | |
| — | Cereal_Buyer_Flag | ★ | Useful for filtering panel to in-category HHs |
| — | Plant_Based_Buyer_Flag | ★ | |
| — | Panel_Tenure_Months | ★ | |
| — | Weight | ★ | Projection weight |

---

## 6. Household Transactions — `acme-household-transactions-30k.csv` ↔ `transactions.csv`

| Kellogg column | Acme column | Status | Notes |
|---|---|---|---|
| Household_ID | Household_ID | ✓ | |
| Week_Start | Week_Start | ✓ | |
| Country | Country | ✓ | |
| Country_Code | Country_Code | ✓ | |
| — | State | ★ | |
| — | DMA | ★ | |
| City | City | ✓ | |
| Urban | Urbanicity | ✓ (renamed) | |
| Currency | Currency | ✓ | |
| — | Retailer | ★ | Specific banner (Walmart, Rouses, etc.) |
| Retailer_Type | Retailer_Type | ✓ | Hypermarket / Supermarket / etc |
| Channel | Channel | ✓ | |
| Category | Category | ✓ | |
| Brand | Brand | ✓ | |
| — | Manufacturer | ★ | |
| Product_SKU | Product_SKU | ✓ | |
| — | Product_Description | ★ | |
| Pack_Weight_g | Pack_Weight_oz | ✓ (renamed) | US units |
| Units | Units | ✓ | |
| Unit_Price_Local | Unit_Price | ✓ (simplified) | |
| Discount_Percent | Discount_Percent | ✓ | |
| Total_Price_Paid_Local | Total_Price_Paid | ✓ (simplified) | |
| — | Promotion_Type | ★ | |
| Children_Flag | Children_Flag | ✓ | |
| Income_Bracket | Income_Bracket | ✓ | |
| — | Ethnicity | ★ | |
| Price_Sensitivity_Segment | Price_Sensitivity_Segment | ✓ | |
| Brand_Loyalty_Segment | Brand_Loyalty_Segment | ✓ | |
| Adopter_Type | Adopter_Type | ✓ | |
| — | Switching_Flag | ★ | "Yes" when an Acme-loyal HH switched to a competitor on this transaction (LA → Honey Bunches Q4'25–Q1'26) |

---

## Decisions about what was dropped

- **Ramadan-specific flag** → replaced with `Holiday_Season_Flag` and the broader `Seasonality_Flag` enum. The Acme calendar peaks in Back-to-School (Aug–Sep) and Holiday (Nov–Dec); Easter and Super Bowl are secondary.
- **Country-level grain on syndicated weekly** → replaced with **DMA grain**, because the Louisiana decline is a DMA-level story and the Kellogg country grain doesn't capture US regional dynamics.
- **Local Brand awareness** → replaced with explicit private-label awareness (`aided_aw_great_value_pl`) and an expanded competitor set, because in the US PL is not a long-tail "local brand" — it's a top-3 competitor in many DMAs.
- **Weetabix and Nestlé awareness** → dropped (not relevant in US). Replaced with US-relevant brand awareness (Cheerios, Honey Bunches of Oats, Frosted Flakes, Quaker, Great Value PL).
