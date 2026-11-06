"""
06_generate_presentation.py
Generates a master-level, 19-slide widescreen PowerPoint presentation (.pptx)
for Group 4: "From bailout to backstop: what drives Portugal’s 10-year sovereign spread over Germany, 1999-2026?"
"""

import os
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE_DIR, 'figures')
TAB_DIR = os.path.join(BASE_DIR, 'tables')
PPTX_PATH = os.path.join(BASE_DIR, 'Portuguese_Sovereign_Spread_1999_2026.pptx')

# Initialize 16:9 widescreen presentation
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Colors
C_NAVY = RGBColor(0, 43, 91)       # #002B5B primary dark
C_BLUE = RGBColor(26, 95, 122)     # #1A5F7A secondary
C_ACCENT = RGBColor(217, 83, 79)   # #D9534F coral/red
C_BG_LIGHT = RGBColor(245, 247, 250) # #F5F7FA
C_CARD_BG = RGBColor(255, 255, 255)
C_TEXT_DARK = RGBColor(33, 37, 41)
C_TEXT_MUTED = RGBColor(108, 117, 125)
C_WHITE = RGBColor(255, 255, 255)
C_GREEN = RGBColor(40, 167, 69)

def add_header(slide, title_text, category_text="DATA ANALYSIS IN FINANCE | MASTER IN FINANCE"):
    # Header bar container
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_NAVY
    top_bar.line.fill.background()
    
    # Text box
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.text = category_text.upper()
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(180, 205, 237)
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

def add_card(slide, left, top, width, height, title=None, bg_color=C_CARD_BG, border_color=RGBColor(220, 225, 230)):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
        
    if title:
        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.4))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
    return shape

# ==============================================================================
# SLIDE 1: Title Slide
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = C_NAVY
bg1.line.fill.background()

# Title text box
tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(4.5))
tf1 = tb1.text_frame
tf1.word_wrap = True

p_inst = tf1.paragraphs[0]
p_inst.text = "ISEG – LISBON SCHOOL OF ECONOMICS & MANAGEMENT | DATA ANALYSIS IN FINANCE"
p_inst.font.size = Pt(13)
p_inst.font.bold = True
p_inst.font.color.rgb = RGBColor(180, 215, 255)
p_inst.space_after = Pt(24)

p_title = tf1.add_paragraph()
p_title.text = "From Bailout to Backstop:"
p_title.font.size = Pt(36)
p_title.font.bold = True
p_title.font.color.rgb = C_WHITE

p_sub = tf1.add_paragraph()
p_sub.text = "What Drives Portugal’s 10-Year Sovereign Spread over Germany, 1999–2026?"
p_sub.font.size = Pt(26)
p_sub.font.bold = True
p_sub.font.color.rgb = RGBColor(240, 180, 100)
p_sub.space_after = Pt(36)

p_grp = tf1.add_paragraph()
p_grp.text = "Group 4 Presentation"
p_grp.font.size = Pt(14)
p_grp.font.bold = True
p_grp.font.color.rgb = C_WHITE

p_names = tf1.add_paragraph()
p_names.text = "Karl Grywenz (L67517) • Daniel Seratila (66886) • Jort Petersen (67605)\nDanylo Karpenko (l67795) • Elias Wetterberg (l67031) • Sipan Zeyrek (67789)"
p_names.font.size = Pt(12)
p_names.font.color.rgb = RGBColor(210, 225, 245)
p_names.space_after = Pt(18)

p_date = tf1.add_paragraph()
p_date.text = "Discussion Group: Group 6 | Presentation Date: December 18, 2026"
p_date.font.size = Pt(11)
p_date.font.italic = True
p_date.font.color.rgb = RGBColor(170, 190, 215)


# ==============================================================================
# SLIDE 2: Research Motivation & Questions
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "Executive Summary & Core Research Questions")

# Card 1: Context & Problem
add_card(s2, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5), "Research Context & Relevance")
tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.7))
tf = tb.text_frame
tf.word_wrap = True

points_s2_left = [
    ("27-Year Sovereign Journey: ", "From EMU launch (1999) through the Great Financial Crisis and 2011 Troika bailout to the modern ECB anti-fragmentation backstop (TPI)."),
    ("Extreme Regime Shifts: ", "Portuguese 10-year yield spread over Germany expanded from under 20 bps in 2000 to a devastating peak of 1,203 bps in Jan 2012, before normalizing to under 40 bps by 2026."),
    ("The Sovereign-Bank Nexus: ", "During the crisis, sovereign risk threatened Portuguese banking solvency, public finances, and Eurozone membership."),
    ("The Modern Decoupling: ", "Today, Portugal has consolidated public debt (137% → 92% of GDP) and trades inside Italy and tight to Spain, challenging the traditional GIIPS periphery narrative.")
]
for title, desc in points_s2_left:
    p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
    p.space_after = Pt(14)
    run_t = p.add_run()
    run_t.text = title
    run_t.font.bold = True
    run_t.font.size = Pt(12)
    run_t.font.color.rgb = C_NAVY
    run_d = p.add_run()
    run_d.text = desc
    run_d.font.size = Pt(12)
    run_d.font.color.rgb = C_TEXT_DARK

# Card 2: Research Questions & Contributions
add_card(s2, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5), "Core Research Hypotheses & Methodology")
tb = s2.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
tf = tb.text_frame
tf.word_wrap = True

points_s2_right = [
    ("Q1: Macro Drivers: ", "Which global (VIX), monetary (ECB DFR), and domestic fiscal/macro factors (Debt/GDP, HICP inflation, unemployment) drive month-to-month changes in Portuguese sovereign spreads?"),
    ("Q2: Structural Break & Policy Backstops: ", "Did Mario Draghi's July 2012 'Whatever it takes' speech and subsequent ECB programs (OMT, PSPP, PEPP, TPI) sever the feedback loop between domestic debt and sovereign spreads?"),
    ("Q3: Time-Series Predictability: ", "Can an identified ARIMA model exploit autocorrelation to outperform a naive Random Walk benchmark in out-of-sample forecast accuracy?"),
    ("Q4: Peripheral Cross-Country Divergence: ", "How did Portugal's spread dynamics evolve relative to other GIIPS economies (Spain, Italy, Greece, Ireland)?")
]
for title, desc in points_s2_right:
    p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
    p.space_after = Pt(14)
    run_t = p.add_run()
    run_t.text = title
    run_t.font.bold = True
    run_t.font.size = Pt(12)
    run_t.font.color.rgb = C_BLUE
    run_d = p.add_run()
    run_d.text = desc
    run_d.font.size = Pt(12)
    run_d.font.color.rgb = C_TEXT_DARK


# ==============================================================================
# SLIDE 3: Four Institutional Policy Regimes
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "Institutional Framework: Four Distinct Historical Regimes (1999–2026)")

