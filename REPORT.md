# From Bailout to Backstop: What Drives Portugal’s 10-Year Sovereign Spread over Germany, 1999–2026?

**Course:** Data Analysis in Finance (DAF) | Master in Finance  
**Institution:** ISEG – Lisbon School of Economics & Management, Universidade de Lisboa  
**Group 4:** Karl Grywenz (L67517), Daniel Seratila (66886), Jort Petersen (67605), Danylo Karpenko (l67795), Elias Wetterberg (l67031), Sipan Zeyrek (67789)  
**Discussion Group:** Group 6 | **Presentation Date:** December 18, 2026  

---

## 1. Executive Summary & Research Question

Over the past 27 years (1999–2026), Portuguese government bond yields underwent extreme historical regimes:
1. **EMU Convergence (1999–2007):** Spread compressed to under 20 bps as markets priced periphery debt as virtually risk-free.
2. **The Sovereign Debt Crisis & Troika Bailout (2008–2012):** Global financial contagion and domestic fiscal deterioration drove spreads to an unprecedented peak of **1,203 bps** in January 2012, requiring a €78 billion EU/IMF/ECB bailout package.
3. **The ECB Backstop & Quantitative Easing (2012–2019):** Mario Draghi’s July 2012 *"Whatever it takes"* speech and subsequent Outright Monetary Transactions (OMT) and Public Sector Purchase Programme (PSPP) dismantled the redenomination risk premium.
4. **Pandemic Shock, Tightening Cycle & TPI (2020–2026):** Backstopped by the PEPP and the Transmission Protection Instrument (TPI), Portugal decoupled from fellow periphery borrowers, navigating 450 bps of ECB rate hikes with spreads narrowing to **37 bps** in 2026.

### Core Research Questions
1. **Macro & Monetary Drivers:** Which global risk factors ($VIX$), monetary policy stances ($ECB\_DFR$), and domestic macro/fiscal fundamentals ($Debt/GDP$, $HICP$, $Unemployment$) govern month-to-month changes in Portuguese sovereign spreads?
2. **Structural Break:** Did the institutional architecture shift under Mario Draghi in July 2012, severing the feedback loop between domestic debt accumulation and sovereign yield spreads?
3. **Forecasting Power:** Can an identified ARIMA specification outperform a naive Random Walk in out-of-sample spread forecasting?
4. **Cross-Country Decoupling:** How does Portugal’s sovereign spread trajectory compare against Spain, Italy, Greece, and Ireland?

---

## 2. Data & Empirical Sample

The master dataset spans **333 monthly observations** from **January 1999 to September 2026**:
- **10-Year Benchmark Sovereign Yields:** Portugal, Germany, Spain, Italy, Greece, Ireland (ECB Data Portal, `IRS.M.<Country>.L.L40.CI.0000.EUR.N.Z`).
- **Dependent Variable ($Spread_t$):** Portugal 10-year yield spread over Germany in basis points:  
  $$Spread_t = (Y_{PT,t} - Y_{DE,t}) \times 100$$
- **Global Risk Aversion ($VIX_t$):** Monthly average CBOE Volatility Index (FRED / Yahoo Finance `^VIX`).
- **ECB Monetary Policy Stance ($ECB\_DFR_t$):** ECB Deposit Facility Rate (ECB Data Portal `FM.B.U2.EUR.4F.KR.DFR.LEV`), daily calendar resampled to monthly mean.
- **Domestic Macro & Fiscal Indicators:**
  - **HICP Inflation ($HICP_t$):** Harmonized Index of Consumer Prices, annual rate of change (% YoY), Eurostat (`prc_hicp_manr`).
  - **Unemployment Rate ($Unemp_t$):** Harmonized unemployment rate, seasonally adjusted (% of active population), Eurostat (`une_rt_m`).
  - **Debt-to-GDP Ratio ($Debt_t$):** General government consolidated gross debt (% of GDP, Maastricht definition), Eurostat (`gov_10q_ggdebt`), interpolated monthly.

---

## 3. Summary Statistics & Distributional Properties

### Table 1: Full Sample Descriptive Statistics (1999–2026, N = 333)

