"""
Shared toolkit for the Acme report pack (reports 11-40).

Design goals: every headline number traces to acme.duckdb / seeds; consistent
CPG-document styling; charts rendered once to reports/charts/ and embedded.

Public API used by the per-report builders:
    con()                         -> read-only duckdb connection
    df(sql)                       -> pandas DataFrame
    Doc(...)                      -> document builder (see class docstring)
    palette                       -> dict of hex colors
    chart_* helpers               -> return a PNG path to embed via Doc.image()

Run any builder module with `python -m generators.<module>` from the repo root,
or `python generators/build_all.py` to (re)generate all 30 PDFs.
"""
from __future__ import annotations
import os, textwrap
import duckdb
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
matplotlib.rcParams["text.parse_math"] = False  # treat '$' literally in all chart text

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, KeepTogether, HRFlowable, ListFlowable, ListItem, NextPageTemplate,
)

# ---------------------------------------------------------------- paths -----
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(REPO, "acme.duckdb")
CHART_DIR = os.path.join(REPO, "reports", "charts")
OUT_DIR = os.path.join(REPO, "reports")
os.makedirs(CHART_DIR, exist_ok=True)

# --------------------------------------------------------------- palette ----
palette = {
    "navy":    "#1F2A44",   # primary / headers
    "ink":     "#2B2F38",   # body text
    "teal":    "#2E7D75",   # positive / accent 1
    "gold":    "#B98A2E",   # accent 2
    "rust":    "#B24A2E",   # negative / risk
    "sky":     "#3E6DA8",   # accent 3
    "slate":   "#5B6472",   # muted text
    "mist":    "#EAEEF2",   # light fill
    "mist2":   "#F5F7F9",   # zebra fill
    "line":    "#C9D2DB",   # rules
    "white":   "#FFFFFF",
    "green":   "#2E7D5B",
    "amber":   "#C08A1E",
}
def C(name): return colors.HexColor(palette[name])

_MPL = {"navy": "#1F2A44", "ink": "#2B2F38", "teal": "#2E7D75", "gold": "#B98A2E",
        "rust": "#B24A2E", "sky": "#3E6DA8", "slate": "#5B6472", "green": "#2E7D5B",
        "amber": "#C08A1E", "line": "#C9D2DB", "mist": "#EAEEF2"}
CYCLE = [_MPL[k] for k in ("navy", "teal", "gold", "sky", "rust", "slate", "green")]

# ----------------------------------------------------------------- data -----
_CON = None
def con():
    global _CON
    if _CON is None:
        _CON = duckdb.connect(DB_PATH, read_only=True)
    return _CON

def df(sql: str) -> pd.DataFrame:
    return con().execute(sql).fetchdf()

def seed_csv(name: str) -> pd.DataFrame:
    """Read a seed CSV directly (some seeds load oddly into duckdb)."""
    return pd.read_csv(os.path.join(REPO, "seeds", name))

def money(x, unit="M", dp=1):
    return f"${x:,.{dp}f}{unit}"

