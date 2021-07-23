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
# # EPS analysis

# %% [markdown]
# ## import modules and difine basic modules & functions

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import yahoo_fin.stock_info as si

# private module
import mystock_info as mi

# %%
import importlib
importlib.reload(mi)

# %% [markdown]
# ## Basic usage of mystock_info
#
# `get_earnings_history(tickers, clear_cache=1, verbose=False)`
# arguments:
# - `tickers`: list of tickers or string of a ticker
# - `clear_cache`: number of days cache should be kept

# %%
# test code
df=mi.get_earnings_history("A",verbose=False)
display(df.head(3))
mi.plot_eps(df,last=20,largefig=False)

# %% [markdown]
# ## Get stock info of your favorite

# %% [markdown]
# ### Find Tickers with high EPS beat ratio
#  
# `mi.search_good_eps(tickers, last=20, threshold=80, min_qtrs=4, clear_cache=False, verbose=False)`
#
# arguments:
# - last: number of quarters to be considred
# - min_qtrs: number of quarters required for evaluation
# - threshold: minimum EPS beat ratio in `last` quarters
#
# `mi.show_beat_ratio(df,last=40,threshold=95,min_qtrs=20)`
# - analyze data obtained by mi.search_good_eps()
# - arguments are same as mi.search_good_eps()

# %%
# pd.set_option('display.max_rows', df.shape[0]+1)
tickers_nasdaq = si.tickers_nasdaq()
nas10=mi.search_good_eps(tickers=tickers_nasdaq[0:10],last=20,threshold=90,verbose=False)
mi.show_beat_ratio(nas10,last=40,threshold=95,min_qtrs=20)

# %% [markdown]
# ## analyze tech companies

# %%
fangam=["FB","AAPL","NFLX","GOOG","AMZN","MSFT"]

###
ant=["ADBE","NVDA","TSLA"]
saas=["CRWD","OKTA","ZS","TTD","TWLO"]
ecommerce=["SHOP","ETSY","FIVN"]

fintech=["SQ","DOCU"]
media=["TWTR","PINS"]
techs=["U","ZM","FVRR","ABNB","ROKU"]
eauto=["F","GM","MGA"]

growth1=ant+saas+ecommerce
growth2=fintech+media+techs+eauto

# %%
df_fangam=mi.get_all_data(fangam)
mi.plot_eps(df_fangam[0],last=20)

# growth1
df_growth1=mi.get_all_data(growth1)
mi.plot_eps(df_growth1[0],last=20)

# growth2
df_growth2=mi.get_all_data(growth2)
mi.plot_eps(df_growth2[0],last=20)


df_all=pd.concat([df_fangam[0],df_growth1[0],df_growth2[0]])
display(mi.show_beat_ratio(df_all, last=20))

# all PSR
df_all_psr=pd.concat([df_fangam[1],df_growth1[1],df_growth2[1]])
df_res=mi.plot_financials(df_all_psr, table=True)

# %% [markdown]
# ## FANGAMのみ大きく出してみる

# %%
plot_eps(df_fangam[0],largefig=True)
show_beat_ratio(df_fangam[0], last=200)

# %% [markdown]
# ## Health

# %%
tickers_health=["A","AMGN","ANTM","BMY","BNTX","BIIB","MRNA","PGNY","PFE","RPRX","VEEV"]

# %%
# EPS history
df_health_eps,df_health_fin=mi.get_all_data(tickers_health)
mi.plot_eps(df_health_eps,last=20)
mi.show_beat_ratio(df_health_eps)

df_res=mi.plot_financials(df_health_fin,table=True)
