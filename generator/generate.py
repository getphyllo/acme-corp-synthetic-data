"""
Acme Corp synthetic-data generator.

One run produces:
  - data/*.parquet                — sixteen tables (Kellogg-shape, US-anchored)
  - samples/*.csv                  — 100-row CSV slices for previewing
  - acme.duckdb                    — single-file SQL database with everything loaded

The narrative is encoded across two layered scenarios (see docs/narrative-anchors.md):

  Scenario 1 — Louisiana Cereal Decline (Q1 2026)
  -----------------------------------------------
  - Crunchwell LA share drops from ~6% (2024) to ~3.0% (Q1 2026, -340 bps)
  - Walmart Sept 2025 modular reset: Crunchwell Mega/Honey Nut Mega/Multigrain
    lose 2 facings (8 → 6) at Walmart stores in the South division
  - Hurricane Tonya (Nov 8, 2025) drops Crunchwell Mega OSA in LA from ~97% to ~67%
  - Field & Honey heavy promo at Rouses Q4 '25 → Q1 '26
  - LA Crunchwell-loyal HHs flagged with Switching_Flag = "Yes"

  Scenario 2 — ProteinPeak Q2 2026 Launch Read
  ---------------------------------------------
  - ProteinPeak Cinnamon Crunch (PP005) + Cocoa Almond (PP006) co-launch 2026-04-20
  - Trial 113% of plan in Target endcap, 78% of plan in Walmart-pilot (mass)
  - Repeat curve at Week 2 = 1.2x Berry Crunch (PP003) at the same week-since-launch
  - Cannibalization of PP001 Vanilla Almond Original = ~6% steady-state (~11% W1 dip)
  - $4.2M [sample] retail-media budget (Hugo Lin / Tasha Brooks Pacvue)
  - Sage Park's athlete cohort drives creator activation (CR-0012 anchor + cohort)
  - Week-4 read scheduled for Friday May 22, 2026; Whitfield meeting Tues May 26
  - HH Switching_Flag adds value "Cannibalization" (PP001 -> PP005/PP006)

Reproducible — `random.seed(42)`. Run:
    python3 generator/generate.py
"""

from __future__ import annotations

import csv
import io
import os
import random
from datetime import date, datetime, timedelta

import pandas as pd

random.seed(42)

# -----------------------------------------------------------------------------
# Narrative constants — shared across all generators
# -----------------------------------------------------------------------------
# Louisiana decline (Scenario 1)
LA_DECLINE_START      = date(2025, 9, 15)   # Walmart reset
HURRICANE_TONYA_START = date(2025, 11, 8)
HURRICANE_TONYA_END   = date(2025, 12, 15)
LARKSFIELD_PROMO_START = date(2025, 10, 13)

# ProteinPeak Q2 2026 launch (Scenario 2)
PP_Q2_LAUNCH_DATE     = date(2026, 4, 20)   # PP005 + PP006 on-shelf
PP_Q2_WEEK4_DATE      = date(2026, 5, 18)   # Week-4 read window
PP_Q2_NEW_SKUS        = ("PP005", "PP006")
PP_Q2_CANNIBALIZED    = "PP001"             # Vanilla Almond Original
PP_Q2_REFERENCE_SKU   = "PP003"             # Berry Crunch (historical compare)
PP_Q2_TARGET_TRIAL_INDEX = 1.13   # 113% of plan in Target
PP_Q2_MASS_TRIAL_INDEX   = 0.78   # 78% of plan in Mass (Walmart-pilot)

# Global data window — extended to 2026-05-31 to cover the ProteinPeak Q2 launch
DATA_END_DATE         = date(2026, 5, 31)

# Repo root is the parent of this script's directory
REPO_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR   = os.path.join(REPO_ROOT, "data")
SAMPLE_DIR = os.path.join(REPO_ROOT, "samples")
DUCKDB_PATH = os.path.join(REPO_ROOT, "acme.duckdb")
SEEDS_DIR  = os.path.join(REPO_ROOT, "seeds")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SAMPLE_DIR, exist_ok=True)


# -----------------------------------------------------------------------------
# Anchor data
# -----------------------------------------------------------------------------

SKUS = [
    ("CR001", "Crunchwell Original Family 14oz",   "Crunchwell",  "RTE Cereal", "Family Oat",        14, 4.29),
    ("CR002", "Crunchwell Original Mega 18oz",     "Crunchwell",  "RTE Cereal", "Family Oat",        18, 5.49),
    ("CR003", "Crunchwell Honey Nut 14oz",         "Crunchwell",  "RTE Cereal", "Family Sweet",      14, 4.49),
    ("CR004", "Crunchwell Honey Nut Mega 18oz",    "Crunchwell",  "RTE Cereal", "Family Sweet",      18, 5.69),
    ("CR005", "Crunchwell Multigrain 13oz",        "Crunchwell",  "RTE Cereal", "Family Wholegrain", 13, 4.49),
    ("CR006", "Crunchwell Cinnamon Twist 14oz",    "Crunchwell",  "RTE Cereal", "Family Sweet",      14, 4.59),
    ("CR007", "Crunchwell Berry Burst 13oz",       "Crunchwell",  "RTE Cereal", "Family Sweet",      13, 4.69),
    ("HN001", "HoneyNest Original 12oz",           "HoneyNest",   "RTE Cereal", "Kids Sweet",        12, 4.29),
    ("HN003", "HoneyNest Chocolate 12oz",          "HoneyNest",   "RTE Cereal", "Kids Sweet",        12, 4.39),
    ("HN007", "HoneyNest Frosted Flakes 14oz",     "HoneyNest",   "RTE Cereal", "Kids Sweet",        14, 4.59),
    ("PP001", "ProteinPeak Vanilla Almond Original 12oz", "ProteinPeak", "RTE Cereal", "Wellness Protein",  12, 7.49),
    ("PP002", "ProteinPeak Chocolate Hazelnut",    "ProteinPeak", "RTE Cereal", "Wellness Protein",  12, 7.49),
    ("PP003", "ProteinPeak Berry Crunch 12oz",     "ProteinPeak", "RTE Cereal", "Wellness Protein",  12, 7.49),
    ("PP005", "ProteinPeak Cinnamon Crunch 12oz",  "ProteinPeak", "RTE Cereal", "Wellness Protein",  12, 7.49),
    ("PP006", "ProteinPeak Cocoa Almond 12oz",     "ProteinPeak", "RTE Cereal", "Wellness Protein",  12, 7.49),
    ("MO001", "MorningOats Instant Original 8ct",  "MorningOats", "Hot Cereal", "Instant",           12, 4.99),
    ("MO004", "MorningOats Cup Maple",             "MorningOats", "Hot Cereal", "Single-Serve",      1.7, 2.49),
    ("MO007", "MorningOats Steel Cut 30oz",        "MorningOats", "Hot Cereal", "Steel-Cut",         30, 7.99),
    ("TG001", "TrailGrove Honey Almond 12oz",      "TrailGrove",  "Granola",    "Granola Pouch",     12, 6.49),
    ("TG002", "TrailGrove PB Chocolate 12oz",      "TrailGrove",  "Granola",    "Granola Pouch",     12, 6.49),
    ("TG007", "TrailGrove Bars Honey Almond",      "TrailGrove",  "Bar",        "Granola Bar",       7.5, 5.49),
    ("RD001", "RootDay Oat Milk Original 32oz",    "RootDay",     "Plant-Based Milk", "Oat",         32, 4.99),
    ("RD002", "RootDay Oat Milk Barista 32oz",     "RootDay",     "Plant-Based Milk", "Oat",         32, 5.49),
]

COMP_SKUS = [
    ("GM001", "Cheerios 12oz",                    "Cheerios",            "General Mills", "RTE Cereal", "Family Oat",   12, 4.29),
    ("GM002", "Honey Nut Cheerios 14oz",          "Honey Nut Cheerios",  "General Mills", "RTE Cereal", "Family Sweet", 14, 4.49),
    ("PF001", "Field & Honey 14oz",               "Field & Honey",       "Larksfield Foods", "RTE Cereal", "Family Sweet", 14, 4.39),
    ("PF002", "Harvest Hearth 14oz",              "Harvest Hearth",      "Larksfield Foods", "RTE Cereal", "Family Wholegrain", 14, 4.79),
    ("KL001", "Frosted Flakes 13.5oz",            "Frosted Flakes",      "Kellanova",     "RTE Cereal", "Kids Sweet",   13.5, 4.59),
    ("PL001", "GV Honey Toasted Oats 14oz",       "Great Value",         "Walmart PL",    "RTE Cereal", "Family Sweet", 14, 2.89),
    ("PL002", "GV Toasted Oats Original 14oz",    "Great Value",         "Walmart PL",    "RTE Cereal", "Family Oat",   14, 2.69),
    ("QT001", "Quaker Old Fashioned 18oz",        "Quaker",              "PepsiCo",       "Hot Cereal", "Steel-Cut",    18, 5.99),
]

RETAILERS = [
    ("Walmart",       "Mass",              "Hypermarket",       "L"),
    ("Target",        "Mass",              "Hypermarket",       "L"),
    ("Kroger",        "Grocery",           "Supermarket",       "M"),
    ("Albertsons",    "Grocery",           "Supermarket",       "M"),
    ("Publix",        "Grocery",           "Supermarket",       "M"),
    ("H-E-B",         "Grocery",           "Supermarket",       "L"),
    ("Rouses",        "Grocery",           "Supermarket",       "M"),
    ("Brookshires",   "Grocery",           "Supermarket",       "S"),
    ("Winn-Dixie",    "Grocery",           "Supermarket",       "S"),
    ("Costco",        "Club",              "Hypermarket",       "L"),
    ("Sams Club",     "Club",              "Hypermarket",       "L"),
    ("Sprouts",       "Grocery Premium",   "Supermarket",       "M"),
    ("Whole Foods",   "Grocery Premium",   "Supermarket",       "M"),
    ("Wegmans",       "Grocery",           "Supermarket",       "M"),
    ("Meijer",        "Grocery",           "Hypermarket",       "L"),
    ("Aldi",          "Discount Grocery",  "Supermarket",       "S"),
    ("CVS",           "Drug",              "Convenience",       "S"),
    ("Walgreens",     "Drug",              "Convenience",       "S"),
    ("7-Eleven",      "Convenience",       "Convenience",       "S"),
    ("Amazon",        "E-commerce",        "Online",            "L"),
    ("Walmart.com",   "E-commerce",        "Online",            "L"),
    ("Target.com",    "E-commerce",        "Online",            "L"),
    ("Instacart",     "E-commerce",        "Online",            "S"),
]

DMAS = [
    ("LA-DMA",  "Louisiana DMA",       "Southeast", 4.65,  76, 0.020),
    ("DAL",     "Dallas-Fort Worth",   "Southwest", 7.85, 108, 0.045),
    ("HOU",     "Houston",             "Southwest", 7.21, 113, 0.045),
    ("ATL",     "Atlanta",             "Southeast", 6.32,  89, 0.040),
    ("CHI",     "Chicago",             "Midwest",   9.49, 141, 0.062),
    ("NYC",     "New York",            "Northeast", 19.62, 71, 0.090),
    ("LAX",     "Los Angeles",         "West",      13.26, 94, 0.080),
    ("MIN",     "Minneapolis",         "Midwest",   3.69, 138, 0.030),
    ("DEN",     "Denver",              "Mountain",  3.00,  88, 0.025),
    ("PHX",     "Phoenix",             "Mountain",  5.07,  90, 0.035),
    ("SEA",     "Seattle-Tacoma",      "PNW",       4.07, 121, 0.030),
    ("BOS",     "Boston",              "Northeast", 4.94,  74, 0.030),
    ("PHL",     "Philadelphia",        "Northeast", 6.20,  79, 0.040),
    ("DET",     "Detroit",             "Midwest",   4.32, 132, 0.030),
    ("MIA",     "Miami-Fort Lauderdale","Southeast",6.25,  85, 0.040),
    ("MS-DMA",  "Mississippi DMA",     "Southeast", 2.94,  82, 0.018),
    ("AL-DMA",  "Alabama DMA",         "Southeast", 5.07,  86, 0.025),
    ("AR-DMA",  "Arkansas DMA",        "Southwest", 3.05, 103, 0.020),
    ("OK-DMA",  "Oklahoma DMA",        "Southwest", 3.99,  92, 0.024),
    ("ORL",     "Orlando-Daytona",     "Southeast", 4.20,  86, 0.030),
    ("CIN",     "Cincinnati",          "Midwest",   2.27, 132, 0.022),
    ("STL",     "St. Louis",           "Midwest",   2.81, 122, 0.025),
    ("KAN",     "Kansas City",         "Midwest",   2.20, 115, 0.020),
    ("PIT",     "Pittsburgh",          "Northeast", 2.32,  84, 0.020),
    ("PDX",     "Portland OR",         "PNW",       2.51, 116, 0.020),
    ("SFO",     "San Francisco",       "West",      4.66,  98, 0.040),
    ("CLE",     "Cleveland",           "Midwest",   2.10, 114, 0.018),
    ("IND",     "Indianapolis",        "Midwest",   2.11, 124, 0.018),
    ("BAL",     "Baltimore",           "Northeast", 2.85,  82, 0.022),
    ("WAS",     "Washington DC",       "Northeast", 6.39,  85, 0.045),
    # v0.7.0 — leading-indicator DMAs (early-stage LA pattern: Larksfield
    # endcap activation up, Crunchwell Mega velocity softening). Lower volume
    # weights — they are watch-list, not full-volume DMAs yet.
    ("BIR-DMA", "Birmingham-Tuscaloosa-Anniston DMA", "Southeast", 2.21, 88, 0.012),
    ("MEM-DMA", "Memphis DMA",         "Southeast", 1.81, 85, 0.010),
]

DMA_CITIES = {
    "LA-DMA":  ["New Orleans", "Baton Rouge", "Lafayette", "Lake Charles", "Shreveport"],
    "DAL":     ["Dallas", "Fort Worth", "Plano", "Arlington"],
    "HOU":     ["Houston", "Sugar Land", "Pasadena", "The Woodlands"],
    "ATL":     ["Atlanta", "Marietta", "Alpharetta", "Decatur"],
    "CHI":     ["Chicago", "Naperville", "Schaumburg", "Evanston"],
    "NYC":     ["New York", "Brooklyn", "Queens", "Newark", "Jersey City"],
    "LAX":     ["Los Angeles", "Long Beach", "Anaheim", "Pasadena CA"],
    "MIN":     ["Minneapolis", "St Paul", "Bloomington"],
    "DEN":     ["Denver", "Aurora", "Lakewood"],
    "PHX":     ["Phoenix", "Scottsdale", "Mesa", "Tempe"],
    "SEA":     ["Seattle", "Tacoma", "Bellevue"],
    "BOS":     ["Boston", "Cambridge", "Worcester"],
    "PHL":     ["Philadelphia", "Camden", "Wilmington"],
    "DET":     ["Detroit", "Ann Arbor", "Warren"],
    "MIA":     ["Miami", "Fort Lauderdale", "Hollywood FL"],
    "MS-DMA":  ["Jackson MS", "Gulfport", "Hattiesburg"],
    "AL-DMA":  ["Birmingham", "Huntsville", "Mobile"],
    "AR-DMA":  ["Little Rock", "Fayetteville", "Bentonville"],
    "OK-DMA":  ["Oklahoma City", "Tulsa", "Norman"],
    "ORL":     ["Orlando", "Daytona Beach", "Lakeland"],
    "CIN":     ["Cincinnati", "Dayton", "Hamilton"],
    "STL":     ["St Louis", "St Charles"],
    "KAN":     ["Kansas City", "Overland Park"],
    "PIT":     ["Pittsburgh", "Monroeville"],
    "PDX":     ["Portland", "Beaverton", "Hillsboro"],
    "SFO":     ["San Francisco", "Oakland", "San Jose"],
    "CLE":     ["Cleveland", "Akron"],
    "IND":     ["Indianapolis", "Carmel"],
    "BAL":     ["Baltimore", "Annapolis"],
    "WAS":     ["Washington", "Arlington VA", "Alexandria"],
    # v0.7.0 — leading-indicator DMAs
    "BIR-DMA": ["Birmingham", "Tuscaloosa", "Anniston"],
    "MEM-DMA": ["Memphis", "Germantown", "Collierville"],
}

DMA_STATE = {
    "LA-DMA":"LA","DAL":"TX","HOU":"TX","ATL":"GA","CHI":"IL","NYC":"NY","LAX":"CA",
    "MIN":"MN","DEN":"CO","PHX":"AZ","SEA":"WA","BOS":"MA","PHL":"PA","DET":"MI",
    "MIA":"FL","MS-DMA":"MS","AL-DMA":"AL","AR-DMA":"AR","OK-DMA":"OK","ORL":"FL",
    "CIN":"OH","STL":"MO","KAN":"MO","PIT":"PA","PDX":"OR","SFO":"CA","CLE":"OH",
    "IND":"IN","BAL":"MD","WAS":"DC",
    # v0.7.0
    "BIR-DMA":"AL","MEM-DMA":"TN",
}

# -----------------------------------------------------------------------------
# Banner division / region mapping (v0.2.0)
# -----------------------------------------------------------------------------
# Maps (retailer_chain, DMA) → (banner_division, banner_region) so divisional
# rollups become possible (e.g., "Walmart South", "Kroger Cincinnati", "H-E-B
# Houston"). Encoded narrative: Walmart South division was hit hardest by the
# Sept 2025 cereal modular reset.

WMT_DMA_DIVISION = {
    "LA-DMA": ("Walmart Division 1 - South", "Walmart South"),
    "MS-DMA": ("Walmart Division 1 - South", "Walmart South"),
    "AL-DMA": ("Walmart Division 1 - South", "Walmart South"),
    "AR-DMA": ("Walmart Division 1 - South", "Walmart South"),
    "ATL":    ("Walmart Division 1 - South", "Walmart South"),
    "DAL":    ("Walmart Division 2 - Southwest", "Walmart Southwest"),
    "HOU":    ("Walmart Division 2 - Southwest", "Walmart Southwest"),
    "OK-DMA": ("Walmart Division 2 - Southwest", "Walmart Southwest"),
    "ORL":    ("Walmart Division 1 - South", "Walmart South"),
    "MIA":    ("Walmart Division 1 - South", "Walmart South"),
    "CHI":    ("Walmart Division 3 - Midwest", "Walmart Midwest"),
    "DET":    ("Walmart Division 3 - Midwest", "Walmart Midwest"),
    "MIN":    ("Walmart Division 3 - Midwest", "Walmart Midwest"),
    "CIN":    ("Walmart Division 3 - Midwest", "Walmart Midwest"),
    "STL":    ("Walmart Division 3 - Midwest", "Walmart Midwest"),
    "KAN":    ("Walmart Division 3 - Midwest", "Walmart Midwest"),
    "CLE":    ("Walmart Division 3 - Midwest", "Walmart Midwest"),
    "IND":    ("Walmart Division 3 - Midwest", "Walmart Midwest"),
    "NYC":    ("Walmart Division 4 - Northeast", "Walmart Northeast"),
    "BOS":    ("Walmart Division 4 - Northeast", "Walmart Northeast"),
    "PHL":    ("Walmart Division 4 - Northeast", "Walmart Northeast"),
    "PIT":    ("Walmart Division 4 - Northeast", "Walmart Northeast"),
    "BAL":    ("Walmart Division 4 - Northeast", "Walmart Northeast"),
    "WAS":    ("Walmart Division 4 - Northeast", "Walmart Northeast"),
    "LAX":    ("Walmart Division 5 - West", "Walmart West"),
    "SFO":    ("Walmart Division 5 - West", "Walmart West"),
    "SEA":    ("Walmart Division 5 - West", "Walmart West"),
    "PDX":    ("Walmart Division 5 - West", "Walmart West"),
    "PHX":    ("Walmart Division 5 - West", "Walmart West"),
    "DEN":    ("Walmart Division 5 - West", "Walmart West"),
}