regime_cards = [
    ("1. EMU Convergence\n(1999-01 to 2007-12)",
     "• Euro adoption eliminates currency risk\n• Markets treat periphery debt as virtually risk-free\n• PT spread averages 20.7 bps (min -0.4 bps)\n• Massive underpricing of sovereign credit risk",
     RGBColor(230, 243, 250), C_BLUE),
    ("2. GFC & Troika Bailout\n(2008-01 to 2012-06)",
     "• Lehman collapse triggers sudden stop in capital flows\n• Periphery debt crisis explodes; ratings downgraded\n• May 2011: €78bn EU/IMF/ECB Troika bailout\n• Peak spread: 1,203 bps (Jan 2012); mean 381 bps",
     RGBColor(253, 237, 236), C_ACCENT),
    ("3. Draghi OMT & QE\n(2012-07 to 2019-12)",
     "• July 2012: Draghi 'Whatever it takes' speech\n• Outright Monetary Transactions (OMT) backstop\n• 2015: Public Sector Purchase Programme (PSPP/QE)\n• Yields collapse; spread drops from 925 to 65 bps",
     RGBColor(235, 247, 238), C_GREEN),
    ("4. Pandemic & TPI Backstop\n(2020-01 to 2026-09)",
     "• PEPP cushions COVID-19 pandemic shock\n• 2022-24 inflation surge triggers 450 bps ECB rate hikes\n• Transmission Protection Instrument (TPI) backstop\n• PT spreads stabilize ~71 bps; drops to 37 bps in 2026",
     RGBColor(255, 248, 230), RGBColor(190, 130, 20))
]

card_w = Inches(2.7)
card_h = Inches(5.4)
for i, (title, text, bg, accent) in enumerate(regime_cards):
    left = Inches(0.8 + i * 2.95)
    top = Inches(1.4)
    shape = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, card_w, card_h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg
    shape.line.color.rgb = accent
    shape.line.width = Pt(1.5)
    
    tb = s3.shapes.add_textbox(left + Inches(0.15), top + Inches(0.2), card_w - Inches(0.3), card_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.bold = True
    p0.font.size = Pt(13)
    p0.font.color.rgb = accent
    p0.space_after = Pt(18)
    
    for line in text.split('\n'):
        p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEXT_DARK
        p.space_after = Pt(8)


# ==============================================================================
# SLIDE 4: Data Sources & Variables
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "Data Sources & Variables Specification (1999–2026)")

# Add table of variables
table_shape = s4.shapes.add_table(8, 5, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.4))
tbl = table_shape.table
tbl.columns[0].width = Inches(2.4)
tbl.columns[1].width = Inches(2.2)
tbl.columns[2].width = Inches(1.8)
tbl.columns[3].width = Inches(1.5)
tbl.columns[4].width = Inches(3.8)

headers = ["Variable Name", "Economic Concept", "Source", "Frequency", "Transformation & Role"]
for j, h in enumerate(headers):
    cell = tbl.cell(0, j)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = C_WHITE

var_rows = [
    ("Spread_PT_bps", "PT-DE 10Y Yield Spread", "ECB Data Portal", "Monthly", "Dependent Variable (bps). Y_PT - Y_DE"),
    ("Yield_10Y_DE", "German 10Y Bund Yield", "ECB Data Portal", "Monthly", "Risk-free Eurozone benchmark rate (%)"),
    ("VIX", "CBOE Volatility Index", "Yahoo Finance / FRED", "Monthly Mean", "Global financial market risk aversion / fear index"),
    ("ECB_DFR", "ECB Deposit Facility Rate", "ECB Data Portal", "Monthly Resampled", "Monetary policy stance & policy rate expectations (%)"),
    ("HICP_Inflation_PT", "HICP Headline Inflation", "Eurostat (prc_hicp_manr)", "Monthly", "Domestic price pressures (% YoY annual change)"),
    ("Unemp_Rate_PT", "Harmonized Unemployment", "Eurostat (une_rt_m)", "Monthly SA", "Domestic economic slack (% of labor force)"),
    ("Debt_to_GDP_PT", "Maastricht Gross Debt", "Eurostat (gov_10q_ggdebt)", "Quarterly → Monthly", "Fiscal solvency proxy (% of GDP, interpolated)")
]

for i, row in enumerate(var_rows):
    bg_row = RGBColor(245, 248, 252) if i % 2 == 1 else RGBColor(255, 255, 255)
    for j, val in enumerate(row):
        cell = tbl.cell(i + 1, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_row
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_DARK
        if j == 0:
            p.font.bold = True


# ==============================================================================
# SLIDE 5: Historical Evolution Plot
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "Historical Trajectory: Portugal vs Germany 10-Year Yields & Sovereign Spread")

# Add image
fig1_path = os.path.join(FIG_DIR, 'fig01_yields_and_spread_regimes.png')
if os.path.exists(fig1_path):
    s5.shapes.add_picture(fig1_path, Inches(0.8), Inches(1.35), Inches(8.8), Inches(5.6))

# Right side insight card
add_card(s5, Inches(9.8), Inches(1.35), Inches(2.7), Inches(5.6), "Key Takeaways", bg_color=RGBColor(245, 247, 250))
tb = s5.shapes.add_textbox(Inches(9.95), Inches(1.9), Inches(2.4), Inches(4.9))
tf = tb.text_frame
tf.word_wrap = True

takeaways_s5 = [
    ("Illusion of Zero Risk:", "1999–2007: Spreads compressed to ~20 bps. Markets ignored sovereign default risk."),
    ("Crisis Re-pricing:", "2010–2012: Troika bailout (€78bn) and debt crisis drove yields to 13.8% and spread to 1,203 bps."),
    ("The Draghi Watershed:", "July 2012 speech reversed the spiral overnight without spending a single euro."),
    ("Modern Stability:", "2024–2026: Spread trading below 40 bps despite 450 bps of ECB rate hikes.")
]
for title, text in takeaways_s5:
    p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
    p.space_after = Pt(12)
    r1 = p.add_run()
    r1.text = title + " "
    r1.font.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = C_NAVY
    r2 = p.add_run()
    r2.text = text
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = C_TEXT_DARK


# ==============================================================================
# SLIDE 6: Descriptive Statistics Full Sample
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "Summary Statistics & Distributional Properties (Full Sample, N = 333)")

table_s6 = s6.shapes.add_table(9, 8, Inches(0.8), Inches(1.4), Inches(11.7), Inches(4.3))
tbl6 = table_s6.table
for j, w in enumerate([Inches(2.5), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.6), Inches(1.6)]):
    tbl6.columns[j].width = w

headers_s6 = ["Variable", "Mean", "Std Dev", "Median", "Min", "Max", "Skewness", "Kurtosis"]
for j, h in enumerate(headers_s6):
    cell = tbl6.cell(0, j)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_WHITE