| Variable | Mean | Std Dev | Median | Min | Max | Skewness | Kurtosis | Jarque-Bera p-val |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **PT-DE Spread (bps)** | 162.35 | 228.44 | 70.10 | -0.40 | 1,202.90 | 2.71 | 10.42 | < 0.0001 |
| **PT 10Y Yield (%)** | 4.02 | 2.40 | 3.86 | 0.03 | 13.85 | 1.34 | 5.37 | < 0.0001 |
| **DE 10Y Yield (%)** | 2.40 | 1.77 | 2.55 | -0.65 | 5.54 | -0.04 | 1.83 | < 0.0001 |
| **VIX Index** | 19.96 | 7.79 | 18.02 | 10.13 | 62.64 | 2.21 | 10.15 | < 0.0001 |
| **ECB Deposit Rate (%)** | 1.10 | 1.42 | 1.00 | -0.50 | 4.00 | 0.36 | 1.95 | < 0.0001 |
| **PT HICP Inflation (% YoY)** | 2.20 | 1.99 | 2.30 | -1.80 | 10.60 | 1.18 | 5.61 | < 0.0001 |
| **PT Unemployment Rate (%)** | 9.11 | 3.43 | 8.10 | 5.00 | 18.40 | 0.81 | 2.91 | < 0.0001 |
| **PT Debt-to-GDP (%)** | 97.38 | 28.46 | 96.90 | 54.00 | 137.50 | -0.21 | 1.48 | < 0.0001 |

### Table 2: Portuguese Sovereign Spread (bps) Across Historical Regimes

| Regime | Period | N | Mean (bps) | Std Dev (bps) | Median (bps) | Max (bps) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. EMU Convergence** | 1999-01 – 2007-12 | 108 | **20.70** | 10.66 | 18.30 | 43.50 |
| **2. Crisis & Troika Bailout** | 2008-01 – 2012-06 | 54 | **381.00** | 385.81 | 168.65 | 1,202.90 |
| **3. Post-Draghi QE** | 2012-07 – 2019-12 | 90 | **282.95** | 172.53 | 234.45 | 925.20 |
| **4. Pandemic & TPI** | 2020-01 – 2026-09 | 81 | **71.46** | 24.70 | 69.60 | 141.80 |

---

## 4. Stationarity Analysis: Unit Root Tests

### Table 3: Augmented Dickey-Fuller (ADF) & KPSS Tests

| Variable | ADF Stat (Level) | ADF p-val (Level) | Level Order | ADF Stat ($\Delta$ Diff) | ADF p-val ($\Delta$ Diff) | Difference Order |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Spread (bps)** | -2.30 | 0.173 | **I(1)** | -5.19 | **< 0.0001** | **I(0)** |
| **VIX** | -4.72 | < 0.001 | **I(0)** | -11.52 | **< 0.0001** | **I(0)** |
| **ECB Rate** | -2.23 | 0.194 | **I(1)** | -5.53 | **< 0.0001** | **I(0)** |
| **Inflation** | -2.78 | 0.061 | **I(1)** | -6.89 | **< 0.0001** | **I(0)** |
| **Unemployment** | -1.59 | 0.486 | **I(1)** | -3.79 | **0.003** | **I(0)** |
| **Debt-to-GDP** | -1.77 | 0.397 | **I(1)** | -2.75 | **0.065** | **I(0)** |

> [!IMPORTANT]
> **Econometric Justification for Differencing:** In levels, the spread and domestic macro drivers fail to reject the unit root null. Estimating in levels leads to spurious correlation ($R^2 = 0.645$, but Durbin-Watson is an alarming $0.14$). Differencing resolves unit roots across all series, warranting estimation in first differences ($\Delta$).

---

## 5. Econometric Regression Results & Diagnostic Battery

### Table 4: Regression Models Comparison

$$\Delta Spread_t = \beta_0 + \beta_1 \Delta VIX_t + \beta_2 \Delta ECB\_DFR_t + \beta_3 \Delta Inflation_t + \beta_4 \Delta Unemployment_t + \beta_5 \Delta DebtGDP_t + \varepsilon_t$$

