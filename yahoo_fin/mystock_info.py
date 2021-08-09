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
    """Save obj in the pickle format in `data_dir`.
    if obj is None, empty dataframe is saved.

    Args:
        dfname (str): Name of file
        obj (object): Object to be saved
        data_dir: place where the object is saved. Default is defined as .cache_dir

    Returns:
        int: Sum of param1 and param2.

    Examples:
        Examples should be written in doctest format, and should illustrate how
        to use the function.

        >>> example_function(4, 5)])
        9

    """
    if obj is None:
        obj=pd.DataFrame()

    Path(data_dir).mkdir(parents=True, exist_ok=True)
    fname = data_dir + "/{}.pkl".format(dfname)
    pickle.dump(obj, open(fname, "wb"))

def load_pickle(dfname, data_dir=cache_dir):
"""Load data from `dfname` in `data_dir`"""
    fname = "{}/{}.pkl".format(data_dir, dfname)
    obj = pickle.load(open(fname, "rb"))
    return(obj)

def isnewfile(dfname, clear_cache=1, verbose=False):
    """Check the existence of the file `dfname`

    Args:
        clear_cache: number of days of preserving cache
                     set 0 if you want to clear cache and 99999 to preserve 
                     despite the time stamp of the file.
    Returns:
        None if the file `dfname` doesn't exist
        True if (cache was created within `cache_dir` days) or (cache exists and use it (clear_cache=False))
        False otherwise
    """
    fname = "{}/{}.pkl".format(cache_dir, dfname)

    if not os.path.isfile(fname):
        verbose and print("{} not found".format(fname))
        return None

    if clear_cache is False:
        verbose and print("{} is found and preserve cache: {}".format(fname,dfname))
        return True
    
    now = datetime.utcnow()
    file_time = datetime.utcfromtimestamp(os.path.getmtime(fname))
    if (now - file_time) > timedelta(clear_cache):
        verbose and print("more than {} day has passed: {}".format(clear_cache,dfname))
        return False
    else:
        verbose and print("you have new file within {} day: {}".format(clear_cache,dfname))
        return True


def get_cache(fname, clear_cache=1, verbose=False):
# return
#   object if dfname is a file within `clear_cache` days
#   None otherwise (no data file)    
    if isnewfile(fname, clear_cache=clear_cache, verbose=verbose):
        verbose and print("loading cache data: {}".format(fname))
        obj = load_pickle(fname)
        return obj
    else:
        verbose and print("no cache found:".format(fname))
        return None
    
def check_ticker(ticker):
# check if `ticker` is valid (True) or not (False)
    ret=True
    try:
        si.get_company_officers(ticker)
    except:
        ret=False
    return(ret)


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
    df=get_cache(fname=dfname, clear_cache=clear_cache, verbose=verbose)
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


#def plot_eps(df, last=1000, largefig=False):
def plot_eps(tickers, clear_cache=1, last=20, largefig=False, verbose=False):

    df=get_earnings_history(tickers, clear_cache=clear_cache, verbose=verbose)
    tickers = df.ticker.unique()
    n_tick = len(tickers)

    if largefig == True:
        width = 10
        height = 6
        max_col = 1
    else:
        width = 5
        height = 4
        if n_tick <= 4:
            max_col = n_tick
        else:
            max_col = 4
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
    return(df)


# get_valuation_data() calls si.get_quote_table() and si.get_stats_valuation(), and combine the results
# plot_financials() shows a plot of the data from get_basic_data()
# Usage:
#   df=get_valuation_data(tickers)
#   res=plot_valuation(df, table=True)

def _get_valuation_data(ticker, clear_cache=7, verbose=False):
    dfname = ticker + "_valuation"
    df = get_cache(fname=dfname, clear_cache=clear_cache, verbose=verbose)
    if df is not None: # True if data file exists (df is empty if no data is available)
        return(df)
    
    if not check_ticker(ticker):
        print("invalid ticker name".format(ticker))
        return None    
        
    verbose and print("getting new quote table")
    dct_qt = si.get_quote_table(ticker)
    if len(dct_qt) == 0:
        print("no quote_table data for {}".format(ticker))
        save_pickle(dfname=dfname, obj=None)
        return None    
    
    df_qt = (
        pd.json_normalize(dct_qt)
        .transpose()
        .reset_index()
        .set_axis(["info", "values"], axis=1)
    )

    df_val = si.get_stats_valuation(ticker).set_axis(["info", "values"], axis=1)
    if len(df_val) == 0:
        print("no valuation data for {}".format(ticker))
        save_pickle(dfname=df_val, obj=None)
        return None    
    
    df = pd.concat([df_qt, df_val], ignore_index=True).sort_values(by="info")
    df["Ticker"] = ticker
    save_pickle(dfname=dfname, obj=df)

    return df