# ------------------------------------------------------------- pdf styles ---
def _styles():
    ss = getSampleStyleSheet()
    def add(name, **kw):
        ss.add(ParagraphStyle(name=name, **kw))
    add("Cover_Kicker", fontName="Helvetica-Bold", fontSize=10.5, textColor=C("teal"),
        leading=14, spaceAfter=6, tracking=1)
    add("Cover_Title", fontName="Helvetica-Bold", fontSize=27, textColor=C("navy"),
        leading=31, spaceAfter=10)
    add("Cover_Sub", fontName="Helvetica", fontSize=13, textColor=C("slate"),
        leading=18, spaceAfter=4)
    add("Cover_Meta", fontName="Helvetica", fontSize=9.5, textColor=C("slate"), leading=15)
    add("H1", fontName="Helvetica-Bold", fontSize=15.5, textColor=C("navy"),
        leading=19, spaceBefore=16, spaceAfter=7)
    add("H2", fontName="Helvetica-Bold", fontSize=11.5, textColor=C("navy"),
        leading=15, spaceBefore=11, spaceAfter=4)
    add("Body", fontName="Helvetica", fontSize=9.7, textColor=C("ink"),
        leading=14.2, spaceAfter=7, alignment=TA_LEFT)
    add("Body_S", fontName="Helvetica", fontSize=8.8, textColor=C("ink"), leading=12.8, spaceAfter=5)
    add("Blt", fontName="Helvetica", fontSize=9.6, textColor=C("ink"), leading=13.6)
    add("Lede", fontName="Helvetica-Oblique", fontSize=11, textColor=C("slate"),
        leading=16, spaceAfter=9)
    add("Caption", fontName="Helvetica-Oblique", fontSize=7.8, textColor=C("slate"),
        leading=10.5, spaceBefore=2, spaceAfter=8)
    add("Source", fontName="Helvetica-Oblique", fontSize=7.4, textColor=C("slate"), leading=10)
    add("TblHead", fontName="Helvetica-Bold", fontSize=8.4, textColor=C("white"), leading=11)
    add("TblCell", fontName="Helvetica", fontSize=8.4, textColor=C("ink"), leading=11)
    add("TblCellB", fontName="Helvetica-Bold", fontSize=8.4, textColor=C("navy"), leading=11)
    add("KpiVal", fontName="Helvetica-Bold", fontSize=17, textColor=C("navy"), leading=19)
    add("KpiLbl", fontName="Helvetica-Bold", fontSize=7.2, textColor=C("slate"), leading=9)
    add("KpiNote", fontName="Helvetica", fontSize=7.4, textColor=C("slate"), leading=9.5)
    add("CalloutTitle", fontName="Helvetica-Bold", fontSize=9.5, textColor=C("navy"), leading=12, spaceAfter=2)
    add("CalloutBody", fontName="Helvetica", fontSize=8.9, textColor=C("ink"), leading=12.5)
    add("Foot", fontName="Helvetica", fontSize=7, textColor=C("slate"), leading=9)
    return ss

STYLES = _styles()
def S(name): return STYLES[name]

def _p(text, style="Body"):
    return Paragraph(text, S(style))

