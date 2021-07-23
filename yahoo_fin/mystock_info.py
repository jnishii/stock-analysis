import yahoo_fin.stock_info as si
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import time

import os.path, time
from datetime import datetime, timedelta
from pathlib import Path

# Basic definitions

cache_dir = "cache"

def defaultPlotting():
    sns.set_theme(
        rc={
            "figure.figsize": (6, 5),
            "axes.titlesize": 20,
            "axes.labelsize": 20,
            "font.size": 20,
            "legend.fontsize": 15,
        },
        style="white",
    )
    sns.set_style("whitegrid")


def today(time=False):
    if time==True:
        return datetime.today().strftime("%Y-%m-%d-%H:%M:%S")
    else:
        return datetime.today().strftime("%Y-%m-%d")

def save_pickle(dfname, obj, data_dir=cache_dir):
# save obj in the pickle format in `data_dir`
# if obj is None, empty dataframe is saved
    if obj is None:
        obj=pd.DataFrame()

    Path(data_dir).mkdir(parents=True, exist_ok=True)
    fname = data_dir + "/{}.pkl".format(dfname)
    pickle.dump(obj, open(fname, "wb"))

def load_pickle(dfname, data_dir=cache_dir):
# load from `dfname` in `data_dir`
    fname = "{}/{}.pkl".format(data_dir, dfname)
    obj = pickle.load(open(fname, "rb"))
    return(obj)

def isnewfile(dfname, clear_cache=1, verbose=False):
# Check the existence of the file `dfname`
# arguments:
#    clear_cache: number of days of preserving cache
#                 set False if you want to use cache despite the time stamp
#                 of the file.
# return value:
#    None if the file `dfname` doesn't exist
#    True if (cache was created within `cache_dir` days) or (cache exists and use it (clear_cache=False))
#    False otherwise
    fname = "{}/{}.pkl".format(cache_dir, dfname)

    if not os.path.isfile(fname):
        verbose and print("{} not found".format(fname))
        return None

    if clear_cache is False:
        verbose and print("{} is found and preserve cache".format(fname))
        return True
    
    now = datetime.utcnow()
    file_time = datetime.utcfromtimestamp(os.path.getmtime(fname))
    if (now - file_time) > timedelta(clear_cache):
        verbose and print("more than {} day has passed".format(clear_cache))
        return False
    else:
        verbose and print("you have new file within {} day".format(clear_cache))
        return True


def get_df_from_file(dfname, clear_cache=1, verbose=False):
# return
#   object if dfname is a file within `clear_cache` days
#   None otherwise (no data file)    
    if isnewfile(dfname, clear_cache=clear_cache, verbose=verbose):
        verbose and print("loading cache dat")
        df = load_pickle(dfname)
        return df
    else:
        verbose and print("no file found")
        return None
    
def check_ticker(ticker):
# check if `ticker` is valid (True) or not (False)
    ret=True
    try:
        si.get_company_officers(ticker)
    except:
        ret=False
    return(ret)


# ## Define financial functions
#
# get_earnings_history() gets actual/expected EPS history
# plot_eps() shows the result
# get_earnings_history store data in cache/ and keeps it one day
# Usage:
#   ticker=["SQ"]
#   df_earnings=get_earnings_history(ticker)
#   plot_eps(df_earnings)

def _get_earnings_history(ticker, clear_cache=1, verbose=False):
# return None if no data is available

    verbose and print("getting data of {}".format(ticker))

    dfname = ticker + "_earnings"
    df=get_df_from_file(dfname, clear_cache=clear_cache, verbose=verbose)
    if df is not None: # True if data file exists (df is empty if no data is available)
        return(df)
    
    if not check_ticker(ticker):
        print("invalid ticker name {}".format(ticker))
        return None
    
    verbose and print("getting new dat")
    dct = si.get_earnings_history(ticker)
    if len(dct) == 0:
        print("no data for {}".format(ticker))
        save_pickle(dfname=dfname, obj=None)
        return None

    df = pd.json_normalize(dct).dropna()
    if len(df) == 0:
        print("no data for {}".format(ticker))
        save_pickle(dfname=dfname, obj=None)
        return None

    df["startdatetime"] = df["startdatetime"].str.replace(r"T.*$", "", regex=True)

    save_pickle(dfname=dfname, obj=df)

    return df