| Regressor | (1) Levels OLS | (2) Diff OLS | (3) Diff HAC | (4) Pre-2012 HAC | (5) Post-2012 HAC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Constant** | -643.22*** (55.50) | -0.515 (1.61) | -0.515 (1.95) | 0.407 (1.75) | **-6.302\*\*** (2.86) |
| **$\Delta$ VIX** | 3.509*** (1.00) | 0.459 (0.37) | 0.459 (0.31) | -0.149 (0.53) | **+0.951\*\*\*** (0.23) |
| **$\Delta$ ECB Rate** | 2.263 (8.07) | 1.373 (12.37) | 1.373 (14.30) | 9.742 (16.33) | 7.422 (7.89) |
| **$\Delta$ Inflation** | 29.855*** (4.29) | 3.385 (3.36) | 3.385 (3.19) | -2.249 (4.55) | 5.098 (3.66) |
| **$\Delta$ Unemployment** | 46.753*** (2.58) | -6.628 (7.39) | -6.628 (10.05) | -12.519 (21.35) | -14.572 (9.35) |
| **$\Delta$ Debt-to-GDP** | 2.478*** (0.40) | 5.357*** (1.78) | 5.357 (3.53) | **+14.376\*\*** (6.52) | **-0.825** (2.08) |
| **Observations** | 333 | 332 | 332 | 161 | 171 |
| **$R^2$** | 0.645 | 0.036 | 0.036 | 0.103 | 0.066 |
| **Standard Errors** | Non-robust | Non-robust | Newey-West (4) | Newey-West (4) | Newey-West (4) |

*Note: Standard errors in parentheses. \*\*\* p < 0.01, \*\* p < 0.05, \* p < 0.1.*

### Table 5: Econometric Diagnostic Battery (Model 2 Residuals)

| Diagnostic Test | Test Statistic | p-value | Null Hypothesis ($H_0$) | Empirical Decision |
| :--- | :---: | :---: | :---: | :---: |
| **Variance Inflation Factor (Max VIF)** | 1.106 | — | VIF < 5 (No Collinearity) | **Pass: No multicollinearity** |
| **Breusch-Pagan Test** | 24.899 | 0.0001 | Homoskedasticity | **Reject $H_0$: Heteroskedasticity** |
| **White Test** | 47.242 | 0.0005 | Homoskedasticity | **Reject $H_0$: Heteroskedasticity** |
| **Durbin-Watson** | 1.640 | — | No First-Order Autocorrelation | **Mild positive autocorrelation** |
| **Breusch-Godfrey LM (lag 4)** | 47.664 | < 0.0001 | No Serial Correlation | **Reject $H_0$: Autocorrelation** |
| **Jarque-Bera Test** | 898.04 | < 0.0001 | Normal Residuals | **Reject $H_0$: Heavy tails / Leptokurtic** |

> [!NOTE]
> **Need for Newey-West HAC Standard Errors:** Because the model exhibits both conditional heteroskedasticity (White p < 0.001) and serial correlation (Breusch-Godfrey p < 0.001), standard OLS standard errors underestimate variance. All statistical tests are evaluated under **Newey-West HAC covariance matrices** (maxlags = 4).

---

## 6. Structural Break: The Chow Test at July 2012

To evaluate whether Mario Draghi’s July 26, 2012 *"Whatever it takes"* announcement altered the sovereign pricing mechanism, a Chow structural break test was conducted:

$$F = \frac{(SSR_{pooled} - (SSR_1 + SSR_2)) / k}{(SSR_1 + SSR_2) / (N_1 + N_2 - 2k)}$$

### Table 6: Chow Test Results

| Breakpoint | $N_1$ (Pre) | $N_2$ (Post) | $SSR_{pooled}$ | $SSR_{unrestricted}$ | Chow $F$-Stat | p-value | Decision |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **July 2012** | 161 | 171 | 863,229.4 | 790,622.7 | **4.982** | **0.000068** | **Reject $H_0$ (p < 0.0001)** |