KR_DMA_DIVISION = {
    "CIN":    ("Kroger Cincinnati", "Kroger Midwest"),
    "CLE":    ("Kroger Columbus", "Kroger Midwest"),
    "IND":    ("Kroger Cincinnati", "Kroger Midwest"),
    "ATL":    ("Kroger Atlanta", "Kroger Southeast"),
    "AL-DMA": ("Kroger Atlanta", "Kroger Southeast"),
    "DAL":    ("Kroger Dallas", "Kroger Southwest"),
    "HOU":    ("Kroger Houston", "Kroger Southwest"),
    "WAS":    ("Kroger Mid-Atlantic", "Kroger Mid-Atlantic"),
    "BAL":    ("Kroger Mid-Atlantic", "Kroger Mid-Atlantic"),
    "DEN":    ("Kroger King Soopers", "Kroger Mountain"),
    "PHX":    ("Kroger Smith's", "Kroger West"),
    "LAX":    ("Kroger Ralphs", "Kroger West"),
    "SFO":    ("Kroger Ralphs", "Kroger West"),
    "PDX":    ("Kroger Fred Meyer", "Kroger West"),
    "SEA":    ("Kroger Fred Meyer", "Kroger West"),
    "CHI":    ("Kroger Mariano's", "Kroger Midwest"),
    "MS-DMA": ("Kroger Delta", "Kroger South"),
    "AR-DMA": ("Kroger Delta", "Kroger South"),
    "LA-DMA": ("Kroger Delta", "Kroger South"),
    "OK-DMA": ("Kroger Dallas", "Kroger Southwest"),
    "STL":    ("Kroger Cincinnati", "Kroger Midwest"),
    "MIN":    ("Kroger Cincinnati", "Kroger Midwest"),
    "DET":    ("Kroger Columbus", "Kroger Midwest"),
    "KAN":    ("Kroger Cincinnati", "Kroger Midwest"),
    "PIT":    ("Kroger Mid-Atlantic", "Kroger Mid-Atlantic"),
    "PHL":    ("Kroger Mid-Atlantic", "Kroger Mid-Atlantic"),
    "MIA":    ("Kroger Atlanta", "Kroger Southeast"),
    "ORL":    ("Kroger Atlanta", "Kroger Southeast"),
    "BOS":    ("Kroger Mid-Atlantic", "Kroger Mid-Atlantic"),
    "NYC":    ("Kroger Mid-Atlantic", "Kroger Mid-Atlantic"),
}

TGT_REGION = {
    "Eastern":  ["NYC","BOS","PHL","ATL","MIA","ORL","BAL","WAS","PIT","AL-DMA","MS-DMA"],
    "Central":  ["CHI","DET","DAL","HOU","MIN","CIN","STL","KAN","DEN","IND","CLE","LA-DMA","AR-DMA","OK-DMA"],
    "Western":  ["LAX","SFO","SEA","PDX","PHX"],
}

ALB_REGION = {
    "Albertsons Southwest":   ["PHX","DAL","HOU","OK-DMA"],
    "Albertsons Northwest":   ["SEA","PDX"],
    "Albertsons West":        ["LAX","SFO"],
    "Albertsons East":        ["NYC","PHL","WAS","BAL","BOS","PIT"],
    "Albertsons Mountain":    ["DEN"],
}

HEB_REGION = {
    "H-E-B South Texas":  ["HOU"],
    "H-E-B Central Texas":["DAL","HOU"],
    "H-E-B North Texas":  ["DAL"],
}

PUB_REGION = {
    "Publix Florida":  ["MIA","ORL"],
    "Publix Georgia":  ["ATL","AL-DMA"],
    "Publix Alabama":  ["AL-DMA"],
}

ROU_REGION = {
    "Rouses NOLA":          ["LA-DMA"],
    "Rouses Baton Rouge":   ["LA-DMA"],
    "Rouses Lafayette":     ["LA-DMA"],
    "Rouses Alabama Coast": ["MS-DMA","AL-DMA"],
}

COS_REGION = {
    "Costco Northeast": ["NYC","BOS","PHL","PIT","BAL","WAS"],
    "Costco Southeast": ["MIA","ATL","LA-DMA","AL-DMA","MS-DMA","ORL"],
    "Costco Central":   ["CHI","DET","CIN","STL","KAN","MIN","CLE","IND"],
    "Costco West":      ["LAX","SFO","SEA","PDX","PHX","DEN"],
    "Costco Texas":     ["DAL","HOU","OK-DMA","AR-DMA"],
}


def _first_match_region(map_, dma):
    for region, dmas in map_.items():
        if dma in dmas:
            return region
    return None


def assign_banner(chain: str, dma: str) -> tuple[str, str]:
    """Return (banner_division, banner_region) for a (chain, DMA) pair.

    Falls back to ('National', '<chain> National') if no specific division is
    mapped — keeps the column populated even for retailers without explicit
    divisional structure.
    """
    if chain == "Walmart":
        d = WMT_DMA_DIVISION.get(dma)
        return d if d else ("Walmart National", "Walmart National")
    if chain == "Kroger":
        d = KR_DMA_DIVISION.get(dma)
        return d if d else ("Kroger National", "Kroger National")
    if chain == "Target":
        for region, dmas in TGT_REGION.items():
            if dma in dmas:
                return (f"Target {region}", f"Target {region}")
        return ("Target National", "Target National")
    if chain == "Albertsons":
        r = _first_match_region(ALB_REGION, dma)
        return (r, r) if r else ("Albertsons National", "Albertsons National")
    if chain == "H-E-B":
        r = _first_match_region(HEB_REGION, dma)
        return (r, r) if r else ("H-E-B Other", "H-E-B Other")
    if chain == "Publix":
        r = _first_match_region(PUB_REGION, dma)
        return (r, r) if r else ("Publix Other", "Publix Other")
    if chain == "Rouses":
        r = _first_match_region(ROU_REGION, dma)
        return (r, r) if r else ("Rouses Other", "Rouses Other")
    if chain == "Costco":
        r = _first_match_region(COS_REGION, dma)
        return (r, r) if r else ("Costco National", "Costco National")
    if chain == "Sams Club":
        return ("Sams Club National", "Sams Club National")
    if chain in ("Brookshires",):
        return ("Brookshire's Texas-Louisiana", "Brookshire's Southwest")
    if chain in ("Winn-Dixie",):
        return ("Winn-Dixie Southeast", "Winn-Dixie Southeast")
    if chain in ("Sprouts",):
        return ("Sprouts National", "Sprouts National")
    if chain in ("Whole Foods",):
        return ("Whole Foods National", "Whole Foods National")
    if chain in ("Wegmans",):
        return ("Wegmans Northeast", "Wegmans Northeast")
    if chain in ("Meijer",):
        return ("Meijer Midwest", "Meijer Midwest")
    if chain in ("Aldi","Lidl"):
        return (f"{chain} National", f"{chain} National")
    if chain in ("CVS","Walgreens","7-Eleven"):
        return (f"{chain} National", f"{chain} National")
    if chain in ("Amazon","Walmart.com","Target.com","Instacart"):
        return (f"{chain} E-Commerce", f"{chain} E-Commerce")
    return (f"{chain} National", f"{chain} National")


PROMO_TYPES = ["None", "Price Off", "Multi-Buy", "Bundle", "Loyalty"]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "Cash", "Mobile Pay", "EBT"]
INCOME_BANDS = ["<30K", "30-50K", "50-75K", "75-100K", "100-150K", "150K+"]
EDU_LEVELS = ["High School", "Some College", "Bachelors", "Graduate"]
MARITAL = ["Single", "Married", "Divorced", "Widowed"]
ETHNICITY = ["Hispanic", "Non-Hispanic White", "Non-Hispanic Black", "Asian", "Other"]
URBANICITY = ["Urban", "Suburban", "Rural"]
LOYALTY_SEG = ["Acme Loyal", "Multi-Brand Switcher", "Competitor Loyal", "Light Buyer"]
PRICE_SEG = ["Low", "Medium", "High"]
ADOPTER = ["Innovator", "Early Adopter", "Mainstream", "Late Mainstream", "Laggard"]


def weighted_choice(pairs):
    items, weights = zip(*pairs)
    return random.choices(items, weights=weights, k=1)[0]


# -----------------------------------------------------------------------------
# 1. EPOS
# -----------------------------------------------------------------------------

def gen_epos(n_rows=30000):
    sku_pool = []
    for s in SKUS:
        sku_pool.append({"id":s[0], "name":s[1], "brand":s[2], "cat":s[3], "subcat":s[4],
                         "oz":s[5], "price":s[6], "mfr":"Acme Corp"})
    for c in COMP_SKUS:
        sku_pool.append({"id":c[0], "name":c[1], "brand":c[2], "cat":c[4], "subcat":c[5],
                         "oz":c[6], "price":c[7], "mfr":c[3]})

    dma_weights = [(d[0], d[5]) for d in DMAS]
    start, end = date(2024, 1, 1), DATA_END_DATE
    days = (end - start).days
    rows = []
    for i in range(1, n_rows+1):
        d_offset = random.randint(0, days)
        tx_date = start + timedelta(days=d_offset)
        hour = random.choices(range(7, 23),
                              weights=[3,5,8,10,15,18,15,10,8,7,7,6,5,4,3,2])[0]
        dt = datetime(tx_date.year, tx_date.month, tx_date.day,
                      hour, random.randint(0,59), random.randint(0,59))

        dma_id = weighted_choice(dma_weights)
        city = random.choice(DMA_CITIES[dma_id])
        state = DMA_STATE[dma_id]

        retailer = random.choice(RETAILERS)
        chain, channel, store_type = retailer[0], retailer[1], retailer[2]
        store_id = f"{chain[:3].upper()}{random.randint(1000,9999)}"
        banner_division, banner_region = assign_banner(chain, dma_id)

        sku = random.choice(sku_pool)

        # ProteinPeak Q2 launch gating: PP005/PP006 don't exist before launch date.
        # On/after launch, they're available primarily at the launch retailers.
        if sku["id"] in PP_Q2_NEW_SKUS:
            if tx_date < PP_Q2_LAUNCH_DATE:
                # Pre-launch — re-roll to another Acme/competitor SKU
                sku = random.choice([s for s in sku_pool if s["id"] not in PP_Q2_NEW_SKUS])
            else:
                # Launch retailer gating: ~85% chance at launch retailers, else re-roll
                pp_retailers = ("Target","Whole Foods","Sprouts","Amazon","Target.com",
                                "Kroger","Walmart")  # Walmart-pilot
                if chain not in pp_retailers and random.random() < 0.7:
                    sku = random.choice([s for s in sku_pool if s["id"] not in PP_Q2_NEW_SKUS])

        qty = random.choices([1,2,3,4], weights=[60,25,10,5])[0]
        base = sku["price"]

        promo_flag, promo_type, disc = "No", "None", 0.0
        if random.random() < 0.22:
            promo_flag, promo_type = "Yes", random.choice(["Price Off","Multi-Buy","Bundle","Loyalty"])
            disc = round(random.uniform(0.05, 0.30), 2)
        if (sku["brand"] == "Field & Honey" and chain in ("Rouses","Brookshires")
                and dma_id == "LA-DMA" and tx_date >= date(2025,10,1)):
            if random.random() < 0.85:
                promo_flag, promo_type, disc = "Yes", "Price Off", 0.21
        if sku["id"] in ("CR002","CR004","CR005") and dma_id == "LA-DMA":
            if date(2025,11,8) <= tx_date <= date(2025,12,15):
                if random.random() < 0.55:
                    sku = random.choice([s for s in sku_pool if s["brand"] == "Field & Honey"])

        # ProteinPeak launch promo flags (Target endcap + Amazon coupon)
        if sku["id"] in PP_Q2_NEW_SKUS and tx_date >= PP_Q2_LAUNCH_DATE:
            if chain == "Target" and random.random() < 0.85:
                # On endcap — display flag without depth (launch is full-price endcap)
                promo_flag, promo_type, disc = "Yes", "Display", 0.0
            elif chain == "Amazon" and random.random() < 0.65:
                promo_flag, promo_type, disc = "Yes", "Price Off", 0.08
            elif chain in ("Whole Foods","Sprouts") and random.random() < 0.55:
                promo_flag, promo_type, disc = "Yes", "Price Off", 0.06

        unit_price = round(base * (1 - disc), 2)
        seas = "None"
        m = tx_date.month
        if m in (8,9): seas = "BackToSchool"
        elif m in (11,12): seas = "Holiday"
        elif m == 4: seas = "Easter"
        elif m == 2 and tx_date.day < 15: seas = "SuperBowl"

        rows.append({
            "Transaction_ID": f"TXN{i:07d}",
            "Date_Time": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "Country":"United States", "Country_Code":"USA",
            "State":state, "DMA":dma_id, "City":city,
            "Retail_Chain":chain, "Banner_Division":banner_division, "Banner_Region":banner_region,
            "Store_Type":store_type, "Store_ID":store_id,
            "Customer_ID": f"C{random.randint(100000,999999)}",
            "Product_SKU":sku["id"], "Product_Name":sku["name"],
            "Brand":sku["brand"], "Manufacturer":sku["mfr"],
            "Product_Category":sku["cat"],
            "Quantity_Sold":qty, "Currency":"USD",
            "Unit_Price_Local":base, "Total_Sale_Amount":round(base*qty,2),
            "Discount_Percent":disc, "Final_Sale_Amount":round(unit_price*qty,2),
            "Promotion_Type":promo_type, "Promotion_Flag":promo_flag,
            "Payment_Method":random.choice(PAYMENT_METHODS),
            "Weekday":tx_date.strftime("%A"), "Month":tx_date.month,
            "Hour":hour, "Seasonality_Flag":seas,
        })
    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# 2. Perfect Store
# -----------------------------------------------------------------------------

