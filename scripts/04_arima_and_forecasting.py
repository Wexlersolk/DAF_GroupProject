"""
04_arima_and_forecasting.py
Performs Time Series Decomposition, ACF/PACF analysis, ARIMA model grid search (AIC/BIC),
residual diagnostic checks (Ljung-Box), and out-of-sample forecasting benchmarked against a Random Walk.
"""

import os
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

warnings.filterwarnings('ignore')

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
FIG_DIR = os.path.join(os.path.dirname(__file__), '..', 'figures')
TAB_DIR = os.path.join(os.path.dirname(__file__), '..', 'tables')

master = pd.read_csv(os.path.join(DATA_DIR, 'sovereign_spreads_master.csv'), index_col='TIME_PERIOD', parse_dates=True)
spread = master['Spread_PT_bps'].dropna()
d_spread = master['d_Spread_PT_bps'].dropna()

# --- 1. Time Series Decomposition ---
decomp = seasonal_decompose(spread, model='additive', period=12)

# --- 2. ACF / PACF and Identification ---
fig, axes = plt.subplots(3, 2, figsize=(13, 10))

# Decomposition plots
axes[0, 0].plot(decomp.observed, color='#004b87', lw=1.5)
axes[0, 0].set_title('Observed PT Spread (bps)', fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(decomp.trend, color='#d9534f', lw=1.8)
axes[0, 1].set_title('Trend Component', fontweight='bold')
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].plot(decomp.seasonal, color='#2ca02c', lw=1.2)
axes[1, 0].set_title('Seasonal Component (Annual)', fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot(decomp.resid, color='#7f7f7f', lw=1.0)
axes[1, 1].axhline(0, color='red', linestyle='--', lw=0.8)
axes[1, 1].set_title('Residual Component', fontweight='bold')
axes[1, 1].grid(True, alpha=0.3)

# ACF and PACF of First Differenced Spread
sm.graphics.tsa.plot_acf(d_spread, lags=24, ax=axes[2, 0], color='#004b87', auto_ylims=True)
axes[2, 0].set_title('ACF of Δ Spread (Identification)', fontweight='bold')
axes[2, 0].set_xlabel('Lag (Months)')
axes[2, 0].grid(True, alpha=0.3)

sm.graphics.tsa.plot_pacf(d_spread, lags=24, ax=axes[2, 1], color='#004b87', auto_ylims=True, method='ywm')
axes[2, 1].set_title('PACF of Δ Spread (Identification)', fontweight='bold')
axes[2, 1].set_xlabel('Lag (Months)')
axes[2, 1].grid(True, alpha=0.3)

plt.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'fig06_ts_decomposition_and_acf.png'), dpi=300)
plt.close(fig)
print(" Saved fig06_ts_decomposition_and_acf.png")

# --- 3. ARIMA Model Selection Grid Search ---
grid_results = []
p_vals = [0, 1, 2, 3]
d_vals = [1]
q_vals = [0, 1, 2, 3]

for p in p_vals:
    for d in d_vals:
        for q in q_vals:
            if p == 0 and q == 0:
                continue # Random walk case
            try:
                mod = ARIMA(spread, order=(p, d, q)).fit()
                grid_results.append({
                    'Order': f'ARIMA({p},{d},{q})',
                    'p': p, 'd': d, 'q': q,
                    'AIC': mod.aic,
                    'BIC': mod.bic,
                    'HQIC': mod.hqic,
                    'Log_Likelihood': mod.llf
                })
            except Exception as e:
                pass

grid_df = pd.DataFrame(grid_results).sort_values('AIC')
grid_df.to_csv(os.path.join(TAB_DIR, 'table10_arima_model_selection.csv'), index=False)
grid_df.to_markdown(os.path.join(TAB_DIR, 'table10_arima_model_selection.md'), index=False)
print("\n=== Top 5 ARIMA Models by AIC ===")
print(grid_df.head(5).to_string(index=False))

best_order_tuple = (grid_df.iloc[0]['p'], grid_df.iloc[0]['d'], grid_df.iloc[0]['q'])
best_order_name = grid_df.iloc[0]['Order']
print(f"\nBest ARIMA Model selected: {best_order_name}")

best_model = ARIMA(spread, order=best_order_tuple).fit()
print(best_model.summary())

# --- 4. Residual Diagnostics of Best ARIMA ---
lb_test = acorr_ljungbox(best_model.resid, lags=[6, 12, 18, 24], return_df=True)
lb_test.to_csv(os.path.join(TAB_DIR, 'table11_arima_residual_diagnostics.csv'))
lb_test.to_markdown(os.path.join(TAB_DIR, 'table11_arima_residual_diagnostics.md'))
print("\n=== Ljung-Box Test on Best ARIMA Residuals ===")
print(lb_test)

# --- 5. Out-of-Sample Forecasting vs Random Walk ---
# Split sample: Train up to 2024-12, Test 2025-01 to 2026-09 (21 months)
split_date = '2025-01-01'
train = spread.loc[:'2024-12-01']
test = spread.loc[split_date:]
n_forecast = len(test)

print(f"\nForecasting sample split: Train N={len(train)} (up to 2024-12), Test N={n_forecast} (2025-01 to 2026-09)")

# Model 1: Random Walk without Drift (Naive: S_t+h = S_T)
rw_forecast = np.full(n_forecast, train.iloc[-1])

# Model 2: Random Walk with Drift
drift = (train.iloc[-1] - train.iloc[0]) / (len(train) - 1)
rw_drift_forecast = train.iloc[-1] + drift * np.arange(1, n_forecast + 1)

