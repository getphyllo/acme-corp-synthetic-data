"""
Acme Corp synthetic-data generator.

One run produces:
  - data/*.parquet                — six tables (Kellogg-shape, US-anchored)
  - samples/*.csv                  — 100-row CSV slices for previewing
  - acme.duckdb                    — single-file SQL database with everything loaded

The narrative is encoded in the data:
  - Crunchwell LA share drops from ~6% (2024) to ~3.9% (Q1 2026)
  - Walmart Sept 2025 modular reset: Crunchwell Mega/Honey Nut Mega/Multigrain
    lose 2 facings (8 → 6) at Walmart stores in the South division
  - Hurricane Tonya (Nov 8, 2025) drops Crunchwell Mega OSA in LA from ~97% to ~67%
  - Honey Bunches of Oats heavy promo at Rouses Q4 '25 → Q1 '26
  - LA Crunchwell-loyal HHs flagged with Switching_Flag = "Yes"

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
    ("PP001", "ProteinPeak Original 12oz",         "ProteinPeak", "RTE Cereal", "Wellness Protein",  12, 7.49),
    ("PP002", "ProteinPeak Chocolate Hazelnut",    "ProteinPeak", "RTE Cereal", "Wellness Protein",  12, 7.49),
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
    ("PF001", "Honey Bunches of Oats 14oz",       "Honey Bunches Oats",  "Post Foods",    "RTE Cereal", "Family Sweet", 14, 4.39),
    ("PF002", "Great Grains 14oz",                "Great Grains",        "Post Foods",    "RTE Cereal", "Family Wholegrain", 14, 4.79),
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
}

DMA_STATE = {
    "LA-DMA":"LA","DAL":"TX","HOU":"TX","ATL":"GA","CHI":"IL","NYC":"NY","LAX":"CA",
    "MIN":"MN","DEN":"CO","PHX":"AZ","SEA":"WA","BOS":"MA","PHL":"PA","DET":"MI",
    "MIA":"FL","MS-DMA":"MS","AL-DMA":"AL","AR-DMA":"AR","OK-DMA":"OK","ORL":"FL",
    "CIN":"OH","STL":"MO","KAN":"MO","PIT":"PA","PDX":"OR","SFO":"CA","CLE":"OH",
    "IND":"IN","BAL":"MD","WAS":"DC",
}

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
    start, end = date(2024, 1, 1), date(2026, 3, 31)
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

        sku = random.choice(sku_pool)
        qty = random.choices([1,2,3,4], weights=[60,25,10,5])[0]
        base = sku["price"]

        promo_flag, promo_type, disc = "No", "None", 0.0
        if random.random() < 0.22:
            promo_flag, promo_type = "Yes", random.choice(["Price Off","Multi-Buy","Bundle","Loyalty"])
            disc = round(random.uniform(0.05, 0.30), 2)
        if (sku["brand"] == "Honey Bunches Oats" and chain in ("Rouses","Brookshires")
                and dma_id == "LA-DMA" and tx_date >= date(2025,10,1)):
            if random.random() < 0.85:
                promo_flag, promo_type, disc = "Yes", "Price Off", 0.21
        if sku["id"] in ("CR002","CR004","CR005") and dma_id == "LA-DMA":
            if date(2025,11,8) <= tx_date <= date(2025,12,15):
                if random.random() < 0.55:
                    sku = random.choice([s for s in sku_pool if s["brand"] == "Honey Bunches Oats"])

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
            "Retail_Chain":chain, "Store_Type":store_type, "Store_ID":store_id,
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
        stores.append({"id":f"{retailer[0][:3].upper()}{1000+i}",
                       "chain":retailer[0], "channel":retailer[1], "store_type":retailer[2],
                       "size":size, "dma":dma_id, "state":state, "city":city})

    start, end = date(2025, 1, 1), date(2026, 3, 31)
    days = (end - start).days
    rows = []
    for _ in range(n_rows):
        d = start + timedelta(days=random.randint(0, days))
        store = random.choice(stores)
        sku = random.choice(sku_pool)
        unit_price = round(sku["price"] * random.uniform(0.92, 1.05), 2)

        promo_flag, promo_type, promo_depth = "No", "None", 0
        if random.random() < 0.18:
            promo_flag, promo_type = "Yes", random.choice(["Price Off","Multi-Buy","Bundle","Loyalty"])
            promo_depth = random.choices([10,15,20,25,30], weights=[30,30,20,15,5])[0]
        if (sku["brand"] == "Honey Bunches Oats" and store["chain"] in ("Rouses","Brookshires")
                and store["dma"] == "LA-DMA" and d >= date(2025,10,1)):
            if random.random() < 0.65:
                promo_flag, promo_type, promo_depth = "Yes", "Price Off", 21

        base_facings = {"S":4, "M":6, "L":8}[store["size"]]
        facings = base_facings
        if (sku["id"] in ("CR002","CR004","CR005","CR006")
                and store["chain"] == "Walmart" and d >= date(2025,9,15)):
            facings = max(2, base_facings - 2)
        if sku["brand"] != "Crunchwell" and random.random() < 0.3:
            facings = max(1, base_facings - random.randint(0,3))

        osa = random.uniform(95.0, 99.9)
        if sku["id"] in ("CR002","CR004","CR005") and store["dma"] == "LA-DMA":
            if date(2025,11,8) <= d <= date(2025,12,15):
                osa = random.uniform(48.0, 78.0)
            elif d >= date(2025,9,15):
                osa = random.uniform(85.0, 96.0)

        opening = random.randint(0, 300)
        received = random.choices([0,12,24,36,48,72,144], weights=[60,5,8,8,7,7,5])[0]
        sales_units = max(0, min(opening + received, int(random.gauss(8 + facings*1.5, 4))))
        closing = max(0, opening + received - sales_units)

        rows.append({
            "Date":d.strftime("%Y-%m-%d"), "Store_ID":store["id"],
            "Country":"United States", "Country_Code":"USA",
            "State":store["state"], "DMA":store["dma"], "City":store["city"],
            "Cluster":store["channel"], "Banner":store["chain"], "Size_Tier":store["size"],
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
    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# 3. Syndicated Weekly (NielsenIQ-style)
# -----------------------------------------------------------------------------

def gen_syndicated_weekly():
    categories = ["RTE Cereal", "Hot Cereal", "Granola", "Plant-Based Milk", "Bar"]
    channels = ["Mass", "Grocery", "Club", "E-commerce", "Drug & Conv"]
    weeks = []
    d = date(2024,1,1)
    while d <= date(2026,5,4):
        wk = d.strftime("%G-W%V")
        if wk not in weeks: weeks.append(wk)
        d += timedelta(days=7)
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
                    acme_share = (crunch_share +
                                  (random.uniform(0.012,0.025) if cat=="RTE Cereal"
                                   else random.uniform(0.04,0.10)))
                    avg_p = round(random.uniform(3.50, 7.20), 2)
                    rows.append({
                        "Country":"United States", "DMA":dma[0], "Region":dma[2],
                        "Category":cat, "Channel":ch, "Week":wk,
                        "Value_USD_MM":round(base_value, 3),
                        "Volume_Units_K":round(base_value * 1000 / avg_p, 1),
                        "Acme_Value_Share":round(acme_share, 4),
                        "Crunchwell_Value_Share":round(crunch_share, 4),
                        "Post_Value_Share":round(random.uniform(0.10,0.18) if cat=="RTE Cereal" else random.uniform(0.0,0.05), 4),
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
    waves = ["2024Q1","2024Q2","2024Q3","2024Q4","2025Q1","2025Q2","2025Q3","2025Q4","2026Q1"]
    primary_cats = ["RTE Cereal","Hot Cereal","Granola","Plant-Based Milk","Bar","Snacks"]
    competitors = ["Cheerios","Honey Bunches Oats","Frosted Flakes","Quaker","Great Value PL","Magic Spoon","Kashi"]
    rows = []
    for i in range(1, n_rows+1):
        wave = random.choice(waves)
        yr, q = int(wave[:4]), int(wave[5])
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
            "aided_aw_proteinpeak":random.choices([0,1], weights=[55,45])[0],
            "aided_aw_morningoats":random.choices([0,1], weights=[35,65])[0],
            "aided_aw_trailgrove":random.choices([0,1], weights=[45,55])[0],
            "aided_aw_rootday":random.choices([0,1], weights=[58,42])[0],
            "aided_aw_cheerios":random.choices([0,1], weights=[8,92])[0],
            "aided_aw_honey_bunches":a_hboo,
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
    while d <= date(2026, 3, 31):
        weeks.append(d); d += timedelta(days=7)

    hh_records = hh_df.to_dict("records")
    rows = []
    for _ in range(n_rows):
        hh = random.choice(hh_records)
        wk = random.choice(weeks)
        retailer = random.choice(RETAILERS)
        sku = random.choice(pool)

        disc, promo = 0.0, "None"
        if random.random() < 0.18:
            disc = round(random.uniform(0.05, 0.3), 2)
            promo = random.choice(["Price Off","Multi-Buy","Bundle","Loyalty"])

        switching_flag = "No"
        if (hh["DMA"]=="LA-DMA" and hh["Brand_Loyalty_Segment"]=="Acme Loyal"
                and wk >= date(2025,11,1) and random.random() < 0.14):
            sku = next(s for s in pool if s["brand"]=="Honey Bunches Oats")
            switching_flag = "Yes"

        units = random.choices([1,2,3,4], weights=[55,28,12,5])[0]
        unit_price = round(sku["price"] * (1 - disc), 2)

        rows.append({
            "Household_ID":hh["Household_ID"], "Week_Start":wk.strftime("%Y-%m-%d"),
            "Country":"United States", "Country_Code":"USA",
            "State":hh["State"], "DMA":hh["DMA"], "City":hh["City"],
            "Urbanicity":hh["Urbanicity"], "Currency":"USD",
            "Retailer":retailer[0], "Retailer_Type":retailer[2], "Channel":retailer[1],
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
    print("[1/6] EPOS")
    epos = gen_epos(30000)
    print("[2/6] Perfect Store")
    perfect_store = gen_perfect_store(50000)
    print("[3/6] Syndicated weekly (NielsenIQ-style)")
    syndicated = gen_syndicated_weekly()
    print("[4/6] Brand Health")
    brand_health = gen_brand_health(15000)
    print("[5/6] Households")
    hh = gen_households(5000)
    print("[6/6] Household transactions")
    hh_tx = gen_hh_transactions(hh, 30000)

    tables = {
        "epos":                  epos,
        "perfect_store":         perfect_store,
        "syndicated_weekly":     syndicated,
        "brand_health":          brand_health,
        "households":            hh,
        "household_transactions":hh_tx,
    }
    print("Building parquet, samples, duckdb …")
    build_artifacts(tables)
    print("Done.")


if __name__ == "__main__":
    main()