def gen_perfect_store(n_rows=50000):
    sku_pool = []
    for s in SKUS:
        sku_pool.append({"id":s[0], "name":s[1], "brand":s[2], "cat":s[3],
                         "oz":s[5], "price":s[6], "mfr":"Acme Corp"})
    for c in COMP_SKUS:
        sku_pool.append({"id":c[0], "name":c[1], "brand":c[2], "cat":c[4],
                         "oz":c[6], "price":c[7], "mfr":c[3]})

    stores = []
    for i in range(600):
        retailer = random.choice(RETAILERS)
        dma_id = weighted_choice([(d[0], d[5]) for d in DMAS])
        city = random.choice(DMA_CITIES[dma_id])
        state = DMA_STATE[dma_id]
        size = random.choices(["S","M","L"], weights=[35,45,20])[0]
        bd, br = assign_banner(retailer[0], dma_id)
        stores.append({"id":f"{retailer[0][:3].upper()}{1000+i}",
                       "chain":retailer[0], "channel":retailer[1], "store_type":retailer[2],
                       "size":size, "dma":dma_id, "state":state, "city":city,
                       "banner_division":bd, "banner_region":br})

    start, end = date(2025, 1, 1), DATA_END_DATE
    days = (end - start).days
    rows = []
    for _ in range(n_rows):
        d = start + timedelta(days=random.randint(0, days))
        store = random.choice(stores)
        sku = random.choice(sku_pool)

        # ProteinPeak Q2 launch gating in perfect_store
        if sku["id"] in PP_Q2_NEW_SKUS:
            if d < PP_Q2_LAUNCH_DATE:
                sku = random.choice([s for s in sku_pool if s["id"] not in PP_Q2_NEW_SKUS])
            elif store["chain"] not in ("Target","Whole Foods","Sprouts","Amazon","Target.com",
                                          "Walmart.com","Kroger","Walmart") and random.random() < 0.92:
                sku = random.choice([s for s in sku_pool if s["id"] not in PP_Q2_NEW_SKUS])

        unit_price = round(sku["price"] * random.uniform(0.92, 1.05), 2)

        promo_flag, promo_type, promo_depth = "No", "None", 0
        if random.random() < 0.18:
            promo_flag, promo_type = "Yes", random.choice(["Price Off","Multi-Buy","Bundle","Loyalty"])
            promo_depth = random.choices([10,15,20,25,30], weights=[30,30,20,15,5])[0]
        if (sku["brand"] == "Field & Honey" and store["chain"] in ("Rouses","Brookshires")
                and store["dma"] == "LA-DMA" and d >= date(2025,10,1)):
            if random.random() < 0.65:
                promo_flag, promo_type, promo_depth = "Yes", "Price Off", 21

        # ProteinPeak Q2 launch — Target endcap, Amazon coupon, Sprouts/WFM TPR
        if sku["id"] in PP_Q2_NEW_SKUS and d >= PP_Q2_LAUNCH_DATE:
            wk_since_launch = (d - PP_Q2_LAUNCH_DATE).days // 7
            if store["chain"] == "Target" and wk_since_launch < 4:
                promo_flag, promo_type, promo_depth = "Yes", "Endcap", 0  # display only
            elif store["chain"] == "Amazon" and random.random() < 0.75:
                promo_flag, promo_type, promo_depth = "Yes", "Price Off", 8
            elif store["chain"] in ("Whole Foods","Sprouts") and random.random() < 0.55:
                promo_flag, promo_type, promo_depth = "Yes", "Price Off", random.choice([5,7])

        base_facings = {"S":4, "M":6, "L":8}[store["size"]]
        facings = base_facings
        if (sku["id"] in ("CR002","CR004","CR005","CR006")
                and store["chain"] == "Walmart" and d >= date(2025,9,15)):
            # Walmart South division hit hardest in Sept 2025 modular reset
            cut = 3 if store.get("banner_region") == "Walmart South" else 2
            facings = max(2, base_facings - cut)
        if sku["brand"] != "Crunchwell" and random.random() < 0.3:
            facings = max(1, base_facings - random.randint(0,3))
        # ProteinPeak Q2 launch facings (full launch shelf at Target endcap; pilot at Walmart)
        if sku["id"] in PP_Q2_NEW_SKUS and d >= PP_Q2_LAUNCH_DATE:
            if store["chain"] == "Target":
                facings = max(facings, 4)  # endcap-supported
            elif store["chain"] == "Walmart":
                facings = max(1, min(base_facings - 2, 3))  # pilot shelf
            elif store["chain"] in ("Whole Foods","Sprouts","Kroger"):
                facings = max(facings, 3)

        osa = random.uniform(95.0, 99.9)
        if sku["id"] in ("CR002","CR004","CR005") and store["dma"] == "LA-DMA":
            if date(2025,11,8) <= d <= date(2025,12,15):
                osa = random.uniform(48.0, 78.0)
            elif d >= date(2025,9,15):
                osa = random.uniform(85.0, 96.0)
        # ProteinPeak Q2 launch — small OSA dip Week 1 due to allocation supply-pull at Target
        if sku["id"] in PP_Q2_NEW_SKUS and d >= PP_Q2_LAUNCH_DATE:
            if store["chain"] == "Target" and (d - PP_Q2_LAUNCH_DATE).days <= 9:
                osa = random.uniform(82.0, 94.0)  # allocation tightness early
            else:
                osa = random.uniform(91.0, 99.0)

        opening = random.randint(0, 300)
        received = random.choices([0,12,24,36,48,72,144], weights=[60,5,8,8,7,7,5])[0]
        # Trial signal: PP005/PP006 in Target sell at 113% of plan velocity;
        # in Walmart-pilot at 78% of plan
        velocity_mu = 8 + facings * 1.5
        if sku["id"] in PP_Q2_NEW_SKUS and d >= PP_Q2_LAUNCH_DATE:
            if store["chain"] == "Target":
                velocity_mu *= PP_Q2_TARGET_TRIAL_INDEX
            elif store["chain"] == "Walmart":
                velocity_mu *= PP_Q2_MASS_TRIAL_INDEX
            elif store["chain"] == "Amazon":
                velocity_mu *= 1.04
            elif store["chain"] in ("Whole Foods","Sprouts"):
                velocity_mu *= 1.08

        # Cannibalization: PP001 velocity dips 11% W1 then ~6% steady-state when
        # PP005/PP006 are on launch endcap at the same retailer
        if sku["id"] == PP_Q2_CANNIBALIZED and d >= PP_Q2_LAUNCH_DATE:
            wk_since_launch = (d - PP_Q2_LAUNCH_DATE).days // 7
            if store["chain"] in ("Target","Amazon","Whole Foods","Sprouts","Kroger"):
                if wk_since_launch == 0:
                    velocity_mu *= 0.89  # -11% W1
                elif wk_since_launch <= 4:
                    velocity_mu *= 0.94  # -6% steady-state
        sales_units = max(0, min(opening + received, int(random.gauss(velocity_mu, 4))))
        closing = max(0, opening + received - sales_units)

        rows.append({
            "Date":d.strftime("%Y-%m-%d"), "Store_ID":store["id"],
            "Country":"United States", "Country_Code":"USA",
            "State":store["state"], "DMA":store["dma"], "City":store["city"],
            "Cluster":store["channel"], "Banner":store["chain"],
            "Banner_Division":store["banner_division"], "Banner_Region":store["banner_region"],
            "Size_Tier":store["size"],
            "SKU":sku["id"], "Product_Description":sku["name"],
            "Brand":sku["brand"], "Manufacturer":sku["mfr"], "Category":sku["cat"],
            "Unit_Price_Local_Proxy":unit_price,
            "Promotion_Flag":promo_flag, "Promotion_Type":promo_type,
            "Promotion_Depth_Pct":promo_depth,
            "Opening_Inventory_Units":opening, "Received_Units":received,
            "Sales_Units":sales_units,
            "Sales_Value":round(sales_units * (unit_price * (1 - promo_depth/100.0)), 2),
            "Closing_Inventory_Units":closing,
            "OSA_Pct":round(osa, 2), "Planogram_Compliance_Pct":round(random.uniform(91.0,100.0),1),
            "Facings":facings,
        })

    # ProteinPeak Q2 launch — dedicated oversample of perfect_store rows so the
    # Week-4 trial-vs-plan story is statistically visible (~1200 rows).
    pp_skus = [s for s in sku_pool if s["id"] in PP_Q2_NEW_SKUS]
    pp_stores = [s for s in stores if s["chain"] in
                 ("Target","Walmart","Amazon","Whole Foods","Sprouts","Kroger","Target.com","Walmart.com")]
    pp_launch_days = (DATA_END_DATE - PP_Q2_LAUNCH_DATE).days
    if pp_stores and pp_skus and pp_launch_days > 0:
        for _ in range(1200):
            d = PP_Q2_LAUNCH_DATE + timedelta(days=random.randint(0, pp_launch_days))
            store = random.choice(pp_stores)
            sku = random.choice(pp_skus)
            unit_price = round(sku["price"] * random.uniform(0.95, 1.02), 2)
            base_facings = {"S":4, "M":6, "L":8}[store["size"]]
            facings = base_facings
            wk_since_launch = (d - PP_Q2_LAUNCH_DATE).days // 7
            promo_flag, promo_type, promo_depth = "No", "None", 0
            if store["chain"] == "Target":
                facings = max(facings, 4)
                if wk_since_launch < 4:
                    promo_flag, promo_type = "Yes", "Endcap"
            elif store["chain"] == "Walmart":
                facings = max(1, min(base_facings - 2, 3))
                if random.random() < 0.18:
                    promo_flag, promo_type, promo_depth = "Yes", "Price Off", 3
            elif store["chain"] == "Amazon":
                promo_flag, promo_type, promo_depth = "Yes", "Price Off", 8
            elif store["chain"] in ("Whole Foods","Sprouts"):
                facings = max(facings, 3)
                if random.random() < 0.55:
                    promo_flag, promo_type, promo_depth = "Yes", "Price Off", random.choice([5,7])
            elif store["chain"] == "Kroger":
                facings = max(facings, 3)
                if random.random() < 0.30:
                    promo_flag, promo_type, promo_depth = "Yes", "Price Off", 5
            osa = random.uniform(82.0, 94.0) if (store["chain"] == "Target" and wk_since_launch <= 1) \
                  else random.uniform(91.0, 99.0)
            velocity_mu = 8 + facings * 1.5
            if store["chain"] == "Target":
                velocity_mu *= PP_Q2_TARGET_TRIAL_INDEX
            elif store["chain"] == "Walmart":
                velocity_mu *= PP_Q2_MASS_TRIAL_INDEX
            elif store["chain"] == "Amazon":
                velocity_mu *= 1.04
            elif store["chain"] in ("Whole Foods","Sprouts"):
                velocity_mu *= 1.08
            opening = random.randint(0, 300)
            received = random.choices([0,12,24,36,48,72,144], weights=[60,5,8,8,7,7,5])[0]
            sales_units = max(0, min(opening + received, int(random.gauss(velocity_mu, 4))))
            closing = max(0, opening + received - sales_units)
            rows.append({
                "Date":d.strftime("%Y-%m-%d"), "Store_ID":store["id"],
                "Country":"United States", "Country_Code":"USA",
                "State":store["state"], "DMA":store["dma"], "City":store["city"],
                "Cluster":store["channel"], "Banner":store["chain"],
                "Banner_Division":store["banner_division"], "Banner_Region":store["banner_region"],
                "Size_Tier":store["size"],
                "SKU":sku["id"], "Product_Description":sku["name"],
                "Brand":sku["brand"], "Manufacturer":sku["mfr"], "Category":sku["cat"],
                "Unit_Price_Local_Proxy":unit_price,
                "Promotion_Flag":promo_flag, "Promotion_Type":promo_type,
                "Promotion_Depth_Pct":promo_depth,
                "Opening_Inventory_Units":opening, "Received_Units":received,
                "Sales_Units":sales_units,
                "Sales_Value":round(sales_units * (unit_price * (1 - promo_depth/100.0)), 2),
                "Closing_Inventory_Units":closing,
                "OSA_Pct":round(osa, 2),
                "Planogram_Compliance_Pct":round(random.uniform(94.0,100.0),1),
                "Facings":facings,
            })

    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# 3. Syndicated Weekly (NielsenIQ-style)
# -----------------------------------------------------------------------------

def gen_syndicated_weekly():
    categories = ["RTE Cereal", "Hot Cereal", "Granola", "Plant-Based Milk", "Bar"]
    channels = ["Mass", "Grocery", "Club", "E-commerce", "Drug & Conv"]
    weeks = []
    week_to_date = {}
    d = date(2024,1,1)
    while d <= DATA_END_DATE:
        wk = d.strftime("%G-W%V")
        if wk not in weeks:
            weeks.append(wk)
            week_to_date[wk] = d
        d += timedelta(days=7)
    pp_launch_week_num = PP_Q2_LAUNCH_DATE.isocalendar()[1]
    rows = []
    for dma in DMAS:
        for cat in categories:
            for ch in channels:
                for wk in weeks:
                    base_value = random.uniform(0.4, 12.0) * dma[3]/5.0
                    crunch_share = random.uniform(0.045, 0.075)
                    if dma[0]=="LA-DMA" and cat=="RTE Cereal":
                        wk_year = int(wk.split("-")[0]); wk_num = int(wk.split("W")[1])
                        if wk_year == 2025 and wk_num >= 36:
                            crunch_share -= 0.012
                        if wk_year == 2025 and wk_num >= 45:
                            crunch_share -= 0.010
                        if wk_year == 2026:
                            crunch_share -= 0.020
                    if cat != "RTE Cereal":
                        crunch_share = 0.0
                    # ProteinPeak Q2 launch — bump the Wellness Protein subcategory
                    # signal in syndicated. Encoded as an Acme_Value_Share lift
                    # for RTE Cereal in the launch weeks.
                    pp_lift = 0.0
                    wk_year = int(wk.split("-")[0]); wk_num = int(wk.split("W")[1])
                    if cat == "RTE Cereal" and wk_year == 2026 and wk_num >= pp_launch_week_num:
                        # Larger lift in Mass/Grocery/E-commerce (the launch channels);
                        # extra boost in Target-skew Mass+E-comm DMAs (national signal)
                        if ch in ("Mass","Grocery","E-commerce"):
                            pp_lift = random.uniform(0.004, 0.010)
                    acme_share = (crunch_share +
                                  (random.uniform(0.012,0.025) if cat=="RTE Cereal"
                                   else random.uniform(0.04,0.10))
                                  + pp_lift)
                    avg_p = round(random.uniform(3.50, 7.20), 2)
                    rows.append({
                        "Country":"United States", "DMA":dma[0], "Region":dma[2],
                        "Category":cat, "Channel":ch, "Week":wk,
                        "Value_USD_MM":round(base_value, 3),
                        "Volume_Units_K":round(base_value * 1000 / avg_p, 1),
                        "Acme_Value_Share":round(acme_share, 4),
                        "Crunchwell_Value_Share":round(crunch_share, 4),
                        "Larksfield_Value_Share":round(random.uniform(0.10,0.18) if cat=="RTE Cereal" else random.uniform(0.0,0.05), 4),
                        "GeneralMills_Value_Share":round(random.uniform(0.20,0.32) if cat=="RTE Cereal" else random.uniform(0.0,0.08), 4),
                        "Kellanova_Value_Share":round(random.uniform(0.18,0.26) if cat=="RTE Cereal" else random.uniform(0.0,0.04), 4),
                        "PL_Value_Share":round(random.uniform(0.06,0.14), 4),
                        "Promo_Share":round(random.uniform(0.18,0.42), 4),
                        "Avg_Price_USD":avg_p,
                        "ACV_Distribution_Pct":round(random.uniform(72.0,96.0), 1),
                        "TDP":int(round(random.uniform(72.0,96.0) * random.uniform(0.85,1.10))),
                        "Avg_Facings":round(random.uniform(3.5,7.5), 1),
                    })
    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# 4. Brand Health
# -----------------------------------------------------------------------------

def gen_brand_health(n_rows=15000):
    waves = ["2024Q1","2024Q2","2024Q3","2024Q4","2025Q1","2025Q2","2025Q3","2025Q4","2026Q1","2026Q2"]
    primary_cats = ["RTE Cereal","Hot Cereal","Granola","Plant-Based Milk","Bar","Snacks"]
    competitors = ["Cheerios","Field & Honey","Frosted Flakes","Quaker","Great Value PL","Magic Spoon","Kashi"]
    rows = []
    for i in range(1, n_rows+1):
        wave = random.choice(waves)
        yr, q = int(wave[:4]), int(wave[5])
        # Bound month sampling — 2026Q2 should fall in April/May (not June, since data ends May 31)
        if wave == "2026Q2":
            month = random.choice([4, 5])
        else:
            month = (q-1)*3 + random.randint(1,3)
        day = random.randint(1,28)
        dma = random.choices(DMAS, weights=[d[5] for d in DMAS], k=1)[0]
        unaided = random.choices([0,1], weights=[68,32])[0]
        aided = random.choices([0,1], weights=[18,82])[0]
        considers = random.choices([0,1], weights=[55,45])[0] if aided else 0
        base_score = 3.6
        penalty = 0.4 if (dma[0]=="LA-DMA" and wave in ("2025Q4","2026Q1")) else 0
        top_comp = random.choice(competitors)
        if dma[0]=="LA-DMA" and wave in ("2025Q4","2026Q1"):
            top_comp = random.choices(competitors, weights=[20,55,5,5,10,3,2])[0]
        a_hboo = random.choices([0,1], weights=[18,82])[0]
        if dma[0]=="LA-DMA" and wave in ("2025Q4","2026Q1"):
            a_hboo = 1 if random.random()<0.94 else 0
        rows.append({
            "response_id": f"R_{i:08d}", "wave":wave,
            "response_date":f"{yr}-{month:02d}-{day:02d}",
            "country":"United States", "state":DMA_STATE[dma[0]], "dma":dma[0],
            "city_tier":random.choices(["Tier 1","Tier 2","Tier 3"], weights=[40,40,20])[0],
            "age_band":random.choice(["18-24","25-34","35-44","45-54","55-64","65+"]),
            "gender":random.choices(["Female","Male","Other"], weights=[55,43,2])[0],
            "household_size":random.choices([1,2,3,4,5], weights=[20,30,25,18,7])[0],
            "children_present":random.choices([0,1,2,3], weights=[55,22,18,5])[0],
            "ethnicity":random.choices(ETHNICITY, weights=[18,60,12,6,4])[0],
            "income_bracket":random.choice(INCOME_BANDS),
            "education_level":random.choice(EDU_LEVELS),
            "marital_status":random.choices(MARITAL, weights=[35,50,10,5])[0],
            "primary_category":random.choice(primary_cats),
            "channel_preference":random.choices(["In-store","Online","Mixed"], weights=[55,18,27])[0],
            "retailer_type":random.choices(["Hypermarket","Supermarket","Club","Drug","Online"], weights=[35,40,10,5,10])[0],
            "holiday_season_flag":1 if month in (11,12) else 0,
            "unaided_aw_crunchwell":unaided,
            "aided_aw_crunchwell":aided,
            "considers_crunchwell":considers,
            "consideration_set_size":random.choices([0,1,2,3,4,5], weights=[8,12,28,30,15,7])[0],
            "purchase_frequency_qtr":random.choices([0,1,2,3,4,5,6], weights=[15,20,22,18,12,8,5])[0],
            "price_sensitivity_1to5":random.choices([1,2,3,4,5], weights=[5,12,28,35,20])[0],
            "promo_propensity_0to1":round(random.uniform(0.2,0.95), 3),
            "usage_primary":random.choices(["Breakfast","Snack","Post-Workout","Late Night","Multi-Use"], weights=[55,20,8,7,10])[0],
            "taste":max(1,min(5,int(round(random.gauss(base_score-penalty,0.85))))),
            "quality":max(1,min(5,int(round(random.gauss(base_score-penalty,0.85))))),
            "health":max(1,min(5,int(round(random.gauss(3.3-penalty*0.5,0.9))))),
            "value":max(1,min(5,int(round(random.gauss(3.4-penalty*0.5,0.9))))),
            "family_friendly":max(1,min(5,int(round(random.gauss(3.8-penalty*0.4,0.8))))),
            "innovation":max(1,min(5,int(round(random.gauss(3.0,0.85))))),
            "trust":max(1,min(5,int(round(random.gauss(3.7-penalty*0.4,0.8))))),
            "likelihood_repurchase_1to5":max(1,min(5,int(round(random.gauss(3.5-penalty*0.5,0.9))))),
            "nps_0to10":max(0,min(10,int(round(random.gauss(6.5-penalty*1.5,2.4))))),
            "top_competitor":top_comp,
            "price_paid_usd":round(random.uniform(2.49,7.99), 2),
            "respondent_weight":round(random.uniform(0.4,1.6), 4),
            "aided_aw_honeynest":random.choices([0,1], weights=[40,60])[0],
            # ProteinPeak awareness bumps in 2026Q2 wave (launch driven by Sage Park media)
            "aided_aw_proteinpeak":(
                random.choices([0,1], weights=[35,65])[0] if wave == "2026Q2"
                else random.choices([0,1], weights=[55,45])[0]
            ),
            "aided_aw_morningoats":random.choices([0,1], weights=[35,65])[0],
            "aided_aw_trailgrove":random.choices([0,1], weights=[45,55])[0],
            "aided_aw_rootday":random.choices([0,1], weights=[58,42])[0],
            "aided_aw_cheerios":random.choices([0,1], weights=[8,92])[0],
            "aided_aw_field_honey":a_hboo,
            "aided_aw_frosted_flakes":random.choices([0,1], weights=[10,90])[0],
            "aided_aw_quaker":random.choices([0,1], weights=[12,88])[0],
            "aided_aw_great_value_pl":random.choices([0,1], weights=[25,75])[0],
        })
    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# 5. Households
# -----------------------------------------------------------------------------

def gen_households(n_hh=5000):
    rows = []
    for i in range(n_hh):
        dma = random.choices(DMAS, weights=[d[5] for d in DMAS], k=1)[0]
        sz = random.choices([1,2,3,4,5,6], weights=[18,30,22,18,8,4])[0]
        kids = sz > 2 and random.random() < 0.6
        rows.append({
            "Household_ID":f"HH{200000+i:06d}",
            "Country":"United States", "Country_Code":"USA",
            "State":DMA_STATE[dma[0]], "DMA":dma[0],
            "City":random.choice(DMA_CITIES[dma[0]]),
            "Urbanicity":random.choices(URBANICITY, weights=[42,40,18])[0],
            "Currency":"USD", "HH_Size":sz,
            "Income_Bracket":random.choice(INCOME_BANDS),
            "HOH_Age":random.randint(22,78),
            "HOH_Gender":random.choices(["Female","Male","Other"], weights=[60,38,2])[0],
            "Education_Level":random.choice(EDU_LEVELS),
            "Marital_Status":random.choices(MARITAL, weights=[28,55,12,5])[0],
            "Ethnicity":random.choices(ETHNICITY, weights=[18,60,12,6,4])[0],
            "Children_Flag":"Yes" if kids else "No",
            "Children_Age_Band":random.choice(["0-5","6-11","12-17","Mixed"]) if kids else "None",
            "Number_Of_Children":random.choices([1,2,3], weights=[55,35,10])[0] if kids else 0,
            "Loyalty_Score":round(random.uniform(0.05,0.95), 3),
            "Brand_Loyalty_Segment":random.choices(LOYALTY_SEG, weights=[28,42,18,12])[0],
            "Price_Sensitivity_Segment":random.choices(PRICE_SEG, weights=[25,55,20])[0],
            "Adopter_Type":random.choices(ADOPTER, weights=[5,15,50,22,8])[0],
            "Cereal_Buyer_Flag":"Yes" if random.random()<0.92 else "No",
            "Plant_Based_Buyer_Flag":"Yes" if random.random()<0.31 else "No",
            "Panel_Tenure_Months":random.randint(3,96),
            "Weight":round(random.uniform(0.5,1.6), 4),
        })
    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# 6. Household Transactions
# -----------------------------------------------------------------------------