def get_earnings_history(tickers, clear_cache=1, verbose=False):

    if isinstance(tickers, str):
        tickers = [tickers]

    df = pd.DataFrame()
    for ticker in tickers:
        ticker = ticker.upper()
        tmp = _get_earnings_history(ticker, clear_cache=clear_cache, verbose=verbose)
        if tmp is not None and len(tmp) != 0:
            df = df.append(tmp)

    return df


def _plot_eps(df, ax, last):
    d = df.set_index("startdatetime").sort_index().tail(last)
    sns.lineplot(ax=ax, data=d[["epsactual", "epsestimate"]], marker="o")
    ax.set_title(d["ticker"][0])
    ax.tick_params(axis="x", labelrotation=90)
    ax.set_xlabel("")
    ax.set_ylabel("EPS")


def plot_eps(df, last=1000, largefig=False):

    tickers = df.ticker.unique()
    n_tick = len(tickers)

    if largefig == True:
        width = 12
        height = 8
        max_col = 1
    else:
        width = 6
        height = 4.5
        if n_tick <= 3:
            max_col = n_tick
        elif n_tick == 4:
            max_col = 2
        elif n_tick <= 6:
            max_col = 3
        else:
            max_col = 3
    #        max_col=4

    n_tick = len(tickers)
    n_col = min(n_tick, max_col)
    n_row = (n_tick - 1) // max_col + 1
    print("ntick: {}, nrow: {}, ncol: {}".format(n_tick, n_row, n_col))

    defaultPlotting()
    fig, axes = plt.subplots(n_row, n_col, figsize=(width * n_col, height * n_row))
    fig.suptitle("EPS history within last {} quarters ({})".format(last, today()))

    for i, ticker in enumerate(tickers):
        target = df[df["ticker"] == ticker]

        if n_row == 1 or n_col == 1:
            ax = axes if n_tick == 1 else axes[i]
        else:
            row = i // n_col
            col = i % n_col
            ax = axes[row, col]

        _plot_eps(target, ax, min(last, len(target)))

    fig.tight_layout()
    plt.show()


# get_financial_data() calls si.get_quote_table() and si.get_stats_valuation(), and combine the results
# plot_financials() shows a plot of the data from get_financial_data()
# Usage:
#   df=get_financial_data(tickers)
#   res=plot_financials(df, table=True)

def _get_financial_data(ticker, clear_cache=7, verbose=False):
    dfname = ticker + "_financial"
    df = get_df_from_file(dfname, clear_cache=clear_cache, verbose=verbose)
    if df is not None: # True if data file exists (df is empty if no data is available)
        return(df)
    
    if not check_ticker(ticker):
        print("invalid ticker name")
        return None    
        
    verbose and print("getting new financial dat")
    dct_qt = si.get_quote_table(ticker)
    df_qt = (
        pd.json_normalize(dct_qt)
        .transpose()
        .reset_index()
        .set_axis(["info", "values"], axis=1)
    )

    df_val = si.get_stats_valuation(ticker).set_axis(["info", "values"], axis=1)

    df = pd.concat([df_qt, df_val], ignore_index=True).sort_values(by="info")
    df["Ticker"] = ticker
    save_pickle(dfname=dfname, obj=df)

    return df


def get_financial_data(tickers, clear_cache=7, verbose=False):
    if isinstance(tickers, str):
        tickers = [tickers]

    data = pd.DataFrame(index=[], columns=["Ticker", "info", "values"])
    for ticker in tickers:
        ticker = ticker.upper()
        tmp = _get_financial_data(ticker, clear_cache=clear_cache, verbose=verbose)
        if tmp is not None and len(tmp) != 0:
            data = data.append(tmp, ignore_index=True)

    df = data.pivot(index="Ticker", columns="info", values="values")
    return df


def col_name(df, str):
    return [col for col in df.columns if str in col]


