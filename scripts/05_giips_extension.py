"""
05_giips_extension.py
Cross-Country Extension: Comparative analysis of sovereign spreads across GIIPS
(Portugal, Spain, Italy, Greece, Ireland) relative to Germany (1999–2026).
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
FIG_DIR = os.path.join(os.path.dirname(__file__), '..', 'figures')
TAB_DIR = os.path.join(os.path.dirname(__file__), '..', 'tables')

master = pd.read_csv(os.path.join(DATA_DIR, 'sovereign_spreads_master.csv'), index_col='TIME_PERIOD', parse_dates=True)

giips_cols = {
    'Spread_PT_bps': 'Portugal',
    'Spread_ES_bps': 'Spain',
    'Spread_IT_bps': 'Italy',
    'Spread_GR_bps': 'Greece',
    'Spread_IE_bps': 'Ireland'
}
giips_df = master[list(giips_cols.keys())].rename(columns=giips_cols)

# --- 1. Cross-Country Summary Statistics ---
summary_giips = []
for c in giips_df.columns:
    s = giips_df[c].dropna()
    summary_giips.append({
        'Country': c,
        'N': len(s),
        'Mean (bps)': s.mean(),
        'Std Dev (bps)': s.std(),
        'Median (bps)': s.median(),
        'Min (bps)': s.min(),
        'Max (bps)': s.max(),
        'Latest (2026) (bps)': s.iloc[-1]
    })

giips_summary_df = pd.DataFrame(summary_giips)
giips_summary_df.to_csv(os.path.join(TAB_DIR, 'table13_giips_summary_statistics.csv'), index=False)
giips_summary_df.to_markdown(os.path.join(TAB_DIR, 'table13_giips_summary_statistics.md'), index=False)
print("=== GIIPS Spreads Full Summary Statistics ===")
print(giips_summary_df.to_string(index=False))

# --- 2. GIIPS Spreads by Regime ---
regimes = sorted(master['Regime'].unique())
regime_giips_rows = []
for r in regimes:
    sub = giips_df[master['Regime'] == r]
    for c in giips_df.columns:
        s = sub[c].dropna()
        regime_giips_rows.append({
            'Regime': r,
            'Country': c,
            'Mean (bps)': s.mean(),
            'Std (bps)': s.std(),
            'Median (bps)': s.median(),
            'Max (bps)': s.max()
        })

regime_giips_df = pd.DataFrame(regime_giips_rows)
regime_giips_df.to_csv(os.path.join(TAB_DIR, 'table14_giips_regime_comparison.csv'), index=False)
print("\n=== GIIPS Spreads by Regime ===")
print(regime_giips_df.pivot(index='Country', columns='Regime', values='Mean (bps)'))

# --- 3. Figure: GIIPS Sovereign Spreads Evolution ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 9), gridspec_kw={'height_ratios': [1.2, 1]})

colors = {'Portugal': '#004b87', 'Spain': '#ff7f0e', 'Italy': '#2ca02c', 'Greece': '#d62728', 'Ireland': '#9467bd'}
lw = {'Portugal': 2.4, 'Spain': 1.6, 'Italy': 1.6, 'Greece': 1.6, 'Ireland': 1.6}

# Panel 1: Full scale including Greece crisis peak
for c in giips_df.columns:
    ax1.plot(giips_df.index, giips_df[c], label=c, color=colors[c], lw=lw[c], alpha=0.9)

ax1.axhline(0, color='black', lw=0.8, linestyle=':')
ax1.set_ylabel('Spread over Germany (bps)', fontweight='bold')
ax1.set_title('A: Sovereign 10-Year Yield Spreads Across GIIPS Periphery (1999–2026)', fontsize=12, fontweight='bold')
ax1.legend(loc='upper right', framealpha=0.9)
ax1.grid(True, alpha=0.3)
ax1.set_ylim(-50, 3000)

# Annotate key peaks
ax1.annotate('Greece Peak\n(~2900 bps in 2012)', xy=(pd.Timestamp('2012-02-01'), 2800), xytext=(pd.Timestamp('2014-01-01'), 2600),
             arrowprops=dict(arrowstyle="->", color='#d62728'), fontsize=8.5, color='#d62728')
ax1.annotate('Portugal Peak\n(~1200 bps in Jan 2012)', xy=(pd.Timestamp('2012-01-01'), 1200), xytext=(pd.Timestamp('2006-01-01'), 1400),
             arrowprops=dict(arrowstyle="->", color='#004b87'), fontsize=8.5, color='#004b87')

# Panel 2: Truncated view (-20 to 600 bps) highlighting post-2015 convergence & Portugal's decoupling
for c in giips_df.columns:
    ax2.plot(giips_df.index, giips_df[c], label=c, color=colors[c], lw=lw[c], alpha=0.9)

ax2.axhline(0, color='black', lw=0.8, linestyle=':')
ax2.set_ylim(-20, 650)
ax2.set_ylabel('Spread (bps) [Truncated Scale]', fontweight='bold')
ax2.set_xlabel('Year', fontweight='bold')
ax2.set_title("B: Periphery Convergence & Portugal's Decoupling from Italy (2014–2026)", fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(loc='upper left', framealpha=0.9)

# Shading for Post-Draghi and TPI
ax2.axvspan(pd.Timestamp('2015-03-01'), pd.Timestamp('2019-12-31'), color='#eaf8ea', alpha=0.4, label='ECB PSPP / QE')
ax2.axvspan(pd.Timestamp('2022-07-01'), pd.Timestamp('2026-09-30'), color='#fff6e6', alpha=0.4, label='ECB TPI Backstop')

for ax in (ax1, ax2):
    ax.xaxis.set_major_locator(mdates.YearLocator(3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.set_xlim(pd.Timestamp('1999-01-01'), pd.Timestamp('2026-10-01'))

plt.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'fig08_giips_spreads_comparison.png'), dpi=300)
plt.close(fig)
print(" Saved fig08_giips_spreads_comparison.png")

# --- 4. Figure: Rolling Pairwise Correlation with Portugal ---
rolling_corr = giips_df[['Spain', 'Italy', 'Greece', 'Ireland']].rolling(window=36).corr(giips_df['Portugal'])

fig, ax = plt.subplots(figsize=(12, 5.5))
for c in ['Spain', 'Italy', 'Greece', 'Ireland']:
    ax.plot(rolling_corr.index, rolling_corr[c], label=f'Corr(PT, {c})', color=colors[c], lw=1.8)

ax.axhline(0, color='black', lw=0.8, linestyle=':')
ax.axhline(1, color='gray', lw=0.6, linestyle='--')
ax.axvline(pd.Timestamp('2012-07-01'), color='green', linestyle=':', lw=1.5, label='Draghi 2012 Break')
ax.set_ylabel('36-Month Rolling Correlation', fontweight='bold')
ax.set_xlabel('Year', fontweight='bold')
ax.set_title('Co-Movement Dynamics: 36-Month Rolling Correlation of GIIPS Spreads with Portugal', fontsize=12, fontweight='bold')
ax.legend(loc='lower left', framealpha=0.9)
ax.grid(True, alpha=0.3)
ax.set_ylim(-0.4, 1.05)
ax.xaxis.set_major_locator(mdates.YearLocator(3))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.set_xlim(pd.Timestamp('2002-01-01'), pd.Timestamp('2026-10-01'))

plt.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'fig09_giips_rolling_correlations.png'), dpi=300)
plt.close(fig)
print(" Saved fig09_giips_rolling_correlations.png")
print("\nPhase 5 Complete!")
