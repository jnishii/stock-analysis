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
# # Pyfolioによる情報表示
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
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import pyfolio as pf
import warnings
warnings.filterwarnings('ignore')

# %%
stock_rets = pf.utils.get_symbol_rets('DOCU')
#pf.create_returns_tear_sheet(stock_rets, live_start_date='2015-12-1')
pf.create_returns_tear_sheet(stock_rets)
