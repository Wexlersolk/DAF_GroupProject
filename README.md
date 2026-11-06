# From Bailout to Backstop: What Drives Portugal’s 10-Year Sovereign Spread over Germany, 1999–2026?

**Course:** Data Analysis in Finance (DAF) | Master in Finance  
**Institution:** ISEG – Lisbon School of Economics & Management, Universidade de Lisboa  
**Group 4:** Karl Grywenz (L67517), Daniel Seratila (66886), Jort Petersen (67605), Danylo Karpenko (l67795), Elias Wetterberg (l67031), Sipan Zeyrek (67789)  
**Discussion Group:** Group 6 | **Presentation Date:** December 18, 2026  

---

## Overview

This repository contains the full empirical research project, econometrics codebase, presentation slide deck, and comprehensive report investigating the macroeconomic, global, and monetary determinants of the Portuguese 10-year sovereign bond yield spread over Germany across four distinct historical regimes (1999–2026).

---

## Core Findings

1. **Unit Roots & Econometric Specification:**
   - Yields and spreads are non-stationary in levels $I(1)$ ($ADF\ p = 0.173$), but stationary in first differences $I(0)$ ($ADF\ p < 0.0001$).
   - OLS in levels is spurious ($R^2 = 0.65, DW = 0.14$). First differences ($\Delta$) is strictly required.
2. **Diagnostic Battery & Newey-West HAC:**
   - Zero multicollinearity (Max $VIF = 1.11$).
   - Heteroskedasticity (White $p = 0.0005$) and autocorrelation (Breusch-Godfrey LM $p < 0.0001$) confirmed $\rightarrow$ **Newey-West HAC standard errors** applied throughout.
3. **Chow Structural Break Test (July 2012):**
   - Breakpoint: Mario Draghi's *"Whatever it takes"* / OMT announcement.
   - $F = 4.982$, $p = 0.000068$ ($p < 0.0001$). Confirms a permanent structural break in European sovereign risk pricing.
4. **Economic Mechanism Shift:**
   - *Pre-2012 (Crisis):* $\Delta Debt/GDP$ was positive and significant ($\beta = \mathbf{+14.38^{**}}$, $p = 0.027$).
   - *Post-2012 (Backstop):* $\Delta Debt/GDP$ collapsed to $\mathbf{-0.825}$ (statistically zero). The ECB backstop severed the sovereign-debt doom loop.
   - *Post-2012 Risk Transfer:* $\Delta VIX$ surged to $\mathbf{+0.951^{***}}$ ($p < 0.001$). Spreads are driven by global market risk appetite, not domestic default fears.
5. **Cointegration & GARCH(1,1) Volatility:**
   - Engle-Granger cointegration test ($p = 0.268$): yields are not cointegrated, proving an Error Correction Model (VECM) is invalid.
   - GARCH(1,1) with Student's $t$ errors ($\alpha = 0.174^{***}, \beta = 0.826^{***}, \nu = 4.56^{***}$) models conditional volatility clustering from crisis peaks ($120$ bps/month) to backstop calm ($< 12$ bps).
6. **Out-of-Sample Forecasting (2025–2026):**
   - Selected model: **ARIMA(2,1,2)** ($AIC = 3,143.66$). Residuals are white noise (Ljung-Box lag 6 $p = 0.65$).
   - Test period ($N = 21$): $RMSE = 7.98$ bps vs Random Walk $10.22$ bps ($Theil's\ U = \mathbf{0.780}$, a **22.0% error reduction**).
7. **The "Portuguese Miracle" / GIIPS Decoupling:**
   - In 2012, Portugal had the second-widest spread in the Eurozone ($1,203$ bps).
   - In 2026, Portugal's spread tightened to **$37.3$ bps**, trading inside Spain ($45.4$ bps) and Italy ($88.9$ bps), reflecting rapid fiscal debt reduction ($137\% \rightarrow 92\%$ of GDP).

---

## Deliverables & Repository Structure

```
├── Portuguese_Sovereign_Spread_1999_2026.pptx   # 20-slide widescreen presentation deck
├── Portuguese_Sovereign_Spread_1999_2026.pdf    # Compiled PDF presentation
├── REPORT.md                                    # Comprehensive written econometric report
├── topic.md                                     # Project topic and initial specification
│
├── data/
│   └── sovereign_spreads_master.csv             # 333 monthly obs (1999-2026), 31 variables
│
├── figures/                                     # 10 publication-quality charts (300 DPI)
│   ├── fig01_yields_and_spread_regimes.png
│   ├── fig02_spread_vs_macro_drivers.png
│   ├── fig03_regime_boxplots.png
│   ├── fig04_correlation_heatmaps.png
│   ├── fig05_regression_residuals_diagnostics.png
│   ├── fig06_ts_decomposition_and_acf.png
│   ├── fig07_arima_forecast_vs_random_walk.png
│   ├── fig08_giips_spreads_comparison.png
│   ├── fig09_giips_rolling_correlations.png
│   └── fig10_garch_conditional_volatility.png
│
├── tables/                                      # 16 econometric tables in CSV and Markdown
│   ├── table01_summary_statistics_full.csv
│   ├── table03_spread_by_regime.csv
│   ├── table06_unit_root_tests.csv
│   ├── table07_regression_models_comparison.csv
│   ├── table08_diagnostics_battery.csv
│   ├── table09_chow_test.csv
│   ├── table10_arima_model_selection.csv
│   ├── table12_forecast_performance_metrics.csv
│   ├── table13_giips_summary_statistics.csv
│   ├── table15_cointegration_tests.csv
│   └── table16_garch_model_results.csv
│
└── scripts/                                     # Reproducible python execution pipeline
    ├── 01_fetch_and_process_data.py
    ├── 02_exploratory_and_regimes.py
    ├── 03_regression_and_diagnostics.py
    ├── 04_arima_and_forecasting.py
    ├── 05_giips_extension.py
    ├── 06_generate_presentation.py
    └── 07_cointegration_and_garch.py
```

---

## How to Reproduce

1. Install dependencies:
   ```bash
   pip install pandas numpy statsmodels scipy matplotlib yfinance requests python-pptx arch
   ```
2. Run data pipeline and econometric scripts:
   ```bash
   python scripts/01_fetch_and_process_data.py
   python scripts/02_exploratory_and_regimes.py
   python scripts/03_regression_and_diagnostics.py
   python scripts/04_arima_and_forecasting.py
   python scripts/05_giips_extension.py
   python scripts/07_cointegration_and_garch.py
   python scripts/06_generate_presentation.py
   ```