stats_csv = pd.read_csv(os.path.join(TAB_DIR, 'table01_summary_statistics_full.csv'))
for i, row in stats_csv.iterrows():
    bg_row = RGBColor(245, 248, 252) if i % 2 == 1 else RGBColor(255, 255, 255)
    vals = [
        row['Variable'],
        f"{row['Mean']:.2f}",
        f"{row['Std']:.2f}",
        f"{row['Median']:.2f}",
        f"{row['Min']:.2f}",
        f"{row['Max']:.2f}",
        f"{row['Skewness']:.2f}",
        f"{row['Kurtosis']:.2f}"
    ]
    for j, val in enumerate(vals):
        cell = tbl6.cell(i + 1, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_row
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(10)
        p.font.color.rgb = C_TEXT_DARK
        if j == 0:
            p.font.bold = True

# Bottom takeaway card
add_card(s6, Inches(0.8), Inches(5.9), Inches(11.7), Inches(1.15), bg_color=RGBColor(240, 245, 252))
tb_bot = s6.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.3), Inches(1.0))
tf_bot = tb_bot.text_frame
tf_bot.word_wrap = True
p = tf_bot.paragraphs[0]
p.text = "Key Distributional Takeaways:"
p.font.bold = True
p.font.size = Pt(11)
p.font.color.rgb = C_NAVY

p2 = tf_bot.add_paragraph()
p2.text = "• Severe Right Skewness & Excess Kurtosis: The sovereign spread exhibits skewness of 2.71 and kurtosis of 10.42 (Jarque-Bera p < 0.001), reflecting crisis tail events.\n• Economic Dispersion: Debt-to-GDP ranged between 54.0% and 137.5%, while unemployment spanned 5.0% to 18.4%, providing massive empirical variation."
p2.font.size = Pt(10.5)
p2.font.color.rgb = C_TEXT_DARK


# ==============================================================================
# SLIDE 7: Spread Distribution Across Policy Regimes
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "Regime Comparison: Structural Discontinuities in Sovereign Spreads")

fig3_path = os.path.join(FIG_DIR, 'fig03_regime_boxplots.png')
if os.path.exists(fig3_path):
    s7.shapes.add_picture(fig3_path, Inches(0.8), Inches(1.35), Inches(7.5), Inches(5.6))

# Right table and insight card
add_card(s7, Inches(8.5), Inches(1.35), Inches(4.0), Inches(5.6), "Spread Statistics by Regime (bps)")
tb_r = s7.shapes.add_textbox(Inches(8.7), Inches(1.9), Inches(3.6), Inches(4.9))
tf_r = tb_r.text_frame
tf_r.word_wrap = True

regime_insights = [
    ("1. EMU Convergence (1999–07)", "Mean: 20.7 bps | Std: 10.7 bps\nRange: -0.4 to 43.5 bps\nMarkets completely underpriced default risk."),
    ("2. Crisis & Bailout (2008–12)", "Mean: 381.0 bps | Std: 385.8 bps\nRange: 27.9 to 1,202.9 bps\nExplosion in risk premia and redenomination fears."),
    ("3. Post-Draghi QE (2012–19)", "Mean: 283.0 bps | Std: 172.5 bps\nRange: 65.7 to 925.2 bps\nGradual healing backed by ECB bond buying."),
    ("4. Pandemic & TPI (2020–26)", "Mean: 71.5 bps | Std: 24.7 bps\nRange: 33.3 to 141.8 bps (Current: 37 bps)\nAnti-fragmentation backstop prevents divergence.")
]
for title, body in regime_insights:
    p = tf_r.add_paragraph() if tf_r.paragraphs[0].text else tf_r.paragraphs[0]
    p.space_after = Pt(10)
    r1 = p.add_run()
    r1.text = title + "\n"
    r1.font.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = C_NAVY
    r2 = p.add_run()
    r2.text = body
    r2.font.size = Pt(10)
    r2.font.color.rgb = C_TEXT_DARK


# ==============================================================================
# SLIDE 8: Spread vs Macroeconomic & Monetary Drivers
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "Exploratory Analysis: Sovereign Spread vs Macroeconomic Drivers")

fig2_path = os.path.join(FIG_DIR, 'fig02_spread_vs_macro_drivers.png')
if os.path.exists(fig2_path):
    s8.shapes.add_picture(fig2_path, Inches(0.8), Inches(1.35), Inches(9.0), Inches(5.6))

add_card(s8, Inches(10.0), Inches(1.35), Inches(2.5), Inches(5.6), "Core Dynamics", bg_color=RGBColor(245, 247, 250))
tb_s8 = s8.shapes.add_textbox(Inches(10.15), Inches(1.9), Inches(2.2), Inches(4.9))
tf_s8 = tb_s8.text_frame
tf_s8.word_wrap = True

driver_points = [
    ("Global Risk (VIX):", "Spikes during crisis episodes (Lehman, Euro debt peak, COVID)."),
    ("ECB Policy Rate:", "Rate cuts during crisis failed to lower periphery spreads until QE arrived."),
    ("Debt-to-GDP:", "Strong co-movement during 2010–2014, but decouples after 2015."),
    ("Macro Slack:", "Unemployment peaked at 18.4% in 2013, reinforcing fiscal strain.")
]
for t, d in driver_points:
    p = tf_s8.add_paragraph() if tf_s8.paragraphs[0].text else tf_s8.paragraphs[0]
    p.space_after = Pt(12)
    r1 = p.add_run()
    r1.text = t + " "
    r1.font.bold = True
    r1.font.size = Pt(10.5)
    r1.font.color.rgb = C_NAVY
    r2 = p.add_run()
    r2.text = d
    r2.font.size = Pt(10)
    r2.font.color.rgb = C_TEXT_DARK


# ==============================================================================
# SLIDE 9: Stationarity Check (ADF & KPSS Unit Root Tests)
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "Stationarity Check: Augmented Dickey-Fuller (ADF) & KPSS Tests")

table_s9 = s9.shapes.add_table(7, 7, Inches(0.8), Inches(1.4), Inches(11.7), Inches(3.6))
tbl9 = table_s9.table
for j, w in enumerate([Inches(2.5), Inches(1.5), Inches(1.5), Inches(1.2), Inches(1.5), Inches(1.5), Inches(2.0)]):
    tbl9.columns[j].width = w

headers_s9 = ["Variable", "ADF Stat (Levels)", "ADF p-val (Levels)", "Order", "ADF Stat (Δ Diff)", "ADF p-val (Δ Diff)", "Final Integration"]
for j, h in enumerate(headers_s9):
    cell = tbl9.cell(0, j)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_WHITE

