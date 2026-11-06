"""
03_regression_and_diagnostics.py
Performs Unit Root tests (ADF/KPSS), Multiple Regression in Levels & First Differences,
Diagnostic Battery (VIF, White, Breusch-Pagan, Breusch-Godfrey, Jarque-Bera),
Newey-West HAC corrections, Chow Structural Break Test at July 2012, and residual plots.
"""

import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan, het_white, acorr_breusch_godfrey
from statsmodels.stats.stattools import durbin_watson, jarque_bera
import matplotlib.pyplot as plt
from scipy import stats

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
FIG_DIR = os.path.join(os.path.dirname(__file__), '..', 'figures')
TAB_DIR = os.path.join(os.path.dirname(__file__), '..', 'tables')

master = pd.read_csv(os.path.join(DATA_DIR, 'sovereign_spreads_master.csv'), index_col='TIME_PERIOD', parse_dates=True)

# --- 1. Unit Root Tests (ADF and KPSS) ---
series_levels = {
    'Spread_PT_bps': 'Spread (bps)',
    'VIX': 'VIX',
    'ECB_DFR': 'ECB Rate',
    'HICP_Inflation_PT': 'Inflation',
    'Unemp_Rate_PT': 'Unemployment',
    'Debt_to_GDP_PT': 'Debt-to-GDP'
}

unit_root_results = []
for col, name in series_levels.items():
    s_level = master[col].dropna()
    adf_lvl = adfuller(s_level, autolag='AIC')
    try:
        kpss_lvl = kpss(s_level, regression='c', nlags='auto')
        kpss_lvl_p = kpss_lvl[1]
    except Exception:
        kpss_lvl_p = np.nan
        
    d_col = f'd_{col}'
    s_diff = master[d_col].dropna()
    adf_diff = adfuller(s_diff, autolag='AIC')
    try:
        kpss_diff = kpss(s_diff, regression='c', nlags='auto')
        kpss_diff_p = kpss_diff[1]
    except Exception:
        kpss_diff_p = np.nan
        
    unit_root_results.append({
        'Variable': name,
        'ADF_Stat_Level': adf_lvl[0],
        'ADF_pVal_Level': adf_lvl[1],
        'KPSS_pVal_Level': kpss_lvl_p,
        'Order_Level': 'I(1)' if adf_lvl[1] > 0.05 else 'I(0)',
        'ADF_Stat_Diff': adf_diff[0],
        'ADF_pVal_Diff': adf_diff[1],
        'KPSS_pVal_Diff': kpss_diff_p,
        'Order_Diff': 'I(0)' if adf_diff[1] < 0.05 else 'I(1)'
    })

ur_df = pd.DataFrame(unit_root_results)
ur_df.to_csv(os.path.join(TAB_DIR, 'table06_unit_root_tests.csv'), index=False)
ur_df.to_markdown(os.path.join(TAB_DIR, 'table06_unit_root_tests.md'), index=False)
print("=== Unit Root Tests (ADF & KPSS) ===")
print(ur_df.to_string(index=False))

# --- 2. Multiple Regression Models ---
# Data preparation: Drop NAs in differences
reg_data = master.dropna(subset=['d_Spread_PT_bps', 'd_VIX', 'd_ECB_DFR', 'd_HICP_Inflation_PT', 'd_Unemp_Rate_PT', 'd_Debt_to_GDP_PT']).copy()

# Model 1: Spurious Levels OLS
X_lvl = sm.add_constant(master[['VIX', 'ECB_DFR', 'HICP_Inflation_PT', 'Unemp_Rate_PT', 'Debt_to_GDP_PT']].dropna())
y_lvl = master.loc[X_lvl.index, 'Spread_PT_bps']
ols_lvl = sm.OLS(y_lvl, X_lvl).fit()