# --------------------------------------------------------------- the Doc ----
class Doc:
    """
    Build one report. Typical use:

        d = Doc("11-...pdf", kicker="QUARTERLY BUSINESS REVIEW",
                title="Acme Corp Q1 2026 Company Business Review",
                subtitle="Enterprise performance, all brands and regions",
                owner="Diane Halverson, VP Sales NA", period="Q1 FY2026",
                short="Q1 2026 Company BR")
        d.cover_facts([("Net revenue", "$60.4M/mo"), ...])
        d.exec_summary("...", bullets=[...])
        d.h1("Section"); d.body("..."); d.image(chart_x(...), "caption")
        d.build()
    """
    PAGE_W, PAGE_H = letter
    MARGIN = 0.85 * inch

    def __init__(self, filename, title, kicker, subtitle, owner, period, short,
                 doc_type="Internal report", date_str="June 2026"):
        self.filename = filename
        self.path = os.path.join(OUT_DIR, filename)
        self.title = title
        self.kicker = kicker
        self.subtitle = subtitle
        self.owner = owner
        self.period = period
        self.short = short
        self.doc_type = doc_type
        self.date_str = date_str
        self.story = []
        self._cover()

    # ---- footer / header painter
    def _paint(self, canvas, doc):
        canvas.saveState()
        w, h = self.PAGE_W, self.PAGE_H
        if doc.page > 1:
            # top rule + running head
            canvas.setStrokeColor(C("line")); canvas.setLineWidth(0.5)
            canvas.line(self.MARGIN, h - 0.62 * inch, w - self.MARGIN, h - 0.62 * inch)
            canvas.setFont("Helvetica", 7); canvas.setFillColor(C("slate"))
            canvas.drawString(self.MARGIN, h - 0.55 * inch, "ACME CORP")
            canvas.drawRightString(w - self.MARGIN, h - 0.55 * inch, self.short)
        # footer
        canvas.setStrokeColor(C("line")); canvas.setLineWidth(0.5)
        canvas.line(self.MARGIN, 0.6 * inch, w - self.MARGIN, 0.6 * inch)
        canvas.setFont("Helvetica", 7); canvas.setFillColor(C("slate"))
        canvas.drawString(self.MARGIN, 0.43 * inch,
                          "Internal · Confidential — Acme Corp synthetic demo data. Fictional; not for real decision-making.")
        canvas.drawRightString(w - self.MARGIN, 0.43 * inch, f"{self.short}  ·  p. {doc.page}")
        canvas.restoreState()

    def _cover_paint(self, canvas, doc):
        w, h = self.PAGE_W, self.PAGE_H
        canvas.saveState()
        # left navy band
        canvas.setFillColor(C("navy"))
        canvas.rect(0, 0, 0.32 * inch, h, fill=1, stroke=0)
        canvas.setFillColor(C("teal"))
        canvas.rect(0.32 * inch, 0, 0.06 * inch, h, fill=1, stroke=0)
        # footer
        canvas.setStrokeColor(C("line")); canvas.setLineWidth(0.5)
        canvas.line(self.MARGIN, 0.6 * inch, w - self.MARGIN, 0.6 * inch)
        canvas.setFont("Helvetica", 7); canvas.setFillColor(C("slate"))
        canvas.drawString(self.MARGIN, 0.43 * inch,
                          "Internal · Confidential — Acme Corp synthetic demo data. Fictional; not for real decision-making.")
        canvas.drawRightString(w - self.MARGIN, 0.43 * inch, self.short)
        canvas.restoreState()

    def _cover(self):
        self.story += [Spacer(1, 1.4 * inch),
                       _p(self.kicker, "Cover_Kicker"),
                       _p(self.title, "Cover_Title"),
                       _p(self.subtitle, "Cover_Sub"),
                       Spacer(1, 0.28 * inch),
                       HRFlowable(width="100%", thickness=1, color=C("line"),
                                  spaceBefore=2, spaceAfter=12)]
        meta = (f"<b>Document type</b>&nbsp;&nbsp;{self.doc_type}<br/>"
                f"<b>Period</b>&nbsp;&nbsp;{self.period}<br/>"
                f"<b>Owner</b>&nbsp;&nbsp;{self.owner}<br/>"
                f"<b>Prepared</b>&nbsp;&nbsp;{self.date_str}")
        self.story.append(_p(meta, "Cover_Meta"))

    def cover_facts(self, pairs):
        """A compact 'at a glance' box on the cover. pairs: list of (label, value)."""
        self.story.append(Spacer(1, 0.30 * inch))
        rows = [[_p(l, "KpiLbl"), _p(f"<b>{v}</b>", "CalloutBody")] for l, v in pairs]
        t = Table(rows, colWidths=[2.2 * inch, 3.4 * inch])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), C("mist2")),
            ("LINEBELOW", (0, 0), (-1, -2), 0.4, C("line")),
            ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOX", (0, 0), (-1, -1), 0.6, C("line")),
        ]))
        self.story.append(t)
        self.story.append(PageBreak())

    # ---- headings / text
    def h1(self, text): self.story.append(_p(text, "H1")); self.story.append(
        HRFlowable(width="100%", thickness=0.8, color=C("teal"), spaceBefore=0, spaceAfter=7))
    def h2(self, text): self.story.append(_p(text, "H2"))
    def body(self, text): self.story.append(_p(text, "Body"))
    def lede(self, text): self.story.append(_p(text, "Lede"))
    def source(self, text): self.story.append(_p("Source: " + text, "Source"))
    def spacer(self, h=0.12): self.story.append(Spacer(1, h * inch))
    def pagebreak(self): self.story.append(PageBreak())
    def keep(self, flowables): self.story.append(KeepTogether(flowables))

    def bullets(self, items, style="Blt"):
        lf = ListFlowable(
            [ListItem(_p(it, style), leftIndent=6, value="–") for it in items],
            bulletType="bullet", bulletColor=C("teal"), bulletFontSize=8,
            leftIndent=14, spaceBefore=1, spaceAfter=7,
        )
        self.story.append(lf)

    def exec_summary(self, text, bullets=None):
        self.h1("Executive summary")
        self.lede(text)
        if bullets:
            self.bullets(bullets)

    # ---- KPI strip
    def kpis(self, cards):
        """cards: list of (label, value, note). Renders a horizontal strip."""
        cells = []
        for label, value, note in cards:
            inner = Table([[_p(label.upper(), "KpiLbl")],
                           [_p(str(value), "KpiVal")],
                           [_p(note, "KpiNote")]], colWidths=[(6.9 / len(cards)) * inch])
            inner.setStyle(TableStyle([
                ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]))
            cells.append(inner)
        t = Table([cells], colWidths=[(6.9 / len(cards)) * inch] * len(cards))
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), C("mist2")),
            ("LINEAFTER", (0, 0), (-2, -1), 0.5, C("line")),
            ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("BOX", (0, 0), (-1, -1), 0.6, C("line")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        self.story.append(t); self.spacer(0.06)

    # ---- generic table
    def table(self, headers, rows, widths=None, align=None, total_row=False,
              highlight_col=None, fontsize=8.4):
        """headers: list[str]; rows: list[list]; widths: fractions summing to ~1 or None."""
        avail = self.PAGE_W - 2 * self.MARGIN
        if widths is None:
            widths = [avail / len(headers)] * len(headers)
        else:
            widths = [w * avail for w in widths]
        head = [_p(h, "TblHead") for h in headers]
        body_rows = []
        for r in rows:
            body_rows.append([_p(str(c), "TblCell") for c in r])
        data = [head] + body_rows
        t = Table(data, colWidths=widths, repeatRows=1)
        st = [
            ("BACKGROUND", (0, 0), (-1, 0), C("navy")),
            ("TEXTCOLOR", (0, 0), (-1, 0), C("white")),
            ("FONTSIZE", (0, 0), (-1, -1), fontsize),
            ("TOPPADDING", (0, 0), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, C("line")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C("white"), C("mist2")]),
        ]
        aligns = align or (["LEFT"] + ["RIGHT"] * (len(headers) - 1))
        for i, a in enumerate(aligns):
            st.append(("ALIGN", (i, 0), (i, -1), a))
        if total_row:
            st += [("BACKGROUND", (0, -1), (-1, -1), C("mist")),
                   ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                   ("LINEABOVE", (0, -1), (-1, -1), 0.8, C("navy"))]
        if highlight_col is not None:
            st.append(("TEXTCOLOR", (highlight_col, 1), (highlight_col, -1), C("navy")))
            st.append(("FONTNAME", (highlight_col, 1), (highlight_col, -1), "Helvetica-Bold"))
        t.setStyle(TableStyle(st))
        self.story.append(t); self.spacer(0.05)

    # ---- callout box
    def callout(self, title, text, kind="info"):
        bar = {"info": "teal", "risk": "rust", "action": "gold", "win": "green"}.get(kind, "teal")
        inner = [_p(title, "CalloutTitle"), _p(text, "CalloutBody")]
        cell = Table([[inner]], colWidths=[self.PAGE_W - 2 * self.MARGIN - 0.12 * inch])
        cell.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), C("mist2")),
            ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LINEBEFORE", (0, 0), (0, -1), 3, C(bar)),
        ]))
        self.story.append(KeepTogether([cell, Spacer(1, 0.08 * inch)]))

    def recommendations(self, items):
        self.h2("Recommendations & next steps")
        rows = [[_p(f"<b>{i+1}</b>", "TblCellB"), _p(a, "TblCell"), _p(o, "TblCell"), _p(w, "TblCell")]
                for i, (a, o, w) in enumerate(items)]
        self.table_raw(["#", "Action", "Owner", "When"], rows, [0.06, 0.56, 0.22, 0.16])

    def table_raw(self, headers, prebuilt_rows, widths):
        avail = self.PAGE_W - 2 * self.MARGIN
        widths = [w * avail for w in widths]
        data = [[_p(h, "TblHead") for h in headers]] + prebuilt_rows
        t = Table(data, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), C("navy")),
            ("TOPPADDING", (0, 0), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, C("line")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C("white"), C("mist2")]),
        ]))
        self.story.append(t); self.spacer(0.05)

    # ---- image / chart
    def image(self, png_path, caption=None, width=6.9, ratio=None):
        img = Image(png_path)
        iw, ih = img.imageWidth, img.imageHeight
        w = width * inch
        h = w * ih / iw
        img.drawWidth, img.drawHeight = w, h
        block = [img]
        if caption:
            block.append(_p(caption, "Caption"))
        self.story.append(KeepTogether(block))

    def two_col(self, left_flow, right_flow, widths=(0.5, 0.5)):
        avail = self.PAGE_W - 2 * self.MARGIN
        t = Table([[left_flow, right_flow]],
                  colWidths=[widths[0] * avail, widths[1] * avail])
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("LEFTPADDING", (0, 0), (0, 0), 0),
                               ("RIGHTPADDING", (-1, 0), (-1, 0), 0),
                               ("LEFTPADDING", (-1, 0), (-1, 0), 8)]))
        self.story.append(t)

    # ---- build
    def build(self):
        doc = BaseDocTemplate(
            self.path, pagesize=letter,
            leftMargin=self.MARGIN, rightMargin=self.MARGIN,
            topMargin=self.MARGIN, bottomMargin=0.8 * inch,
            title=self.title, author="Acme Corp (synthetic)")
        frame = Frame(self.MARGIN, 0.8 * inch, self.PAGE_W - 2 * self.MARGIN,
                      self.PAGE_H - self.MARGIN - 0.8 * inch, id="body")
        cover_frame = Frame(self.MARGIN, 0.8 * inch, self.PAGE_W - 2 * self.MARGIN,
                            self.PAGE_H - self.MARGIN - 0.8 * inch, id="cover")
        doc.addPageTemplates([
            PageTemplate(id="cover", frames=[cover_frame], onPage=self._cover_paint),
            PageTemplate(id="body", frames=[frame], onPage=self._paint),
        ])
        # first flowable after cover triggers body template
        self.story.insert(0, NextPageTemplate("body"))
        doc.build(self.story)
        return self.path

