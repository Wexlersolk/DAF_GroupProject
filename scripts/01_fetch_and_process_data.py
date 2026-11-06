"""
01_fetch_and_process_data.py
Fetches sovereign yields, policy rate, VIX, and macroeconomic series.
Builds the master monthly dataset from 1999 to 2026.
"""

import os
import io
import requests
import numpy as np
import pandas as pd
import yfinance as yf

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

print("--- 1. Fetching 10Y Sovereign Yields from ECB Data Portal ---")
countries = {
    'PT': 'M.PT.L.L40.CI.0000.EUR.N.Z',
    'DE': 'M.DE.L.L40.CI.0000.EUR.N.Z',
    'ES': 'M.ES.L.L40.CI.0000.EUR.N.Z',
    'IT': 'M.IT.L.L40.CI.0000.EUR.N.Z',
    'GR': 'M.GR.L.L40.CI.0000.EUR.N.Z',
    'IE': 'M.IE.L.L40.CI.0000.EUR.N.Z',
}

yields_dict = {}
for c, key in countries.items():
    url = f"https://data-api.ecb.europa.eu/service/data/IRS/{key}?format=csvdata"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    s = df[['TIME_PERIOD', 'OBS_VALUE']].rename(columns={'OBS_VALUE': f'Yield_10Y_{c}'})
    s['TIME_PERIOD'] = pd.to_datetime(s['TIME_PERIOD'], format='%Y-%m')
    s = s.set_index('TIME_PERIOD')
    yields_dict[c] = s

yields_df = pd.concat(yields_dict.values(), axis=1).sort_index()
print(f"Yields fetched: {yields_df.shape}, date range: {yields_df.index.min().strftime('%Y-%m')} to {yields_df.index.max().strftime('%Y-%m')}")

print("\n--- 2. Fetching ECB Deposit Facility Rate ---")
url_dfr = "https://data-api.ecb.europa.eu/service/data/FM/B.U2.EUR.4F.KR.DFR.LEV?format=csvdata"
r_dfr = requests.get(url_dfr, timeout=15)
r_dfr.raise_for_status()
df_dfr_raw = pd.read_csv(io.StringIO(r_dfr.text))
df_dfr_raw['Date'] = pd.to_datetime(df_dfr_raw['TIME_PERIOD'])
df_dfr_raw = df_dfr_raw.sort_values('Date').set_index('Date')[['OBS_VALUE']].rename(columns={'OBS_VALUE': 'ECB_DFR'})

# Create a daily calendar from 1999-01-01 to end of yields, forward-fill DFR, then take monthly average and end-of-month
daily_idx = pd.date_range(start='1999-01-01', end=yields_df.index.max() + pd.offsets.MonthEnd(1), freq='D')
daily_dfr = df_dfr_raw.reindex(df_dfr_raw.index.union(daily_idx)).ffill().reindex(daily_idx)
monthly_dfr = daily_dfr.resample('MS').mean() # Month start frequency matching ECB yields
monthly_dfr.index.name = 'TIME_PERIOD'

print(f"ECB DFR resampled: {monthly_dfr.shape}")

print("\n--- 3. Fetching VIX from Yahoo Finance ---")
vix_raw = yf.download('^VIX', start='1999-01-01', end='2026-11-01', progress=False)
if isinstance(vix_raw.columns, pd.MultiIndex):
    vix_close = vix_raw['Close']['^VIX']
else:
    vix_close = vix_raw['Close']
vix_monthly_mean = vix_close.resample('MS').mean().to_frame(name='VIX')
vix_monthly_end = vix_close.resample('MS').last().to_frame(name='VIX_end')
vix_df = pd.concat([vix_monthly_mean, vix_monthly_end], axis=1)
vix_df.index.name = 'TIME_PERIOD'
print(f"VIX fetched: {vix_df.shape}")

print("\n--- 4. Fetching Eurostat HICP Inflation for Portugal ---")
url_hicp = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_manr?coicop=CP00&geo=PT&unit=RCH_A"
r_hicp = requests.get(url_hicp, timeout=15).json()
time_cats_hicp = list(r_hicp['dimension']['time']['category']['index'].keys())
# In JSON-stat, values are indexed by flat index.
# Since only time dimension varies (geo=PT, coicop=CP00, unit=RCH_A are single), index corresponds to time index.
hicp_dict = {}
for t, idx in r_hicp['dimension']['time']['category']['index'].items():
    if str(idx) in r_hicp['value']:
        hicp_dict[pd.to_datetime(t, format='%Y-%m')] = r_hicp['value'][str(idx)]