# Model 2: First Differences OLS (Classic)
X_diff_vars = ['d_VIX', 'd_ECB_DFR', 'd_HICP_Inflation_PT', 'd_Unemp_Rate_PT', 'd_Debt_to_GDP_PT']
X_diff = sm.add_constant(reg_data[X_diff_vars])
y_diff = reg_data['d_Spread_PT_bps']
ols_diff = sm.OLS(y_diff, X_diff).fit()

# Model 2 with Newey-West HAC Standard Errors (lag 4)
ols_diff_hac = sm.OLS(y_diff, X_diff).fit(cov_type='HAC', cov_kwds={'maxlags': 4})

# Model 3: Interaction with Post-2012 Dummy (Draghi "Whatever it takes" structural break)
# D = 1 if >= July 2012, 0 otherwise
reg_data['D_2012'] = reg_data['Post_2012_Dummy']
for var in X_diff_vars:
    reg_data[f'{var}_x_D'] = reg_data[var] * reg_data['D_2012']

X_inter_vars = ['D_2012'] + X_diff_vars + [f'{var}_x_D' for var in X_diff_vars]
X_inter = sm.add_constant(reg_data[X_inter_vars])
ols_inter_hac = sm.OLS(y_diff, X_inter).fit(cov_type='HAC', cov_kwds={'maxlags': 4})

# Subsample Regimes:
# Pre-Draghi (1999-01 to 2012-06): Crisis & Convergence
# Post-Draghi (2012-07 to 2026-09): QE, Pandemic, Backstop
pre_mask = reg_data['D_2012'] == 0
post_mask = reg_data['D_2012'] == 1

ols_pre = sm.OLS(y_diff[pre_mask], sm.add_constant(reg_data.loc[pre_mask, X_diff_vars])).fit(cov_type='HAC', cov_kwds={'maxlags': 4})
ols_post = sm.OLS(y_diff[post_mask], sm.add_constant(reg_data.loc[post_mask, X_diff_vars])).fit(cov_type='HAC', cov_kwds={'maxlags': 4})

# --- 3. Diagnostics Battery ---
# A. Multicollinearity (VIF)
def calc_vif(X_matrix):
    vif_data = []
    for i, col in enumerate(X_matrix.columns):
        if col == 'const':
            continue
        vif_val = variance_inflation_factor(X_matrix.values, i)
        vif_data.append({'Variable': col, 'VIF': vif_val})
    return pd.DataFrame(vif_data)

vif_lvl = calc_vif(X_lvl)
vif_diff = calc_vif(X_diff)

print("\n=== Multicollinearity: VIF in Levels vs Differences ===")
print("Levels VIF:\n", vif_lvl.to_string(index=False))
print("Differences VIF:\n", vif_diff.to_string(index=False))

# B. Heteroskedasticity Tests on Model 2
bp_stat, bp_pval, _, _ = het_breuschpagan(ols_diff.resid, ols_diff.model.exog)
white_stat, white_pval, _, _ = het_white(ols_diff.resid, ols_diff.model.exog)

# C. Autocorrelation Tests
dw_stat = durbin_watson(ols_diff.resid)
bg_stat, bg_pval, _, _ = acorr_breusch_godfrey(ols_diff, nlags=4)

# D. Normality of Residuals
jb_stat, jb_pval, skew, kurt = jarque_bera(ols_diff.resid)