ur_csv = pd.read_csv(os.path.join(TAB_DIR, 'table06_unit_root_tests.csv'))
for i, row in ur_csv.iterrows():
    bg_row = RGBColor(245, 248, 252) if i % 2 == 1 else RGBColor(255, 255, 255)
    vals = [
        row['Variable'],
        f"{row['ADF_Stat_Level']:.2f}",
        f"{row['ADF_pVal_Level']:.3f}",
        row['Order_Level'],
        f"{row['ADF_Stat_Diff']:.2f}",
        f"{row['ADF_pVal_Diff']:.4f}",
        f"{row['Variable']} ~ I(1) → Δ ~ I(0)"
    ]
    for j, val in enumerate(vals):
        cell = tbl9.cell(i + 1, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_row
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(10)
        p.font.color.rgb = C_TEXT_DARK
        if j in [0, 3, 6]:
            p.font.bold = True

add_card(s9, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.8), "Econometric Justification: Why First Differences?", bg_color=RGBColor(253, 237, 236), border_color=C_ACCENT)
tb_ur = s9.shapes.add_textbox(Inches(1.0), Inches(5.75), Inches(11.3), Inches(1.2))
tf_ur = tb_ur.text_frame
tf_ur.word_wrap = True
p = tf_ur.paragraphs[0]
p.text = "• Spurious Regression Risk (Granger & Newbold, 1974): In levels, all series fail to reject the unit root null (ADF p > 0.05). Running OLS in levels creates spurious statistical significance, inflated R², and severe autocorrelation.\n• Differencing Solution: First differences are stationary at p < 0.001 across all variables (ADF test rejects null). Hence, all subsequent econometric regressions are strictly estimated in first differences (Δ)."
p.font.size = Pt(11)
p.font.color.rgb = C_TEXT_DARK


# ==============================================================================
# SLIDE 10: Econometric Model Specification & Comparison
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "Econometric Modeling: Multiple Regression Framework")

# Card Left: Formulas
add_card(s10, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5), "Econometric Specifications")
tb_eq = s10.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.7))
tf_eq = tb_eq.text_frame
tf_eq.word_wrap = True

p = tf_eq.paragraphs[0]
p.text = "Model 1: Spurious Baseline in Levels"
p.font.bold = True
p.font.size = Pt(12)
p.font.color.rgb = C_NAVY

p = tf_eq.add_paragraph()
p.text = "Spread_t = β₀ + β₁ VIX_t + β₂ ECB_t + β₃ Infl_t + β₄ Unemp_t + β₅ Debt_t + ε_t\nProduces R² = 0.645, but DW = 0.14 → completely invalid due to unit roots."
p.font.size = Pt(10.5)
p.space_after = Pt(14)

p = tf_eq.add_paragraph()
p.text = "Model 2: Main Specification in First Differences"
p.font.bold = True
p.font.size = Pt(12)
p.font.color.rgb = C_NAVY

p = tf_eq.add_paragraph()
p.text = "ΔSpread_t = γ₀ + γ₁ ΔVIX_t + γ₂ ΔECB_t + γ₃ ΔInfl_t + γ₄ ΔUnemp_t + γ₅ ΔDebt_t + u_t\nAll series stationary I(0). Eliminates spurious trend."
p.font.size = Pt(10.5)
p.space_after = Pt(14)

p = tf_eq.add_paragraph()
p.text = "Model 3: Robust Inference (Newey-West HAC)"
p.font.bold = True
p.font.size = Pt(12)
p.font.color.rgb = C_NAVY

p = tf_eq.add_paragraph()
p.text = "Estimates Model 2 with Heteroskedasticity and Autocorrelation Consistent (HAC) standard errors (lag=4) to correct for residual clustering."
p.font.size = Pt(10.5)

# Card Right: Summary Table of Models
add_card(s10, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5), "Estimation Results: Levels vs First Differences")
tbl10_s = s10.shapes.add_table(8, 4, Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
tbl10 = tbl10_s.table
for j, w in enumerate([Inches(2.0), Inches(1.1), Inches(1.1), Inches(1.1)]):
    tbl10.columns[j].width = w

headers_10 = ["Regressor", "Levels OLS", "Diff OLS", "Diff HAC"]
for j, h in enumerate(headers_10):
    cell = tbl10.cell(0, j)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_WHITE

m_rows = [
    ("Constant", "-643.22***", "-0.515", "-0.515"),
    ("Δ VIX", "3.509***", "0.459", "0.459"),
    ("Δ ECB Rate", "2.263", "1.373", "1.373"),
    ("Δ Inflation", "29.855***", "3.385", "3.385"),
    ("Δ Unemployment", "46.753***", "-6.628", "-6.628"),
    ("Δ Debt-to-GDP", "2.478***", "5.357***", "5.357"),
    ("R² / Durbin-Watson", "0.645 / 0.14", "0.036 / 1.64", "0.036 / HAC")
]
for i, row in enumerate(m_rows):
    bg_row = RGBColor(245, 248, 252) if i % 2 == 1 else RGBColor(255, 255, 255)
    for j, val in enumerate(row):
        cell = tbl10.cell(i + 1, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_row
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(10)
        p.font.color.rgb = C_TEXT_DARK
        if j == 0 or i == len(m_rows) - 1:
            p.font.bold = True


# ==============================================================================
# SLIDE 11: Regression Diagnostic Battery
# ==============================================================================
s11 = prs.slides.add_slide(blank_layout)
add_header(s11, "Econometric Diagnostics Battery: First Differences Model")

tbl11_s = s11.shapes.add_table(7, 5, Inches(0.8), Inches(1.4), Inches(11.7), Inches(3.8))
tbl11 = tbl11_s.table
for j, w in enumerate([Inches(3.2), Inches(1.6), Inches(1.8), Inches(2.2), Inches(2.9)]):
    tbl11.columns[j].width = w

headers_11 = ["Diagnostic Test", "Test Statistic", "p-value", "Null Hypothesis (H₀)", "Empirical Decision"]
for j, h in enumerate(headers_11):
    cell = tbl11.cell(0, j)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_WHITE

diag_csv = pd.read_csv(os.path.join(TAB_DIR, 'table08_diagnostics_battery.csv'))
for i, row in diag_csv.iterrows():
    bg_row = RGBColor(245, 248, 252) if i % 2 == 1 else RGBColor(255, 255, 255)
    pval_str = f"{row['p-value']:.4e}" if pd.notnull(row['p-value']) else "—"
    vals = [
        row['Test'],
        f"{row['Statistic']:.3f}",
        pval_str,
        row['Threshold / Null'],
        row['Conclusion']
    ]
    for j, val in enumerate(vals):
        cell = tbl11.cell(i + 1, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_row
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(10)
        p.font.color.rgb = C_TEXT_DARK
        if j == 0:
            p.font.bold = True

add_card(s11, Inches(0.8), Inches(5.5), Inches(11.7), Inches(1.6), "Diagnostic Interpretations", bg_color=RGBColor(240, 245, 252))
tb_d = s11.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.3), Inches(1.0))
tf_d = tb_d.text_frame
tf_d.word_wrap = True
p = tf_d.paragraphs[0]
p.text = "• Multicollinearity Ruled Out: Maximum VIF is 1.11, well below the rule-of-thumb threshold of 5 or 10.\n• Severe Heteroskedasticity & Autocorrelation: White test (p < 0.001) and Breusch-Godfrey LM test (p < 0.001) strongly reject homoskedasticity and no serial correlation. OLS standard errors are invalid, rendering Newey-West HAC standard errors mandatory for statistical inference."
p.font.size = Pt(10.5)
p.font.color.rgb = C_TEXT_DARK


# ==============================================================================
# SLIDE 12: Residual Diagnostics Plot
# ==============================================================================
s12 = prs.slides.add_slide(blank_layout)
add_header(s12, "Residual Analysis & Regression Diagnostics")

fig5_path = os.path.join(FIG_DIR, 'fig05_regression_residuals_diagnostics.png')
if os.path.exists(fig5_path):
    s12.shapes.add_picture(fig5_path, Inches(0.8), Inches(1.35), Inches(8.5), Inches(5.6))

add_card(s12, Inches(9.5), Inches(1.35), Inches(3.0), Inches(5.6), "Residual Properties", bg_color=RGBColor(245, 247, 250))
tb_s12 = s12.shapes.add_textbox(Inches(9.65), Inches(1.9), Inches(2.7), Inches(4.9))
tf_s12 = tb_s12.text_frame
tf_s12.word_wrap = True

resid_insights = [
    ("Volatility Clustering:", "Residual variance explodes during the 2010–2012 sovereign crisis and contracts post-2015."),
    ("Leptokurtic Errors:", "Histogram demonstrates heavy tails (kurtosis > 10). Outliers correspond to bailout negotiations."),
    ("Residual Autocorrelation:", "Residual ACF exhibits persistence, motivating time-series ARIMA modeling.")
]
for t, d in resid_insights:
    p = tf_s12.add_paragraph() if tf_s12.paragraphs[0].text else tf_s12.paragraphs[0]
    p.space_after = Pt(14)
    r1 = p.add_run()
    r1.text = t + "\n"
    r1.font.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = C_NAVY
    r2 = p.add_run()
    r2.text = d
    r2.font.size = Pt(10)
    r2.font.color.rgb = C_TEXT_DARK


# ==============================================================================
# SLIDE 13: Chow Structural Break Test (July 2012)
# ==============================================================================
s13 = prs.slides.add_slide(blank_layout)
add_header(s13, "Structural Break: Chow Test at Draghi's July 2012 Speech")

# Left Card: Test Mechanics & Hypothesis
add_card(s13, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5), "The Chow Test Framework")
tb_ch = s13.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.7))
tf_ch = tb_ch.text_frame
tf_ch.word_wrap = True

