# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Tutorial

# %% [markdown]
# ## Initialize

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import yahoo_fin.stock_info as si

# private module to use yahoo_fin
import mystock_info as mi

##
import importlib
importlib.reload(mi)

# %% [markdown]
# ## Overview
#
# This module calls yahoo_fin functions and returns the results by a dataframe. 
#
# **Remarks:** **The downloaded data is cached,** and automatically loaded from the cache if you have new one. The cache is valid for 24 hours in default, but you can change it.
#
# ### Download and plot EPS history
#
# - `get_earnings_history()`
# - `search_good_eps()`
#
# ### Find tickers with high EPS beat ratio
#
# - `search_good_eps()`
# - `show_beat_ratio()`
#
# ### Download and plot financial data
#
# - `get_financial_data()`
# - `plot_financials()`
#
# ### In a nut shell
#
# - `get_all_data(tickers, last=20, table=True)`

# %% [markdown]
# ## Download and plot EPS history
#
# ###  plot_eps(tickers, clear_cache=1, last=20, largefig=False, verbose=False)
# - This function plots EPS history.
# - It calls `get_earnings_history()` (see below) inside the function and returns the obtained dataframe.
# - arguments:
#     - `tickers`: list of tickers (list) or a ticker name (string)
#     - `clear_cache`: number of days cache should be kept
#
# ### screening_eps(tickers, last=20, threshold=80, min_qtrs=4, clear_cache=False, verbose=False)
#
# - You can find good tickers based on the EPS beat ratio 
# - get EPS history data for `tickers` and shows tickers with EPS beat ratio >= `threshold` within `last` quarters and with at least `min_qtrs` EPS data.
# - return value:
#     - combined dataframe of get_earnings_history() for all `tickers`, i.e.,
#     ```
#     for i in tickers:
#         tmp=get_earnings_history(i)
#         df=df.append(tmp)
#     ``` 
# - arguments:
#     - `last`: number of quarters to be considred
#     - `min_qtrs`: number of quarters required for evaluation
#     - `clear_cache`: number of days of preserving cache. Set False if you want to use cache despite the creation date.
#     - `threshold`: minimum EPS beat ratio in `last` quarters
#
# ### get_earnings_history(tickers, clear_cache=1, verbose=False)
#
# - This function download EPS history data and returns the dataframe.
# - Usually you don't need to call this function by yourself.
# - front end of [yahoo_fin.stock_info.get_earnings_history()](http://theautomatic.net/yahoo_fin-documentation/#get_earnings_history) 
# - arguments:
#     - `tickers`: list of tickers or string of a ticker
#     - `clear_cache`: number of days cache should be kept    

# %%
gafam=["GOOG","FB","AAPL","AMZN","MS"]

mi.plot_eps(gafam,last=20,largefig=False)
ret=mi.screening_eps(gafam,threshold=False)
ret=mi.screening_eps(gafam, last=20, threshold=80, min_qtrs=4)

# %% [markdown]
# If you prefer larger graphs, set the argument `largefig=True` in `plot_eps()`.

# %%
mi.plot_eps("AAPL",largefig=True)

# %% [markdown]
# ## Download and plot financial data
#
# You can get financial data including PSR, PBR, and PER using `get_financial_data()` and can plot the distribution of PSRs using `plot_financials()`.
#
# ### plot_financials(df, hist=True, table=True, key="PSR"):
# - Plot histogram of PSR(default) distribution and print the PSR ranking.
# - This function calls `get_financial_data()` (see below) inside the function and retunrs the obtained dataframe.
# - Sorting key can be 
#     - "PSR" : Price to Sales Ratio
#     - "PBR" : Price Book-value Ratio
#     - "PER" : Price Earning Ratio
#     - "EPS" : Earning Per Share
#     - "Cap" : Market Cap --- Currently sorting doesn't work
# - return value:
#     - dataframe sorted by the given key
# - arguments:
#     - `tickers`: list of tickers (list) or a ticker name (string)
#    
# ### get_financial_data(tickers, clear_cache=7, verbose=False)
# - download financial data including PSR, PBR, Pand ER using [`yahoo_fin.stock_info.get_quote_table()`](http://theautomatic.net/yahoo_fin-documentation/#get_quote_table) and [`yahoo_fin.stock_info.get_stats_valuation()`](http://theautomatic.net/yahoo_fin-documentation/#get_stats_valuation), and returns the combined dataframe.
# - Usually you don't need to call this function explicitly.
# - return value:
#     - dataframe of the financial data of `tickers`
#     

# %%
df_psr_sorted = mi.plot_financials(tickers_dow, hist=True, table=True)

# %% [markdown]
# # Download and plot revenue data

# %% [markdown]
# ## def plot_revenue(tickers, clear_cache=7, verbose=False):
#
# - Plot revenue data 
# - This function get revenue data using `si.get_earnings()` (see below) and returns it in dict format.
#
#
# ## def get_revenue(tickers, clear_cache=7, verbose=False):
#
# - get revenue data using `si.get_earnings()` and returns it in dict format.
# return value:
# - dict of which keys are 'quarterly_results', 'yearly_revenue_earnings', and  'quarterly_revenue_earnings' and values are dataframe for `tickers`.

# %%
ret=mi.plot_revenue(gafam)

# %% [markdown]
# ## In a nut shell
#
# **Attention: Under construction from here**
#
# You can get both of EPS history and financial data by `mi.get_all_data()`.
#
# ### get_all_data(tickers, last=20, table=True)
# - run the following
#     1. download EPS history (`get_earnings_history()`))
#     2. download financial data (`get_financial_data()`)
#     3. shows the EPS beat ratios in 'last' quarters (`show_beat_ratio()`)
# - arguments:
#     - `tickers`: list of tickers 
#     - `last=20`: number of quarters to be considred to get EPS beat ratio
#     - `table=False`: show the table of EPS beat ratio or not
# - return value: tuple of return values of get_earnings_history() and get_financial_data()

# %%
df_all=mi.get_all_data(gafam, table=False)
mi.plot_eps(df_all[0],last=20) # show EPS history within last 20 quarters
mi.plot_financials(df_all[1])

# %%