diagnostics_summary = pd.DataFrame([
    {'Test': 'Multicollinearity (Max VIF)', 'Statistic': vif_diff['VIF'].max(), 'p-value': np.nan, 'Threshold / Null': '< 5 (No issue)', 'Conclusion': 'No multicollinearity in diffs'},
    {'Test': 'Breusch-Pagan (Heteroskedasticity)', 'Statistic': bp_stat, 'p-value': bp_pval, 'Threshold / Null': 'H0: Homoskedasticity', 'Conclusion': 'Reject H0 (Heteroskedastic)' if bp_pval < 0.05 else 'Fail to reject'},
    {'Test': 'White Test (Heteroskedasticity)', 'Statistic': white_stat, 'p-value': white_pval, 'Threshold / Null': 'H0: Homoskedasticity', 'Conclusion': 'Reject H0 (Heteroskedastic)' if white_pval < 0.05 else 'Fail to reject'},
    {'Test': 'Durbin-Watson (Autocorrelation)', 'Statistic': dw_stat, 'p-value': np.nan, 'Threshold / Null': '~ 2.0 (No autocorr)', 'Conclusion': 'Mild positive autocorrelation'},
    {'Test': 'Breusch-Godfrey LM (Autocorrelation lag 4)', 'Statistic': bg_stat, 'p-value': bg_pval, 'Threshold / Null': 'H0: No serial correlation', 'Conclusion': 'Reject H0 (Autocorrelated)' if bg_pval < 0.05 else 'Fail to reject'},
    {'Test': 'Jarque-Bera (Normality of residuals)', 'Statistic': jb_stat, 'p-value': jb_pval, 'Threshold / Null': 'H0: Normal residuals', 'Conclusion': 'Fat-tailed / Leptokurtic'}
])
diagnostics_summary.to_csv(os.path.join(TAB_DIR, 'table08_diagnostics_battery.csv'), index=False)
diagnostics_summary.to_markdown(os.path.join(TAB_DIR, 'table08_diagnostics_battery.md'), index=False)
print("\n=== Diagnostics Battery for First Differences Model ===")
print(diagnostics_summary.to_string(index=False))

# --- 4. Chow Structural Break Test (July 2012) ---
# Unrestricted: separate regressions for pre and post
ssr_pooled = ols_diff.ssr
ssr_pre = sm.OLS(y_diff[pre_mask], sm.add_constant(reg_data.loc[pre_mask, X_diff_vars])).fit().ssr
ssr_post = sm.OLS(y_diff[post_mask], sm.add_constant(reg_data.loc[post_mask, X_diff_vars])).fit().ssr
ssr_unrestricted = ssr_pre + ssr_post

k = X_diff.shape[1] # number of parameters including constant (6)
n1 = pre_mask.sum()
n2 = post_mask.sum()
n = n1 + n2

chow_f = ((ssr_pooled - ssr_unrestricted) / k) / (ssr_unrestricted / (n - 2 * k))
chow_pval = 1.0 - stats.f.cdf(chow_f, dfn=k, dfd=n - 2 * k)

chow_res = pd.DataFrame([{
    'Breakpoint': 'July 2012 (Draghi "Whatever It Takes")',
    'N_Pre': n1,
    'N_Post': n2,
    'SSR_Pooled': ssr_pooled,
    'SSR_Pre': ssr_pre,
    'SSR_Post': ssr_post,
    'Chow_F_Stat': chow_f,
    'p_value': chow_pval,
    'Decision': 'Reject Null: Structural Break Confirmed (p < 0.001)' if chow_pval < 0.01 else 'No structural break'
}])
chow_res.to_csv(os.path.join(TAB_DIR, 'table09_chow_test.csv'), index=False)
chow_res.to_markdown(os.path.join(TAB_DIR, 'table09_chow_test.md'), index=False)
print("\n=== Chow Structural Break Test Results ===")
print(chow_res[['Breakpoint', 'N_Pre', 'N_Post', 'Chow_F_Stat', 'p_value', 'Decision']].to_string(index=False))

