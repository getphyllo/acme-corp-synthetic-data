# ProteinPeak Q2 2026 Launch — Scenario Bundle

This folder is the canonical reference for **Scenario 2 — The ProteinPeak Q2 Launch Read**. It mirrors the structure of `docs/louisiana-decline.md` but is broken into multiple files because the launch has more moving parts (two SKUs, four channels, source-of-volume, creator activation, retail media pacing).

Read in this order:

| File | What it covers |
|---|---|
| `01-scenario-overview.md` | The story Maya is handed at 4:47 PM Thursday; stakeholders; today-vs-Clayface arc |
| `02-launch-data-model.md` | How the launch is encoded across all 16 datasets (SKU IDs, anchors, date windows) |
| `03-hypothesis-tree.md` | The four questions Sage asks (trial, repeat, source-of-volume, channel split) — and the evidence map |
| `04-week4-read-deck-outline.md` | The slide structure Maya would have built by hand; what Clayface's Drop-into-Deck produces |
| `05-personas-supplement.md` | New characters (Sage Park, Hugo Lin, Helen Park-Choi, Tasha Brooks, Theo Mannering) and Maya's calendar overlay |
| `06-audit-checklist.md` | The SQL audit queries that verify the launch story holds across all 16 tables |

The **source story** (the brief Maya gets) is preserved verbatim in [`../../00-source/01-proteinpeak-q2-launch-read.md`](#) (also pinned in the workspace inbox as `00-inbox/10-stakeholder-inputs/`).

---

## Why a second scenario

The Louisiana decline scenario tells the **defensive analyst** story — Maya is reading a regional decline that has already happened. The ProteinPeak Q2 launch tells the **offensive analyst** story — Maya is reading a launch that is still happening and needs a Week-4 decision support read.

Together they cover the two most common high-stakes patterns in a CPG insights team's quarter: a regional softness diagnosis, and an innovation launch read.

---

## Anchors at a glance

| Anchor | Value | Where it shows up |
|---|---|---|
| **PP005 = ProteinPeak Cinnamon Crunch** | Launched 2026-04-20 | `seeds/skus.csv`, `competitor_launches`, all 16 parquet tables |
| **PP006 = ProteinPeak Cocoa Almond** | Launched 2026-04-20 | Same |
| **Target endcap support** | 4-wk endcap; trial 113% of plan | `epos`, `perfect_store`, `plan_vs_actual`, `promo_events` |
| **Walmart-pilot** | Soft trial 78% of plan | Same |
| **Repeat curve vs PP003 Berry Crunch** | Reference for "Week-2 1.2x" claim | `household_transactions`, `product_reviews` |
| **Cannibalization of PP001 Vanilla Almond Original** | -11% W1, -6% steady-state | `perfect_store` (PP001 velocity), `household_transactions` (`Switching_Flag = 'Cannibalization'`) |
| **Source-of-volume** | 53% new-to-brand, 32% cannibalization, 15% competitor switch | `household_transactions.Switching_Flag` |
| **Hugo Lin retail-media budget** | $4.2M [sample] Q2 | `seeds/marketing_spend.csv`, `seeds/proteinpeak_q2_launch.csv` |
| **Sage Park athlete cohort** | CR-0012 anchor + CR-0007/0021/0040/0042/0013 | `creator_posts`, `seeds/creators.csv` |
| **Week-4 read date** | 2026-05-22 Friday (Whitfield meeting Tues 2026-05-26) | `seeds/proteinpeak_q2_launch.csv` event PP-E015 |

All anchors are validated by the cross-table assertions in `generator/generate.py::assert_consistency()`.

---

## Coexistence with Louisiana decline

Both scenarios run inside the same synthetic dataset. They don't conflict:

- **Different brands** — LA decline is about Crunchwell; ProteinPeak launch is about ProteinPeak. They share Maya as the analyst but use different SKU IDs, different retailers, and different data windows for their primary signals.
- **Overlapping calendar** — LA decline peaks in Q1 2026; PP launch starts Q2 2026. April-May 2026 is where both stories are present: Maya is balancing the LA recovery plan (Leg 1 starts May 25, 2026) and the Week-4 launch read (Friday May 22, 2026).
- **Shared instrumentation** — Both scenarios use the same data sources (NielsenIQ, Numerator, Walmart Luminate, Brandwatch, Tribe Dynamics, Bazaarvoice, SAP, Spate, Helium 10) and the same cast of supporting characters (Diane, Audrey, Whitfield, Soo-jin, Nina, Robert).

See [`docs/narrative-anchors.md`](../narrative-anchors.md) for the cross-scenario constants list.
