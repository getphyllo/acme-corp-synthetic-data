# Report authoring contract (lib.py API + house style)

You are writing one Python module of report builders on top of the **frozen**
`reports/generators/lib.py`. Do not edit `lib.py`. Match the look, tone, and
grounding of the reference report in `reports/generators/corporate.py`
(function `r11_company_q1_qbr`) — read it before you start.

## How to run / verify (REQUIRED)
From the repo root, generate + self-check with the project venv:
```
.venv/bin/python reports/generators/<your_module>.py
```
Your module's `__main__` must call every builder and print each returned path.
Iterate until it runs clean and every PDF is produced. Each builder must
produce a **4–8 page** PDF. Do a final render and confirm page counts with:
```
.venv/bin/python -c "import fitz;print([ (f, fitz.open('reports/'+f).page_count) for f in __import__('os').listdir('reports') if f.endswith('.pdf')])"
```

## Import (exact)
```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import (Doc, df, seed_csv, money, palette,
                 chart_line, chart_bar, chart_grouped, chart_stacked,
                 chart_waterfall, chart_donut)
```

## Data helpers
- `df(sql)` → pandas DataFrame from `acme.duckdb` (read-only). Table + column names are in FACTS.md / the schema. Week col format `YYYY-Www`; quarter = `CEIL(CAST(SUBSTR(Week,7,2) AS INT)/13.0)`. Period col (plan_vs_actual) = `YYYY-MM`.
- `seed_csv("name.csv")` → DataFrame straight from `seeds/` (use for innovation_pipeline.csv and any seed that reads oddly from duckdb).
- `money(x)` → "$12.3M". Prefer live queries for table/chart values; you MAY hardcode a headline number if it's in FACTS.md.
- **Never invent measured history.** Forward/plan numbers (FY27+ targets, next-2-quarter forecasts, spend reallocations) are fine but must be worded as *target / plan / planning estimate* in the doc.

## Doc API
```python
d = Doc(filename, title, kicker, subtitle, owner, period, short,
        doc_type="...", date_str="...")   # all keyword-friendly; short = running header/footer tag (<24 chars)
d.cover_facts([(label, value), ...])       # 4–6 rows; ends the cover, starts page 2. Call once, early.
d.exec_summary(lede_text, bullets=[...])   # h1 "Executive summary" + italic lede + bullets
d.h1("1 · Section")                        # numbered section headers, teal rule under
d.h2("1.1 · Subsection")
d.body("paragraph ...")                    # inline HTML ok: <b>..</b>, <i>..</i>, &minus; use −, &, etc.
d.lede("emphasis paragraph")
d.bullets(["item", ...])
d.kpis([(label, value, note), ...])        # 3–5 cards, horizontal strip. Keep labels short.
d.table(headers, rows, widths=[frac,...], align=None, total_row=False, highlight_col=None)
      # widths are fractions of text width, sum ≈ 1.0. rows = list of lists (stringify numbers yourself).
      # align defaults to first col left, rest right. total_row bolds/shades last row.
d.table_raw(headers, prebuilt_rows, widths)   # rows are lists of Paragraph flowables (rare; recommendations uses it)
d.callout(title, text, kind)               # kind ∈ {"info","risk","action","win"} → colored left bar
d.recommendations([(action, owner, when), ...])   # standard closing table
d.image(png_path, caption=None, width=6.9) # embed a chart PNG (charts auto-fit width)
d.source("table1, table2 ...")             # small italic provenance line under a table/chart
d.two_col(left_flow, right_flow, widths=(.5,.5))  # side-by-side flowables (advanced; optional)
d.spacer(0.1); d.pagebreak()
path = d.build()                           # writes reports/<filename>, returns path
```

## Charts (return a PNG path → pass to d.image)
Give every chart a **unique** filename prefixed by report number, e.g. `"r18_share.png"`.
```python
chart_line(name, x_labels, {series_label: [y,...], ...}, title="", pct=False, ylabel="", h=3.0)
chart_bar(name, cats, vals, title="", pct=False, color="navy", horizontal=False,
          colors_list=[...], value_labels=True, unit="", h=3.0)   # color name from palette
chart_grouped(name, cats, {label:[vals]}, title="", pct=False, unit="")
chart_stacked(name, cats, {label:[vals]}, title="", pct=False)
chart_waterfall(name, labels, signed_values, title="", ylabel="", unit="")   # cumulative bars
chart_donut(name, labels, values, title="")
```
Palette names for `color`/`colors_list`: navy, teal, gold, rust, sky, slate, green, amber.
Use **2–4 charts per report**. Prefer real query output over made-up series.

## House style
- Tone: senior CPG operator writing to leadership. Crisp, decision-oriented, numbers-first. No fluff, no hype.
- Every report: cover → cover_facts → exec_summary → 3–6 numbered sections → close with `d.callout(...risk...)` and `d.recommendations([...])`.
- Lead sections with the number, then the "so what". Use `d.kpis(...)` once near the top.
- Confidentiality footer is automatic. Don't restate it in body.
- Reuse the real personas (FACTS.md) as owners. Cross-reference sibling reports by number where natural (e.g. "see the CFO read, Report 40").
- Use real dates: today ≈ early July 2026. FY = calendar-ish; Q1 FY26 = Jan–Mar 2026.
- Encode `−` as the literal minus char or `&minus;`. Avoid characters that break XML: escape `&` as `&amp;` inside Paragraph text if literal.

## Filenames (use EXACTLY these)
Your assignment message lists the report numbers, titles, and target filenames. Use them verbatim.