def gen_hh_transactions(hh_df, n_rows=30000):
    pool = []
    for s in SKUS:
        pool.append({"id":s[0],"name":s[1],"brand":s[2],"cat":s[3],"oz":s[5],"price":s[6],"mfr":"Acme Corp"})
    for c in COMP_SKUS:
        pool.append({"id":c[0],"name":c[1],"brand":c[2],"cat":c[4],"oz":c[6],"price":c[7],"mfr":c[3]})

    weeks = []
    d = date(2024, 1, 1)
    while d <= DATA_END_DATE:
        weeks.append(d); d += timedelta(days=7)

    hh_records = hh_df.to_dict("records")
    rows = []
    for _ in range(n_rows):
        hh = random.choice(hh_records)
        wk = random.choice(weeks)
        retailer = random.choice(RETAILERS)
        sku = random.choice(pool)

        # PP005/PP006 only exist on/after launch
        if sku["id"] in PP_Q2_NEW_SKUS and wk < PP_Q2_LAUNCH_DATE:
            sku = random.choice([s for s in pool if s["id"] not in PP_Q2_NEW_SKUS])

        disc, promo = 0.0, "None"
        if random.random() < 0.18:
            disc = round(random.uniform(0.05, 0.3), 2)
            promo = random.choice(["Price Off","Multi-Buy","Bundle","Loyalty"])

        switching_flag = "No"
        if (hh["DMA"]=="LA-DMA" and hh["Brand_Loyalty_Segment"]=="Acme Loyal"
                and wk >= date(2025,11,1) and random.random() < 0.14):
            sku = next(s for s in pool if s["brand"]=="Field & Honey")
            switching_flag = "Yes"

        # ProteinPeak Q2 launch — source-of-volume: ~53% new-to-ProteinPeak,
        # ~32% switching from PP001 (cannibalization), ~15% from competitors.
        # Encoded by upgrading a small share of HH buys to PP005/PP006 in
        # the launch retailers, with a Switching_Flag value of "Cannibalization"
        # or "New_To_Brand" or "Competitor_Switch".
        if (wk >= PP_Q2_LAUNCH_DATE and retailer[0] in
                ("Target","Whole Foods","Sprouts","Amazon","Kroger","Walmart")
                and random.random() < 0.06):
            new_sku_id = random.choices(PP_Q2_NEW_SKUS, weights=[0.58, 0.42])[0]
            new_sku = next(s for s in pool if s["id"] == new_sku_id)
            # Source-of-volume distribution
            sov_roll = random.random()
            if sov_roll < 0.53:
                switching_flag = "New_To_Brand"
            elif sov_roll < 0.85:
                # Cannibalization: was buying PP001, now buying PP005/PP006
                switching_flag = "Cannibalization"
            else:
                # Competitor switching from Magic Spoon / Three Wishes / Catalina
                switching_flag = "Competitor_Switch"
            sku = new_sku

        units = random.choices([1,2,3,4], weights=[55,28,12,5])[0]
        unit_price = round(sku["price"] * (1 - disc), 2)

        rows.append({
            "Household_ID":hh["Household_ID"], "Week_Start":wk.strftime("%Y-%m-%d"),
            "Country":"United States", "Country_Code":"USA",
            "State":hh["State"], "DMA":hh["DMA"], "City":hh["City"],
            "Urbanicity":hh["Urbanicity"], "Currency":"USD",
            "Retailer":retailer[0], "Retailer_Type":retailer[2], "Channel":retailer[1],
            "Banner_Division":assign_banner(retailer[0], hh["DMA"])[0],
            "Banner_Region":assign_banner(retailer[0], hh["DMA"])[1],
            "Category":sku["cat"], "Brand":sku["brand"], "Manufacturer":sku["mfr"],
            "Product_SKU":sku["id"], "Product_Description":sku["name"],
            "Pack_Weight_oz":sku["oz"], "Units":units,
            "Unit_Price":unit_price, "Discount_Percent":disc,
            "Total_Price_Paid":round(unit_price*units, 2),
            "Promotion_Type":promo,
            "Children_Flag":hh["Children_Flag"], "Income_Bracket":hh["Income_Bracket"],
            "Ethnicity":hh["Ethnicity"],
            "Price_Sensitivity_Segment":hh["Price_Sensitivity_Segment"],
            "Brand_Loyalty_Segment":hh["Brand_Loyalty_Segment"],
            "Adopter_Type":hh["Adopter_Type"],
            "Switching_Flag":switching_flag,
        })

    # ProteinPeak Q2 launch — dedicated oversample (~800 HH transactions for
    # PP005/PP006) so source-of-volume waterfall has enough mass to chart.
    pp_pool = [s for s in pool if s["id"] in PP_Q2_NEW_SKUS]
    pp_retailers = [r for r in RETAILERS if r[0] in
                    ("Target","Whole Foods","Sprouts","Amazon","Kroger","Walmart","Target.com")]
    pp_weeks = [w for w in weeks if w >= PP_Q2_LAUNCH_DATE]
    if pp_pool and pp_retailers and pp_weeks:
        for _ in range(800):
            hh = random.choice(hh_records)
            wk = random.choice(pp_weeks)
            retailer = random.choice(pp_retailers)
            sku = random.choices(pp_pool, weights=[0.58, 0.42])[0]
            disc = 0.06 if random.random() < 0.55 else 0.0
            unit_price = round(sku["price"] * (1 - disc), 2)
            sov_roll = random.random()
            if sov_roll < 0.53:
                switching_flag = "New_To_Brand"
            elif sov_roll < 0.85:
                switching_flag = "Cannibalization"
            else:
                switching_flag = "Competitor_Switch"
            units = random.choices([1,2], weights=[80,20])[0]
            promo = "Price Off" if disc > 0 else "None"
            rows.append({
                "Household_ID":hh["Household_ID"], "Week_Start":wk.strftime("%Y-%m-%d"),
                "Country":"United States", "Country_Code":"USA",
                "State":hh["State"], "DMA":hh["DMA"], "City":hh["City"],
                "Urbanicity":hh["Urbanicity"], "Currency":"USD",
                "Retailer":retailer[0], "Retailer_Type":retailer[2], "Channel":retailer[1],
                "Banner_Division":assign_banner(retailer[0], hh["DMA"])[0],
                "Banner_Region":assign_banner(retailer[0], hh["DMA"])[1],
                "Category":sku["cat"], "Brand":sku["brand"], "Manufacturer":sku["mfr"],
                "Product_SKU":sku["id"], "Product_Description":sku["name"],
                "Pack_Weight_oz":sku["oz"], "Units":units,
                "Unit_Price":unit_price, "Discount_Percent":disc,
                "Total_Price_Paid":round(unit_price*units, 2),
                "Promotion_Type":promo,
                "Children_Flag":hh["Children_Flag"], "Income_Bracket":hh["Income_Bracket"],
                "Ethnicity":hh["Ethnicity"],
                "Price_Sensitivity_Segment":hh["Price_Sensitivity_Segment"],
                "Brand_Loyalty_Segment":hh["Brand_Loyalty_Segment"],
                "Adopter_Type":hh["Adopter_Type"],
                "Switching_Flag":switching_flag,
            })

    return pd.DataFrame(rows)


# =============================================================================
# v0.2.0 — Sales-side completeness
# =============================================================================
# Tables added to close Tier 1 gaps from
# `00-inbox/synthetic-data-gap-analysis-vs-mvp.md`:
#   • plan_vs_actual    (T1.1 — Plan / Forecast vs Actual)
#   • sku_authorization (T1.2 — Distribution voids: Authorized vs Distributed)
#   • shipments         (T1.6 — Shipment + fill rate, Hurricane Tonya visible)
#   • promo_events      (T1.5 — Promo events for ALL retailers + mechanic taxonomy)
#   • competitor_launches (T1.4 — passes through hand-curated seed)
# Banner_Division / Banner_Region columns (T1.3) are added inline above.


# -----------------------------------------------------------------------------
# 7. Plan vs Actual  (T1.1)
# -----------------------------------------------------------------------------

def gen_plan_vs_actual(epos_df: pd.DataFrame) -> pd.DataFrame:
    """Monthly plan vs actuals at brand × retailer × DMA grain.

    The actuals are anchored on epos rollups; the plan layer encodes the FY26
    AOP narrative (Crunchwell LA +1.5% plan vs ~-45% actual; ProteinPeak
    +67% plan vs ~+24% actual; HoneyNest -6% managed decline).
    """
    acme_brands = ["Crunchwell", "HoneyNest", "ProteinPeak", "MorningOats", "TrailGrove", "RootDay"]
    retailers = [r[0] for r in RETAILERS]
    dmas = [d[0] for d in DMAS]

    # Brand-level FY26 plan stance, baseline FY25 monthly $ at brand-retailer-DMA level
    fy26_plan_yoy = {
        "Crunchwell": 0.04,
        "HoneyNest": -0.06,
        "ProteinPeak": 0.67,
        "MorningOats": 0.03,
        "TrailGrove": 0.08,
        "RootDay": 0.18,
    }

    # Brand-level realized FY26 actual delta (rough — variance vs plan is the point)
    fy26_actual_yoy = {
        "Crunchwell": -0.012,
        "HoneyNest": -0.071,
        "ProteinPeak": 0.246,
        "MorningOats": 0.018,
        "TrailGrove": 0.063,
        "RootDay": 0.176,
    }

    # Approx FY25 brand $ per retailer-DMA-month (rough proportions of $812M revenue)
    brand_fy25_share = {
        "Crunchwell": 0.384, "HoneyNest": 0.116, "ProteinPeak": 0.059,
        "MorningOats": 0.121, "TrailGrove": 0.187, "RootDay": 0.076,
    }
    # Use trade share from retailers.csv-style weights baked in
    retailer_share = {
        "Walmart": 0.226, "Target": 0.084, "Kroger": 0.115, "Albertsons": 0.064,
        "Publix": 0.036, "H-E-B": 0.039, "Costco": 0.064, "Sams Club": 0.034,
        "Rouses": 0.009, "Brookshires": 0.006, "Winn-Dixie": 0.015, "Wegmans": 0.014,
        "Meijer": 0.026, "Sprouts": 0.014, "Whole Foods": 0.015,
        "Aldi": 0.018, "Amazon": 0.054, "Walmart.com": 0.018, "Target.com": 0.010,
        "Instacart": 0.005, "CVS": 0.015, "Walgreens": 0.012, "7-Eleven": 0.011,
    }
    dma_share = {d[0]: d[5] for d in DMAS}  # last col is consumption share

    months = []
    for y in (2024, 2025, 2026):
        for m in range(1, 13):
            if y == 2026 and m > 5:
                continue
            months.append(f"{y}-{m:02d}")

    rows = []
    annual_company = 812.0  # $812M FY25
    for period in months:
        yr = int(period.split("-")[0])
        mo = int(period.split("-")[1])
        month_factor = 1.0 / 12.0
        for brand in acme_brands:
            for ret in retailers:
                for dma in dmas:
                    base = (annual_company * brand_fy25_share[brand]
                            * retailer_share.get(ret, 0.005) * dma_share.get(dma, 0.02)
                            * month_factor * 1_000_000)
                    if base < 1500:
                        continue  # sparsify - drop trivially small combos
                    if yr == 2024:
                        plan = base * (1.0 + 0.04)  # FY24 plan was +4% YoY
                        actual = base * random.uniform(0.95, 1.05)
                        plan_source = "AOP"
                    elif yr == 2025:
                        plan = base * (1.0 + 0.05)  # FY25 plan was +5% YoY
                        actual = base * (1.0 + random.uniform(0.0, 0.06))
                        plan_source = "AOP"
                    else:  # 2026
                        plan = base * (1.0 + fy26_plan_yoy[brand])
                        if brand == "Crunchwell" and dma == "LA-DMA":
                            actual = base * (1.0 + random.uniform(-0.50, -0.40))
                        elif brand == "ProteinPeak" and mo >= 4:
                            # ProteinPeak Q2 launch (PP005 + PP006). The +67%
                            # FY26 plan loads heavily into April-May. Channel
                            # split: Target over-delivers (~+13%), Walmart
                            # under-delivers (~-22%), Amazon ~flat, rest ~flat.
                            if ret == "Target":
                                actual = plan * (1.0 + random.uniform(0.08, 0.18))
                            elif ret == "Walmart":
                                actual = plan * (1.0 + random.uniform(-0.27, -0.17))
                            elif ret == "Amazon":
                                actual = plan * (1.0 + random.uniform(-0.05, 0.06))
                            else:
                                actual = plan * (1.0 + random.uniform(-0.08, 0.04))
                        else:
                            actual = base * (1.0 + fy26_actual_yoy[brand]
                                             + random.uniform(-0.04, 0.04))
                        plan_source = "FCST_REV" if mo >= 3 else "AOP"
                    plan = round(plan, 2)
                    actual = round(actual, 2)
                    var = (actual - plan) / plan if plan > 0 else 0.0
                    if var < -0.10:
                        status = "Red"
                    elif var < -0.03:
                        status = "Soft"
                    elif var > 0.05:
                        status = "Over"
                    else:
                        status = "On-Track"
                    rows.append({
                        "Period": period,
                        "Brand": brand,
                        "Retailer": ret,
                        "DMA": dma,
                        "Plan_Revenue_USD": plan,
                        "Plan_Units": int(plan / random.uniform(4.5, 6.5)),
                        "Actual_Revenue_USD": actual,
                        "Actual_Units": int(actual / random.uniform(4.5, 6.5)),
                        "Variance_USD": round(actual - plan, 2),
                        "Variance_Pct": round(var, 4),
                        "Variance_Status": status,
                        "Plan_Source": plan_source,
                    })
    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# 8. SKU Authorization  (T1.2)
# -----------------------------------------------------------------------------

def gen_sku_authorization(perfect_store_df: pd.DataFrame) -> pd.DataFrame:
    """Per store × Acme SKU monthly authorization snapshot.

    Encodes the distribution-void story: Cinnamon Twist 41% authorized,
    ProteinPeak at H-E-B 38% authorized (expansion headroom), RootDay 12%
    authorized at Walmart (test only).
    """
    # Use distinct stores from perfect_store + their banner info
    store_keys = perfect_store_df[
        ["Store_ID", "Banner", "DMA", "State", "City", "Banner_Division", "Banner_Region", "Size_Tier"]
    ].drop_duplicates(subset=["Store_ID"]).to_dict("records")

    auth_rate = {
        "CR001": 0.92, "CR002": 0.81, "CR003": 0.85, "CR004": 0.66, "CR005": 0.60,
        "CR006": 0.41,  # Cinnamon Twist underperformer
        "CR007": 0.49,
        "HN001": 0.74, "HN003": 0.66, "HN007": 0.44,
        "PP001": 0.55, "PP002": 0.43, "PP003": 0.30,
        # PP005/PP006 only authorized starting 2026-04 snapshot (launched 2026-04-20)
        "PP005": 0.38, "PP006": 0.28,
        "MO001": 0.71, "MO004": 0.58, "MO007": 0.32,
        "TG001": 0.66, "TG002": 0.61, "TG007": 0.55,
        "RD001": 0.51, "RD002": 0.34,
    }
    # Chain-specific overrides for narrative anchors
    auth_overrides = {
        ("Walmart","CR001"): 0.89, ("Walmart","CR002"): 0.84, ("Walmart","CR006"): 0.34,
        ("Walmart","RD001"): 0.12, ("Walmart","RD002"): 0.08,        # RootDay test-only
        ("H-E-B","PP001"): 0.38, ("H-E-B","PP002"): 0.30,            # ProteinPeak headroom
        ("Albertsons","CR001"): 0.62, ("Albertsons","CR002"): 0.54,  # ~500 stores not distributed
        ("Whole Foods","RD001"): 0.94, ("Whole Foods","RD002"): 0.81,
        ("Sprouts","TG001"): 0.92, ("Sprouts","RD001"): 0.88,
        ("Costco","MO004"): 0.91,
        # ProteinPeak Q2 launch — Target hero, Whole Foods/Sprouts strong,
        # Walmart-pilot light authorization, Amazon strong, H-E-B/Albertsons/Publix none
        ("Target","PP005"): 0.86,    ("Target","PP006"): 0.78,
        ("Whole Foods","PP005"): 0.74, ("Whole Foods","PP006"): 0.66,
        ("Sprouts","PP005"): 0.72,    ("Sprouts","PP006"): 0.64,
        ("Amazon","PP005"): 0.92,     ("Amazon","PP006"): 0.84,
        ("Walmart","PP005"): 0.18,    ("Walmart","PP006"): 0.04,  # pilot only PP005
        ("Kroger","PP005"): 0.32,     ("Kroger","PP006"): 0.28,
        ("Costco","PP005"): 0.0,      ("Costco","PP006"): 0.0,
        ("H-E-B","PP005"): 0.0,       ("H-E-B","PP006"): 0.0,
        ("Albertsons","PP005"): 0.0,  ("Albertsons","PP006"): 0.0,
        ("Publix","PP005"): 0.0,      ("Publix","PP006"): 0.0,
    }
    why_not = ["OOS","store_choice","supply_chain","new_listing_pending","discontinued"]

    snapshots = ["2025-11-30","2025-12-31","2026-01-31","2026-02-28","2026-03-31","2026-04-30","2026-05-31"]
    rows = []
    for snap in snapshots:
        for store in store_keys:
            for sku in SKUS:
                sid = sku[0]
                base = auth_rate.get(sid, 0.5)
                base = auth_overrides.get((store["Banner"], sid), base)
                # Wallmart Sept 2025 reset: Cinnamon Twist authorized -> not authorized in some Walmart stores
                if store["Banner"] == "Walmart" and sid == "CR006" and snap >= "2025-12-31":
                    base = max(0.0, base - 0.06)
                # ProteinPeak Q2 launch — PP005/PP006 only authorized starting
                # 2026-04 snapshot; earlier snapshots show Not_Authorized
                if sid in PP_Q2_NEW_SKUS and snap < "2026-04-30":
                    base = 0.0

                authorized = random.random() < base
                if authorized:
                    # Distribution status
                    dist_prob_distributed = 0.92  # most authorized SKUs are distributed
                    if sid in ("CR002","CR004","CR005") and store["DMA"] == "LA-DMA" and snap in ("2025-11-30","2025-12-31"):
                        dist_prob_distributed = 0.55  # Hurricane Tonya OOS
                    if sid == "CR006" and store["Banner"] == "Walmart":
                        dist_prob_distributed = 0.78  # Cinnamon Twist void
                    if random.random() < dist_prob_distributed:
                        dist_status = "Distributed"
                        wn = "None"
                    else:
                        dist_status = "Authorized_Not_Distributed"
                        if sid in ("CR002","CR004","CR005") and store["DMA"] == "LA-DMA":
                            wn = "OOS"  # Hurricane Tonya
                        else:
                            wn = random.choice(why_not[:4])
                else:
                    dist_status = "Out_Of_Distribution"
                    wn = "store_choice"

                ranged_year = random.choice([2018, 2020, 2022, 2023, 2024, 2025])
                if sid == "CR006":  # launched 2025
                    ranged_year = 2025
                if sid in PP_Q2_NEW_SKUS:  # launched 2026-04-20
                    ranged_year = 2026
                ranged_since = f"{ranged_year}-01-15"
                if sid in PP_Q2_NEW_SKUS:
                    ranged_since = PP_Q2_LAUNCH_DATE.strftime("%Y-%m-%d")
                rows.append({
                    "Snapshot_Date": snap,
                    "Store_ID": store["Store_ID"],
                    "Banner": store["Banner"],
                    "Banner_Division": store["Banner_Division"],
                    "Banner_Region": store["Banner_Region"],
                    "DMA": store["DMA"],
                    "State": store["State"],
                    "Size_Tier": store["Size_Tier"],
                    "SKU": sid,
                    "Brand": sku[2],
                    "Auth_Status": "Authorized" if authorized else "Not_Authorized",
                    "Distribution_Status": dist_status,
                    "Ranged_Since": ranged_since,
                    "ACV_Weight_Pct": round(random.uniform(0.005, 0.12), 4),
                    "Why_Not_Distributed": wn,
                })
    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# 9. Shipments / Fill Rate  (T1.6)
