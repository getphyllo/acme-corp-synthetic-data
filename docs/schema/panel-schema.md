# Acme — Household Panel Schema (Numerator-style)

A reference schema for generating synthetic household-level panel data consistent with the Acme narrative. Use this when building a Crunchwell or category-level demand model, household penetration analysis, or shopper-level switching study.

## Panel design

- **Panel size:** 100,000 households (matches Numerator scale, slightly smaller than Nielsen Homescan)
- **Geography:** All 50 US states + DC; weighted to align with US Census household distribution
- **Demographic representativeness:** Age, income, household size, presence-of-children, race/ethnicity weighted to ACS 5-year
- **Recording method:** Receipt scanning (default; OCR-coded items)
- **Tenure:** Households balanced across 1+ year tenure for repeat behavior modeling

## Tables

### `households`

| Column | Type | Description |
|---|---|---|
| `household_id` | string | Unique HH identifier |
| `state` | string | Two-letter |
| `dma` | string | DMA name |
| `msa` | string | MSA name (when applicable) |
| `zip3` | string | First 3 digits of ZIP |
| `urbanicity` | enum | Urban / Suburban / Rural |
| `hh_size` | int | Members |
| `presence_of_kids` | enum | None / 0–5 / 6–11 / 12–17 / mixed |
| `hoh_age_band` | enum | 18–24 / 25–34 / 35–44 / 45–54 / 55–64 / 65+ |
| `hh_income_band` | enum | <30K / 30–50K / 50–75K / 75–100K / 100–150K / 150K+ |
| `race_ethnicity` | enum | Hispanic / Non-Hisp White / Non-Hisp Black / Asian / Other |
| `primary_shopper_gender` | enum | F / M / NA |
| `panel_tenure_months` | int | |
| `weight` | float | Projection weight |

### `transactions`

| Column | Type | Description |
|---|---|---|
| `transaction_id` | string | |
| `household_id` | string | FK |
| `purchase_date` | date | |
| `retailer` | string | Retailer name |
| `channel` | enum | Mass / Grocery / Club / Drug / Conv / E-com |
| `total_basket_value_usd` | float | |
| `state` | string | |
| `dma` | string | |

### `transaction_items`

| Column | Type | Description |
|---|---|---|
| `transaction_id` | string | FK |
| `upc` | string | Item UPC |
| `sku_id` | string | Acme internal SKU id (joins `acme-skus.csv`) |
| `brand` | string | |
| `category` | string | |
| `subcategory` | string | |
| `units` | int | |
| `unit_price_usd` | float | |
| `was_on_promo` | bool | |
| `promo_depth_pct` | float | |

## Distribution targets (must hold in any generated panel)

These are the "facts" that any synthetic Acme panel must reproduce.

### Crunchwell household penetration (FY25 actual)

| Geography | HH penetration | Buying rate (purchases/yr/buyer) |
|---|---:|---:|
| US national | 13.4% | 3.6 |
| Midwest | 18.7% | 3.9 |
| Northeast | 8.2% | 3.2 |
| Southeast | 11.3% | 3.5 |
| Louisiana DMA — FY25 | 12.1% | 3.4 |
| **Louisiana DMA — Q1 2026** | **6.4%** | **2.8** |

### Crunchwell penetration by HH demographics

| Cut | Penetration |
|---:|---:|
| HHs with kids 6–11 | 19.4% |
| HHs without kids | 9.2% |
| Income $50–75K | 16.1% |
| Income $150K+ | 7.4% |
| Hispanic HH | 4.1% |
| Non-Hisp White HH | 14.8% |

### Switching matrix (FY25 → Q1 2026, LA DMA, lapsed Crunchwell buyers)

| Lost-to brand | % of lapsed Crunchwell buyers in LA |
|---|---:|
| Honey Bunches of Oats (Post) | 14% |
| Cheerios (General Mills) | 9% |
| Walmart Great Value Honey Toasted Oats (PL) | 11% |
| Frosted Flakes (Kellanova) | 4% |
| Other / no purchase | 62% |

### Brand repertoire

Average household keeps 3.4 cereal brands in repertoire over 12 months. Crunchwell-buying households over-index on: HoneyNest (45%), MorningOats (28%), TrailGrove (19%), Cheerios (51% — competing buyers), Honey Bunches of Oats (33%).

## Generation guidance

When creating a synthetic panel:

1. Start with the `households` distribution and weight to ACS.
2. Generate transactions as a Poisson process anchored on category buying rates by demographic.
3. Apply share assignments using the SKU file weighted by ACV (no Crunchwell purchases at retailers where Crunchwell isn't distributed in that DMA).
4. Apply switching behavior in Q1 2026 LA DMA according to the matrix above — this should reproduce the 340bps share decline.

## Test cases (assertions any generated panel should pass)

```python
# Crunchwell US national share FY25
assert 5.7 < crunchwell_share(us, fy25) < 6.0

# Louisiana decline visible
assert crunchwell_share(la_dma, q1_2026) < crunchwell_share(la_dma, fy25) - 3.0

# Walmart concentration in LA
assert walmart_share_of_la_volume() > 0.36

# Switching to Honey Bunches in LA Q1 2026 abnormally high
assert switch_rate(crunchwell, hboo, la_dma, q1_2026) > 2 * switch_rate(crunchwell, hboo, la_dma, fy25)

# Hispanic HH under-penetration confirmed
assert crunchwell_pen(hispanic) / crunchwell_pen(non_hispanic_white) < 0.35
```

If a generation fails any of these, regenerate with adjusted parameters.