def get_valuation_data(tickers, clear_cache=7, verbose=False):
    if isinstance(tickers, str):
        tickers = [tickers]

    data = pd.DataFrame(index=[], columns=["Ticker", "info", "values"])
    for ticker in tickers:
        ticker = ticker.upper()
        tmp = _get_valuation_data(ticker, clear_cache=clear_cache, verbose=verbose)
        if tmp is not None and len(tmp) != 0:
            data = data.append(tmp, ignore_index=True)

    df = data.pivot(index="Ticker", columns="info", values="values")
    return df


def col_name(df, str):
    return [col for col in df.columns if str in col]


def plot_valuation(tickers, clear_cache=7, hist=True, table=True, key="PSR", ascending=False, verbose=False):
    df = get_valuation_data(tickers, clear_cache=clear_cache, verbose=verbose)

# return PSR sorted list
    key=key.upper()
    PSR = col_name(df, "Price/Sales")
    PBR = col_name(df, "Price/Book")
    PER = col_name(df, "PE Ratio")
    EPS = col_name(df, "EPS")
    Target = col_name(df, "Target")
    Cap = ["Market Cap"]
    Date = col_name(df, "Earnings Date")
    Dividend = col_name(df, "Forward Dividend")
    Price = col_name(df, "Close")
    key_dct={"PSR":PSR,"PBR":PBR,"PER":PER,"EPS":EPS,"CAP":Cap}

    num_dct={"T":12,"B":9,"M":6}
    for i in num_dct:
        df[Cap] = df[Cap].apply(lambda x: x.str.replace(r"{}$".format(i), "e{}".format(num_dct[i]), regex=True))
    
    #    numeric=Price+Target+PSR+PER+PBR+EPS
    numeric = Cap + Price + Target + PSR + PER + PBR
    df[numeric] = df[numeric].astype("float")
    #     df[PSR].plot(kind="hist",bins=20)
    #     plt.xlabel("PSR")
    #     plt.show()

    if hist == True:
        defaultPlotting()
        ax = sns.histplot(data=df[key_dct[key]], bins=20).set_title(
            "PSR histogram ({})".format(today())
        )
        plt.xlabel("PSR")
        plt.show()

    target = numeric + Date
    
    df_tgt = df[target].sort_values(by=key_dct[key], ascending=ascending)
    if table == True:
        print("{} sorted list ({})".format(key,today))
        display(df_tgt)
    else:
        print("The top 5 {} stocks ({})".format(key,today))
        display(df_tgt.head())

    return df_tgt

"""
get revenue data using si.get_data()
"""

def _get_revenue(ticker, clear_cache=7, verbose=False):
    fname = ticker + "_revenue"
    dct = get_cache(fname=fname, clear_cache=clear_cache, verbose=verbose)
    if dct is not None: # True if data file exists (df is empty if no data is available)
        return(dct)
    
    if not check_ticker(ticker):
        print("invalid ticker name")
        return None    
        
    verbose and print("getting new revenue dat")
    dct_rev = si.get_earnings(ticker)
    if len(dct_rev) == 0:
        print("no revenue data for {}".format(ticker))
        save_pickle(dfname=fname, obj=None)
        return None    
    
    for key in dct_rev.keys():
        df_tmp=dct_rev[key].copy()
        df_tmp['Ticker']=ticker
        dct_rev[key]=df_tmp

    save_pickle(dfname=fname, obj=dct_rev)

    return dct_rev

def get_revenue(tickers, clear_cache=7, verbose=False):

    if isinstance(tickers, str):
        tickers = [tickers]

    dct = {}
    for ticker in tickers:
        ticker = ticker.upper()
        tmp = _get_revenue(ticker, clear_cache=clear_cache, verbose=verbose)
        if tmp is not None and len(tmp) != 0:
            if len(dct) == 0:
                dct=tmp.copy()
                continue

            for key in tmp.keys():
                dct[key]=dct[key].append(tmp[key])

    return dct