# -----------------------------------------------------------------------------

def gen_shipments() -> pd.DataFrame:
    """Weekly shipment data per Acme plant × retailer DC × SKU.

    Encodes Hurricane Tonya: Houston-origin shipments to Rouses/Brookshire's/
    LA Walmart DCs Nov 8–Dec 10, 2025 collapse to 40-60% fill, then 60-80%
    capacity for 18 more days.
    """
    plant_origin = {
        "Crunchwell": "Lancaster",
        "HoneyNest":  "Battle Creek",
        "ProteinPeak":"Battle Creek",
        "MorningOats":"Lancaster",
        "TrailGrove": "Modesto",
        "RootDay":    "Modesto",
    }
    retailer_dcs = {
        "Walmart":     ["Walmart Bentonville DC","Walmart Houston DC","Walmart Atlanta DC","Walmart Chicago DC","Walmart Reno DC","Walmart NJ DC"],
        "Target":      ["Target Lake City DC","Target Houston DC","Target Atlanta DC","Target Chicago DC","Target Phoenix DC","Target Trenton DC"],
        "Kroger":      ["Kroger Cincinnati DC","Kroger Atlanta DC","Kroger Dallas DC","Kroger Memphis DC","Kroger Compton DC"],
        "Albertsons":  ["Albertsons Tolleson DC","Albertsons Tracy DC","Albertsons Boise DC"],
        "Publix":      ["Publix Lakeland DC","Publix Atlanta DC"],
        "H-E-B":       ["H-E-B San Antonio DC","H-E-B Houston DC"],
        "Costco":      ["Costco Mira Loma DC","Costco Atlanta DC","Costco Chicago DC"],
        "Rouses":      ["Rouses Thibodaux DC"],
        "Brookshires": ["Brookshire's Tyler DC"],
        "Winn-Dixie":  ["Winn-Dixie Hammond DC"],
        "Sprouts":     ["Sprouts Aurora DC"],
        "Whole Foods": ["Whole Foods Stockton DC","Whole Foods Atlanta DC"],
        "Sams Club":   ["Sam's Club Bentonville DC"],
        "Meijer":      ["Meijer Lansing DC"],
        "Aldi":        ["Aldi Center DC"],
        "Amazon":      ["Amazon Phoenix FC","Amazon Memphis FC","Amazon Stockton FC"],
        "Walmart.com": ["Walmart eFC Pedricktown"],
        "Target.com":  ["Target eFC Memphis"],
        "Wegmans":     ["Wegmans Pottsville DC"],
        "Instacart":   ["Instacart Direct"],
        "CVS":         ["CVS Indianapolis DC"],
        "Walgreens":   ["Walgreens Anderson DC"],
        "7-Eleven":    ["7-Eleven Direct"],
    }
    # Houston/LA-anchored DCs (impacted by Hurricane Tonya)
    storm_dcs = {"Walmart Houston DC","Target Houston DC","Rouses Thibodaux DC",
                 "Brookshire's Tyler DC","Winn-Dixie Hammond DC","H-E-B Houston DC",
                 "Kroger Memphis DC"}

    weeks = []
    d = date(2024, 1, 1)
    while d <= DATA_END_DATE:
        weeks.append(d); d += timedelta(days=7)

    rows = []
    sk_id = 0
    for sku in SKUS:
        sid, sname, brand, cat, subcat, oz, price = sku
        plant = plant_origin[brand]
        for retailer, dcs in retailer_dcs.items():
            for dc in dcs:
                # Sparsify — only material combos
                if random.random() < 0.55:
                    continue
                # PP005/PP006 don't ship before launch date
                first_ship_wk = (
                    PP_Q2_LAUNCH_DATE - timedelta(days=14) if sid in PP_Q2_NEW_SKUS else None
                )
                for wk in weeks:
                    if first_ship_wk is not None and wk < first_ship_wk:
                        continue
                    sk_id += 1
                    ordered = random.randint(80, 1800)
                    # Launch SKUs ship larger initial loads, with allocation pinch W0-W1
                    if sid in PP_Q2_NEW_SKUS:
                        wk_since_launch = (wk - PP_Q2_LAUNCH_DATE).days // 7
                        if wk_since_launch < 0:
                            ordered = random.randint(400, 2400)  # initial sell-in
                        elif wk_since_launch <= 4 and retailer == "Target":
                            ordered = random.randint(600, 2200)  # heavy reorder
                        else:
                            ordered = random.randint(120, 900)
                    fill = random.uniform(0.94, 0.99)
                    cut = "None"
                    on_time = 1 if random.random() < 0.93 else 0

                    if dc in storm_dcs and date(2025,11,8) <= wk <= date(2025,12,10):
                        fill = random.uniform(0.40, 0.62); cut = "Storm"; on_time = 0
                    elif dc in storm_dcs and date(2025,12,11) <= wk <= date(2025,12,28):
                        fill = random.uniform(0.62, 0.82); cut = "Storm"; on_time = 0
                    if brand == "Crunchwell" and sid in ("CR002","CR004","CR005") and dc in storm_dcs:
                        if date(2025,11,8) <= wk <= date(2025,12,28):
                            fill = min(fill, random.uniform(0.35, 0.55))
                    if brand == "ProteinPeak" and random.random() < 0.06:
                        fill = random.uniform(0.78, 0.90)
                        cut = random.choice(["Production_Lag","Quality_Hold"])
                    # Crunchwell Mega 4-week Lancaster cycle — occasional tail OOS
                    if sid in ("CR002","CR004") and random.random() < 0.04:
                        fill = random.uniform(0.82, 0.92); cut = "Production_Lag"
                    # PP005/PP006 launch allocation pinch W0-W1 (Battle Creek pull)
                    if sid in PP_Q2_NEW_SKUS:
                        wk_since_launch = (wk - PP_Q2_LAUNCH_DATE).days // 7
                        if 0 <= wk_since_launch <= 1:
                            fill = random.uniform(0.78, 0.92)
                            cut = "Launch_Allocation"

                    shipped = int(ordered * min(1.0, fill + random.uniform(-0.02, 0.02)))
                    delivered = int(shipped * random.uniform(0.97, 1.0))
                    fill_pct = round(delivered / ordered, 4) if ordered else 0
                    rows.append({
                        "Shipment_ID": f"SHP{sk_id:08d}",
                        "Week_Start": wk.strftime("%Y-%m-%d"),
                        "Brand": brand,
                        "Manufacturer": "Acme Corp",
                        "SKU": sid,
                        "Product_Description": sname,
                        "Retailer": retailer,
                        "Retailer_DC": dc,
                        "Origin_Acme_Plant": plant,
                        "Ordered_Units": ordered,
                        "Shipped_Units": shipped,
                        "Delivered_Units": delivered,
                        "Fill_Rate_Pct": fill_pct,
                        "On_Time_Pct": on_time,
                        "Cut_Reason": cut,
                    })
    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# 10. Promo events (all retailers)  (T1.5)
# -----------------------------------------------------------------------------

def gen_promo_events() -> pd.DataFrame:
    """All-retailer promo event log with mechanic taxonomy + ROI.

    The Louisiana Field & Honey sequence (in seeds/promo_events_louisiana.csv)
    is preserved as a hand-curated subset; this generator extends to ~700 events
    across all retailers with industry-typical ROI distributions.
    """
    mechanics_by_retailer = {
        "Walmart":      [("Feature+Display",0.30),("TPR",0.25),("Display",0.20),("Multi-Buy",0.15),("Feature",0.10)],
        "Target":       [("Feature+Display",0.32),("Display",0.22),("TPR",0.20),("Multi-Buy",0.16),("Feature",0.10)],
        "Kroger":       [("Multi-Buy",0.32),("TPR",0.28),("Feature+Display",0.18),("Feature",0.12),("Display",0.10)],
        "Albertsons":   [("Multi-Buy",0.28),("TPR",0.30),("Feature+Display",0.18),("Feature",0.14),("Display",0.10)],
        "Publix":       [("BOGO",0.34),("TPR",0.28),("Feature",0.20),("Display",0.10),("Feature+Display",0.08)],
        "Costco":       [("Bundle",0.42),("Multi-Buy",0.28),("Display",0.16),("Feature",0.14)],
        "Sams Club":    [("Bundle",0.38),("Multi-Buy",0.30),("Display",0.18),("Feature",0.14)],
        "H-E-B":        [("TPR",0.32),("Multi-Buy",0.24),("Feature+Display",0.20),("Display",0.14),("Feature",0.10)],
        "Rouses":       [("Feature+Display",0.36),("TPR",0.28),("Display",0.18),("Multi-Buy",0.10),("Feature",0.08)],
        "Brookshires":  [("TPR",0.32),("Feature+Display",0.24),("Multi-Buy",0.20),("Display",0.14),("Feature",0.10)],
        "Sprouts":      [("TPR",0.42),("Multi-Buy",0.22),("Feature",0.18),("Display",0.10),("Feature+Display",0.08)],
        "Whole Foods":  [("TPR",0.38),("Feature",0.24),("Display",0.18),("Multi-Buy",0.10),("Bundle",0.10)],
        "Amazon":       [("Coupon",0.42),("TPR",0.28),("Multi-Buy",0.20),("Bundle",0.10)],
    }
    feature_types_for = {
        "Feature":          ["Retailer_Circular","Digital_Coupon","Email","None"],
        "Feature+Display":  ["Retailer_Circular","Digital_Coupon","Email"],
        "Display":          ["None"],
        "TPR":              ["Digital_Coupon","None"],
        "Multi-Buy":        ["Retailer_Circular","Digital_Coupon"],
        "BOGO":             ["Retailer_Circular","Digital_Coupon"],
        "Bundle":           ["Retailer_Circular","None"],
        "Coupon":           ["Digital_Coupon"],
    }
    display_types_for = {
        "Feature+Display":["Endcap","In-Aisle","Lobby"],
        "Display":["Endcap","In-Aisle"],
        "BOGO":["Endcap","None"],
        "Bundle":["Lobby","Endcap"],
    }
    retailers = list(mechanics_by_retailer.keys())
    sku_pool = SKUS + [(c[0],c[1],c[2],c[4],c[5],c[6],c[7]) for c in COMP_SKUS]

    start, end = date(2024, 9, 1), DATA_END_DATE
    days = (end - start).days
    rows = []
    eid = 0
    for _ in range(820):
        eid += 1
        ret = random.choice(retailers)
        mech = weighted_choice(mechanics_by_retailer[ret])
        sku = random.choice(sku_pool)
        sid, sname, brand, cat, subcat, oz, price = sku[0], sku[1], sku[2], sku[3], sku[4], sku[5], sku[6]
        manufacturer = "Acme Corp" if sid.startswith(("CR","HN","PP","MO","TG","RD")) else (
            random.choice(["General Mills","Larksfield Foods","Kellanova","Walmart PL","PepsiCo"])
        )
        d_offset = random.randint(0, days)
        sd = start + timedelta(days=d_offset)
        # PP005/PP006 promos only on/after launch
        if sid in PP_Q2_NEW_SKUS and sd < PP_Q2_LAUNCH_DATE:
            sd = PP_Q2_LAUNCH_DATE + timedelta(days=random.randint(0, 35))
        ed = sd + timedelta(days=random.choice([21, 28, 35, 42]))
        depth = random.choices([8,10,12,15,18,20,22,25,28,30,35,40], weights=[10,12,12,14,12,10,8,8,6,4,2,2])[0]
        # Costco bundle deals tend to be deeper effective discounts
        if mech == "Bundle":
            depth = random.choice([15,18,20,25,30])
        if mech == "BOGO":
            depth = 50
        dma = random.choices([d[0] for d in DMAS], weights=[d[5] for d in DMAS])[0]
        baseline = random.randint(100, 6000)
        lift = random.uniform(0.10, 0.95) + (depth / 220.0)
        if mech in ("Feature+Display","Display","Bundle","BOGO"):
            lift += random.uniform(0.10, 0.40)
        promo_units = int(baseline * (1 + lift))
        incremental = promo_units - baseline
        forward_buy = random.uniform(0.05, 0.32)
        # Higher forward-buy on pantry-loadable Mega cereals
        if sid in ("CR002","CR004") or (oz and oz >= 16):
            forward_buy += 0.05
        true_inc = int(incremental * (1 - forward_buy))
        gm_per_unit = round(price * random.uniform(0.30, 0.46), 2)
        trade_spend = round(promo_units * price * (depth/100.0) * random.uniform(0.85, 1.20), 2)
        roi = round((gm_per_unit * true_inc) / trade_spend, 2) if trade_spend else 0.0
        # Industry calibration: median ~1.2x; clip negative outliers
        roi = max(0.1, min(roi, 4.5))
        bd, br = assign_banner(ret, dma)
        rows.append({
            "Event_ID": f"PE{eid:05d}",
            "Start_Date": sd.strftime("%Y-%m-%d"),
            "End_Date": ed.strftime("%Y-%m-%d"),
            "Brand": brand, "Manufacturer": manufacturer,
            "SKU": sid, "Product_Description": sname,
            "Retailer": ret, "Banner_Division": bd, "Banner_Region": br,
            "DMA": dma,
            "Mechanic": mech,
            "Promo_Depth_Pct": depth,
            "Display_Type": random.choice(display_types_for.get(mech, ["None"])),
            "Feature_Type": random.choice(feature_types_for.get(mech, ["None"])),
            "Trade_Spend_USD": trade_spend,
            "Pre_Promo_Baseline_Units": baseline,
            "Promo_Units": promo_units,
            "Lift_Pct": round(lift, 4),
            "Incremental_Units": incremental,
            "Forward_Buy_Pct": round(forward_buy, 4),
            "True_Incremental_Units": true_inc,
            "ROI": roi,
        })

    # Curated ProteinPeak Q2 launch promo events (canonical, from
    # seeds/proteinpeak_q2_launch.csv — added here so they appear in
    # `promo_events.parquet` alongside the seed file).
    pp_launch_seed = os.path.join(SEEDS_DIR, "proteinpeak_q2_launch.csv")
    if os.path.exists(pp_launch_seed):
        try:
            seed_df = pd.read_csv(pp_launch_seed)
            for _, srow in seed_df.iterrows():
                if str(srow.get("sku","")).startswith("PP") is False:
                    continue
                eid += 1
                # Map seed event into the promo_events schema
                bd, br = assign_banner(srow["retailer"], "DAL")
                rows.append({
                    "Event_ID": f"PE{eid:05d}",
                    "Start_Date": srow["start_date"],
                    "End_Date": srow["end_date"],
                    "Brand": srow["brand"],
                    "Manufacturer": srow["manufacturer"],
                    "SKU": srow["sku"],
                    "Product_Description": srow["sku_name"],
                    "Retailer": srow["retailer"],
                    "Banner_Division": bd,
                    "Banner_Region": br,
                    "DMA": "ALL",
                    "Mechanic": "Endcap" if "Endcap" in str(srow["event_type"]) else (
                        "Launch" if "Launch" in str(srow["event_type"]) else
                        "TPR" if "TPR" in str(srow["event_type"]) else "Display"),
                    "Promo_Depth_Pct": int(srow["promo_depth_pct_off"]) if str(srow["promo_depth_pct_off"]).isdigit() else 0,
                    "Display_Type": "Endcap" if str(srow["display"]).strip().upper() == "Y" else "None",
                    "Feature_Type": "Digital_Coupon" if str(srow["feature"]).strip().upper() == "Y" else "None",
                    "Trade_Spend_USD": 1200000.0 if srow["retailer"] == "Target" else 250000.0,
                    "Pre_Promo_Baseline_Units": 0,    # new SKU baseline = 0
                    "Promo_Units": 0,                 # populated downstream
                    "Lift_Pct": 0.0,
                    "Incremental_Units": 0,
                    "Forward_Buy_Pct": 0.0,
                    "True_Incremental_Units": 0,
                    "ROI": 0.0,
                })
        except Exception as e:
            print(f"  ! Could not merge ProteinPeak Q2 launch seed events: {e}")
    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# 11. Competitor launches  (T1.4)
# -----------------------------------------------------------------------------

def gen_competitor_launches() -> pd.DataFrame:
    """Pass-through of seeds/competitor_launches.csv into a parquet table."""
    seed_path = os.path.join(SEEDS_DIR, "competitor_launches.csv")
    df = pd.read_csv(seed_path)
    return df


# =============================================================================
# v0.3.0 — Brand & Insights synthesis
# =============================================================================
# Tier 2 + remaining gaps. Tables added:
#   • social_mentions   (T2.1)
#   • creator_posts     (T2.2)
#   • search_trends     (T2.3)
#   • product_reviews   (T2.4)
#   • data_freshness_log (T3.4)


# -----------------------------------------------------------------------------
# 12. Social mentions (Brandwatch-shape)  (T2.1)
# -----------------------------------------------------------------------------

def _make_proteinpeak_launch_mention(idx: int) -> dict:
    """Helper — narrative-anchored ProteinPeak Q2 launch mention."""
    platform = random.choices(["TikTok","Instagram","Twitter","Reddit","YouTube"],
                               weights=[42,28,10,8,12])[0]
    author = random.choices(["Consumer","Creator","Press","Brand"], weights=[58,32,6,4])[0]
    d_offset = random.randint(0, (DATA_END_DATE - PP_Q2_LAUNCH_DATE).days)
    d = PP_Q2_LAUNCH_DATE + timedelta(days=d_offset)
    topics = ["new-launch","protein","athlete-fuel"]
    flavor = random.choice(["cinnamon","cocoa-chocolate"])
    topics.append(flavor)
    if random.random() < 0.40:
        topics.append("creator-drop")
    if random.random() < 0.35:
        topics.append("target-endcap")
    if random.random() < 0.25:
        topics.append("taste")
    sentiment = random.gauss(0.46, 0.28)
    sentiment = max(-1.0, min(1.0, sentiment))
    if platform == "TikTok":
        reach = random.randint(8000, 3_800_000)
    elif platform == "Instagram":
        reach = random.randint(2000, 1_400_000)
    elif platform == "YouTube":
        reach = random.randint(3000, 1_200_000)
    else:
        reach = random.randint(80, 220_000)
    engagement = int(reach * random.uniform(0.012, 0.092))
    return {
        "Mention_ID": f"SM_PP_{idx:06d}",
        "Date": d.strftime("%Y-%m-%d"),
        "Platform": platform,
        "Brand_Mentioned": "ProteinPeak",
        "Manufacturer": "Acme Corp",
        "Author_Type": author,
        "Reach": reach,
        "Engagement": engagement,
        "Sentiment_-1to1": round(sentiment, 3),
        "Sentiment_Bucket": ("Positive" if sentiment > 0.18
                              else "Negative" if sentiment < -0.18 else "Neutral"),
        "Topic_Tags": ";".join(sorted(set(topics))),
        "Has_Video": 1 if platform in ("TikTok","Instagram","YouTube") and random.random() < 0.65 else 0,
        "DMA_Region": random.choice(["UNKNOWN","NYC","LAX","CHI","ATL","DAL","BOS","SFO"]),
        "Source": "Brandwatch",
    }