p = tf_ch.paragraphs[0]
p.text = "Event: Mario Draghi's 'Whatever It Takes' (26 July 2012)"
p.font.bold = True
p.font.size = Pt(12)
p.font.color.rgb = C_NAVY
p.space_after = Pt(8)

p = tf_ch.add_paragraph()
p.text = "Draghi committed the ECB to preserve the euro within its mandate, introducing Outright Monetary Transactions (OMT). Did this event structurally break the parameters governing sovereign spreads?"
p.font.size = Pt(11)
p.space_after = Pt(14)

p = tf_ch.add_paragraph()
p.text = "Chow Test Hypothesis:"
p.font.bold = True
p.font.size = Pt(12)
p.font.color.rgb = C_NAVY

p = tf_ch.add_paragraph()
p.text = "H₀: Parameters are identical Pre-2012 and Post-2012 (β_pre = β_post)\nH₁: Parameters structurally differ across the 2012 breakpoint\n\nF = [(SSR_pooled - (SSR₁ + SSR₂)) / k] / [(SSR₁ + SSR₂) / (N - 2k)]"
p.font.size = Pt(10.5)
p.space_after = Pt(14)

p = tf_ch.add_paragraph()
p.text = "Conclusion: Reject Null at p < 0.001"
p.font.bold = True
p.font.size = Pt(12)
p.font.color.rgb = C_ACCENT

p = tf_ch.add_paragraph()
p.text = "The ECB backstop created a permanent structural break in European sovereign risk pricing."
p.font.size = Pt(10.5)

