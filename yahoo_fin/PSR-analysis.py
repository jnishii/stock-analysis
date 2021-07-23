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
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # PSR analysis

# %% [markdown]
# ## import modules and difine basic modules & functions

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import yahoo_fin.stock_info as si

# private module
import mystock_info as mi

# %% [markdown]
# ## Ticker list of stock indexes
#
# ticker listの取得

# %%
# get ticker list
tickers_dow = si.tickers_dow()
tickers_nasdaq = si.tickers_nasdaq()
tickers_sp500 = si.tickers_sp500()
tickers_other = si.tickers_other()

print(len(tickers_dow))
print(len(tickers_nasdaq))
print(len(tickers_sp500))
print(len(tickers_other))

# %% [markdown]
# ## Get data! It takes a while, so please be patient!
#
# 一度に取得するのはせいぜい40-50個くらいのデータにしないとエラーが出る。
#
# - データはキャッシュされるので，少しずつためるのでもOK。
# - キャッシュ保存日数は引数`clear_cache`で指定。デフォルトは7日

# %%
# get data of stock indexes
df_dow = mi.get_financial_data(tickers=tickers_dow, clear_cache=7)
df_dow_final = mi.plot_financials(df_dow, table=False)

# %%