def _make_la_crunchwell_mention(idx: int) -> dict:
    """Helper — narrative-anchored LA Crunchwell mention with explicit topic gating."""
    platform = random.choices(["TikTok","Instagram","Twitter","Reddit","Facebook"],
                               weights=[34,28,18,12,8])[0]
    author = random.choices(["Consumer","Creator","Press","Brand"], weights=[80,14,4,2])[0]
    d_offset = random.randint(0, (date(2026,3,31) - date(2025,10,1)).days)
    d = date(2025,10,1) + timedelta(days=d_offset)
    topics = ["supply-issue","negative-experience"]
    if random.random() < 0.55:
        topics.append(random.choice(["taste","packaging","price","family-occasion"]))
    if d >= date(2025,11,8) and d <= date(2025,12,28):
        topics.append("supply-issue")
    sentiment = random.gauss(-0.45, 0.30)
    sentiment = max(-1.0, min(1.0, sentiment))
    if platform == "TikTok":
        reach = random.randint(2000, 1_400_000)
    elif platform == "Instagram":
        reach = random.randint(800, 800_000)
    else:
        reach = random.randint(50, 180_000)
    engagement = int(reach * random.uniform(0.005, 0.085))
    return {
        "Mention_ID": f"SM_LA_{idx:06d}",
        "Date": d.strftime("%Y-%m-%d"),
        "Platform": platform,
        "Brand_Mentioned": "Crunchwell",
        "Manufacturer": "Acme Corp",
        "Author_Type": author,
        "Reach": reach,
        "Engagement": engagement,
        "Sentiment_-1to1": round(sentiment, 3),
        "Sentiment_Bucket": ("Positive" if sentiment > 0.18
                              else "Negative" if sentiment < -0.18 else "Neutral"),
        "Topic_Tags": ";".join(sorted(set(topics))),
        "Has_Video": 1 if platform in ("TikTok","Instagram") and random.random() < 0.55 else 0,
        "DMA_Region": "LA-DMA",
        "Source": "Brandwatch",
    }


def gen_social_mentions(n_rows=18000) -> pd.DataFrame:
    platforms = [("TikTok",0.34),("Instagram",0.28),("Twitter",0.14),("Reddit",0.10),
                 ("YouTube",0.09),("Facebook",0.05)]
    author_types = [("Consumer",0.78),("Creator",0.16),("Press",0.04),("Brand",0.02)]
    brands = [
        # Acme brands + key competitors
        ("Crunchwell","Acme Corp"), ("HoneyNest","Acme Corp"), ("ProteinPeak","Acme Corp"),
        ("MorningOats","Acme Corp"), ("TrailGrove","Acme Corp"), ("RootDay","Acme Corp"),
        ("Cheerios","General Mills"), ("Field & Honey","Larksfield Foods"),
        ("Frosted Flakes","Kellanova"), ("Quaker","PepsiCo"),
        ("Magic Spoon","Magic Spoon"), ("Three Wishes","Three Wishes"),
        ("Catalina Crunch","Catalina"), ("Great Value","Walmart PL"),
        ("Oatly","Oatly"), ("Califia","Califia"), ("KIND","Mars"),
        ("RXBAR","Kellanova"), ("Bear Naked","Kellanova"), ("Kashi","Kellanova"),
    ]
    topics = [
        "protein","sustainability","taste","packaging","price","kids-friendly","health",
        "athlete-fuel","oat-milk","recipes","viral","nostalgic","negative-experience",
        "sweetened","grain-free","family-occasion","late-night","convenience",
        "supply-issue","promo",
        # ProteinPeak Q2 launch topics
        "new-launch","cinnamon","cocoa-chocolate","target-endcap","creator-drop",
    ]

    start, end = date(2024, 1, 1), DATA_END_DATE
    days = (end - start).days
    dma_weights = [(d[0], d[5]) for d in DMAS]

    rows = []
    for i in range(1, n_rows+1):
        platform = weighted_choice(platforms)
        author = weighted_choice(author_types)
        brand, mfr = random.choice(brands)
        d = start + timedelta(days=random.randint(0, days))
        dma = weighted_choice(dma_weights)
        # Topic — multi-tag
        ntags = random.choices([1,2,3,4], weights=[35,40,18,7])[0]
        chosen_topics = random.sample(topics, ntags)
        sentiment = random.gauss(0.18, 0.55)
        # Sentiment narrative anchors
        if brand == "Crunchwell" and dma == "LA-DMA" and d >= date(2025,10,1):
            sentiment -= 0.45
            if random.random() < 0.30:
                chosen_topics = list(set(chosen_topics + ["supply-issue","negative-experience"]))
        if brand == "Field & Honey" and dma == "LA-DMA" and date(2025,10,1) <= d <= date(2026,2,28):
            sentiment = abs(sentiment) + 0.18
            if random.random() < 0.20:
                chosen_topics = list(set(chosen_topics + ["viral","promo"]))
        if brand == "ProteinPeak" and d >= date(2026,1,1) and random.random() < 0.34:
            sentiment += 0.30
            chosen_topics = list(set(chosen_topics + ["protein","athlete-fuel"]))
        # ProteinPeak Q2 launch — strong positive lift; new-launch / cinnamon /
        # cocoa-chocolate / target-endcap / creator-drop topics
        if brand == "ProteinPeak" and d >= PP_Q2_LAUNCH_DATE:
            sentiment = abs(sentiment) + 0.22
            chosen_topics = list(set(chosen_topics + ["new-launch","protein"]))
            if random.random() < 0.5:
                chosen_topics.append(random.choice(["cinnamon","cocoa-chocolate"]))
            if random.random() < 0.30:
                chosen_topics.append("creator-drop")
            if random.random() < 0.25:
                chosen_topics.append("target-endcap")
        sentiment = max(-1.0, min(1.0, sentiment))
        if platform == "TikTok":
            reach = random.randint(2000, 4_500_000)
        elif platform == "Instagram":
            reach = random.randint(800, 2_000_000)
        elif platform == "YouTube":
            reach = random.randint(1500, 1_800_000)
        else:
            reach = random.randint(50, 280_000)
        engagement = int(reach * random.uniform(0.005, 0.085))
        rows.append({
            "Mention_ID": f"SM_{i:08d}",
            "Date": d.strftime("%Y-%m-%d"),
            "Platform": platform,
            "Brand_Mentioned": brand,
            "Manufacturer": mfr,
            "Author_Type": author,
            "Reach": reach,
            "Engagement": engagement,
            "Sentiment_-1to1": round(sentiment, 3),
            "Sentiment_Bucket": ("Positive" if sentiment > 0.18
                                  else "Negative" if sentiment < -0.18 else "Neutral"),
            "Topic_Tags": ";".join(chosen_topics),
            "Has_Video": 1 if platform in ("TikTok","YouTube","Instagram") and random.random() < 0.55 else 0,
            "DMA_Region": dma if random.random() < 0.55 else "UNKNOWN",
            "Source": "Brandwatch",
        })

    # Narrative oversample: boost LA-DMA Crunchwell mentions Q4'25 - Q1'26 so
    # the sentiment dip is statistically visible (~250 dedicated mentions).
    for j in range(1, 251):
        rows.append(_make_la_crunchwell_mention(j))

    # Narrative oversample 2: ProteinPeak Q2 launch buzz (~320 dedicated
    # mentions across April 20 - May 31 2026) — the "viral / endcap / creator
    # drop" pattern that powers the Week-4 read.
    for j in range(1, 321):
        rows.append(_make_proteinpeak_launch_mention(j))

    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# 13. Creator posts (Tribe Dynamics-shape)  (T2.2)
# -----------------------------------------------------------------------------

def gen_creator_posts(n_rows=3500) -> pd.DataFrame:
    """Reads creators.csv seed, generates ~3500 posts with attribution lift."""
    seed_path = os.path.join(SEEDS_DIR, "creators.csv")
    creators = pd.read_csv(seed_path, keep_default_na=False).to_dict("records")

    start, end = date(2024, 6, 1), DATA_END_DATE
    days = (end - start).days
    # Sage Park's Q2 2026 athlete cohort — these creators drive the launch
    # signal. CR-0012 is the signature anchor; cohort 2 = 0007, 0021, 0040, 0042;
    # plus newly-activated CR-0013.
    sage_q2_cohort = {"CR-0012","CR-0007","CR-0021","CR-0040","CR-0042","CR-0013","CR-0027"}
    rows = []
    for i in range(1, n_rows+1):
        c = random.choice(creators)
        d = start + timedelta(days=random.randint(0, days))
        # Pick brand from creator's partnered list, or random brand
        if c.get("partnered_with"):
            options = [s.strip() for s in str(c["partnered_with"]).split(";")]
            brand = random.choice(options)
        else:
            brand = random.choice(["Crunchwell","ProteinPeak","HoneyNest","MorningOats",
                                   "TrailGrove","RootDay","Field & Honey",
                                   "Cheerios","Magic Spoon"])
        # Sage Park cohort heavily skews ProteinPeak on/after launch
        if c.get("creator_id") in sage_q2_cohort and d >= PP_Q2_LAUNCH_DATE - timedelta(days=14):
            brand = "ProteinPeak"
        # Disclosed partnership likelihood
        disclosed = "Yes" if random.random() < 0.42 else "No"
        if c.get("creator_id") in sage_q2_cohort and brand == "ProteinPeak":
            disclosed = "Yes"
        # Reach varies by tier — use creator's followers as anchor
        followers = int(c.get("followers", 100000))
        reach = int(followers * random.uniform(0.18, 0.85))
        engagement_rate = random.uniform(0.018, 0.092)
        engagement = int(reach * engagement_rate)
        # 72hr attribution lift — only for disclosed partnerships
        if disclosed == "Yes":
            base_lift = random.uniform(800, 64000)
            if c.get("acme_partnership_status","").startswith("Active") and brand in ("Crunchwell","ProteinPeak","HoneyNest","MorningOats","TrailGrove","RootDay"):
                base_lift *= random.uniform(1.1, 1.6)
            # ProteinPeak Q2 launch — Sage Park cohort gets boosted lift
            if (c.get("creator_id") in sage_q2_cohort and brand == "ProteinPeak"
                    and d >= PP_Q2_LAUNCH_DATE):
                base_lift *= random.uniform(1.4, 2.2)
            attributed = round(base_lift, 2)
        else:
            attributed = 0.0
        rows.append({
            "Post_ID": f"CP_{i:08d}",
            "Creator_ID": c["creator_id"],
            "Handle": c["handle"],
            "Platform": c["platform"],
            "Date": d.strftime("%Y-%m-%d"),
            "Brand_Mentioned": brand,
            "Disclosed_Partnership": disclosed,
            "Followers_Snapshot": followers,
            "Reach": reach,
            "Engagement": engagement,
            "Engagement_Rate": round(engagement_rate, 4),
            "Attributed_Sales_Lift_72hr_USD": attributed,
            "Niche": c.get("niche","Unknown"),
            "Tier": c.get("tier","Mid"),
            "Source": "Tribe Dynamics",
        })
    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# 14. Search trends (Spate / Helium 10 / Google Trends-shape)  (T2.3)
# -----------------------------------------------------------------------------

def gen_search_trends() -> pd.DataFrame:
    keywords_growth = [
        ("high-protein cereal", "RTE Cereal", 0.18, 78),
        ("oat milk barista", "Plant-Based Milk", 0.16, 88),
        ("cinnamon cereal", "RTE Cereal", 0.10, 64),
        ("grain-free cereal", "RTE Cereal", -0.02, 55),
        ("overnight oats", "Hot Cereal", 0.12, 62),
        ("magic spoon review", "RTE Cereal", 0.04, 48),
        ("crunchwell review", "RTE Cereal", -0.04, 22),
        ("crunchwell coupon", "RTE Cereal", 0.02, 14),
        ("proteinpeak", "RTE Cereal", 0.22, 38),
        ("proteinpeak cinnamon crunch", "RTE Cereal", 0.36, 22),
        ("proteinpeak cocoa almond", "RTE Cereal", 0.34, 16),
        ("proteinpeak target", "RTE Cereal", 0.24, 12),
        ("rootday oat milk", "Plant-Based Milk", 0.14, 26),
        ("field & honey", "RTE Cereal", 0.08, 54),
        ("cheerios oat crunch", "RTE Cereal", 0.34, 64),
        ("kids cereal best", "RTE Cereal", 0.02, 32),
        ("hispanic cereal", "RTE Cereal", 0.08, 18),
        ("maizoro cereal", "RTE Cereal", 0.16, 24),
        ("low sugar cereal", "RTE Cereal", 0.06, 44),
        ("granola best", "Granola", 0.04, 56),
        ("trailgrove granola", "Granola", 0.04, 22),
        ("morningoats steel cut", "Hot Cereal", -0.02, 18),
        ("morningoats overnight", "Hot Cereal", 0.16, 14),
        ("oat milk creamer", "Plant-Based Milk", 0.18, 32),
        ("keto cereal", "RTE Cereal", -0.04, 38),
        ("cereal fasting friendly", "RTE Cereal", -0.06, 24),
        ("cheerios honey vanilla", "RTE Cereal", 0.12, 28),
        ("frosted flakes new", "RTE Cereal", 0.08, 32),
        ("acme cereal recall", "RTE Cereal", 0.02, 8),
        ("field & honey almond", "RTE Cereal", 0.34, 38),
        ("rxbar cookie dough", "Bar", 0.14, 26),
        ("kind bar caramel", "Bar", 0.06, 22),
        ("plant based milk taste", "Plant-Based Milk", 0.10, 30),
    ]

    months = []
    d = date(2024, 1, 1)
    while d <= DATA_END_DATE:
        months.append(d)
        # next month
        d = date(d.year + (1 if d.month == 12 else 0), 1 if d.month == 12 else d.month+1, 1)
    platforms = ["Google","Amazon","TikTok"]
    rows = []
    rid = 0
    for kw, cat, mom, base_vol in keywords_growth:
        for p in platforms:
            v = base_vol * (0.62 if p == "TikTok" else 1.0 if p == "Google" else 0.84)
            for i, m in enumerate(months):
                rid += 1
                # Smooth MoM growth + noise
                drift = (1.0 + mom) ** (i / 12.0)
                volume = v * drift * random.uniform(0.88, 1.14)
                # Cheerios Oat Crunch peaks at launch (Jan 2026)
                if "cheerios oat" in kw and m >= date(2026,1,1):
                    volume *= 1.6
                # Field & Honey Almond peaks at launch (Sept 2025)
                if "field & honey almond" in kw and m >= date(2025,9,1):
                    volume *= 1.8
                # ProteinPeak grows with brand momentum
                if "proteinpeak" in kw and m >= date(2025,9,1):
                    volume *= 1.3
                # ProteinPeak Cinnamon Crunch / Cocoa Almond peak at launch (April 2026)
                if "proteinpeak cinnamon" in kw and m >= date(2026,4,1):
                    volume *= 2.8
                if "proteinpeak cocoa" in kw and m >= date(2026,4,1):
                    volume *= 2.2
                if "proteinpeak target" in kw and m >= date(2026,4,1):
                    volume *= 1.9
                # PP005/PP006 keywords don't exist before launch month
                if ("proteinpeak cinnamon" in kw or "proteinpeak cocoa" in kw) and m < date(2026,4,1):
                    volume *= 0.05
                rows.append({
                    "Date": m.strftime("%Y-%m-01"),
                    "Platform": p,
                    "Keyword": kw,
                    "Category": cat,
                    "Volume_Index_0to100": round(min(100, volume), 1),
                    "Brand_Relevance": (
                        "Crunchwell" if "crunchwell" in kw else
                        "ProteinPeak-PP005" if "proteinpeak cinnamon" in kw else
                        "ProteinPeak-PP006" if "proteinpeak cocoa" in kw else
                        "ProteinPeak" if "proteinpeak" in kw else
                        "RootDay" if "rootday" in kw else
                        "TrailGrove" if "trailgrove" in kw else
                        "MorningOats" if "morningoats" in kw else
                        "Cheerios" if "cheerios" in kw else
                        "Field & Honey" if "field & honey" in kw else
                        "Frosted Flakes" if "frosted flakes" in kw else
                        "Magic Spoon" if "magic spoon" in kw else
                        "Maizoro" if "maizoro" in kw else
                        "RXBAR" if "rxbar" in kw else
                        "KIND" if "kind bar" in kw else
                        "category"
                    ),
                    "MoM_Growth_Pct": round(mom * 100, 1),
                    "Source": "Spate" if p in ("Google","TikTok") else "Helium 10",
                })
    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# 15. Product reviews (Bazaarvoice / PowerReviews-shape)  (T2.4)
# -----------------------------------------------------------------------------

def gen_product_reviews(n_rows=24000) -> pd.DataFrame:
    review_retailers = [("Amazon",0.34),("Walmart.com",0.26),("Target.com",0.18),
                        ("Kroger.com",0.10),("Instacart",0.07),("DTC",0.05)]
    sku_pool = SKUS + [(c[0],c[1],c[2],c[4],c[5],c[6],c[7]) for c in COMP_SKUS]

    topic_options_pos = ["taste","value","kids-love-it","convenience","family-occasion",
                         "athlete-fuel","sustainability","packaging-design","health"]
    topic_options_neg = ["stale","pack-damage","too-sweet","too-bland","price-too-high",
                         "out-of-stock","oos","supply-issue","texture-issue","ingredient-concern"]

    start, end = date(2024, 1, 1), DATA_END_DATE
    days = (end - start).days
    rows = []
    for i in range(1, n_rows+1):
        sku = random.choice(sku_pool)
        sid, sname, brand, cat = sku[0], sku[1], sku[2], sku[3]
        ret = weighted_choice(review_retailers)
        d = start + timedelta(days=random.randint(0, days))
        # PP005/PP006 only exist post-launch
        if sid in PP_Q2_NEW_SKUS and d < PP_Q2_LAUNCH_DATE:
            sku = random.choice([s for s in sku_pool if s[0] not in PP_Q2_NEW_SKUS])
            sid, sname, brand, cat = sku[0], sku[1], sku[2], sku[3]
        # Base rating
        rating = max(1, min(5, int(round(random.gauss(4.3, 0.85)))))
        # Anchor — Cinnamon Twist underperforms, lower ratings
        if sid == "CR006":
            rating = max(1, min(5, int(round(random.gauss(3.4, 1.0)))))
        # Higher-priced premium SKUs get higher ratings on average
        if brand in ("ProteinPeak","TrailGrove","RootDay"):
            rating = max(1, min(5, int(round(random.gauss(4.4, 0.78)))))
        # PP005/PP006 launch — early reviews very positive (athlete cohort skew)
        if sid in PP_Q2_NEW_SKUS:
            rating = max(1, min(5, int(round(random.gauss(4.6, 0.62)))))
        # OOS / supply issue period
        if brand == "Crunchwell" and d >= date(2025,11,8) and d <= date(2026,1,15):
            if random.random() < 0.18:
                rating = max(1, min(rating, 3))
        verified = "Yes" if random.random() < 0.78 else "No"
        # Topic tags
        if rating >= 4:
            tags = random.sample(topic_options_pos, random.choice([1,2,3]))
        else:
            tags = random.sample(topic_options_neg, random.choice([1,2]))
        sentiment = round(random.uniform(0.1, 1.0) if rating >= 4 else random.uniform(-1.0, 0.0), 3)
        rows.append({
            "Review_ID": f"PR_{i:08d}",
            "SKU": sid,
            "Brand": brand,
            "Category": cat,
            "Retailer": ret,
            "Date": d.strftime("%Y-%m-%d"),
            "Rating_1to5": rating,
            "Verified_Purchase": verified,
            "Topic_Tags": ";".join(tags),
            "Sentiment_-1to1": sentiment,
            "Review_Length_Chars": random.choice([60,120,180,260,420,640,820,1200]),
            "Helpful_Votes": random.choices([0,1,2,3,5,8,12,24,38,72], weights=[40,18,12,8,7,5,4,3,2,1])[0],
            "Source": "Bazaarvoice" if ret in ("Walmart.com","Target.com","Kroger.com","DTC") else "PowerReviews" if ret == "Walmart.com" else "Amazon Brand Analytics",
        })
    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# 16. Data freshness log  (T3.4)