### Economic Interpretation of the Break:
1. **Pre-2012 (Crisis Regime):** $\Delta Debt/GDP$ was positive and statistically significant (**+14.38 bps per 1 pp increase in debt**, p = 0.027). When sovereign default and redenomination risk dominated, fiscal deterioration was penalized with widened spreads.
2. **Post-2012 (Backstop Regime):** $\Delta Debt/GDP$ coefficient collapsed to **-0.825 (statistically insignificant)**. The ECB backstop severed the sovereign-debt spiral. Simultaneously, $\Delta VIX$ became highly significant (**+0.951 bps per 1 point VIX increase**, p < 0.001). Under the central bank backstop, Portuguese sovereign debt spreads transitioned from pricing idiosyncratic default risk to tracking global market liquidity and risk appetite.

---

## 7. Time Series Modeling & Out-of-Sample Forecasting

### Model Identification & Selection
Grid search across $(p, 1, q)$ with $p, q \in [0, 3]$ identified **ARIMA(2,1,2)** as the superior model:
- **AIC:** 3,143.66 (Lowest) | **BIC:** 3,162.68 | **Log-Likelihood:** -1,566.83
- **Parameters:**
  - $\phi_1 = 1.572$ (z = 16.41, p < 0.001)
  - $\phi_2 = -0.680$ (z = -7.94, p < 0.001)
  - $\theta_1 = -1.482$ (z = -17.91, p < 0.001)
  - $\theta_2 = 0.700$ (z = 12.20, p < 0.001)
- **Residual White Noise (Ljung-Box):** Lag 6 Q-stat = 4.20 ($p = 0.650$), confirming residuals are white noise at short forecast horizons.

### Out-of-Sample Forecast Evaluation (2025–2026, N = 21 Months)
The sample was partitioned into **In-Sample Estimation** (1999-01 to 2024-12, N = 312) and **Out-of-Sample Forecast** (2025-01 to 2026-09, N = 21).

### Table 7: Out-of-Sample Forecast Performance Metrics

| Forecasting Model | MAE (bps) | RMSE (bps) | MAPE (%) | Theil's U Statistic |
| :--- | :---: | :---: | :---: | :---: |
| **Naive Random Walk ($S_{t+h} = S_T$)** | 8.91 | 10.22 | 22.63% | 1.000 |
| **Random Walk with Drift** | 9.87 | 11.34 | 25.15% | 1.110 |
| **Best ARIMA(2,1,2)** | **6.86** | **7.98** | **16.45%** | **0.780** |
| **ARIMA(0,1,1) (Exponential Smoothing)** | 9.12 | 10.46 | 23.20% | 1.023 |

> [!TIP]
> **Forecasting Performance:** The ARIMA(2,1,2) model outperforms the Random Walk benchmark, achieving a **22.0% reduction in RMSE** (Theil’s U = 0.780) and reducing MAPE from 22.6% to 16.5%.

---

## 8. Cross-Country Periphery Extension: The GIIPS Decoupling

### Table 8: GIIPS Sovereign Spreads over Germany (1999–2026)

| Country | Full Sample Mean | Crisis Max (2011–12) | Post-2020 Mean | Latest (2026) |
| :--- | :---: | :---: | :---: | :---: |
| **Portugal** | **162.4 bps** | **1,202.9 bps** | **71.5 bps** | **37.3 bps** |
| **Spain** | 96.7 bps | 555.4 bps | 81.0 bps | 45.4 bps |
| **Italy** | 126.9 bps | 518.7 bps | 143.4 bps | 88.9 bps |
| **Greece** | 363.3 bps | 2,739.0 bps | 137.5 bps | 74.7 bps |
| **Ireland** | 98.9 bps | 971.0 bps | 41.0 bps | 11.8 bps |

### The "Portuguese Miracle"
- **Crisis Peak:** Portugal was the second-hardest hit sovereign borrower in the Eurozone (spread > 1,200 bps).
- **Modern Decoupling:** By 2026, Portugal's spread (37.3 bps) compressed **inside Spain (45.4 bps)** and **less than half of Italy (88.9 bps)**.
- **Economic Explanation:** While Italian debt remained elevated above 135% of GDP with persistent fiscal deficits, Portugal executed disciplined primary budget surpluses, bringing public debt down from 137.5% toward 92% of GDP. Credible domestic consolidation allowed Portugal to extract the full protection of ECB backstops.

