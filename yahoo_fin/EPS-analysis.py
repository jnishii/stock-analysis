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
ret=mi.search_good_eps(tickers_nasdaq[:10],last=40,threshold=95,min_qtrs=20)

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
E12 = ["FB", "AAPL", "GOOG", "AMZN", "MSFT"] #Billions
E11 = ["NFLX", "TSLA","ADBE", "NVDA", "SHOP", "SQ", "ZM"] # over 100 million
E10_5 = ( # Over 50 million
    ["CRWD", "TWLO","TWTR"]
    + [ "DOCU", "ROKU", "ABNB"]
    + ["GM", "F"]
)
E10_1 = ["EPAM","U", "MGA","ZS","OKTA",  "TTD", "ETSY","FIVN", "PINS"] # over 10 million

E9 = ["FVRR","FSLY"] # over 1 million

LIST=E12+E11+E10_5+E10_1+E9
###

# %%
mi.plot_valuation(LIST, table=False,key="Cap")

# %%
df_eps = pd.DataFrame()
df_psr = pd.DataFrame()

#for i in [fangam, growth1, growth2]:
for i in [E12,E11,E10_5,E10_1,E9]:
    
    mi.plot_eps(i)
    
#mi.screening_eps(fangam+growth1+growth2, last=20)
#df_res = mi.plot_valuation(fangam+growth1+growth2, table=True)
mi.screening_eps(LIST, last=20)
df_res = mi.plot_valuation(LIST, table=True)

# %% [markdown]
# ## FANGAMのみ大きく出してみる

# %%
mi.plot_eps(fangam,largefig=True)
mi.search_good_eps(fangam, last=200)

# %% [markdown]
# ## Health

# %%
H_E11 = [
    "PFE",
    "DHR",
    "MRNA",
    "BMY",
    "AMGN",
    "BNTX",
]
H_E10 = [
    "ANTM",
    "VEEV",
    "BIIB",
    "A",
    "RPRX",
]
H_E9 = [
    "INOV",
    "PGNY",
]
health = H_E11 + H_E10 + H_E9

# %%
# EPS history
mi.plot_eps(health,last=20)
#mi.search_good_eps(tickers_health)
df_res=mi.plot_valuation(health,table=True)
df_cap=mi.plot_valuation(health,table=True,hist=False,key="Cap")

# %%