# -----------------------------------------------------------------------------

def gen_data_freshness_log() -> pd.DataFrame:
    """Lightweight metadata feed — useful for the 'any data gaps?' prompt."""
    feeds = [
        ("NielsenIQ syndicated",      "Daily",   "On-Track"),
        ("IRI Circana syndicated",    "Daily",   "On-Track"),
        ("Numerator panel",           "Daily",   "On-Track"),
        ("Walmart Luminate",          "Daily",   "On-Track"),
        ("Kroger 84.51",              "Daily",   "Lagging"),
        ("Target Roundel",            "Daily",   "On-Track"),
        ("Amazon Brand Analytics",    "Daily",   "On-Track"),
        ("Profitero digital shelf",   "Daily",   "On-Track"),
        ("SAP shipments",             "Hourly",  "On-Track"),
        ("SAP plan",                  "Daily",   "On-Track"),
        ("Brandwatch social",         "Hourly",  "On-Track"),
        ("Sprout Social owned",       "Hourly",  "On-Track"),
        ("Tribe Dynamics creators",   "Daily",   "On-Track"),
        ("Spate search Google",       "Daily",   "On-Track"),
        ("Helium 10 Amazon search",   "Daily",   "Lagging"),
        ("Bazaarvoice reviews",       "Daily",   "On-Track"),
        ("PowerReviews reviews",      "Daily",   "On-Track"),
        ("Mintel GNPD",               "Weekly",  "On-Track"),
        ("Kantar brand health",       "Bi-monthly","On-Track"),
        ("Suzy quick survey",         "On-Demand","On-Track"),
        ("US Census ACS",             "Annual",  "On-Track"),
        ("USDA ERS",                  "Quarterly","On-Track"),
        ("SymphonyAI Retail",         "Daily",   "On-Track"),
        ("Datassential Foodservice",  "Quarterly","On-Track"),
        ("Google Trends (free)",      "Real-time","On-Track"),
    ]
    weeks = []
    d = date(2026, 1, 5)
    while d <= DATA_END_DATE:
        weeks.append(d); d += timedelta(days=7)
    rows = []
    rid = 0
    for wk in weeks:
        for feed_name, cadence, default_status in feeds:
            rid += 1
            # Random small drift events
            lag_hours = random.choices([0,2,6,12,24,48,96],
                                        weights=[55,15,12,8,5,3,2])[0]
            status = default_status
            if lag_hours >= 24 and status == "On-Track":
                status = "Lagging"
            if lag_hours >= 48:
                status = "Stale"
            # Simulated planned outages
            if feed_name == "SAP shipments" and wk == date(2026,2,16):
                status = "Outage"; lag_hours = 18
            rows.append({
                "Week_Start": wk.strftime("%Y-%m-%d"),
                "Feed_Name": feed_name,
                "Cadence": cadence,
                "Last_Refreshed": (wk - timedelta(hours=lag_hours)).strftime("%Y-%m-%d %H:%M:%S"),
                "Lag_Hours": lag_hours,
                "Status": status,
                "Owner_Team": (
                    "Insights" if feed_name.startswith(("NielsenIQ","IRI","Numerator","SymphonyAI"))
                    else "E-Comm" if feed_name in ("Profitero digital shelf","Helium 10 Amazon search","Amazon Brand Analytics")
                    else "Marketing" if "social" in feed_name.lower() or "creator" in feed_name.lower() or feed_name.startswith("Spate")
                    else "Innovation" if "Mintel" in feed_name or "Datassential" in feed_name or "Suzy" in feed_name
                    else "IT" if feed_name.startswith("SAP")
                    else "External"
                ),
            })
    return pd.DataFrame(rows)


# =============================================================================
# v0.7.0 — Marketing & Insights tables (Scenarios S6–S11)
# =============================================================================
# Six new tables anchored to the v2 Marketing & Insights persona pack
# (workspace: 03-research/acme/11-scenarios/v2/). All six are loaded from
# hand-curated seeds; one (ua_study_responses) is expanded from the cohort
# reference grain into per-respondent rows.

# -----------------------------------------------------------------------------
# 17. Brand Equity Tracker — Kantar-shape quarterly tracker with Relevance +
#     Modernity attributes added on top of the v0.1.0 brand_health 5pt battery.
#     Anchors Cory Whitman's FY27 brand plan diagnosis (Relevance -6 over 6 quarters).
# -----------------------------------------------------------------------------

def gen_brand_equity_quarterly() -> pd.DataFrame:
    seed_path = os.path.join(SEEDS_DIR, "brand_equity_tracker_quarterly.csv")
    df = pd.read_csv(seed_path)
    # Normalize column names to repo convention (TitleCase)
    df = df.rename(columns={
        "brand":             "Brand",
        "dma":               "DMA",
        "wave":              "Wave",
        "wave_close_date":   "Wave_Close_Date",
        "attribute":         "Attribute",
        "top_two_box_pct":   "Top_Two_Box_Pct",
        "n_respondents":     "N_Respondents",
    })
    df["Source"] = "Kantar Brand Equity Tracker"
    df["Methodology_Note"] = df["Attribute"].map({
        "Trust":     "5pt top-two-box; long-running attribute since 2019",
        "Relevance": "5pt top-two-box; added FY24 — Cory's lead-indicator attribute",
        "Quality":   "5pt top-two-box; long-running attribute since 2019",
        "Taste":     "5pt top-two-box; long-running attribute since 2019",
        "Modernity": "5pt top-two-box; added FY24 — paired with Relevance",
    }).fillna("5pt top-two-box")
    return df


# -----------------------------------------------------------------------------
# 18. U&A Study Responses — April 2026 Ipsos U&A behavioral study, expanded from
#     the cohort × occasion reference grain into per-respondent rows (n=2,400).
#     Anchors Nina Ortega's Q3 SOTB and Maya's Chocolate Almond concept test.
# -----------------------------------------------------------------------------

def gen_ua_study_responses(n_total: int = 2400) -> pd.DataFrame:
    """Expand the cohort reference grain into n=2,400 per-respondent rows.

    Anchors:
      - 28% of households skip cereal 3+ mornings/week
      - 64% of skippers cite protein as the swap driver
      - cereal-skipper cohort n=672 (large enough for segment-level, not regional)
      - intent to add protein to the morning +9 pts YoY
    """
    cohort_sizes = {
        "cereal-skipper":   672,
        "protein-returner": 540,
        "loyal-family":     768,
        "price-shopper":    420,
    }
    assert sum(cohort_sizes.values()) == n_total, "U&A cohort sizes must sum to 2400"

    # Occasion priors (sums to ~100% per cohort)
    occasion_priors = {
        "cereal-skipper":   {"weekday-am": 0.15, "weekend-am": 0.30,
                             "post-workout": 0.18, "afternoon-snack": 0.22, "evening": 0.15},
        "protein-returner": {"weekday-am": 0.48, "weekend-am": 0.22,
                             "post-workout": 0.18, "afternoon-snack": 0.08, "evening": 0.04},
        "loyal-family":     {"weekday-am": 0.62, "weekend-am": 0.24,
                             "post-workout": 0.04, "afternoon-snack": 0.06, "evening": 0.04},
        "price-shopper":    {"weekday-am": 0.51, "weekend-am": 0.26,
                             "post-workout": 0.07, "afternoon-snack": 0.10, "evening": 0.06},
    }
    # Cite-protein-as-swap rate by cohort
    cite_protein = {"cereal-skipper": 0.64, "protein-returner": 0.78,
                    "loyal-family": 0.18, "price-shopper": 0.22}
    # Intent to add protein to morning (10pt scale; +9pp YoY for cereal-skipper + protein-returner)
    intent_add_protein = {"cereal-skipper": 7.4, "protein-returner": 8.6,
                          "loyal-family": 4.2, "price-shopper": 5.1}
    # Skip frequency (mornings/week)
    skip_freq = {"cereal-skipper": 4.2, "protein-returner": 1.8,
                 "loyal-family": 0.4, "price-shopper": 1.2}

    rows = []
    rid = 1
    for cohort, n in cohort_sizes.items():
        occ_keys = list(occasion_priors[cohort].keys())
        occ_weights = [occasion_priors[cohort][k] for k in occ_keys]
        for _ in range(n):
            dma_pick = random.choices(DMAS, weights=[d[5] for d in DMAS], k=1)[0]
            dma = dma_pick[0]
            primary_occ = random.choices(occ_keys, weights=occ_weights, k=1)[0]
            # Skip-cereal-3plus flag — cereal-skipper is the cohort defined by
            # this behavior (672/2400 = 28% exact, per v2 canon). Other cohorts
            # do not flag, by construction — protein-returners *swap back* to
            # cereal via protein offers, loyal-family stay, price-shoppers buy
            # whichever is cheapest.
            skip_3plus = 1 if cohort == "cereal-skipper" else 0
            cite_p = 1 if random.random() < cite_protein[cohort] else 0
            intent = max(0.0, min(10.0,
                       random.gauss(intent_add_protein[cohort], 1.6)))
            sf = max(0.0, min(7.0,
                       random.gauss(skip_freq[cohort], 1.1)))
            chocolate_pref = 1 if (cohort == "protein-returner" and random.random() < 0.30) or \
                                  (cohort == "cereal-skipper" and random.random() < 0.18) else 0
            glp1_adjacent = 1 if random.random() < (
                0.22 if cohort == "cereal-skipper" else
                0.18 if cohort == "protein-returner" else
                0.06 if cohort == "loyal-family" else 0.08) else 0
            rows.append({
                "Response_ID":           f"UA_{rid:06d}",
                "Field_Date":            "2026-04-08",
                "Wave":                  "2026Q2",
                "Cohort":                cohort,
                "DMA":                   dma,
                "State":                 DMA_STATE[dma],
                "Primary_Occasion":      primary_occ,
                "Skip_Cereal_3plus_Mornings": skip_3plus,
                "Cite_Protein_As_Swap_Driver": cite_p,
                "Intent_Add_Protein_Morning_0to10": round(intent, 1),
                "Skip_Frequency_Mornings_Per_Wk": round(sf, 1),
                "Chocolate_Breakfast_Pref":     chocolate_pref,
                "GLP1_Adjacent":         glp1_adjacent,
                "HOH_Age_Band":          random.choice(["18-24","25-34","35-44","45-54","55-64","65+"]),
                "Income_Band":           random.choice(INCOME_BANDS),
                "Presence_Of_Kids_5_14": random.choices([0, 1], weights=[60, 40])[0],
                "Vendor":                "Ipsos",
                "Respondent_Weight":     round(random.uniform(0.6, 1.4), 4),
            })
            rid += 1
    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# 19. U&A Qual Pointers — 36 in-home interview index, loaded from seed.
# -----------------------------------------------------------------------------

def gen_ua_qual_pointers() -> pd.DataFrame:
    seed_path = os.path.join(SEEDS_DIR, "ua_qual_pointers_2026q2.csv")
    df = pd.read_csv(seed_path)
    df = df.rename(columns={
        "interview_id":            "Interview_ID",
        "cohort":                  "Cohort",
        "dma":                     "DMA",
        "hoh_age_band":            "HOH_Age_Band",
        "n_kids":                  "N_Kids",
        "income_band":             "Income_Band",
        "themes":                  "Themes",
        "chocolate_mention_flag":  "Chocolate_Mention_Flag",
        "chocolate_unprompted_flag": "Chocolate_Unprompted_Flag",
        "duration_min":            "Duration_Min",
        "transcript_path":         "Transcript_Path",
        "notes":                   "Notes",
    })
    df["Wave"] = "2026Q2"
    df["Field_Date"] = "2026-04-08"
    df["Vendor"] = "Ipsos qual partner"
    return df


# -----------------------------------------------------------------------------
# 20. Kantar Worldpanel Cohort Frame — household penetration + frequency by
#     cohort × DMA × quarter. Anchors Nina's SOTB and Jordan's LA diagnostic.
# -----------------------------------------------------------------------------

def gen_kantar_worldpanel_cohort() -> pd.DataFrame:
    seed_path = os.path.join(SEEDS_DIR, "kantar_worldpanel_cohort_frame.csv")
    df = pd.read_csv(seed_path)
    df = df.rename(columns={
        "cohort":                       "Cohort",
        "dma":                          "DMA",
        "quarter":                      "Quarter",
        "wave_close_date":              "Wave_Close_Date",
        "hh_penetration_pct":           "HH_Penetration_Pct",
        "purchases_per_buyer_per_qtr":  "Purchases_Per_Buyer_Per_Qtr",
        "n_panel_hh":                   "N_Panel_HH",
    })
    df["Source"] = "Kantar Worldpanel"
    return df


# -----------------------------------------------------------------------------
# 21. Numerator BTS Occasion — back-to-school occasion benchmark from the 2025
#     Target program. Anchors Wes Okafor's Target BTS 2026 scenario.
# -----------------------------------------------------------------------------

def gen_numerator_bts_occasion() -> pd.DataFrame:
    seed_path = os.path.join(SEEDS_DIR, "numerator_bts_occasion_2025.csv")
    df = pd.read_csv(seed_path)
    df = df.rename(columns={
        "retailer":                                  "Retailer",
        "iso_week":                                  "ISO_Week",
        "week_start_date":                           "Week_Start_Date",
        "hh_kids_5_14_buying_cereal_share":          "HH_Kids_5_14_Buying_Cereal_Share",
        "protein_curious_cohort_overlap":            "Protein_Curious_Cohort_Overlap",
        "target_circle_membership_overlap":          "Target_Circle_Membership_Overlap",
        "incremental_category_dollars_kusd":         "Incremental_Category_Dollars_KUSD",
        "definition":                                "Definition",
    })
    df["Program_Year"] = 2025
    df["Source"] = "Numerator household panel + Target Circle membership overlay"
    return df


# -----------------------------------------------------------------------------
# 22. Concept Tests — combines Chocolate Almond + April launch-claims tests
#     into one parquet table. Anchors Maya Chen's concept-test workspace and
#     Renee Alvarez's launch comms plan.
# -----------------------------------------------------------------------------

def gen_concept_tests() -> pd.DataFrame:
    ca_path = os.path.join(SEEDS_DIR, "concept_test_chocolate_almond.csv")
    lc_path = os.path.join(SEEDS_DIR, "concept_test_launch_claims_2026q2.csv")
    ca = pd.read_csv(ca_path)
    lc = pd.read_csv(lc_path)

    # Normalize Chocolate Almond to canonical columns
    ca = ca.rename(columns={
        "section": "Section", "metric": "Metric", "value": "Value",
        "unit": "Unit", "scope": "Scope", "notes": "Notes",
    })
    ca["Test_ID"] = "CT_CHOC_ALMOND_2026Q3"
    ca["Test_Name"] = "ProteinPeak Chocolate Almond Extension"
    ca["Vendor"] = "Ipsos"
    ca["Acme_Segmentation_Used"] = 1
    ca["Cannibalization_Threshold_Pp"] = 12

    # Normalize launch-claims
    lc = lc.rename(columns={
        "claim_id": "Section", "metric": "Metric", "value": "Value",
        "unit": "Unit", "cohort": "Scope", "notes": "Notes",
    })
    lc["Test_ID"] = "CT_LAUNCH_CLAIMS_2026Q2"
    lc["Test_Name"] = "ProteinPeak Launch Claims Test"
    lc["Vendor"] = "Kantar"
    lc["Acme_Segmentation_Used"] = 1
    lc["Cannibalization_Threshold_Pp"] = None

    df = pd.concat([ca, lc], ignore_index=True)
    # Standard column order
    df = df[["Test_ID", "Test_Name", "Vendor", "Section", "Metric",
             "Value", "Unit", "Scope", "Acme_Segmentation_Used",
             "Cannibalization_Threshold_Pp", "Notes"]]
    return df


# -----------------------------------------------------------------------------
# Cross-table assertions  (v0.2.0)
# -----------------------------------------------------------------------------