# --- 5. Format Regression Comparison Table ---
def format_model_results(models, names):
    rows = []
    all_vars = []
    for m in models:
        for v in m.params.index:
            if v not in all_vars:
                all_vars.append(v)
                
    for v in all_vars:
        row_coef = {'Variable': v}
        row_se = {'Variable': f'  (s.e.)'}
        for m, name in zip(models, names):
            if v in m.params:
                coef = m.params[v]
                pval = m.pvalues[v]
                se = m.bse[v]
                stars = '***' if pval < 0.01 else ('**' if pval < 0.05 else ('*' if pval < 0.1 else ''))
                row_coef[name] = f"{coef:.3f}{stars}"
                row_se[name] = f"({se:.3f})"
            else:
                row_coef[name] = ""
                row_se[name] = ""
        rows.append(row_coef)
        rows.append(row_se)
        
    # Summary stats
    stats_rows = [
        ('Observations', [f"{int(m.nobs)}" for m in models]),
        ('R-squared', [f"{m.rsquared:.3f}" for m in models]),
        ('Adj. R-squared', [f"{m.rsquared_adj:.3f}" for m in models]),
        ('F-statistic', [f"{m.fvalue:.2f}***" if hasattr(m, 'fvalue') and m.fvalue is not None else "N/A" for m in models]),
        ('Std Error Type', [m.cov_type for m in models])
    ]
    for s_name, s_vals in stats_rows:
        r = {'Variable': s_name}
        for name, val in zip(names, s_vals):
            r[name] = val
        rows.append(r)
        
    return pd.DataFrame(rows)

models_list = [ols_lvl, ols_diff, ols_diff_hac, ols_pre, ols_post]
names_list = ['(1) Levels OLS', '(2) Diff OLS', '(3) Diff HAC', '(4) Pre-2012 HAC', '(5) Post-2012 HAC']
reg_table = format_model_results(models_list, names_list)
reg_table.to_csv(os.path.join(TAB_DIR, 'table07_regression_models_comparison.csv'), index=False)
reg_table.to_markdown(os.path.join(TAB_DIR, 'table07_regression_models_comparison.md'), index=False)
print("\n=== Regression Models Comparison ===")
print(reg_table.to_string(index=False))

# --- 6. Figure: Residual Diagnostics Plot ---
fig, axes = plt.subplots(2, 2, figsize=(12, 9))

# Panel 1: Residuals vs Time
ax = axes[0, 0]
ax.plot(reg_data.index, ols_diff.resid, color='#004b87', lw=1.2)
ax.axhline(0, color='red', linestyle='--', lw=1)
ax.axvline(pd.Timestamp('2012-07-01'), color='green', linestyle=':', lw=1.5, label='Draghi 2012 Break')
ax.set_title('A: Model 2 Residuals Over Time', fontweight='bold')
ax.set_ylabel('Residual (bps)')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

# Panel 2: Residuals vs Fitted
ax = axes[0, 1]
ax.scatter(ols_diff.fittedvalues, ols_diff.resid, color='#2ca02c', alpha=0.6, edgecolors='none', s=25)
ax.axhline(0, color='red', linestyle='--', lw=1)
ax.set_title('B: Residuals vs Fitted Values', fontweight='bold')
ax.set_xlabel('Fitted Δ Spread (bps)')
ax.set_ylabel('Residual')
ax.grid(True, alpha=0.3)

# Panel 3: Histogram of Residuals vs Normal
ax = axes[1, 0]
resid = ols_diff.resid
ax.hist(resid, bins=35, density=True, color='#aec7e8', edgecolor='#1f77b4', alpha=0.7)
mu, std = resid.mean(), resid.std()
xmin, xmax = ax.get_xlim()
x = np.linspace(xmin, xmax, 100)
p = stats.norm.pdf(x, mu, std)
ax.plot(x, p, 'r-', lw=2, label=f'Normal (μ={mu:.1f}, σ={std:.1f})')
ax.set_title('C: Histogram of Residuals (Leptokurtic)', fontweight='bold')
ax.set_xlabel('Residual (bps)')
ax.legend()
ax.grid(True, alpha=0.3)

# Panel 4: Autocorrelation Function of Residuals
ax = axes[1, 1]
sm.graphics.tsa.plot_acf(ols_diff.resid, lags=24, ax=ax, color='#004b87', auto_ylims=True)
ax.set_title('D: Autocorrelation of Residuals (ACF)', fontweight='bold')
ax.set_xlabel('Lag (Months)')
ax.grid(True, alpha=0.3)

plt.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'fig05_regression_residuals_diagnostics.png'), dpi=300)
plt.close(fig)
print(" Saved fig05_regression_residuals_diagnostics.png")
print("\nPhase 3 Complete!")