# Model 3: Best ARIMA fitted on Train
arima_train_model = ARIMA(train, order=best_order_tuple).fit()
arima_forecast_res = arima_train_model.get_forecast(steps=n_forecast)
arima_forecast = arima_forecast_res.predicted_mean
arima_ci = arima_forecast_res.conf_int(alpha=0.05)

# Model 4: Parsimonious ARIMA(0,1,1) / Exponential Smoothing
arima011_train = ARIMA(train, order=(0, 1, 1)).fit()
arima011_forecast = arima011_train.forecast(steps=n_forecast)

# Compute forecast evaluation metrics
def calc_metrics(actual, pred):
    actual = np.array(actual)
    pred = np.array(pred)
    mae = np.mean(np.abs(actual - pred))
    rmse = np.sqrt(np.mean((actual - pred)**2))
    mape = np.mean(np.abs((actual - pred) / actual)) * 100
    return mae, rmse, mape

mae_rw, rmse_rw, mape_rw = calc_metrics(test, rw_forecast)
mae_rwd, rmse_rwd, mape_rwd = calc_metrics(test, rw_drift_forecast)
mae_arima, rmse_arima, mape_arima = calc_metrics(test, arima_forecast)
mae_011, rmse_011, mape_011 = calc_metrics(test, arima011_forecast)

# Theil's U statistic (RMSE relative to naive random walk)
u_arima = rmse_arima / rmse_rw
u_011 = rmse_011 / rmse_rw
u_rwd = rmse_rwd / rmse_rw

forecast_metrics_df = pd.DataFrame([
    {'Model': 'Naive Random Walk (S_t+h = S_T)', 'MAE (bps)': mae_rw, 'RMSE (bps)': rmse_rw, 'MAPE (%)': mape_rw, "Theil's U": 1.000},
    {'Model': 'Random Walk with Drift', 'MAE (bps)': mae_rwd, 'RMSE (bps)': rmse_rwd, 'MAPE (%)': mape_rwd, "Theil's U": u_rwd},
    {'Model': f'Best {best_order_name}', 'MAE (bps)': mae_arima, 'RMSE (bps)': rmse_arima, 'MAPE (%)': mape_arima, "Theil's U": u_arima},
    {'Model': 'ARIMA(0,1,1) Moving Average', 'MAE (bps)': mae_011, 'RMSE (bps)': rmse_011, 'MAPE (%)': mape_011, "Theil's U": u_011}
])

forecast_metrics_df.to_csv(os.path.join(TAB_DIR, 'table12_forecast_performance_metrics.csv'), index=False)
forecast_metrics_df.to_markdown(os.path.join(TAB_DIR, 'table12_forecast_performance_metrics.md'), index=False)
print("\n=== Out-of-Sample Forecast Evaluation (2025–2026) ===")
print(forecast_metrics_df.to_string(index=False))

# --- 6. Forecast Plot ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8.5), gridspec_kw={'height_ratios': [1.3, 1]})

# Panel 1: Full context with zoom box
ax1.plot(train.index, train, color='#004b87', lw=1.5, label='In-Sample History (1999–2024)')
ax1.plot(test.index, test, color='#2ca02c', lw=2.2, label='Actual Out-of-Sample (2025–2026)')
ax1.plot(test.index, arima_forecast, color='#d9534f', lw=2.0, linestyle='--', label=f'{best_order_name} Forecast')
ax1.fill_between(test.index, arima_ci.iloc[:, 0], arima_ci.iloc[:, 1], color='#d9534f', alpha=0.18, label='95% Confidence Interval')
ax1.plot(test.index, rw_forecast, color='#ff7f0e', lw=1.8, linestyle=':', label='Naive Random Walk')
ax1.axvline(pd.Timestamp(split_date), color='black', linestyle='-.', lw=1.2, label='Forecast Origin (2025-01)')
ax1.set_title('A: Out-of-Sample Sovereign Spread Forecast vs Historical Context (1999–2026)', fontweight='bold')
ax1.set_ylabel('Spread (bps)', fontweight='bold')
ax1.legend(loc='upper right', framealpha=0.9)
ax1.grid(True, alpha=0.3)
ax1.xaxis.set_major_locator(mdates.YearLocator(4))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# Panel 2: Zoomed-in Evaluation Period (2023 to 2026)
zoom_start = '2023-01-01'
ax2.plot(train.loc[zoom_start:].index, train.loc[zoom_start:], color='#004b87', lw=1.8, label='In-Sample')
ax2.plot(test.index, test, color='#2ca02c', marker='o', markersize=4, lw=2.2, label='Actual Test Spread')
ax2.plot(test.index, arima_forecast, color='#d9534f', marker='s', markersize=4, lw=2.0, linestyle='--', label=f'{best_order_name}')
ax2.fill_between(test.index, arima_ci.iloc[:, 0], arima_ci.iloc[:, 1], color='#d9534f', alpha=0.2, label='95% CI')
ax2.plot(test.index, rw_forecast, color='#ff7f0e', lw=1.8, linestyle=':', label='Random Walk')
ax2.axvline(pd.Timestamp(split_date), color='black', linestyle='-.', lw=1.2)
ax2.set_title('B: Zoomed Out-of-Sample Performance Comparison (2025–2026)', fontweight='bold')
ax2.set_ylabel('Spread (bps)', fontweight='bold')
ax2.set_xlabel('Month', fontweight='bold')
ax2.legend(loc='lower left', framealpha=0.9)
ax2.grid(True, alpha=0.3)
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.tight_layout()
fig.savefig(os.path.join(FIG_DIR, 'fig07_arima_forecast_vs_random_walk.png'), dpi=300)
plt.close(fig)
print(" Saved fig07_arima_forecast_vs_random_walk.png")
print("\nPhase 4 Complete!")