def assert_consistency(tables: dict[str, pd.DataFrame]):
    """Lightweight invariants. Raises AssertionError if a narrative anchor drifts."""
    pva = tables["plan_vs_actual"]
    la_q1 = pva[(pva["Brand"]=="Crunchwell") & (pva["DMA"]=="LA-DMA")
                & (pva["Period"].isin(["2026-01","2026-02","2026-03"]))]
    if not la_q1.empty:
        avg_var = la_q1["Variance_Pct"].mean()
        assert avg_var < -0.30, f"LA Crunchwell Q1 2026 variance not Red enough: {avg_var:.2%}"

    ship = tables["shipments"]
    storm = ship[(ship["Week_Start"] >= "2025-11-08") & (ship["Week_Start"] <= "2025-12-10")
                 & ship["Retailer_DC"].str.contains("Houston|Thibodaux|Tyler|Hammond", regex=True)]
    if len(storm) > 0:
        assert storm["Fill_Rate_Pct"].mean() < 0.75, "Hurricane Tonya fill rate not impacted enough"

    auth = tables["sku_authorization"]
    cinn = auth[(auth["SKU"]=="CR006") & (auth["Auth_Status"]=="Authorized")]
    cinn_ratio = len(cinn) / max(1, len(auth[auth["SKU"]=="CR006"]))
    assert 0.30 <= cinn_ratio <= 0.55, f"Cinnamon Twist auth rate off: {cinn_ratio:.0%}"

    soc = tables["social_mentions"]
    la_cw = soc[(soc["Brand_Mentioned"]=="Crunchwell") & (soc["DMA_Region"]=="LA-DMA")
                & (soc["Date"] >= "2025-10-01")]
    if len(la_cw) > 50:
        avg_sent = la_cw["Sentiment_-1to1"].mean()
        assert avg_sent < -0.10, f"LA Crunchwell sentiment not negative enough: {avg_sent:.2f}"

    rev = tables["product_reviews"]
    cinn_rev = rev[rev["SKU"]=="CR006"]["Rating_1to5"].mean()
    hero_rev = rev[rev["SKU"].isin(["CR001","CR002","CR003"])]["Rating_1to5"].mean()
    assert cinn_rev < hero_rev - 0.5, "Cinnamon Twist not rated worse than hero SKUs"

    # -------------------------------------------------------------------------
    # ProteinPeak Q2 2026 launch (Scenario 2) assertions
    # -------------------------------------------------------------------------
    ps = tables["perfect_store"]
    pp_launch_window = ps[(ps["SKU"].isin(["PP005","PP006"]))
                          & (ps["Date"] >= "2026-04-20")]
    pp_target = pp_launch_window[pp_launch_window["Banner"] == "Target"]
    pp_walmart = pp_launch_window[pp_launch_window["Banner"] == "Walmart"]
    if len(pp_target) > 30 and len(pp_walmart) > 30:
        tgt_vel = pp_target["Sales_Units"].mean()
        wal_vel = pp_walmart["Sales_Units"].mean()
        assert tgt_vel > wal_vel, (
            f"ProteinPeak Q2 launch Target velocity {tgt_vel:.2f} should exceed "
            f"Walmart velocity {wal_vel:.2f}"
        )

    # Cannibalization check: PP001 launch-window velocity slightly under FY26 base.
    pp001_pre  = ps[(ps["SKU"]=="PP001") & (ps["Date"] >= "2026-01-01")
                    & (ps["Date"] <  "2026-04-20")]["Sales_Units"].mean()
    pp001_post = ps[(ps["SKU"]=="PP001") & (ps["Date"] >= "2026-04-20")]["Sales_Units"].mean()
    if not pd.isna(pp001_pre) and not pd.isna(pp001_post):
        assert pp001_post < pp001_pre * 1.02, (
            f"PP001 post-launch velocity {pp001_post:.2f} should reflect "
            f"cannibalization vs pre-launch {pp001_pre:.2f}"
        )

    # Authorization: PP005/PP006 should be ~0% authorized before 2026-04
    auth_pre = tables["sku_authorization"]
    pp_pre = auth_pre[(auth_pre["SKU"].isin(["PP005","PP006"]))
                       & (auth_pre["Snapshot_Date"] < "2026-04-30")
                       & (auth_pre["Auth_Status"] == "Authorized")]
    assert len(pp_pre) == 0, "PP005/PP006 should not be authorized pre-2026-04-30"

    # Plan vs Actual: April 2026 ProteinPeak Target should be over plan
    pva = tables["plan_vs_actual"]
    pp_apr_tgt = pva[(pva["Brand"]=="ProteinPeak") & (pva["Retailer"]=="Target")
                     & (pva["Period"].isin(["2026-04","2026-05"]))]
    pp_apr_wal = pva[(pva["Brand"]=="ProteinPeak") & (pva["Retailer"]=="Walmart")
                     & (pva["Period"].isin(["2026-04","2026-05"]))]
    if not pp_apr_tgt.empty and not pp_apr_wal.empty:
        tgt_var = pp_apr_tgt["Variance_Pct"].mean()
        wal_var = pp_apr_wal["Variance_Pct"].mean()
        assert tgt_var > wal_var, (
            f"ProteinPeak Q2 launch: Target variance {tgt_var:+.1%} should "
            f"exceed Walmart variance {wal_var:+.1%}"
        )

    # Social mentions: ProteinPeak Q2 launch period sentiment is positive
    pp_soc = tables["social_mentions"][
        (tables["social_mentions"]["Brand_Mentioned"]=="ProteinPeak")
        & (tables["social_mentions"]["Date"] >= "2026-04-20")
    ]
    if len(pp_soc) > 50:
        pp_avg = pp_soc["Sentiment_-1to1"].mean()
        assert pp_avg > 0.10, (
            f"ProteinPeak Q2 launch social sentiment {pp_avg:+.2f} should be positive"
        )

    # Household-level new SKU buys with launch-period Switching_Flag
    hh_tx = tables["household_transactions"]
    pp_hh = hh_tx[hh_tx["Product_SKU"].isin(["PP005","PP006"])]
    assert len(pp_hh) > 0, "Expected PP005/PP006 buys in household_transactions"
    canniba = pp_hh[pp_hh["Switching_Flag"] == "Cannibalization"]
    new_to  = pp_hh[pp_hh["Switching_Flag"] == "New_To_Brand"]
    assert len(new_to) > len(canniba), "New-to-brand should exceed cannibalization"

    # -------------------------------------------------------------------------
    # v0.7.0 — Marketing & Insights v2 scenario assertions
    # -------------------------------------------------------------------------

    # Brand equity: Crunchwell Trust roughly flat over 6 quarters; Relevance
    # falling. Compare FY25Q1 vs FY26Q2 at US-NAT level.
    be = tables["brand_equity_quarterly"]
    cw_nat = be[(be["Brand"] == "Crunchwell") & (be["DMA"] == "US-NAT")]
    if not cw_nat.empty:
        trust_q1 = cw_nat[(cw_nat["Wave"] == "FY25Q1") & (cw_nat["Attribute"] == "Trust")]["Top_Two_Box_Pct"]
        trust_q2 = cw_nat[(cw_nat["Wave"] == "FY26Q2") & (cw_nat["Attribute"] == "Trust")]["Top_Two_Box_Pct"]
        rel_q1   = cw_nat[(cw_nat["Wave"] == "FY25Q1") & (cw_nat["Attribute"] == "Relevance")]["Top_Two_Box_Pct"]
        rel_q2   = cw_nat[(cw_nat["Wave"] == "FY26Q2") & (cw_nat["Attribute"] == "Relevance")]["Top_Two_Box_Pct"]
        if len(trust_q1) and len(trust_q2) and len(rel_q1) and len(rel_q2):
            trust_delta = float(trust_q2.iloc[0]) - float(trust_q1.iloc[0])
            rel_delta   = float(rel_q2.iloc[0]) - float(rel_q1.iloc[0])
            assert abs(trust_delta) < 3.0, (
                f"Crunchwell Trust drift {trust_delta:+.1f}pp — should be roughly flat"
            )
            assert rel_delta <= -3.0, (
                f"Crunchwell Relevance drift {rel_delta:+.1f}pp — should be down ≥3pp "
                f"over six quarters (v2 canon: ~-6pp)"
            )

    # U&A: 28% of households skip cereal 3+ mornings/wk
    ua = tables["ua_study_responses"]
    skip_rate = ua["Skip_Cereal_3plus_Mornings"].mean()
    assert 0.24 <= skip_rate <= 0.32, (
        f"U&A skip-cereal-3plus rate {skip_rate:.1%} — v2 canon is 28%"
    )

    # U&A: cereal-skipper cohort n=672 (cell-size constraint)
    skipper_n = (ua["Cohort"] == "cereal-skipper").sum()
    assert skipper_n == 672, (
        f"U&A cereal-skipper cell-size {skipper_n} — v2 canon is exactly 672"
    )

    # U&A: 64% of cereal-skippers cite protein as the swap driver
    skipper = ua[ua["Cohort"] == "cereal-skipper"]
    cite_rate = skipper["Cite_Protein_As_Swap_Driver"].mean()
    assert 0.58 <= cite_rate <= 0.70, (
        f"U&A cereal-skipper protein-cite rate {cite_rate:.1%} — v2 canon is 64%"
    )

    # Kantar: cereal-skipper penetration trending UP over six quarters
    kw = tables["kantar_worldpanel_cohort"]
    cs_q1 = kw[(kw["Cohort"] == "cereal-skipper") & (kw["DMA"] == "US-NAT") & (kw["Quarter"] == "FY25Q1")]["HH_Penetration_Pct"]
    cs_q6 = kw[(kw["Cohort"] == "cereal-skipper") & (kw["DMA"] == "US-NAT") & (kw["Quarter"] == "FY26Q2")]["HH_Penetration_Pct"]
    if len(cs_q1) and len(cs_q6):
        assert float(cs_q6.iloc[0]) > float(cs_q1.iloc[0]), (
            "Kantar: cereal-skipper cohort penetration should grow over 6 quarters"
        )

    # Numerator BTS: 2025 Target program incremental total ≈ $14.2M
    # (sum across Target rows, in KUSD)
    bts_tab = tables["numerator_bts_occasion"]
    target_incremental_kusd = bts_tab[bts_tab["Retailer"] == "Target"]["Incremental_Category_Dollars_KUSD"].sum()
    assert 13_000 <= target_incremental_kusd <= 15_400, (
        f"Numerator BTS: Target 2025 incremental ${target_incremental_kusd:,.0f}K — "
        f"v2 canon is $14.2M"
    )

    # Numerator BTS: Target shopper × ProteinPeak cohort overlap = 64% (highest)
    target_overlap = bts_tab[bts_tab["Retailer"] == "Target"]["Protein_Curious_Cohort_Overlap"].mean()
    wal_overlap = bts_tab[bts_tab["Retailer"] == "Walmart"]["Protein_Curious_Cohort_Overlap"].mean()
    assert target_overlap > wal_overlap, (
        "Numerator BTS: Target protein-curious overlap should exceed Walmart's"
    )
    assert 0.60 <= target_overlap <= 0.68, (
        f"Numerator BTS: Target overlap {target_overlap:.1%} — v2 canon is 64%"
    )

    # Concept test: Chocolate Almond top-two-box = 64% (clears 55% standard)
    ct = tables["concept_tests"]
    ca_t2b = ct[(ct["Test_ID"] == "CT_CHOC_ALMOND_2026Q3") &
                (ct["Section"] == "topline") &
                (ct["Metric"] == "top_two_box_pct")]["Value"]
    assert not ca_t2b.empty, "Chocolate Almond top-two-box missing"
    assert float(ca_t2b.iloc[0]) >= 55, (
        f"Chocolate Almond top-two-box {ca_t2b.iloc[0]} must clear 55% action standard"
    )

    # Concept test: cannibalization gate — substitutional < 12pp threshold
    sub_pp = ct[(ct["Test_ID"] == "CT_CHOC_ALMOND_2026Q3") &
                (ct["Metric"] == "substitutional_overlap_pp") &
                (ct["Scope"] == "launch_sku")]["Value"]
    assert not sub_pp.empty, "Chocolate Almond substitutional cannibalization missing"
    assert float(sub_pp.iloc[0]) < 12, (
        f"Chocolate Almond substitutional cannibalization {sub_pp.iloc[0]}pp "
        f"must clear 12pp steerco threshold"
    )

    # Competitor launches: Field & Honey 14g protein extension present
    launches_tab = tables["competitor_launches"]
    ff14 = launches_tab[launches_tab["Sku_New"] == "LF-FH-14P"] if "Sku_New" in launches_tab.columns else \
           launches_tab[launches_tab["sku_new"] == "LF-FH-14P"] if "sku_new" in launches_tab.columns else \
           pd.DataFrame()
    if not ff14.empty:
        # F&H 14g launched 2026-05-12
        launch_date_col = "Launch_Date" if "Launch_Date" in ff14.columns else "launch_date"
        assert "2026-05-12" in str(ff14[launch_date_col].iloc[0]), \
            "Field & Honey 14g launch_date must be 2026-05-12"

    # Geographies: BIR-DMA + MEM-DMA present as leading-indicator watch list
    # (Verifies the DMAs list has been extended.)
    syn = tables["syndicated_weekly"]
    dma_col = "DMA" if "DMA" in syn.columns else "dma"
    dmas_present = set(syn[dma_col].unique())
    assert "BIR-DMA" in dmas_present and "MEM-DMA" in dmas_present, (
        f"v0.7.0 leading-indicator DMAs missing — got {sorted(dmas_present)}"
    )

    print(f"  ✓ LA Crunchwell Q1 plan-vs-actual variance: {avg_var:.1%} (Red)")
    print(f"  ✓ Hurricane Tonya storm-DC fill rate avg:    {storm['Fill_Rate_Pct'].mean():.1%}")
    print(f"  ✓ Cinnamon Twist (CR006) authorization rate: {cinn_ratio:.0%}")
    print(f"  ✓ LA Crunchwell social sentiment Q4'25-Q1'26: {avg_sent:+.2f} on n={len(la_cw)} mentions")
    print(f"  ✓ Cinnamon Twist (CR006) avg review rating:  {cinn_rev:.2f} vs hero SKUs {hero_rev:.2f}")
    if len(pp_target) > 30 and len(pp_walmart) > 30:
        print(f"  ✓ PP Q2 launch Target velocity:              {tgt_vel:.2f} vs Walmart {wal_vel:.2f}")
    if not pp_apr_tgt.empty and not pp_apr_wal.empty:
        print(f"  ✓ PP Q2 plan-vs-actual variance (Tgt/Wal):   {tgt_var:+.1%} / {wal_var:+.1%}")
    if len(pp_soc) > 50:
        print(f"  ✓ PP Q2 launch social sentiment:             {pp_avg:+.2f} on n={len(pp_soc)} mentions")
    print(f"  ✓ PP Q2 household source-of-volume:          new-to-brand={len(new_to)}, cannibalization={len(canniba)}")
    # v0.7.0 prints
    if not cw_nat.empty and len(rel_q1) and len(rel_q2):
        print(f"  ✓ Crunchwell Trust drift (FY25Q1→FY26Q2):    {trust_delta:+.1f}pp (flat)")
        print(f"  ✓ Crunchwell Relevance drift (FY25Q1→FY26Q2): {rel_delta:+.1f}pp (declining)")
    print(f"  ✓ U&A skip-cereal-3plus mornings rate:       {skip_rate:.1%} (canon 28%)")
    print(f"  ✓ U&A cereal-skipper cohort n:               {skipper_n} (canon 672)")
    print(f"  ✓ U&A protein-as-swap-driver (skippers):     {cite_rate:.1%} (canon 64%)")
    print(f"  ✓ Numerator BTS Target 2025 incremental:     ${target_incremental_kusd/1000:.1f}M (canon $14.2M)")
    print(f"  ✓ Numerator BTS Target × protein-curious:    {target_overlap:.1%} (canon 64%)")
    print(f"  ✓ Concept test Chocolate Almond top-two-box: {float(ca_t2b.iloc[0]):.0f}% (clears 55% standard)")
    print(f"  ✓ Concept test substitutional cannibalization: {float(sub_pp.iloc[0]):.0f}pp (clears 12pp gate)")


# -----------------------------------------------------------------------------
# Build artifacts: parquet + samples + duckdb
# -----------------------------------------------------------------------------

def build_artifacts(tables: dict[str, pd.DataFrame]):
    import duckdb
    # parquet + sample CSVs
    for name, df in tables.items():
        pq_path = os.path.join(DATA_DIR, f"{name}.parquet")
        df.to_parquet(pq_path, compression="zstd", index=False)
        sample_path = os.path.join(SAMPLE_DIR, f"{name}_sample.csv")
        df.head(100).to_csv(sample_path, index=False)
        print(f"  wrote {pq_path:>70}  ({len(df):>7,} rows)")
        print(f"  wrote {sample_path:>70}  (100-row sample)")
    # DuckDB file with seeds + parquet tables.
    # Build in /tmp first (some mounts don't permit unlink on WAL files);
    # then stream the final bytes into DUCKDB_PATH via plain file write
    # (overwrites without needing unlink).
    import tempfile
    tmp_db = os.path.join(tempfile.gettempdir(), "acme_build.duckdb")
    for p in (tmp_db, tmp_db + ".wal"):
        try:
            if os.path.exists(p): os.remove(p)
        except OSError:
            open(p, "wb").close()  # truncate as fallback

    con = duckdb.connect(tmp_db)
    for name, df in tables.items():
        con.execute(f"CREATE TABLE {name} AS SELECT * FROM df")
    for fn in os.listdir(SEEDS_DIR):
        if fn.endswith(".csv"):
            tn = "seed_" + os.path.splitext(fn)[0]
            con.execute(
                f"CREATE TABLE {tn} AS SELECT * FROM read_csv_auto('{os.path.join(SEEDS_DIR, fn)}')"
            )
    con.execute("CHECKPOINT")
    con.close()

    # Truncate any pre-existing destination (including .wal) and stream-copy.
    for p in (DUCKDB_PATH, DUCKDB_PATH + ".wal"):
        if os.path.exists(p):
            open(p, "wb").close()
    with open(tmp_db, "rb") as src, open(DUCKDB_PATH, "wb") as dst:
        for chunk in iter(lambda: src.read(1 << 20), b""):
            dst.write(chunk)
    print(f"  wrote {DUCKDB_PATH}")


def main():
    print("[ 1/22] EPOS")
    epos = gen_epos(34000)
    print("[ 2/22] Perfect Store")
    perfect_store = gen_perfect_store(56000)
    print("[ 3/22] Syndicated weekly (NielsenIQ-style)")
    syndicated = gen_syndicated_weekly()
    print("[ 4/22] Brand Health")
    brand_health = gen_brand_health(16500)
    print("[ 5/22] Households")
    hh = gen_households(5000)
    print("[ 6/22] Household transactions")
    hh_tx = gen_hh_transactions(hh, 34000)
    print("[ 7/22] Plan vs Actual")
    pva = gen_plan_vs_actual(epos)
    print("[ 8/22] SKU Authorization")
    sku_auth = gen_sku_authorization(perfect_store)
    print("[ 9/22] Shipments / Fill Rate")
    shipments = gen_shipments()
    print("[10/22] Promo Events (all retailers)")
    promo = gen_promo_events()
    print("[11/22] Competitor Launches (from seed)")
    launches = gen_competitor_launches()
    print("[12/22] Social Mentions (Brandwatch-shape)")
    social = gen_social_mentions(20000)
    print("[13/22] Creator Posts (Tribe Dynamics-shape)")
    cposts = gen_creator_posts(3500)
    print("[14/22] Search Trends (Spate / Helium 10-shape)")
    search = gen_search_trends()
    print("[15/22] Product Reviews (Bazaarvoice-shape)")
    reviews = gen_product_reviews(26500)
    print("[16/22] Data Freshness Log")
    freshness = gen_data_freshness_log()
    # v0.7.0 — Marketing & Insights tables
    print("[17/22] Brand Equity Quarterly (Kantar Relevance + Modernity)")
    brand_equity = gen_brand_equity_quarterly()
    print("[18/22] U&A Study Responses (Ipsos Apr 2026, n=2400)")
    ua_resp = gen_ua_study_responses(2400)
    print("[19/22] U&A Qual Pointers (36 in-homes)")
    ua_qual = gen_ua_qual_pointers()
    print("[20/22] Kantar Worldpanel Cohort Frame")
    kantar = gen_kantar_worldpanel_cohort()
    print("[21/22] Numerator BTS Occasion (Target 2025 benchmark)")
    bts = gen_numerator_bts_occasion()
    print("[22/22] Concept Tests (Chocolate Almond + Launch Claims)")
    concept = gen_concept_tests()

    tables = {
        # v0.1.0 core six
        "epos":                  epos,
        "perfect_store":         perfect_store,
        "syndicated_weekly":     syndicated,
        "brand_health":          brand_health,
        "households":            hh,
        "household_transactions":hh_tx,
        # v0.2.0 sales-side completeness
        "plan_vs_actual":        pva,
        "sku_authorization":     sku_auth,
        "shipments":             shipments,
        "promo_events":          promo,
        "competitor_launches":   launches,
        # v0.3.0 brand & insights synthesis
        "social_mentions":       social,
        "creator_posts":         cposts,
        "search_trends":         search,
        "product_reviews":       reviews,
        # v0.4.0 polish
        "data_freshness_log":    freshness,
        # v0.7.0 marketing & insights
        "brand_equity_quarterly": brand_equity,
        "ua_study_responses":     ua_resp,
        "ua_qual_pointers":       ua_qual,
        "kantar_worldpanel_cohort": kantar,
        "numerator_bts_occasion": bts,
        "concept_tests":          concept,
    }
    print("Cross-table consistency assertions …")
    try:
        assert_consistency(tables)
    except AssertionError as e:
        print(f"  ! Consistency warning: {e}")
    print("Building parquet, samples, duckdb …")
    build_artifacts(tables)
    print("Done.")


if __name__ == "__main__":
    main()
