# Acme Crunchwell — MMM Schema

A reference schema for building a Market Mix Model on Crunchwell that is internally consistent with the Acme narrative. Use as the canonical structure for any synthetic MMM dataset generation.

## Grain

- **Geography:** Geo level = DMA (210 US DMAs, with Louisiana DMA highlighted)
- **Time:** Weekly, FY24 W1 through FY26 W18 (~125 weeks)
- **Brand:** Crunchwell only (separate models for ProteinPeak, MorningOats etc.)

## Variables (one row per DMA × week)

### Outcome (KPI)

| Variable | Type | Description | Source seed |
|---|---|---|---|
| `crunchwell_dollars_dma_week` | numeric | Dollar sales | `acme-monthly-pos-fy25-q12026.csv` (disaggregate to weekly) |
| `crunchwell_units_dma_week` | numeric | Unit volume | derived |
| `crunchwell_share_dma_week` | numeric (0–1) | $ share of cereal category | derived |

### Marketing variables

| Variable | Type | Description | Adstock decay (default) |
|---|---|---|---|
| `tv_grp_dma_week` | numeric | Linear TV GRPs delivered | 0.55 |
| `ctv_imps_dma_week` | numeric | Connected TV impressions | 0.45 |
| `display_imps_dma_week` | numeric | Programmatic display | 0.30 |
| `paid_social_imps_dma_week` | numeric | Meta + TikTok | 0.40 |
| `retail_media_walmart_imps_dma_week` | numeric | Walmart Connect | 0.20 |
| `retail_media_target_imps_dma_week` | numeric | Roundel | 0.20 |
| `retail_media_amazon_imps_dma_week` | numeric | Amazon Ads | 0.20 |
| `search_clicks_dma_week` | numeric | Google branded + non-branded | 0.10 |
| `influencer_imps_dma_week` | numeric | Macro + micro | 0.50 |

### Trade & price

| Variable | Type | Description |
|---|---|---|
| `avg_unit_price_dma_week` | numeric | Volume-weighted unit price |
| `promo_depth_pct_dma_week` | numeric | % off vs. everyday price |
| `pct_acv_promoted_dma_week` | numeric | % ACV with any temporary price reduction |
| `pct_acv_feature_dma_week` | numeric | % ACV with feature ad |
| `pct_acv_display_dma_week` | numeric | % ACV with display |
| `competitive_promo_depth_dma_week` | numeric | Same for top 3 competitors |
| `pl_promo_depth_dma_week` | numeric | Private label depth |

### Distribution

| Variable | Type | Description |
|---|---|---|
| `tdp_dma_week` | numeric | Total distribution points |
| `acv_dma_week` | numeric | All commodity volume distribution |
| `walmart_facings_dma_week` | numeric | Crunchwell facings at Walmart in DMA |
| `oos_pct_dma_week` | numeric | Out-of-stock rate |

### Macro / external

| Variable | Type | Description |
|---|---|---|
| `gas_price_dma_week` | numeric | Regional gas price (cost of living proxy) |
| `unemployment_rate_dma_week` | numeric | BLS, lagged |
| `temperature_anomaly_dma_week` | numeric | Weather (cold weather lifts hot cereal but not RTE) |
| `is_holiday_week` | boolean | Thanksgiving, Christmas, NY, Easter, Memorial Day, July 4 |
| `is_back_to_school_week` | boolean | Mid-Aug to mid-Sep |
| `disaster_flag` | categorical | Hurricane, snowstorm, etc. (Hurricane Tonya = Nov 2025 LA DMA) |

### Innovation / events

| Variable | Type | Description |
|---|---|---|
| `is_pack_refresh_week` | boolean | Crunchwell pack refresh launches Q3 2026 |
| `is_new_sku_launch_week` | boolean | E.g., Cinnamon Twist Q1 2025 |
| `claim_test_active` | boolean | Whether a media campaign with new claim is in market |

## Suggested model form

```
log(crunchwell_dollars) = β0
                       + β1 * adstock(tv_grp, λ=0.55)
                       + β2 * adstock(ctv_imps, λ=0.45)
                       + β3 * adstock(paid_social, λ=0.40)
                       + β4 * retail_media_walmart * is_walmart_market
                       + β5 * log(avg_unit_price)
                       + β6 * promo_depth
                       + β7 * pct_acv_promoted
                       + β8 * tdp
                       + β9 * walmart_facings
                       + β10 * disaster_flag
                       + γ * holiday_dummies
                       + δ * dma_fixed_effects
                       + ε
```

## Coefficient priors (sanity ranges)

These are the directional ranges the model should land in if the data is generated correctly. Use these as test assertions when generating synthetic data.

| Variable | Expected sign | Plausible elasticity |
|---|---|---|
| TV GRPs (adstocked) | + | 0.04 – 0.09 |
| CTV impressions | + | 0.03 – 0.08 |
| Paid social | + | 0.02 – 0.07 |
| Retail media Walmart | + (in WMT markets) | 0.05 – 0.12 |
| Average unit price | − | -1.4 to -0.9 |
| Promo depth | + | 0.6 – 1.2 |
| TDP | + | 0.7 – 1.1 |
| Walmart facings | + | 0.20 – 0.40 (per facing point) |
| Disaster flag | − | -0.3 to -0.6 |

## Saturation / diminishing returns

Use Hill saturation curves with the following shape parameters as defaults:

| Channel | k (saturation point) | s (slope) |
|---|---|---|
| TV | 600 GRPs | 1.4 |
| CTV | 800 mln imps | 1.3 |
| Paid social | 1500 mln imps | 1.5 |
| Retail media | 250 mln imps | 1.2 |

## Hold-out validation

The Q1 2026 LA DMA observation is the natural hold-out. The model trained on FY24–Q3 2025 should over-predict Crunchwell LA Q1 2026 by 250–340 bps, demonstrating that the decline is "unexplained by media+price+trade alone" and is therefore a distribution event (Walmart facing reset). This is the intended test case.

## Where this connects to the narrative

When the model is trained, the residual analysis should attribute:
- ~55% of the Q1 2026 LA shortfall to the `walmart_facings_dma_week` reduction
- ~20% to `competitive_promo_depth_dma_week` increase (Larksfield)
- ~12% to `disaster_flag` (Hurricane Tonya residual)
- ~13% to other / unexplained

This is exactly the decomposition in `05-louisiana-sales-decline-report.md`. The MMM is meant to validate that human analysis programmatically.