# ============================================================== charts ======
def _fig(w=7.6, h=3.1):
    fig, ax = plt.subplots(figsize=(w, h), dpi=150)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(_MPL["line"])
    ax.tick_params(colors=_MPL["slate"], labelsize=8, length=0)
    ax.yaxis.grid(True, color=_MPL["line"], lw=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    return fig, ax

def _save(fig, name):
    path = os.path.join(CHART_DIR, name)
    fig.tight_layout(pad=0.6)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path

def chart_line(name, x, series, ylabel="", title="", pct=False, marker=True,
               annotate_last=True, w=7.6, h=3.0):
    """series: dict label->list(y). x: list of category labels."""
    fig, ax = _fig(w, h)
    for i, (lab, ys) in enumerate(series.items()):
        c = CYCLE[i % len(CYCLE)]
        ax.plot(range(len(x)), ys, color=c, lw=2.1, marker="o" if marker else None,
                ms=4.5, mfc=c, mec="white", mew=0.8, label=lab, zorder=3)
        if annotate_last and ys and ys[-1] is not None:
            ax.annotate(f"{ys[-1]:.1f}{'%' if pct else ''}", (len(x) - 1, ys[-1]),
                        textcoords="offset points", xytext=(6, 0), fontsize=7.5,
                        color=c, fontweight="bold", va="center")
    ax.set_xticks(range(len(x))); ax.set_xticklabels(x, fontsize=7.6)
    if pct: ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    if ylabel: ax.set_ylabel(ylabel, fontsize=8, color=_MPL["slate"])
    if title: ax.set_title(title, fontsize=9.5, color=_MPL["navy"], fontweight="bold", loc="left", pad=8)
    if len(series) > 1:
        ax.legend(frameon=False, fontsize=7.6, ncol=min(len(series), 4), loc="upper center",
                  bbox_to_anchor=(0.5, -0.16))
    return _save(fig, name)

def chart_bar(name, cats, vals, ylabel="", title="", pct=False, color="navy",
              value_labels=True, horizontal=False, colors_list=None, w=7.6, h=3.0, unit=""):
    fig, ax = _fig(w, h)
    cs = colors_list or [_MPL[color]] * len(cats)
    if horizontal:
        ax.barh(range(len(cats)), vals, color=cs, zorder=3, height=0.62)
        ax.set_yticks(range(len(cats))); ax.set_yticklabels(cats, fontsize=7.8)
        ax.invert_yaxis(); ax.xaxis.grid(True, color=_MPL["line"], lw=0.6); ax.yaxis.grid(False)
        if value_labels:
            for i, v in enumerate(vals):
                ax.annotate(f"{v:.1f}{'%' if pct else ''}{unit}", (v, i), textcoords="offset points",
                            xytext=(4, 0), va="center", fontsize=7.4, color=_MPL["ink"], fontweight="bold")
    else:
        ax.bar(range(len(cats)), vals, color=cs, zorder=3, width=0.62)
        ax.set_xticks(range(len(cats))); ax.set_xticklabels(cats, fontsize=7.6)
        if value_labels:
            for i, v in enumerate(vals):
                ax.annotate(f"{v:.1f}{'%' if pct else ''}{unit}", (i, v), textcoords="offset points",
                            xytext=(0, 3), ha="center", fontsize=7.4, color=_MPL["ink"], fontweight="bold")
        if pct: ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    if ylabel: ax.set_ylabel(ylabel, fontsize=8, color=_MPL["slate"])
    if title: ax.set_title(title, fontsize=9.5, color=_MPL["navy"], fontweight="bold", loc="left", pad=8)
    return _save(fig, name)

def chart_grouped(name, cats, series, ylabel="", title="", pct=False, w=7.6, h=3.1, unit=""):
    """series: dict label->list aligned to cats."""
    fig, ax = _fig(w, h)
    n = len(series); width = 0.8 / n
    for i, (lab, ys) in enumerate(series.items()):
        xs = [j + (i - (n - 1) / 2) * width for j in range(len(cats))]
        ax.bar(xs, ys, width=width, color=CYCLE[i % len(CYCLE)], label=lab, zorder=3)
    ax.set_xticks(range(len(cats))); ax.set_xticklabels(cats, fontsize=7.6)
    if pct: ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    if ylabel: ax.set_ylabel(ylabel, fontsize=8, color=_MPL["slate"])
    if title: ax.set_title(title, fontsize=9.5, color=_MPL["navy"], fontweight="bold", loc="left", pad=8)
    ax.legend(frameon=False, fontsize=7.6, ncol=min(n, 4), loc="upper center", bbox_to_anchor=(0.5, -0.16))
    return _save(fig, name)

def chart_stacked(name, cats, series, ylabel="", title="", pct=False, w=7.6, h=3.1):
    fig, ax = _fig(w, h)
    bottom = [0] * len(cats)
    for i, (lab, ys) in enumerate(series.items()):
        ax.bar(range(len(cats)), ys, bottom=bottom, color=CYCLE[i % len(CYCLE)],
               label=lab, zorder=3, width=0.6)
        bottom = [b + y for b, y in zip(bottom, ys)]
    ax.set_xticks(range(len(cats))); ax.set_xticklabels(cats, fontsize=7.6)
    if pct: ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    if ylabel: ax.set_ylabel(ylabel, fontsize=8, color=_MPL["slate"])
    if title: ax.set_title(title, fontsize=9.5, color=_MPL["navy"], fontweight="bold", loc="left", pad=8)
    ax.legend(frameon=False, fontsize=7.6, ncol=min(len(series), 4), loc="upper center", bbox_to_anchor=(0.5, -0.16))
    return _save(fig, name)

def chart_waterfall(name, labels, values, title="", ylabel="", w=7.6, h=3.2, unit=""):
    """values: signed contributions; first bar is start (absolute), last is end (absolute) if flagged.
    Simple version: all are deltas plotted cumulatively with a running total line."""
    fig, ax = _fig(w, h)
    cum = 0; xs = range(len(labels))
    for i, v in enumerate(values):
        start = cum
        c = _MPL["teal"] if v >= 0 else _MPL["rust"]
        ax.bar(i, v, bottom=start, color=c, zorder=3, width=0.62)
        ax.annotate(f"{v:+.1f}{unit}", (i, start + v + (0.4 if v >= 0 else -0.4)),
                    ha="center", va="bottom" if v >= 0 else "top", fontsize=7.2,
                    color=_MPL["ink"], fontweight="bold")
        cum += v
    ax.set_xticks(list(xs)); ax.set_xticklabels(labels, fontsize=7.4)
    ax.axhline(0, color=_MPL["slate"], lw=0.8)
    if ylabel: ax.set_ylabel(ylabel, fontsize=8, color=_MPL["slate"])
    if title: ax.set_title(title, fontsize=9.5, color=_MPL["navy"], fontweight="bold", loc="left", pad=8)
    return _save(fig, name)

def chart_donut(name, labels, values, title="", w=4.4, h=3.1):
    fig, ax = plt.subplots(figsize=(w, h), dpi=150)
    cs = [CYCLE[i % len(CYCLE)] for i in range(len(labels))]
    wedges, _ = ax.pie(values, colors=cs, startangle=90, counterclock=False,
                       wedgeprops=dict(width=0.42, edgecolor="white", linewidth=1.5))
    total = sum(values)
    ax.legend(wedges, [f"{l} · {v/total*100:.0f}%" for l, v in zip(labels, values)],
              frameon=False, fontsize=7.6, loc="center left", bbox_to_anchor=(0.98, 0.5))
    if title: ax.set_title(title, fontsize=9.5, color=_MPL["navy"], fontweight="bold", loc="left", pad=6)
    ax.set(aspect="equal")
    return _save(fig, name)