hicp_df = pd.DataFrame.from_dict(hicp_dict, orient='index', columns=['HICP_Inflation_PT']).sort_index()
hicp_df.index.name = 'TIME_PERIOD'
print(f"HICP fetched: {hicp_df.shape}, range: {hicp_df.index.min().strftime('%Y-%m')} to {hicp_df.index.max().strftime('%Y-%m')}")

print("\n--- 5. Fetching Eurostat Unemployment Rate for Portugal ---")
url_unemp = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/une_rt_m?geo=PT"
r_un = requests.get(url_unemp, timeout=15).json()
# Dimensions: ['freq', 's_adj', 'age', 'unit', 'sex', 'geo', 'time']
# We want: s_adj='SA', age='TOTAL', unit='PC_ACT', sex='T', geo='PT'
dims = r_un['id']
sizes = r_un['size']
cats = {d: r_un['dimension'][d]['category']['index'] for d in dims}

# Calculate stride multipliers
strides = {}
prod = 1
for d, s in zip(reversed(dims), reversed(sizes)):
    strides[d] = prod
    prod *= s

unemp_dict = {}
for t, t_idx in cats['time'].items():
    flat_idx = (
        cats['freq']['M'] * strides['freq'] +
        cats['s_adj']['SA'] * strides['s_adj'] +
        cats['age']['TOTAL'] * strides['age'] +
        cats['unit']['PC_ACT'] * strides['unit'] +
        cats['sex']['T'] * strides['sex'] +
        cats['geo']['PT'] * strides['geo'] +
        t_idx * strides['time']
    )
    if str(flat_idx) in r_un['value']:
        unemp_dict[pd.to_datetime(t, format='%Y-%m')] = r_un['value'][str(flat_idx)]

unemp_df = pd.DataFrame.from_dict(unemp_dict, orient='index', columns=['Unemp_Rate_PT']).sort_index()
unemp_df.index.name = 'TIME_PERIOD'
print(f"Unemployment fetched: {unemp_df.shape}, range: {unemp_df.index.min().strftime('%Y-%m')} to {unemp_df.index.max().strftime('%Y-%m')}")

print("\n--- 6. Fetching Eurostat Government Debt-to-GDP for Portugal ---")
url_debt = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/gov_10q_ggdebt?geo=PT"
r_debt = requests.get(url_debt, timeout=15).json()
# Dimensions: ['freq', 'na_item', 'sector', 'unit', 'geo', 'time']
# na_item='GD' (gross debt), sector='S13' (general govt), unit='PC_GDP' (% of GDP), geo='PT'
dims_d = r_debt['id']
sizes_d = r_debt['size']
cats_d = {d: r_debt['dimension'][d]['category']['index'] for d in dims_d}

strides_d = {}
prod = 1
for d, s in zip(reversed(dims_d), reversed(sizes_d)):
    strides_d[d] = prod
    prod *= s

debt_dict = {}
for t, t_idx in cats_d['time'].items():
    flat_idx = (
        cats_d['freq']['Q'] * strides_d['freq'] +
        cats_d['na_item']['GD'] * strides_d['na_item'] +
        cats_d['sector']['S13'] * strides_d['sector'] +
        cats_d['unit']['PC_GDP'] * strides_d['unit'] +
        cats_d['geo']['PT'] * strides_d['geo'] +
        t_idx * strides_d['time']
    )
    if str(flat_idx) in r_debt['value']:
        # Format: YYYY-Q1 -> convert to date
        year, q = t.split('-Q')
        month = (int(q) - 1) * 3 + 1
        debt_dict[pd.to_datetime(f"{year}-{month:02d}-01")] = r_debt['value'][str(flat_idx)]

debt_quarterly = pd.DataFrame.from_dict(debt_dict, orient='index', columns=['Debt_to_GDP_PT']).sort_index()
debt_quarterly.index.name = 'TIME_PERIOD'
print(f"Quarterly Debt-to-GDP fetched: {debt_quarterly.shape}, range: {debt_quarterly.index.min().strftime('%Y-%m')} to {debt_quarterly.index.max().strftime('%Y-%m')}")

print("\n--- 7. Merging and Interpolating to Monthly Master Dataset ---")
# Filter all to 1999-01 onwards
start_date = '1999-01-01'
end_date = '2026-09-01'

