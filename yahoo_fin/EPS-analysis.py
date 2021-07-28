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
# ## Get stock info of your favorite

# %% [markdown]
# ### Find Tickers with high EPS beat ratio

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

fintech=["SQ","DOCU", "PYPL"]
media=["TWTR","PINS"]
techs=["U","ZM","FVRR","ABNB","ROKU"]
eauto=["F","GM","MGA"]

growth1=ant+saas+ecommerce
growth2=fintech+media+techs+eauto

# %%
df_eps = pd.DataFrame()
df_psr = pd.DataFrame()

for i in [fangam, growth1, growth2]:
    df = mi.get_all_data(i, table=False)
    mi.plot_eps(df[0], last=20)
    df_eps = df_eps.append(df[0])
    df_psr = df_psr.append(df[1])
    

display(mi.show_beat_ratio(df_eps, last=20))
df_res = mi.plot_financials(df_psr, table=True)

# %% [markdown]
# ## FANGAMのみ大きく出してみる

# %%
mi.plot_eps(df_fangam[0],largefig=True)
mi.show_beat_ratio(df_fangam[0], last=200)

# %% [markdown]
# ## Health

# %%
tickers_health = [
    "A",
    "AMGN",
    "ANTM",
    "BMY",
    "BNTX",
    "BIIB",
    "DHR",
    "MRNA",
    "PGNY",
    "PFE",
    "RPRX",
    "VEEV",
    "INOV"
]

# %%
# EPS history
df_health_eps,df_health_fin=mi.get_all_data(tickers_health)
mi.plot_eps(df_health_eps,last=20)
mi.show_beat_ratio(df_health_eps)

df_res=mi.plot_financials(df_health_fin,table=True)

# %%
