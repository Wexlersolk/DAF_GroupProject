"""
02_exploratory_and_regimes.py
Generates summary statistics tables, regime comparisons, correlation matrices,
and publication-quality figures.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
FIG_DIR = os.path.join(os.path.dirname(__file__), '..', 'figures')
TAB_DIR = os.path.join(os.path.dirname(__file__), '..', 'tables')
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(TAB_DIR, exist_ok=True)

# Load data
master = pd.read_csv(os.path.join(DATA_DIR, 'sovereign_spreads_master.csv'), index_col='TIME_PERIOD', parse_dates=True)

# Define clean labels
var_labels = {
    'Spread_PT_bps': 'PT-DE Spread (bps)',
    'Yield_10Y_PT': 'PT 10Y Yield (%)',
    'Yield_10Y_DE': 'DE 10Y Yield (%)',
    'VIX': 'VIX Index',
    'ECB_DFR': 'ECB Deposit Rate (%)',
    'HICP_Inflation_PT': 'PT HICP Inflation (% YoY)',
    'Unemp_Rate_PT': 'PT Unemployment Rate (%)',
    'Debt_to_GDP_PT': 'PT Debt-to-GDP (%)'
}

# --- 1. Summary Statistics Table ---
def calc_summary_stats(df, vars_dict):
    rows = []
    for var, label in vars_dict.items():
        s = df[var].dropna()
        jb_stat, jb_p = stats.jarque_bera(s)
        rows.append({
            'Variable': label,
            'N': len(s),
            'Mean': s.mean(),
            'Std': s.std(),
            'Median': s.median(),
            'Min': s.min(),
            'Max': s.max(),
            'Skewness': s.skew(),
            'Kurtosis': s.kurtosis() + 3.0, # Fisher kurtosis + 3 = Pearson kurtosis
            'JB_Stat': jb_stat,
            'JB_pVal': jb_p
        })
    return pd.DataFrame(rows)

full_stats = calc_summary_stats(master, var_labels)
full_stats.to_csv(os.path.join(TAB_DIR, 'table01_summary_statistics_full.csv'), index=False)
full_stats.to_markdown(os.path.join(TAB_DIR, 'table01_summary_statistics_full.md'), index=False)
print("=== Full Sample Summary Statistics ===")
print(full_stats[['Variable', 'Mean', 'Std', 'Median', 'Min', 'Max', 'JB_pVal']].to_string(index=False))

# --- 2. Summary Statistics by Regime ---
regimes = sorted(master['Regime'].unique())
regime_stats_list = []
for r in regimes:
    sub = master[master['Regime'] == r]
    rs = calc_summary_stats(sub, var_labels)
    rs['Regime'] = r
    regime_stats_list.append(rs)

regime_stats_df = pd.concat(regime_stats_list, ignore_index=True)
regime_stats_df.to_csv(os.path.join(TAB_DIR, 'table02_summary_statistics_by_regime.csv'), index=False)

# Summary of Spread specifically across regimes
spread_by_regime = master.groupby('Regime')['Spread_PT_bps'].agg(['count', 'mean', 'std', 'min', 'median', 'max'])
spread_by_regime.to_csv(os.path.join(TAB_DIR, 'table03_spread_by_regime.csv'))
spread_by_regime.to_markdown(os.path.join(TAB_DIR, 'table03_spread_by_regime.md'))
print("\n=== PT Spread (bps) by Regime ===")
print(spread_by_regime.to_string())

# --- 3. Correlation Matrices ---
levels_vars = list(var_labels.keys())
corr_levels = master[levels_vars].rename(columns=var_labels).corr()
corr_levels.to_csv(os.path.join(TAB_DIR, 'table04_correlation_levels.csv'))

diff_vars = ['d_Spread_PT_bps', 'd_VIX', 'd_ECB_DFR', 'd_HICP_Inflation_PT', 'd_Unemp_Rate_PT', 'd_Debt_to_GDP_PT']
diff_labels = {
    'd_Spread_PT_bps': 'Δ Spread (bps)',
    'd_VIX': 'Δ VIX',
    'd_ECB_DFR': 'Δ ECB Rate',
    'd_HICP_Inflation_PT': 'Δ Inflation',
    'd_Unemp_Rate_PT': 'Δ Unemployment',
    'd_Debt_to_GDP_PT': 'Δ Debt-to-GDP'
}
corr_diffs = master[diff_vars].rename(columns=diff_labels).corr()
corr_diffs.to_csv(os.path.join(TAB_DIR, 'table05_correlation_differences.csv'))

# --- 4. Publication Figures ---
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.35

# Figure 1: Historical Evolution of Yields and Spread with Policy Regimes
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [1.2, 1]})

# Shading for regimes
regime_spans = [
    (pd.Timestamp('1999-01-01'), pd.Timestamp('2007-12-31'), '#e8f4f8', '1. EMU Convergence (1999-07)'),
    (pd.Timestamp('2008-01-01'), pd.Timestamp('2012-06-30'), '#fbeae7', '2. Debt Crisis & Bailout (2008-12)'),
    (pd.Timestamp('2012-07-01'), pd.Timestamp('2019-12-31'), '#eaf8ea', '3. Post-Draghi QE (2012-19)'),
    (pd.Timestamp('2020-01-01'), pd.Timestamp('2026-09-30'), '#fff6e6', '4. Pandemic & TPI (2020-26)')
]

for start, end, color, label in regime_spans:
    ax1.axvspan(start, end, color=color, alpha=0.6)
    ax2.axvspan(start, end, color=color, alpha=0.6)

# Yields
ax1.plot(master.index, master['Yield_10Y_PT'], color='#004b87', lw=2.2, label='Portugal 10Y Yield')
ax1.plot(master.index, master['Yield_10Y_DE'], color='#d9534f', lw=2.0, linestyle='--', label='Germany 10Y Yield (Benchmark)')
ax1.set_ylabel('Yield (%)', fontweight='bold')
ax1.set_title("From Bailout to Backstop: Portugal vs Germany 10-Year Government Bond Yields (1999–2026)", fontsize=13, fontweight='bold', pad=12)
ax1.legend(loc='upper right', frameon=True, framealpha=0.9)
ax1.set_ylim(-1.5, 17.5)

# Key event annotations
events = [
    (pd.Timestamp('2011-05-01'), 11.5, 'Troika Bailout\n(May 2011: €78bn)'),
    (pd.Timestamp('2012-01-01'), 16.0, 'Peak Spread\n(Jan 2012: ~1240 bps)'),
    (pd.Timestamp('2012-07-26'), 10.5, '"Whatever It Takes"\n(July 2012)'),
    (pd.Timestamp('2015-03-01'), 1.8, 'ECB PSPP / QE\n(Mar 2015)'),
    (pd.Timestamp('2022-07-01'), 2.5, 'TPI Backstop &\nHikes (Jul 2022)')
]
for date, yval, text in events:
    ax1.annotate(text, xy=(date, yval), xytext=(date, yval + 1.2),
                 arrowprops=dict(arrowstyle="->", color='black', lw=1),
                 fontsize=8.5, ha='center', bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor='gray'))

# Spread
ax2.plot(master.index, master['Spread_PT_bps'], color='#2ca02c', lw=2.2, label='10Y Sovereign Spread (PT - DE, bps)')
ax2.axhline(0, color='black', lw=0.8, linestyle=':')
ax2.set_ylabel('Spread (Basis Points)', fontweight='bold')
ax2.legend(loc='upper right', frameon=True, framealpha=0.9)
ax2.set_xlabel('Year', fontweight='bold')
ax2.xaxis.set_major_locator(mdates.YearLocator(2))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax2.set_xlim(pd.Timestamp('1999-01-01'), pd.Timestamp('2026-10-01'))

plt.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'fig01_yields_and_spread_regimes.png'), dpi=300)
plt.close(fig)
print(" Saved fig01_yields_and_spread_regimes.png")

# Figure 2: Spread vs Macroeconomic & Monetary Drivers
fig, axes = plt.subplots(2, 2, figsize=(14, 9))

# Panel A: Spread vs VIX
ax = axes[0, 0]
ax.plot(master.index, master['Spread_PT_bps'], color='#004b87', lw=1.8, label='PT Spread (bps, left)')
ax.set_ylabel('PT Spread (bps)', color='#004b87', fontweight='bold')
ax.tick_params(axis='y', labelcolor='#004b87')
ax_twin = ax.twinx()
ax_twin.plot(master.index, master['VIX'], color='#ff7f0e', lw=1.4, linestyle='--', label='VIX Index (right)')
ax_twin.set_ylabel('VIX (Global Risk)', color='#ff7f0e', fontweight='bold')
ax_twin.tick_params(axis='y', labelcolor='#ff7f0e')
ax.set_title('A: Sovereign Spread vs Global Risk Aversion (VIX)', fontweight='bold')
ax.grid(True, alpha=0.3)

# Panel B: Spread vs ECB Deposit Facility Rate
ax = axes[0, 1]
ax.plot(master.index, master['Spread_PT_bps'], color='#004b87', lw=1.8, label='PT Spread (bps, left)')
ax.set_ylabel('PT Spread (bps)', color='#004b87', fontweight='bold')
ax.tick_params(axis='y', labelcolor='#004b87')
ax_twin = ax.twinx()
ax_twin.step(master.index, master['ECB_DFR'], color='#9467bd', lw=1.6, where='post', label='ECB DFR (right)')
ax_twin.set_ylabel('ECB Deposit Rate (%)', color='#9467bd', fontweight='bold')
ax_twin.tick_params(axis='y', labelcolor='#9467bd')
ax.set_title('B: Sovereign Spread vs ECB Monetary Policy Rate', fontweight='bold')
ax.grid(True, alpha=0.3)

# Panel C: Spread vs Debt-to-GDP
ax = axes[1, 0]
ax.plot(master.index, master['Spread_PT_bps'], color='#004b87', lw=1.8)
ax.set_ylabel('PT Spread (bps)', color='#004b87', fontweight='bold')
ax.tick_params(axis='y', labelcolor='#004b87')
ax_twin = ax.twinx()
ax_twin.plot(master.index, master['Debt_to_GDP_PT'], color='#d62728', lw=1.6, linestyle='-.')
ax_twin.set_ylabel('Public Debt / GDP (%)', color='#d62728', fontweight='bold')
ax_twin.tick_params(axis='y', labelcolor='#d62728')
ax.set_title('C: Sovereign Spread vs Public Debt-to-GDP Ratio', fontweight='bold')
ax.grid(True, alpha=0.3)

# Panel D: Spread vs Domestic Macro (Inflation & Unemployment)
ax = axes[1, 1]
ax.plot(master.index, master['HICP_Inflation_PT'], color='#8c564b', lw=1.6, label='HICP Inflation (% YoY)')
ax.plot(master.index, master['Unemp_Rate_PT'], color='#17becf', lw=1.6, linestyle='--', label='Unemployment Rate (%)')
ax.set_ylabel('Percentage (%)', fontweight='bold')
ax.set_title('D: Domestic Macro Fundamentals (Inflation & Unemployment)', fontweight='bold')
ax.legend(loc='upper right', framealpha=0.9)
ax.grid(True, alpha=0.3)

for ax in axes.flat:
    ax.xaxis.set_major_locator(mdates.YearLocator(4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'fig02_spread_vs_macro_drivers.png'), dpi=300)
plt.close(fig)
print(" Saved fig02_spread_vs_macro_drivers.png")

# Figure 3: Boxplot of Spread by Regime
fig, ax = plt.subplots(figsize=(9, 5.5))
regime_clean_names = [
    '1. Convergence\n(1999-2007)',
    '2. Crisis & Troika\n(2008-2012)',
    '3. Post-Draghi QE\n(2012-2019)',
    '4. Pandemic & TPI\n(2020-2026)'
]
box_data = [master[master['Regime'] == r]['Spread_PT_bps'].dropna() for r in regimes]
bp = ax.boxplot(box_data, patch_artist=True, tick_labels=regime_clean_names, notch=True,
                boxprops=dict(facecolor='#d9edf7', color='#31708f', lw=1.5),
                medianprops=dict(color='#d9534f', lw=2),
                whiskerprops=dict(color='#31708f', lw=1.2),
                capprops=dict(color='#31708f', lw=1.2))

# Color individual boxes
colors = ['#cce5ff', '#f8d7da', '#d4edda', '#fff3cd']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

ax.set_ylabel('Spread (Basis Points)', fontweight='bold')
ax.set_title('Distribution of Portuguese 10-Year Spread Across Policy Regimes', fontsize=12, fontweight='bold', pad=10)
ax.axhline(0, color='gray', linestyle=':', lw=0.8)

# Add text with mean and std
for i, d in enumerate(box_data):
    mean_val = d.mean()
    sd_val = d.std()
    ax.text(i + 1, d.quantile(0.85) + 35, f"μ = {mean_val:.0f} bp\nσ = {sd_val:.0f} bp",
            ha='center', fontsize=9, bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor='gray'))

plt.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'fig03_regime_boxplots.png'), dpi=300)
plt.close(fig)
print(" Saved fig03_regime_boxplots.png")

# Figure 4: Correlation Matrix Heatmap
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

def draw_corr_mat(ax, cmat, title):
    im = ax.imshow(cmat, cmap='coolwarm', vmin=-1, vmax=1)
    ax.set_xticks(range(len(cmat.columns)))
    ax.set_yticks(range(len(cmat.index)))
    ax.set_xticklabels(cmat.columns, rotation=45, ha='right', fontsize=8.5)
    ax.set_yticklabels(cmat.index, fontsize=8.5)
    ax.set_title(title, fontweight='bold', pad=8)
    for i in range(len(cmat.index)):
        for j in range(len(cmat.columns)):
            val = cmat.iloc[i, j]
            color = 'white' if abs(val) > 0.6 else 'black'
            ax.text(j, i, f"{val:.2f}", ha='center', va='center', color=color, fontsize=8)
    return im

draw_corr_mat(ax1, corr_levels, "Correlation in Levels")
im2 = draw_corr_mat(ax2, corr_diffs, "Correlation in First Differences (MoM)")
fig.colorbar(im2, ax=[ax1, ax2], orientation='horizontal', fraction=0.06, pad=0.18, label='Correlation Coefficient')

plt.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'fig04_correlation_heatmaps.png'), dpi=300)
plt.close(fig)
print(" Saved fig04_correlation_heatmaps.png")
print("\nPhase 2 Complete!")
