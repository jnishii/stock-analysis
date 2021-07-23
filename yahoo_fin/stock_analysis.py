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
# # get financial data

# %% [markdown]
# ## import modules and difine basic modules & functions

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# private module
import mystock_info as mi

# %% [markdown]
# ## basic usage
# EPSの履歴取得とグラフ化

# %%
# test code
df=mi.get_earnings_history("A",verbose=False)
display(df.head(3))
mi.plot_eps(df,last=20,largefig=False)

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
# データはキャッシュされるので，少しずつためるのでOK

# %%
# get data of stock indexes
df_dow = get_financial_data(tickers=tickers_dow)
df_dow_final=plot_financials(df_dow,table=False)
# df_nasdaq=get_financial_data(tickers=tickers_nasdaq)
# df_sp500=get_financial_data(tickers=tickers_sp500)

# %% [markdown]
# ## Get stock info of your favorite
# ### EPS beat ratio が高いTickerを見つける

# %%
# pd.set_option('display.max_rows', df.shape[0]+1)

#nas500=search_good_eps(tickers=tickers_nasdaq[0:400],last=20,threshold=90,verbose=False)
#save_pickle('nas400_eps',nas400)
#target='nas400_eps'
#nas400 = pickle.load( open( "data/{}.pkl".format(target), "rb" ) )
#print(len(nas400.ticker.unique()))
show_beat_ratio(nas400,last=40,threshold=95,min_qtrs=20)

#nas200_best = pickle.load( open( "data/nas200_best.pkl", "rb" ) )

#nas100=search_good_eps(tickers=tickers_nasdaq[0:100],last=20,threshold=80,verbose=False)
#save_pickle('nas100_eps',nas100)


# %%
df=get_earnings_history("A")
plot_eps(df,last=20,largefig=False)

# %%
#target="nas400_eps"
#nas400 = pickle.load( open( "data/{}.pkl".format(target), "rb" ) )

#df=pd.concat([nas200,nas400,nas600,nas1000])
#save_pickle('nas1000_eps',df)
target="nas1000_eps"
nas1000 = pickle.load( open( "data/{}.pkl".format(target), "rb" ) )

print(len(nas1000.ticker.unique()))

#display(df)
#show_beat_ratio(nas1000,last=20,threshold=95,min_qtrs=4)
show_beat_ratio(nas1000,last=20,threshold=95,min_qtrs=4)

# %%
#df = pickle.load( open( "data/nas200_eps.pkl", "rb" ) )
#display(df[:10])
#show_beat_ratio(df,last=20,threshold=95,min_qtrs=4)


# %% [markdown]
# ## Tech

# %%
fangam=["FB","AAPL","NFLX","GOOG","AMZN","MSFT"]

###
ant=["ADBE","NVDA","TSLA"]
saas=["CRWD","OKTA","ZS","TTD","TWLO"]
ecommerce=["SHOP","ETSY","FIVN"]

fintech=["SQ","DOCU"]
media=["TWTR","PINS"]
techs=["U","ZM","FVRR","ABNB","ROKU"]

growth1=ant+saas+ecommerce
growth2=fintech+media+techs

###
eauto=["F","GM","MGA"]

# %%
df_fangam=get_all_data(fangam)
#"target='df_fangam'
# save_pickle(target,df_fangam)
#df_fangam = pickle.load( open( "data/{}.pkl".format(target), "rb" ) )
plot_eps(df_fangam[0],last=20)

# growth1
df_growth1=get_all_data(growth1)
#target='df_growth1'
#save_pickle(target,df_growth1)
#df_growth1 = pickle.load( open( "data/{}.pkl".format(target), "rb" ) )
plot_eps(df_growth1[0],last=20)

# growth2
df_growth2=get_all_data(growth2)
#target='df_growth2'
#save_pickle(target,df_growth2)
#df_growth2 = pickle.load( open( "data/{}.pkl".format(target), "rb" ) )
plot_eps(df_growth2[0],last=20)

# eauto
df_eauto=get_all_data(eauto)
#target='df_eauto'
#save_pickle(target,df_eauto)
#df_eauto = pickle.load( open( "data/{}.pkl".format(target), "rb" ) )
plot_eps(df_eauto[0],last=20)

df_all=pd.concat([df_fangam[0],df_growth1[0],df_growth2[0],df_eauto[0]])
display(show_beat_ratio(df_all, last=20))

# all PSR
df_all_psr=pd.concat([df_fangam[1],df_growth1[1],df_growth2[1],df_eauto[1]])
df_res=plot_financials(df_all_psr, table=True)

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
df_health_eps,df_health_fin=get_all_data(tickers_health)
plot_eps(df_health_eps,last=20)
show_beat_ratio(df_health_eps)

df_res=plot_financials(df_health_fin,table=True)

# %% [markdown]
# ## Pyfolioによる情報表示
#
# - [pyfolio](https://github.com/quantopian/pyfolio)
#
# ```bash
# $ pip install pyfolio
# ```
#
# ## references
#
# - [HOW TO DOWNLOAD FUNDAMENTALS DATA WITH PYTHON](http://theautomatic.net/2020/05/05/how-to-download-fundamentals-data-with-python/)
# - [pyfolioを使ってみる](https://qiita.com/mrsn28/items/445553c24861b9930682)

# %%
import pyfolio as pf
# %matplotlib inline

# silence warnings
import warnings
warnings.filterwarnings('ignore')

# %%
stock_rets = pf.utils.get_symbol_rets('DOCU')
#pf.create_returns_tear_sheet(stock_rets, live_start_date='2015-12-1')
pf.create_returns_tear_sheet(stock_rets)

# %%