master = yields_df.loc[start_date:end_date].copy()
master = master.join(monthly_dfr, how='left')
master = master.join(vix_df, how='left')
master = master.join(hicp_df, how='left')
master = master.join(unemp_df, how='left')

# Interpolate quarterly debt to monthly
debt_monthly = debt_quarterly.reindex(master.index)
# Smooth monotonic cubic spline or quadratic / linear interpolation
debt_monthly = debt_monthly.interpolate(method='time').bfill().ffill()
master['Debt_to_GDP_PT'] = debt_monthly['Debt_to_GDP_PT']

# Fill any trailing HICP/Unemp with latest available (ffill)
master['HICP_Inflation_PT'] = master['HICP_Inflation_PT'].ffill()
master['Unemp_Rate_PT'] = master['Unemp_Rate_PT'].ffill()
master['ECB_DFR'] = master['ECB_DFR'].ffill()
master['VIX'] = master['VIX'].ffill()

# Compute Sovereign Spreads over Germany (in percentage points and in basis points)
master['Spread_PT'] = master['Yield_10Y_PT'] - master['Yield_10Y_DE']
master['Spread_ES'] = master['Yield_10Y_ES'] - master['Yield_10Y_DE']
master['Spread_IT'] = master['Yield_10Y_IT'] - master['Yield_10Y_DE']
master['Spread_GR'] = master['Yield_10Y_GR'] - master['Yield_10Y_DE']
master['Spread_IE'] = master['Yield_10Y_IE'] - master['Yield_10Y_DE']

master['Spread_PT_bps'] = master['Spread_PT'] * 100.0
master['Spread_ES_bps'] = master['Spread_ES'] * 100.0
master['Spread_IT_bps'] = master['Spread_IT'] * 100.0
master['Spread_GR_bps'] = master['Spread_GR'] * 100.0
master['Spread_IE_bps'] = master['Spread_IE'] * 100.0

# Compute First Differences (Month-on-Month changes)
master['d_Spread_PT'] = master['Spread_PT'].diff()
master['d_Spread_PT_bps'] = master['Spread_PT_bps'].diff()
master['d_VIX'] = master['VIX'].diff()
master['d_ECB_DFR'] = master['ECB_DFR'].diff()
master['d_HICP_Inflation_PT'] = master['HICP_Inflation_PT'].diff()
master['d_Unemp_Rate_PT'] = master['Unemp_Rate_PT'].diff()
master['d_Debt_to_GDP_PT'] = master['Debt_to_GDP_PT'].diff()

# Regimes definition:
# Regime 1: Convergence (1999-01 to 2007-12)
# Regime 2: GFC & Sovereign Debt Crisis / Troika (2008-01 to 2012-06)
# Regime 3: Post Draghi / QE / Low Rates (2012-07 to 2019-12)
# Regime 4: COVID / Inflation shock / Rate hikes & TPI (2020-01 to 2026-09)
def assign_regime(dt):
    if dt < pd.Timestamp('2008-01-01'):
        return '1_Convergence_1999_2007'
    elif dt < pd.Timestamp('2012-07-01'):
        return '2_Crisis_Troika_2008_2012'
    elif dt < pd.Timestamp('2020-01-01'):
        return '3_Post_Draghi_QE_2012_2019'
    else:
        return '4_Pandemic_TPI_2020_2026'

master['Regime'] = [assign_regime(dt) for dt in master.index]
# Chow Dummy for post-July 2012
master['Post_2012_Dummy'] = (master.index >= pd.Timestamp('2012-07-01')).astype(int)

# Save Master Dataset
out_path = os.path.join(DATA_DIR, 'sovereign_spreads_master.csv')
master.to_csv(out_path)
print(f"\n Master dataset saved to {out_path}")
print(f"Shape: {master.shape}")
print(f"Columns: {list(master.columns)}")
print("\nSample Data (First 3 rows):")
print(master[['Yield_10Y_PT', 'Yield_10Y_DE', 'Spread_PT_bps', 'VIX', 'ECB_DFR', 'HICP_Inflation_PT', 'Unemp_Rate_PT', 'Debt_to_GDP_PT']].head(3))
print("\nSample Data (Last 3 rows):")
print(master[['Yield_10Y_PT', 'Yield_10Y_DE', 'Spread_PT_bps', 'VIX', 'ECB_DFR', 'HICP_Inflation_PT', 'Unemp_Rate_PT', 'Debt_to_GDP_PT']].tail(3))