def plot_financials(df, table=False):
# return PSR sorted list

    PSR = col_name(df, "Price/Sales")
    PBR = col_name(df, "Price/Book")
    PER = col_name(df, "PE Ratio")
    EPS = col_name(df, "EPS")
    Target = col_name(df, "Target")
    Cap = ["Market Cap"]
    Date = col_name(df, "Earnings Date")
    Dividend = col_name(df, "Forward Dividend")
    Price = col_name(df, "Close")

    #    numeric=Price+Target+PSR+PER+PBR+EPS
    numeric = Price + Target + PSR + PER + PBR
    df[numeric] = df[numeric].astype("float")

    #     df[PSR].plot(kind="hist",bins=20)
    #     plt.xlabel("PSR")
    #     plt.show()

    defaultPlotting()
    ax = sns.histplot(data=df[PSR], bins=20).set_title(
        "PSR histogram ({})".format(today())
    )
    plt.xlabel("PSR")
    plt.show()

    target = Cap + numeric + Date
    df_tgt = df[target].sort_values(by=PSR, ascending=False)

    if table == True:
        print("PSR sorted list ({})".format(today))
        display(df_tgt)
    else:
        print("The top 5 PSR stocks ({})".format(today))
        display(df_tgt.head())

    return df_tgt


# ## Get stock info of your favorite
# ### EPS beat ratio が高いTickerを見つける
# show_beat_ratio(): EPS beat ratioの一覧作成
# Arguments:
#   last=20      # # of quarters to be considered 
#   threshold=80 # if you want to show only beatratio > 80%
# Usage:
#   df_eps=get_earnings_history(ticker)
#   show_beat_ratio(df_eps)
#

def show_beat_ratio(
    df, last=20, threshold=False, min_qtrs=1, verbose=False
):
    group = ["ticker", "companyshortname"]
    target = (
        df[["startdatetime", "ticker", "epssurprisepct", "companyshortname"]]
        .dropna()
        .set_index("startdatetime")
        .sort_index()
        .groupby(group)
        .tail(last)
    )
    target["beat"] = target["epssurprisepct"] >= 0
    if verbose: display(target)
        
    ratio = target.groupby(group).mean().rename(columns={"beat": "beat ratio"})
    count = (
        target.groupby(group)
        .count()
        .drop("epssurprisepct", axis=1)
        .rename(columns={"beat": "count"})
    )
    if verbose: display(count)
    
    beat = target.groupby(group).sum().drop("epssurprisepct", axis=1)

    result = ratio.join(count)
    result = result.join(beat).sort_values(by="beat ratio", ascending=False)
    result["beat ratio"] = result["beat ratio"] * 100
    if verbose: display(target)
    
    if threshold == False:
        print("EPS beat ratio (%) within last {} quarters ({})".format(last, today()))
    else:
        print(
            "Tickers list of which beat ratio >= {} % within last {} quarters".format(
                threshold, last, today()
            )
        )
        print("(data with more than {} quarter EPSs)".format(min_qtrs))
        result = result[ (result["beat ratio"] >= threshold) & (result["count"] >= min_qtrs)]

    return result[["beat ratio", "beat", "count"]]


# get_all_data(): get_earnings_history()とget_financial_data()の結果を返す。ついでに EPS beat ratioの一覧表示
def get_all_data(ticker, last=20):
    # get eps history
    df_earnings = get_earnings_history(ticker)
    # get PSR and others
    df_ticker = get_financial_data(ticker)

    display(show_beat_ratio(df_earnings, last))
    return (df_earnings, df_ticker)


# %%
# search_good_eps(): Search Tickers of which EPS beat ratio is larger than a threshold
# arguments:
# - last: number of quarters to be considred
# - min_qtrs: number of quarters required for evaluation
# - threshold: minimum EPS beat ratio in `last` quarters
def search_good_eps(tickers, last=20, threshold=80, min_qtrs=4, clear_cache=False, verbose=False):

    n_tick = len(tickers)
    step = 10
    i = 0
    df = pd.DataFrame()
    while i < n_tick:
        end = min(i + step, n_tick)
        df_new = get_earnings_history(tickers[i:end], clear_cache, verbose=verbose)
        if len(df_new) != 0:
            df = df.append(df_new)
        i = i + step
        time.sleep(60)

    df_best = show_beat_ratio(df, last=last, threshold=threshold, min_qtrs=min_qtrs)
    display(df_best)
    return df