---

## 9. Deliverables Inventory

| Artifact / Deliverable | File Path | Description |
| :--- | :--- | :--- |
| **Presentation Deck (PPTX)** | [Portuguese_Sovereign_Spread_1999_2026.pptx](file:///home/wexlersolk/Notes/10-Courses/DAF/DAF_Project/Portuguese_Sovereign_Spread_1999_2026.pptx) | 19-slide widescreen (16:9) master's presentation deck |
| **Presentation Deck (PDF)** | [Portuguese_Sovereign_Spread_1999_2026.pdf](file:///home/wexlersolk/Notes/10-Courses/DAF/DAF_Project/Portuguese_Sovereign_Spread_1999_2026.pdf) | Compiled PDF version of presentation |
| **Master Dataset** | [sovereign_spreads_master.csv](file:///home/wexlersolk/Notes/10-Courses/DAF/DAF_Project/data/sovereign_spreads_master.csv) | 333 monthly observations (1999–2026), 31 variables |
| **Figure 1: Yields & Regimes** | [fig01_yields_and_spread_regimes.png](file:///home/wexlersolk/Notes/10-Courses/DAF/DAF_Project/figures/fig01_yields_and_spread_regimes.png) | 10Y PT vs DE yield and spread evolution across regimes |
| **Figure 2: Macro Drivers** | [fig02_spread_vs_macro_drivers.png](file:///home/wexlersolk/Notes/10-Courses/DAF/DAF_Project/figures/fig02_spread_vs_macro_drivers.png) | 4-panel spread vs VIX, ECB rate, Debt/GDP, unemployment |
| **Figure 3: Regime Boxplots** | [fig03_regime_boxplots.png](file:///home/wexlersolk/Notes/10-Courses/DAF/DAF_Project/figures/fig03_regime_boxplots.png) | Spread distributions across 4 policy regimes |
| **Figure 4: Correlation Heatmaps**| [fig04_correlation_heatmaps.png](file:///home/wexlersolk/Notes/10-Courses/DAF/DAF_Project/figures/fig04_correlation_heatmaps.png) | Levels vs first differences correlation matrices |
| **Figure 5: Residual Diagnostics**| [fig05_regression_residuals_diagnostics.png](file:///home/wexlersolk/Notes/10-Courses/DAF/DAF_Project/figures/fig05_regression_residuals_diagnostics.png) | Time series, fitted vs residual, histogram, and residual ACF |
| **Figure 6: Decomposition & ACF**| [fig06_ts_decomposition_and_acf.png](file:///home/wexlersolk/Notes/10-Courses/DAF/DAF_Project/figures/fig06_ts_decomposition_and_acf.png) | Additive decomposition and identification ACF/PACF |
| **Figure 7: Forecast vs Random Walk**| [fig07_arima_forecast_vs_random_walk.png](file:///home/wexlersolk/Notes/10-Courses/DAF/DAF_Project/figures/fig07_arima_forecast_vs_random_walk.png) | Out-of-sample forecast with 95% confidence intervals |
| **Figure 8: GIIPS Spreads** | [fig08_giips_spreads_comparison.png](file:///home/wexlersolk/Notes/10-Courses/DAF/DAF_Project/figures/fig08_giips_spreads_comparison.png) | Comparative spreads across Portugal, Spain, Italy, Greece, Ireland |
| **Figure 9: Rolling Correlations**| [fig09_giips_rolling_correlations.png](file:///home/wexlersolk/Notes/10-Courses/DAF/DAF_Project/figures/fig09_giips_rolling_correlations.png) | 36-month rolling correlation with Portugal spread |
| **Tables Inventory (14 CSVs)** | [tables/](file:///home/wexlersolk/Notes/10-Courses/DAF/DAF_Project/tables/) | Full econometric output tables (CSV and Markdown) |
| **Scripts Inventory (6 files)** | [scripts/](file:///home/wexlersolk/Notes/10-Courses/DAF/DAF_Project/scripts/) | Reproducible data pipeline, regression, ARIMA, PPTX scripts |