def _plot_revenue(df, ax, target, title="", ytitle=""):

    d = df.set_index("date")#.sort_index()
    sns.lineplot(ax=ax, data=d[target], marker="o")
    ax.set_title(title)
    ax.tick_params(axis="x", labelrotation=90)
    ax.axhline(linewidth=1, linestyle="--")
    ax.set_xlabel("")
    ax.set_ylabel(ytitle)

def plot_revenue(tickers, clear_cache=7, verbose=False):
    dct=get_revenue(tickers, clear_cache=clear_cache, verbose=verbose)

    tickers = dct['quarterly_results'].Ticker.unique()

    sns.set_theme(
        rc={
            "axes.titlesize": 16,
            "axes.labelsize": 14,
            "font.size": 16,
            "legend.fontsize": 12,
        },
        style="white",
    )

    n_tick = len(tickers)
    n_col= n_tick
#    n_row = 3
    n_row = 2

    width = 3
    height = 2.5

#    defaultPlotting()
    fig, axes = plt.subplots(n_row, n_col, figsize=(width * n_col, height * n_row))
    fig.suptitle("Revenue history ({})".format(today()))

#    keys=["quarterly_results","quarterly_revenue_earnings","yearly_revenue_earnings"]
    # omit "quarterly_revenue_earnings" because it's only last quarters data of EPS estimate/actual.
    keys=["quarterly_revenue_earnings","yearly_revenue_earnings"]

    for col, ticker in enumerate(tickers):
#        for col, key in enumerate(dct):
        for row, key in enumerate(keys):

            if n_col == 1:
                ax = axes[row]
            else:
                ax = axes[row, col]

            df=dct[key]
            df=df[df['Ticker']==ticker]
#            if key == 'quarterly_results':
#                _plot_revenue(df,ax,target=["actual","estimate"],ytitle=key, title=ticker)
            if key == 'quarterly_revenue_earnings':
                _plot_revenue(df,ax,target=["revenue","earnings"],ytitle="Quarterly revenue", title=ticker)
            else: # key == "yearly_revenue_earnings"
                _plot_revenue(df,ax,target=["revenue","earnings"],ytitle="Yearly revenue", title=None)

    fig.tight_layout()
    plt.show()
    return(dct)


"""
## Get stock info of your favorite
### find tickers with high EPS beat ratio from dataframe
show_beat_ratio()
Arguments:
  last=20      # # of quarters to be considered 
  threshold=80 # if you want to show only beatratio > 80%
Usage:
  df_eps=get_earnings_history(ticker)
  show_beat_ratio(df_eps)
"""

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
            "Tickers list of which beat ratio >= {}% within last {} quarters".format(
                threshold, last, today()
            )
        )
        print("(data with more than {} quarter EPSs)".format(min_qtrs))
        result = result[ (result["beat ratio"] >= threshold) & (result["count"] >= min_qtrs)]

    return result[["beat ratio", "beat", "count"]]

# %%
# eps_screaning(): Search Tickers of which EPS beat ratio is larger than a threshold
# arguments:
# - last: number of quarters to be considred
# - min_qtrs: number of quarters required for evaluation
# - threshold: minimum EPS beat ratio in `last` quarters
def screening_eps(tickers, last=20, threshold=80, min_qtrs=4, clear_cache=False, verbose=False):

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

    df_best = show_beat_ratio(df, last=last, threshold=threshold, min_qtrs=min_qtrs)
    display(df_best)
    return df


"""
`get_all_data(tickers, last=20, table=True)`
- run the following
    1. download EPS history (`get_earnings_history()`))
    2. download valuation data (`get_valuation_data()`)
    3. shows the EPS beat ratios in 'last' quarters (`show_beat_ratio()`)
- arguments:
    - `tickers`: list of tickers 
    - `last=20`: number of quarters to be considred to get EPS beat ratio
    - `table=False`: show the table of EPS beat ratio or not
- return value: tuple of return values of get_earnings_history() and get_valuation_data()
"""

def get_all_data(tickers, last=20, table=True):
    # get eps history
    df_earnings = get_earnings_history(tickers)
    # get PSR and others
    df_tickers = get_valuation_data(tickers)

    table == True and display(show_beat_ratio(df_earnings, last))
    return (df_earnings, df_tickers)