# Right Card: Test Statistics Table
add_card(s13, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5), "Chow Test Statistical Results")
tbl13_s = s13.shapes.add_table(7, 2, Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
tbl13 = tbl13_s.table
tbl13.columns[0].width = Inches(3.3)
tbl13.columns[1].width = Inches(2.0)

chow_data = [
    ("Breakpoint Date", "July 2012 (Month 162)"),
    ("Pre-Break Observations (N₁)", "161 months (1999–2012)"),
    ("Post-Break Observations (N₂)", "171 months (2012–2026)"),
    ("Pooled Residual SSR", "863,229.4"),
    ("Unrestricted SSR (SSR₁ + SSR₂)", "790,622.7"),
    ("Chow F-Statistic", "4.982***"),
    ("p-value", "0.000068 (p < 0.0001)")
]
for i, (k_val, v_val) in enumerate(chow_data):
    bg_row = RGBColor(245, 248, 252) if i % 2 == 1 else RGBColor(255, 255, 255)
    for j, val in enumerate([k_val, v_val]):
        cell = tbl13.cell(i, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_row
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEXT_DARK
        if i >= 5:
            p.font.bold = True
            p.font.color.rgb = C_NAVY


# ==============================================================================
# SLIDE 14: Regime Subsample Analysis (Pre-2012 vs Post-2012)
# ==============================================================================
s14 = prs.slides.add_slide(blank_layout)
add_header(s14, "Subsample Regimes: Pre-2012 Crisis vs Post-2012 Backstop")

# Table comparing Pre and Post
tbl14_s = s14.shapes.add_table(8, 4, Inches(0.8), Inches(1.4), Inches(7.8), Inches(5.5))
tbl14 = tbl14_s.table
for j, w in enumerate([Inches(2.4), Inches(1.8), Inches(1.8), Inches(1.8)]):
    tbl14.columns[j].width = w

headers_14 = ["Regressor", "Full Sample HAC", "Pre-2012 HAC", "Post-2012 HAC"]
for j, h in enumerate(headers_14):
    cell = tbl14.cell(0, j)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_WHITE

sub_rows = [
    ("Constant", "-0.515 (1.95)", "0.407 (1.75)", "-6.302** (2.86)"),
    ("Δ VIX (Global Risk)", "0.459 (0.31)", "-0.149 (0.53)", "+0.951*** (0.23)"),
    ("Δ ECB Rate", "1.373 (14.30)", "9.742 (16.33)", "7.422 (7.89)"),
    ("Δ Inflation", "3.385 (3.19)", "-2.249 (4.55)", "5.098 (3.66)"),
    ("Δ Unemployment", "-6.628 (10.05)", "-12.519 (21.35)", "-14.572 (9.35)"),
    ("Δ Debt-to-GDP", "+5.357 (3.53)", "+14.376** (6.52)", "-0.825 (2.08)"),
    ("Observations / R²", "332 / 0.036", "161 / 0.103", "171 / 0.066")
]
for i, row in enumerate(sub_rows):
    bg_row = RGBColor(245, 248, 252) if i % 2 == 1 else RGBColor(255, 255, 255)
    for j, val in enumerate(row):
        cell = tbl14.cell(i + 1, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_row
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_DARK
        if j == 0:
            p.font.bold = True

# Right Card: The Economic Revelation
add_card(s14, Inches(8.9), Inches(1.4), Inches(3.6), Inches(5.5), "The Economic Revelation", bg_color=RGBColor(240, 245, 252))
tb_rev = s14.shapes.add_textbox(Inches(9.1), Inches(1.9), Inches(3.2), Inches(4.9))
tf_rev = tb_rev.text_frame
tf_rev.word_wrap = True

rev_points = [
    ("1. Pre-2012: Fiscal Solvency Dominance", "ΔDebt-to-GDP was +14.38** (p < 0.05). In crisis, markets scrutinized fiscal debt. Each 1 pp increase in debt expanded spread by ~14 bps."),
    ("2. Post-2012: The Severed Debt Spiral", "ΔDebt-to-GDP collapsed to -0.825 (insignificant). The ECB backstop severed the doom-loop between debt and spreads."),
    ("3. Post-2012: Global Market Sensitivity", "ΔVIX surged to +0.951*** (p < 0.01). With default risk backstopped, spreads move with international risk appetite, not domestic panic.")
]
for t, d in rev_points:
    p = tf_rev.add_paragraph() if tf_rev.paragraphs[0].text else tf_rev.paragraphs[0]
    p.space_after = Pt(12)
    r1 = p.add_run()
    r1.text = t + "\n"
    r1.font.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = C_NAVY
    r2 = p.add_run()
    r2.text = d
    r2.font.size = Pt(10)
    r2.font.color.rgb = C_TEXT_DARK


# ==============================================================================
# SLIDE 15: Time Series Decomposition & Identification
# ==============================================================================
s15 = prs.slides.add_slide(blank_layout)
add_header(s15, "Time Series Analysis: Decomposition & ACF/PACF Identification")

fig6_path = os.path.join(FIG_DIR, 'fig06_ts_decomposition_and_acf.png')
if os.path.exists(fig6_path):
    s15.shapes.add_picture(fig6_path, Inches(0.8), Inches(1.35), Inches(8.5), Inches(5.6))

add_card(s15, Inches(9.5), Inches(1.35), Inches(3.0), Inches(5.6), "Identification Insights", bg_color=RGBColor(245, 247, 250))
tb_s15 = s15.shapes.add_textbox(Inches(9.65), Inches(1.9), Inches(2.7), Inches(4.9))
tf_s15 = tb_s15.text_frame
tf_s15.word_wrap = True

id_points = [
    ("No Seasonality:", "Seasonal component is negligible (< 1 bp amplitude). Spread is driven by macro fundamentals and sentiment."),
    ("ACF Pattern:", "ACF of differenced spread shows significant correlation at lag 1 and lag 2, dying out gradually."),
    ("PACF Pattern:", "PACF cuts off after lag 2, indicating potential AR(2) dynamics."),
    ("Candidate Models:", "ARIMA(1,1,1), ARIMA(2,1,2), and ARIMA(3,1,0) should be tested via information criteria.")
]
for t, d in id_points:
    p = tf_s15.add_paragraph() if tf_s15.paragraphs[0].text else tf_s15.paragraphs[0]
    p.space_after = Pt(12)
    r1 = p.add_run()
    r1.text = t + "\n"
    r1.font.bold = True
    r1.font.size = Pt(10.5)
    r1.font.color.rgb = C_NAVY
    r2 = p.add_run()
    r2.text = d
    r2.font.size = Pt(10)
    r2.font.color.rgb = C_TEXT_DARK


# ==============================================================================
# SLIDE 16: ARIMA Model Selection & White Noise Diagnostics
# ==============================================================================
s16 = prs.slides.add_slide(blank_layout)
add_header(s16, "ARIMA Selection Grid & Residual Diagnostics (Ljung-Box Test)")

# Table of Top Models
tbl16_s = s16.shapes.add_table(6, 4, Inches(0.8), Inches(1.4), Inches(5.8), Inches(3.5))
tbl16 = tbl16_s.table
for j, w in enumerate([Inches(1.8), Inches(1.3), Inches(1.3), Inches(1.4)]):
    tbl16.columns[j].width = w

headers_16 = ["Specification", "AIC", "BIC", "Log-Likelihood"]
for j, h in enumerate(headers_16):
    cell = tbl16.cell(0, j)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_WHITE

top_arima = [
    ("ARIMA(2,1,2) ★", "3143.66", "3162.68", "-1566.83"),
    ("ARIMA(3,1,0)", "3144.27", "3159.49", "-1568.14"),
    ("ARIMA(3,1,1)", "3144.67", "3163.69", "-1567.33"),
    ("ARIMA(1,1,3)", "3144.69", "3163.71", "-1567.34"),
    ("ARIMA(1,1,2)", "3144.76", "3159.98", "-1568.38")
]
for i, row in enumerate(top_arima):
    bg_row = RGBColor(235, 247, 238) if i == 0 else (RGBColor(245, 248, 252) if i % 2 == 1 else RGBColor(255, 255, 255))
    for j, val in enumerate(row):
        cell = tbl16.cell(i + 1, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_row
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(10)
        p.font.color.rgb = C_TEXT_DARK
        if i == 0 or j == 0:
            p.font.bold = True

# Right Card: Best Model Parameters
add_card(s16, Inches(7.0), Inches(1.4), Inches(5.5), Inches(3.5), "Best Model: ARIMA(2,1,2) Parameter Estimates")
tb_p = s16.shapes.add_textbox(Inches(7.2), Inches(1.9), Inches(5.1), Inches(2.8))
tf_p = tb_p.text_frame
tf_p.word_wrap = True

p = tf_p.paragraphs[0]
p.text = "Estimated Equation: (1 - 1.572B + 0.680B²) (1 - B) Spread_t = (1 - 1.482B + 0.700B²) a_t"
p.font.bold = True
p.font.size = Pt(11)
p.font.color.rgb = C_NAVY
p.space_after = Pt(10)

p2 = tf_p.add_paragraph()
p2.text = "• ar.L1 = +1.572 (z = 16.41, p < 0.001) | ar.L2 = -0.680 (z = -7.94, p < 0.001)\n• ma.L1 = -1.482 (z = -17.91, p < 0.001) | ma.L2 = +0.700 (z = 12.20, p < 0.001)\n• All parameters statistically significant at 1% level\n• Roots lie outside unit circle → Model is stationary and invertible"
p2.font.size = Pt(10.5)
p2.font.color.rgb = C_TEXT_DARK

# Bottom Card: Ljung-Box White Noise Test
add_card(s16, Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.8), "Residual White Noise Verification: Ljung-Box Test", bg_color=RGBColor(240, 245, 252))
tb_lb = s16.shapes.add_textbox(Inches(1.0), Inches(5.65), Inches(11.3), Inches(1.2))
tf_lb = tb_lb.text_frame
tf_lb.word_wrap = True
p = tf_lb.paragraphs[0]
p.text = "• Lag 6: Q-stat = 4.20, p-value = 0.650 → Fail to reject H₀ (Residuals are white noise at short horizons)\n• Lag 12: Q-stat = 23.83, p-value = 0.021 → Mild residual clustering during 2011–2012 crisis volatility\n• Conclusion: ARIMA(2,1,2) adequately captures linear dependence in Portuguese sovereign spread."
p.font.size = Pt(11)
p.font.color.rgb = C_TEXT_DARK





# ==============================================================================
# SLIDE 17: Volatility Clustering & GARCH(1,1) Modeling
# ==============================================================================
s17_v = prs.slides.add_slide(blank_layout)
add_header(s17_v, "Advanced Time Series: Cointegration & GARCH(1,1) Volatility")

fig10_path = os.path.join(FIG_DIR, 'fig10_garch_conditional_volatility.png')
if os.path.exists(fig10_path):
    s17_v.shapes.add_picture(fig10_path, Inches(0.8), Inches(1.35), Inches(7.5), Inches(5.6))

# Right Table: GARCH Model Estimates
add_card(s17_v, Inches(8.5), Inches(1.35), Inches(4.0), Inches(5.6), "GARCH(1,1)-t Volatility Model")
tbl_garch_s = s17_v.shapes.add_table(7, 3, Inches(8.65), Inches(1.9), Inches(3.7), Inches(2.7))
tbl_g = tbl_garch_s.table
for j, w in enumerate([Inches(1.8), Inches(0.9), Inches(1.0)]):
    tbl_g.columns[j].width = w

headers_g = ["Parameter", "Estimate", "p-value"]
for j, h in enumerate(headers_g):
    cell = tbl_g.cell(0, j)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_WHITE

g_rows = [
    ("ω (Intercept)", "0.794", "0.145"),
    ("α₁ (ARCH shock)", "0.174***", "0.0001"),
    ("β₁ (GARCH persist)", "0.826***", "< 0.0001"),
    ("ν (Student-t df)", "4.559***", "< 0.0001"),
    ("Persistence (α+β)", "1.000", "IGARCH"),
    ("Engle ARCH LM", "96.83***", "< 0.0001")
]
for i, row in enumerate(g_rows):
    bg_row = RGBColor(235, 247, 238) if i in [1, 2, 3] else (RGBColor(245, 248, 252) if i % 2 == 1 else RGBColor(255, 255, 255))
    for j, val in enumerate(row):
        cell = tbl_g.cell(i + 1, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_row
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(9)
        p.font.color.rgb = C_TEXT_DARK
        if i in [1, 2, 3]:
            p.font.bold = True

tb_gv = s17_v.shapes.add_textbox(Inches(8.65), Inches(4.75), Inches(3.7), Inches(2.1))
tf_gv = tb_gv.text_frame
tf_gv.word_wrap = True
p = tf_gv.paragraphs[0]
p.text = "Cointegration & Volatility Insights:"
p.font.bold = True
p.font.size = Pt(11)
p.font.color.rgb = C_NAVY

p2 = tf_gv.add_paragraph()
p2.text = "• Cointegration Test: Engle-Granger p = 0.268 (Fail to reject H₀: No Cointegration). The long-run yield relationship broke in crisis; VECM is invalid, proving First Differences is required.\n• Volatility Regime Shift: Conditional volatility peaked at 120 bps/month in 2011–12 and collapsed to under 12 bps under ECB backstops."
p2.font.size = Pt(9.5)
p2.font.color.rgb = C_TEXT_DARK


# ==============================================================================
# SLIDE 18: Out-of-Sample Forecasting vs Random Walk
# ==============================================================================
s18_f = prs.slides.add_slide(blank_layout)
add_header(s18_f, "Out-of-Sample Forecasting: ARIMA(2,1,2) vs Random Walk (2025–2026)")

fig7_path = os.path.join(FIG_DIR, 'fig07_arima_forecast_vs_random_walk.png')
if os.path.exists(fig7_path):
    s18_f.shapes.add_picture(fig7_path, Inches(0.8), Inches(1.35), Inches(7.5), Inches(5.6))

# Right Table: Forecast Evaluation Metrics
add_card(s18_f, Inches(8.5), Inches(1.35), Inches(4.0), Inches(5.6), "Out-of-Sample Accuracy (N = 21)")
tbl17_s = s18_f.shapes.add_table(5, 4, Inches(8.65), Inches(1.9), Inches(3.7), Inches(2.6))
tbl17 = tbl17_s.table
for j, w in enumerate([Inches(1.5), Inches(0.7), Inches(0.7), Inches(0.8)]):
    tbl17.columns[j].width = w

headers_17 = ["Model", "MAE", "RMSE", "Theil's U"]
for j, h in enumerate(headers_17):
    cell = tbl17.cell(0, j)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_WHITE

f_rows = [
    ("Naive Random Walk", "8.91", "10.22", "1.000"),
    ("RW with Drift", "9.87", "11.34", "1.110"),
    ("ARIMA(2,1,2) ★", "6.86", "7.98", "0.780"),
    ("ARIMA(0,1,1)", "9.12", "10.46", "1.023")
]
for i, row in enumerate(f_rows):
    bg_row = RGBColor(235, 247, 238) if "ARIMA(2,1,2)" in row[0] else (RGBColor(245, 248, 252) if i % 2 == 1 else RGBColor(255, 255, 255))
    for j, val in enumerate(row):
        cell = tbl17.cell(i + 1, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_row
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(9)
        p.font.color.rgb = C_TEXT_DARK
        if "ARIMA(2,1,2)" in row[0]:
            p.font.bold = True

tb_fc = s18_f.shapes.add_textbox(Inches(8.65), Inches(4.7), Inches(3.7), Inches(2.1))
tf_fc = tb_fc.text_frame
tf_fc.word_wrap = True
p = tf_fc.paragraphs[0]
p.text = "Key Forecasting Results:"
p.font.bold = True
p.font.size = Pt(11)
p.font.color.rgb = C_NAVY

p2 = tf_fc.add_paragraph()
p2.text = "• ARIMA Beats Random Walk: Theil's U = 0.780 confirms that ARIMA(2,1,2) outperforms the random walk by 22% in RMSE and 23% in MAE.\n• Mean Absolute Percentage Error (MAPE) drops from 22.6% (RW) to 16.5%.\n• Spread Mean Reversion: The model successfully captures the gentle upward mean reversion in 2025–2026."
p2.font.size = Pt(9.5)
p2.font.color.rgb = C_TEXT_DARK


# ==============================================================================
# SLIDE 19: Cross-Country Extension: The GIIPS Periphery
# ==============================================================================
s19_g = prs.slides.add_slide(blank_layout)
add_header(s19_g, "Cross-Country Extension: Portugal’s Decoupling from GIIPS")

fig8_path = os.path.join(FIG_DIR, 'fig08_giips_spreads_comparison.png')
if os.path.exists(fig8_path):
    s19_g.shapes.add_picture(fig8_path, Inches(0.8), Inches(1.35), Inches(7.5), Inches(5.6))

# Right Table: Current vs Crisis Spreads
add_card(s19_g, Inches(8.5), Inches(1.35), Inches(4.0), Inches(5.6), "Cross-Country Divergence (bps)")
tbl19_s = s19_g.shapes.add_table(6, 4, Inches(8.65), Inches(1.9), Inches(3.7), Inches(2.6))
tbl19 = tbl19_s.table
for j, w in enumerate([Inches(1.2), Inches(0.8), Inches(0.8), Inches(0.9)]):
    tbl19.columns[j].width = w

headers_19 = ["Country", "Crisis Peak", "Pandemic", "Latest (2026)"]
for j, h in enumerate(headers_19):
    cell = tbl19.cell(0, j)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_WHITE

giips_comp = [
    ("Portugal", "1,203 bp", "71 bp", "37 bp ★"),
    ("Spain", "555 bp", "81 bp", "45 bp"),
    ("Italy", "519 bp", "143 bp", "89 bp"),
    ("Greece", "2,739 bp", "137 bp", "75 bp"),
    ("Ireland", "971 bp", "41 bp", "12 bp")
]
for i, row in enumerate(giips_comp):
    bg_row = RGBColor(235, 247, 238) if i == 0 else (RGBColor(245, 248, 252) if i % 2 == 1 else RGBColor(255, 255, 255))
    for j, val in enumerate(row):
        cell = tbl19.cell(i + 1, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_row
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(9)
        p.font.color.rgb = C_TEXT_DARK
        if i == 0 or j == 0:
            p.font.bold = True

tb_g = s19_g.shapes.add_textbox(Inches(8.65), Inches(4.7), Inches(3.7), Inches(2.1))
tf_g = tb_g.text_frame
tf_g.word_wrap = True
p = tf_g.paragraphs[0]
p.text = "The 'Portuguese Miracle':"
p.font.bold = True
p.font.size = Pt(11)
p.font.color.rgb = C_NAVY

p2 = tf_g.add_paragraph()
p2.text = "• From Bailout to Tier-1 Periphery: In 2012, Portugal had the 2nd widest spread in Europe. By 2026, Portugal's spread (37 bps) is less than half of Italy's (89 bps) and below Spain (45 bps).\n• Fiscal Prudence: Sustained primary budget surpluses and rapid debt reduction dismantled the peripheral penalty."
p2.font.size = Pt(9.5)
p2.font.color.rgb = C_TEXT_DARK


# ==============================================================================
# SLIDE 20: Conclusions, Policy Implications & Limitations
# ==============================================================================
s20 = prs.slides.add_slide(blank_layout)
add_header(s20, "Conclusions, Policy Implications & Limitations")

# Card Left: Conclusions
add_card(s20, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5), "Core Conclusions")
tb_c = s20.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.7))
tf_c = tb_c.text_frame
tf_c.word_wrap = True

conc_points = [
    ("1. Regimes Matter More Than Levels:", "Sovereign bond pricing cannot be treated as a single linear process across 1999–2026. The 2012 structural break transformed market mechanics."),
    ("2. Backstops Alter Market Pricing:", "Prior to July 2012, public debt increases directly expanded spreads (+14.4 bps/pp). Post-2012, the ECB backstop neutralized default fear, shifting spread sensitivity to global risk appetite (VIX)."),
    ("3. ARIMA Outperforms Random Walk:", "An identified ARIMA(2,1,2) specification achieves a Theil's U of 0.780, beating naive random walk forecasts."),
    ("4. Periphery Decoupling:", "Portugal transitioned from distressed Troika debtor to a resilient sovereign borrower trading inside Italy.")
]
for t, d in conc_points:
    p = tf_c.add_paragraph() if tf_c.paragraphs[0].text else tf_c.paragraphs[0]
    p.space_after = Pt(12)
    r1 = p.add_run()
    r1.text = t + " "
    r1.font.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = C_NAVY
    r2 = p.add_run()
    r2.text = d
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = C_TEXT_DARK

# Card Right: Policy & Limitations
add_card(s20, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5), "Policy Implications & Limitations")
tb_p = s20.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
tf_p = tb_p.text_frame
tf_p.word_wrap = True

pol_points = [
    ("Policy: Credible Backstops are Crucial:", "ECB anti-fragmentation tools (OMT, PEPP, TPI) are vital to eliminate redenomination premia and prevent speculative self-fulfilling crises in currency unions."),
    ("Policy: Backstops Require Fiscal Virtue:", "ECB backstops provide liquidity insurance, but Portugal's decoupling demonstrates that domestic fiscal discipline (debt-to-GDP reduction) is essential for permanent spread compression."),
    ("Limitation: Data Frequency:", "Monthly frequency smooths high-frequency announcement effects; event-study methodology could capture daily market surprises."),
    ("Limitation: Interpolated Debt:", "Quarterly debt-to-GDP requires interpolation to monthly frequency, which may dampen short-term fiscal shock volatility.")
]
for t, d in pol_points:
    p = tf_p.add_paragraph() if tf_p.paragraphs[0].text else tf_p.paragraphs[0]
    p.space_after = Pt(12)
    r1 = p.add_run()
    r1.text = t + " "
    r1.font.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = C_BLUE
    r2 = p.add_run()
    r2.text = d
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = C_TEXT_DARK

# Save presentation
prs.save(PPTX_PATH)
print(f"\n Presentation saved successfully to {PPTX_PATH}")
print(f"Total Slides: {len(prs.slides)}")
