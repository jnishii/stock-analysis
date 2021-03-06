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
# ## Tech companies

# %%
fangam=["FB","AAPL","NFLX","GOOG","AMZN","MSFT"]

###
ant=["ADBE","NVDA","TSLA"]
saas=["CRWD","OKTA","TTD","TWLO"]
ecommerce=["SHOP","ETSY","FIVN"]

fintech=["SQ","DOCU", "PYPL"]
media=["TWTR","PINS"]
techs=["U","ZM","FVRR","ABNB","ROKU"]
eauto=["F","GM"]

jicchama=["DOCS","UPST","DLO","SNOW","PLTR","DDOG","COUR","ABNB","LAW"]

growth1=ant+saas+ecommerce
growth2=fintech+media+techs+eauto

# %%
E12 = ["AAPL", "GOOG", "AMZN", "MSFT"] # Trillion
E11 = ["TSLA", "NVDA", "FB","NFLX", "ADBE","PYPL"] # over 100 Billion
E10_5 = ["SHOP","ABNB","SQ", "SNOW"]  #, "GM", "F"  # Over 50 Billion
E10_1 = ["DDOG","ZM", "VEEV", "PLTR","TWTR", "TTD","U", "MGA","ROKU", "OKTA", "EPAM",
         "ETSY","PINS","MDB", "HUBS"] + ["CRWD", "TWLO", "DOCU" ,"LCID"]
# over 10 Billion

E9 = ["FIVN",  "MQ", "FVRR","COUR","LAW","SPT", "ONON","UPST"] # Under 1 Billion

#NODATA=["DLO"]

LIST=E12+E11+E10_5+E10_1+E9
SLIST=E11+E10_5+E10_1+E9

###
#TMP = ["VEEV", "PLTR","TWTR", "TTD","U"]
# TMP=["MGA","ROKU", "OKTA", "EPAM"]
# TMP=["ETSY","PINS","UPST","MDB", "HUBS"] 
# TMP=["CRWD", "TWLO", "DOCU" ]#,"LCID"]
#mi.show_valuation(TMP, hist=False, table=True, key="PSR")    

# %%
#sorted(LIST)

# %% [markdown]
# ### PSR distribution and Market Cap

# %%
import importlib

importlib.reload(mi)
df=mi.show_valuation(LIST, table=False, key="Cap")

# %%
df["Market Cap"].sort_values(ascending=False)

# %% [markdown]
# ### EPS history

# %%
import importlib
importlib.reload(mi)

#for i in [fangam, growth1, growth2]:
for i in [E12,E11,E10_5,E10_1,E9]:
#for i in [E12,E11,E10_5,E10_1]:
    mi.plot_eps_history(i)
    mi.show_valuation(i, hist=False, table=True, key="PSR")    

# %%
ret=mi.plot_eps_history(jicchama)

# %% [markdown]
# ### FANGAM??????????????????????????????

# %%
mi.plot_eps(fangam,largefig=True)
mi.search_good_eps(fangam, last=200)

# %% [markdown]
# ## Energy

# %%
ENE=["AR", "BP","CVX", "DVN", "FANG","FLNG", "HES", "HLX","MRO", "PBR", "PXD","STNG","SLB","TNP","XOM","YPF"]
df_res=mi.plot_eps_history(ENE,last=20)

# %%
ENE=["AR", "BP","CVX", "DVN", "FANG","FLNG", "HES"]+["HLX","MRO", "PBR", "PXD", "TNP","XOM"]
#,"YPF"]#"SLB", "STNG",

df_res=mi.show_valuation(ENE,table=True)

# %% [markdown]
# ## Health/Bio

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
    "PGNY",
    "RGEN",
    "INMD",
    "DOCS",
    "MRK",
#    "JAZZ"
]
health = H_E11 + H_E10 + H_E9

# %%
import importlib
importlib.reload(mi)
# EPS history
df_res=mi.plot_eps_history(H_E11,last=20)
df_res=mi.plot_eps_history(H_E10,last=20)
df_res=mi.plot_eps_history(H_E9,last=20)

# %%
import importlib
importlib.reload(mi)
df_res=mi.show_valuation(health,table=True)#,verbose=True)
#df_cap=mi.show_valuation(health,table=True,hist=False,key="Cap")

# %% [markdown]
# ## ???????????????

# %%
MINE=["RIO","VALE"]

VALUE=["AOS","CTAS","COST","EURN","HD","KO","LOW","NUE","UNP","TGT","XMTR","W"]#,"HIMS"]
df_res=mi.show_valuation(VALUE,table=True)

# %% [markdown]
# # VUG???IWF??????????????????570????????????????????????

# %%
GOOD=["ADP","AKAM","AZO","BC","BRO","CRL","CPRT","DHR","EFX","FB","FND","IQV","LPX","MKSI","MMC","MPWR","MSFT","MTD","NVDA","ORLY","ROL","SCCO","SPGI","TPX","TRU"]
df_res = mi.show_valuation(GOOD, hist=True, table=True, key="PSR")

# %%
df_res=mi.plot_eps_history(GOOD,last=20)

# %%
ret=mi.show_beat_ratio(GOOD,last=40,threshold=95,min_qtrs=20)

# %% [markdown]
# ## Get stock info of your favorite

# %% [markdown]
# ### Find Tickers with high EPS beat ratio

# %%
# pd.set_option('display.max_rows', df.shape[0]+1)
tickers_nasdaq = si.tickers_nasdaq()
ret=mi.search_good_eps(tickers_nasdaq[:10],last=40,threshold=95,min_qtrs=20)

# %%
# !pip  install pandas==1.3.1

# %%
