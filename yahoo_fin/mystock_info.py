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


def get_data(fn, tickers, **kwargs):
    if isinstance(tickers, str):
        tickers = [tickers]

    df = pd.DataFrame()
    for ticker in tickers:
        ticker = ticker.upper()
        tmp = fn(ticker=ticker, **kwargs)
        if tmp is not None and len(tmp) != 0:
            df = df.append(tmp)

    return df

# get_earnings_history() gets actual/expected EPS history
# plot_eps() shows the result
# get_earnings_history store data in cache/ and keeps it one day
# Usage:
#   ticker=["SQ"]
#   df_earnings=get_earnings_history(ticker)
#   plot_eps_history(df_earnings)

def _get_earnings_history(ticker, clear_cache=1, verbose=False):
# return None if no data is available

    verbose and print("getting data of {}".format(ticker))
    type="earnings"

    dfname = ticker + "_" + type
    df=get_cache(fname=dfname, clear_cache=clear_cache, verbose=verbose)
    if df is not None: # True if data file exists (df is empty if no data is available)
        return(df)
    
    if not check_ticker(ticker):
        print("invalid ticker name {}".format(ticker))
        return None
    
    verbose and print("getting new {} data".format(type))
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
    df["startdatetime"] = pd.to_datetime(df["startdatetime"], errors='coerce')

    save_pickle(dfname=dfname, obj=df)

    return df


def get_earnings_history(tickers, clear_cache=1, verbose=False):
    return get_data(fn=_get_earnings_history, tickers=tickers,clear_cache=clear_cache,verbose=verbose)

def _plot_fig(df, ax, target, title="", ylabel=""):
    sns.lineplot(ax=ax, data=df[target], marker="o")
    ax.set_title(title)
    ax.tick_params(axis="x", labelrotation=90)
    ax.axhline(linewidth=1, linestyle="--")
    ax.set_xlabel("")
    ax.set_ylabel(ylabel)
    ax.legend(title='')
    ax.set_xticks(df.index)
    ax.set_xticklabels(df.index.strftime("%Y-%m"))
#    ax.xaxis.set_major_locator(plt.MaxNLocator(len(df)))

def plot_eps_history(tickers, clear_cache=1, last=20, largefig=False, verbose=False):

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
        max_col = 4

    n_tick = len(tickers)
#    n_col = min(n_tick, max_col)
    n_col = max_col
    n_row = (n_tick - 1) // max_col + 1
    print("ntick: {}, nrow: {}, ncol: {}".format(n_tick, n_row, n_col))

    defaultPlotting()
    fig, axes = plt.subplots(n_row, n_col, figsize=(width * n_col, height * n_row))
    fig.suptitle("EPS history within last {} quarters ({})".format(last, today()))

    for i, ticker in enumerate(tickers):

        if n_row == 1 or n_col == 1:
            ax = axes if n_tick == 1 else axes[i]
        else:
            row = i // n_col
            col = i % n_col
            ax = axes[row, col]

        df_ticker = df[df["ticker"] == ticker].set_index("startdatetime").sort_index()
        df_ticker=df_ticker.tail(min(last, len(df_ticker)))

        _plot_fig(df_ticker, ax, target =["epsactual", "epsestimate"],
        title=df_ticker["ticker"][0],ylabel="EPS")

    fig.tight_layout()
    plt.show()
    return(df)



def _get_valuation(ticker, clear_cache=7, verbose=False):
    """Get valuation data of a `ticker` (str)

    See `get_valuation()` for more detail.
    """
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

    df_st = si.get_stats(ticker).set_axis(["info", "values"], axis=1)
    df_st = df_st[df_st["info"] != 'Beta (5Y Monthly)']
    df_val = si.get_stats_valuation(ticker).set_axis(["info", "values"], axis=1)
    if len(df_st) == 0 or len(df_val) == 0:
        print("no stats data for {}".format(ticker))
        save_pickle(dfname=df_val, obj=None)
        return None 
    
    df = pd.concat([df_qt, df_st, df_val], ignore_index=True).sort_values(by="info")
    df["ticker"] = ticker

    save_pickle(dfname=dfname, obj=df)

    return df

def get_valuation(tickers, clear_cache=7, verbose=False):
    """Get statistics data of a ticker and return a dataframe

    This function calls 
        - si.get_quote_table()
        ['1y Target Est', '52 Week Range', 'Ask', 'Avg. Volume', 
        'Beta (5Y Monthly)', 'Bid', "Day's Range", 'EPS (TTM)', 
        'Earnings Date', 'Ex-Dividend Date', 'Forward Dividend & Yield', 
        'Market Cap', 'Open', 'PE Ratio (TTM)', 'Previous Close', 
        'Quote Price', 'Volume']
        - si.get_stats()
        ['Beta (5Y Monthly)', '52-Week Change 3', 'S&P500 52-Week Change 3',
         '52 Week High 3', '52 Week Low 3', '50-Day Moving Average 3',
         '200-Day Moving Average 3', 'Avg Vol (3 month) 3', 'Avg Vol (10 day) 3',
         'Shares Outstanding 5', 'Implied Shares Outstanding 6', 'Float',
         '% Held by Insiders 1',  '% Held by Institutions 1', 'Shares Short (Jul 29, 2021) 4',
         'Short Ratio (Jul 29, 2021) 4', 'Short % of Float (Jul 29, 2021) 4',
         'Short % of Shares Outstanding (Jul 29, 2021) 4', 'Shares Short (prior month Jun 29, 2021) 4',
         'Forward Annual Dividend Rate 4', 'Forward Annual Dividend Yield 4',
         'Trailing Annual Dividend Rate 3', 'Trailing Annual Dividend Yield 3',
         '5 Year Average Dividend Yield 4', 'Payout Ratio 4',
         'Dividend Date 3', 'Ex-Dividend Date 4', 'Last Split Factor 2',
         'Last Split Date 3', 'Fiscal Year Ends', 'Most Recent Quarter (mrq)',
         'Profit Margin', 'Operating Margin (ttm)', 'Return on Assets (ttm)',
         'Return on Equity (ttm)', 'Revenue (ttm)', 'Revenue Per Share (ttm)',
         'Quarterly Revenue Growth (yoy)', 'Gross Profit (ttm)', 'EBITDA',
         'Net Income Avi to Common (ttm)', 'Diluted EPS (ttm)',
         'Quarterly Earnings Growth (yoy)', 'Total Cash (mrq)',
         'Total Cash Per Share (mrq)', 'Total Debt (mrq)',
         'Total Debt/Equity (mrq)', 'Current Ratio (mrq)',
         'Book Value Per Share (mrq)', 'Operating Cash Flow (ttm)',
         'Levered Free Cash Flow (ttm)']
        - si.get_stats_valuation()
        ['Market Cap (intraday) 5', 'Enterprise Value 3',
         'Trailing P/E', 'Forward P/E 1', 'PEG Ratio (5 yr expected) 1',
         'Price/Sales (ttm)', 'Price/Book (mrq)', 
         'Enterprise Value/Revenue 3', 'Enterprise Value/EBITDA 7']
    and combine the results.
    """
    df = get_data(fn=_get_valuation,tickers=tickers,clear_cache=clear_cache,verbose=verbose)
    tmp=df.info
    df = df.pivot(index="ticker", columns="info", values="values")
    return df

# def get_valuation_data(tickers, clear_cache=7, verbose=False):
#     if isinstance(tickers, str):
#         tickers = [tickers]

#     data = pd.DataFrame(index=[], columns=["ticker", "info", "values"])
#     for ticker in tickers:
#         ticker = ticker.upper()
#         tmp = _get_valuation_data(ticker, clear_cache=clear_cache, verbose=verbose)
#         if tmp is not None and len(tmp) != 0:
#             data = data.append(tmp, ignore_index=True)

#     df = data.pivot(index="ticker", columns="info", values="values")
#     return df


def col_name(df, str):
    return [col for col in df.columns if str in col]

def show_valuation(tickers, clear_cache=7, hist=True, table=True, key="PSR", ascending=False, verbose=False):
    """Return PSR sorted list."""
    key=key.upper()

    df = get_valuation(tickers, clear_cache=clear_cache, verbose=verbose)
    
    PSR = col_name(df, "Price/Sales")
    PBR = col_name(df, "Price/Book")
    PER = col_name(df, "PE Ratio")
    EPS = col_name(df, "EPS (TTM)")
    Target = col_name(df, "Target")
    Cap = ["Market Cap"]
    Date = col_name(df, "Earnings Date")
    Dividend = col_name(df, "Forward Dividend")
    Price = col_name(df, "Close")

    PM = col_name(df, "Profit Margin")
    QEG= col_name(df, "Quarterly Earnings Growth (yoy)")
    QRG= col_name(df, "Quarterly Revenue Growth (yoy)")
    ROE = col_name(df, "Return on Equity (ttm)")
    OM= col_name(df, "Operating Margin (ttm)")
    OCF= col_name(df, "Operating Cash Flow (ttm)")
    Revenue = col_name(df, "Revenue (ttm)")
    OCFM=["Operating Cash Flow Margin(ttm)"]
  

    key_dct={"PSR":PSR,"PBR":PBR,"PER":PER,"EPS":EPS,"CAP":Cap,"QEG":QEG,"QRG":QRG,"ROE":ROE}

    num_dct={"T":12,"B":9,"M":6}
#    col= [Cap,PM,QEG,QRG,OM,OCF,Revenue]
    for col in [Cap,PM,QEG,QRG,OM,OCF,ROE,Revenue]:
        for i in num_dct:
           df[col] = df[col].apply(lambda x: x.str.replace(r"{}$".format(i), "e{}".format(num_dct[i]), regex=True))
        df[col] = df[col].apply(lambda x: x.str.replace(r"[,\%$]", "", regex=True))

#    numeric = Cap + Price + Target + PSR + PER + PBR + PM + QEG + QRG + QM
    numeric = Cap + Price + Target + PSR + PER + PBR + QRG + PM + ROE + OM + OCF + Revenue
    df[numeric] = df[numeric].astype("float")
    df[OCFM[0]]=df[OCF[0]]/df[Revenue[0]]

    if hist:
        defaultPlotting()
        ax = sns.histplot(data=df[key_dct[key]], bins=20).set_title(
            "PSR histogram ({})".format(today())
        )
        plt.xlabel("PSR")
        plt.show()

    # clickable link in pandas dataframe
    # https://stackoverflow.com/questions/50209206/clickable-link-in-pandas-dataframe
    yahoo="https://finance.yahoo.com/quote/"
    alpha="https://seekingalpha.com/symbol/"
    TS="https://jp.tradingview.com/chart/?symbol="

    df["Y!"]="Y"+"#"+yahoo+df.index
    df["alpha"]="a"+"#"+alpha+df.index
    df["TS"]="TS"+"#"+TS+df.index


    #    target = numeric + Date
    target = Cap + Price + Target + PSR + PER + PBR + ROE + QRG  + OCFM + ["Y!","alpha","TS"]# + PM +OM
    df_tgt = df[target].sort_values(by=key_dct[key], ascending=ascending)
    df_tgt.to_latex(escape=False)

    # https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html
    # pandas 1.3 allows the following style!!
    # df_tgt=df_tgt.style.format(na_rep="-", 
    #     formatter={
    #     Cap[0]: "{:3.2e}",  
    #     (Price[0], Target[0]): "{:,.1f}", 
    #     (PSR[0], PER[0], PBR[0]): "{:,.1f}", 
    #     (PM[0], QRG[0], QM[0]): "{:.1f}%"
    #     })

    # http://seaborn.pydata.org/tutorial/color_palettes.html
    cm = sns.color_palette("Blues", as_cmap=True) # seabornのlight_paletteで緑グラデーションオブジェクトを作成


    def make_clickable(val):
        name, url = val.split('#')
        return f'<a href="{url}">{name}</a>'

    def df_styler(df):
        # Pandas style.bar color based on condition?
        # https://stackoverflow.com/questions/57580589/pandas-style-bar-color-based-on-condition
        i_pos = pd.IndexSlice[df.loc[(df[OCFM[0]]>0.15)].index, OCFM[0]]
        i_neg = pd.IndexSlice[df.loc[~(df[OCFM[0]]>0.15)].index, OCFM[0]]
        return df.style.format(
            {
            Cap[0]: "${:3.2e}",   
            Price[0]:"${:,.1f}", Target[0]:"${:,.1f}", 
            PSR[0]:"{:,.1f}", PER[0]:"{:,.1f}", PBR[0]:"{:,.1f}", ROE[0]:"{:.1f}%",
            PM[0]: "{:.1f}%", QRG[0]: "{:.1f}%", OM[0]:"{:.1f}%", OCFM[0]:"{:.1%}"}, na_rep="-")\
                .highlight_max(subset=Price+Target,axis=1,color='#fda37b')\
                .background_gradient(subset=Cap, cmap=cm)\
                .bar(subset=PSR+PBR, align='left', vmin=0, color=['#e68f8f', '#549e3f'])\
                .bar(subset=PER, align='left', vmin=0, color=['#bcde93'])\
                .bar(subset=ROE, align='mid', color=['#e68f8f', '#bcde93'])\
                .bar(subset=QRG, align='mid', vmin=min(0,df[QRG[0]].min()), color=['#e68f8f', '#f4d18b'])\
                .bar(subset=i_pos, align='mid', vmin=min(0,df[OCFM[0]].min()), vmax=.6, color=['#e68f8f', '#3c76af'])\
                .bar(subset=i_neg, align='mid', vmin=min(0,df[OCFM[0]].min()), vmax=.6, color=['#e68f8f', '#7eb8ef'])\
                .format(make_clickable, subset=["Y!","alpha","TS"])
#                .bar(subset=OCFM, align='left', vmin=0, vmax=.6, color=['#3c76af'])\
#                .bar(subset=PM, align='left', vmin=0, color=['#aecde1'])\
#                .bar(subset=OM, align='left', vmin=0, color=['#3c76af'])\

    df_result = df_styler(df_tgt)
    html=df_result.render()
#    html=df_result.to_html() # pandas >= 1.3.0

    file = open("financials.html","w")
    file.write(html)
    file.close()

    if table:
        print("{} sorted list ({})".format(key,today()))
        display(df_result)
    else:
        print("The top 5 {} stocks ({})".format(key,today()))
        display(df_styler(df_tgt.head()))

    return df_tgt

# # revenue
# def _get_revenue_history(ticker, clear_cache=7, verbose=False):
#     """get revenue data using si.get_data()"""
#     fname = ticker + "_revenue"
#     dct = get_cache(fname=fname, clear_cache=clear_cache, verbose=verbose)
#     if dct is not None: # True if data file exists (df is empty if no data is available)
#         return(dct)
    
#     if not check_ticker(ticker):
#         print("invalid ticker name")
#         return None    
        
#     verbose and print("getting new revenue dat")
#     dct_rev = si.get_earnings(ticker)
#     if len(dct_rev) == 0:
#         print("no revenue data for {}".format(ticker))
#         save_pickle(dfname=fname, obj=None)
#         return None    
    
#     for key in dct_rev.keys():
#         df_tmp=dct_rev[key].copy()
#         df_tmp['Ticker']=ticker
#         dct_rev[key]=df_tmp

#     save_pickle(dfname=fname, obj=dct_rev)

#     return dct_rev


# def get_revenue_history(tickers, clear_cache=7, verbose=False):

#     if isinstance(tickers, str):
#         tickers = [tickers]

#     dct = {}
#     for ticker in tickers:
#         ticker = ticker.upper()
#         tmp = _get_revenue(ticker, clear_cache=clear_cache, verbose=verbose)
#         if tmp is not None and len(tmp) != 0:
#             if len(dct) == 0:
#                 dct=tmp.copy()
#                 continue

#             for key in tmp.keys():
#                 dct[key]=dct[key].append(tmp[key])

#     return dct

# def plot_revenue_history(tickers, clear_cache=7, verbose=False):
#     dct=get_revenue(tickers, clear_cache=clear_cache, verbose=verbose)

#     tickers = dct['quarterly_results'].Ticker.unique()

#     sns.set_theme(
#         rc={
#             "axes.titlesize": 16,
#             "axes.labelsize": 14,
#             "font.size": 16,
#             "legend.fontsize": 12,
#         },
#         style="white",
#     )

#     n_tick = len(tickers)
#     n_col= n_tick
# #    n_row = 3
#     n_row = 2

#     width = 3
#     height = 2.5

# #    defaultPlotting()
#     fig, axes = plt.subplots(n_row, n_col, figsize=(width * n_col, height * n_row))
#     fig.suptitle("Revenue history ({})".format(today()))

# #    keys=["quarterly_results","quarterly_revenue_earnings","yearly_revenue_earnings"]
#     # omit "quarterly_revenue_earnings" because it's only last quarters data of EPS estimate/actual.
#     keys=["quarterly_revenue_earnings","yearly_revenue_earnings"]

#     for col, ticker in enumerate(tickers):
# #        for col, key in enumerate(dct):
#         for row, key in enumerate(keys):

#             if n_col == 1:
#                 ax = axes[row]
#             else:
#                 ax = axes[row, col]

#             df=dct[key]
#             df=df[df['Ticker']==ticker].set_index("date")

# #            if key == 'quarterly_results':
# #                _plot_revenue(df,ax,target=["actual","estimate"],ytitle=key, title=ticker)
#             if key == 'quarterly_revenue_earnings':
#                 _plot_fig(df,ax,target=["revenue","earnings"],ylabel="Quarterly revenue", title=ticker)
#             else: # key == "yearly_revenue_earnings"
#                 _plot_fig(df,ax,target=["revenue","earnings"],ylabel="Yearly revenue", title=None)

#     fig.tight_layout()
#     plt.show()
#     return(dct)

# EPS beat ratio
def _show_beat_ratio(
    df, last=20, threshold=False, min_qtrs=1, verbose=False
):
    """get EPS beat ratio
    Find tickers with high EPS beat ratio from dataframe.

    Args:
        last=20      # of quarters to be considered 
        threshold=80 the threshold of EPS beat ratio to be shown

    Examples:
        df_eps=get_earnings_history(ticker)
        show_beat_ratio(df_eps)
    """
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


def show_beat_ratio(tickers, last=20, threshold=80, min_qtrs=4, clear_cache=False, verbose=False):
    """Search tickers of which EPS beat ratio is larger than a threshold

    Args:
        - last: number of quarters to be considred
        - min_qtrs: number of quarters required for evaluation
        - threshold: minimum EPS beat ratio in `last` quarters
    """
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

    df_best = _show_beat_ratio(df, last=last, threshold=threshold, min_qtrs=min_qtrs)
    display(df_best)
    return df

## financial data
def _get_financial_history(ticker, clear_cache=1, yearly=True, verbose=False):
    """return None if no data is available"""

    verbose and print("getting data of {}".format(ticker))
    type="financial"
    term="_y" if yearly else "_q"
    dfname = ticker + "_" + type + term
    df=get_cache(fname=dfname, clear_cache=clear_cache, verbose=verbose)
    if df is not None: # True if data file exists (df is empty if no data is available)
        return(df)
    
    if not check_ticker(ticker):
        print("invalid ticker name {}".format(ticker))
        return None
    
    verbose and print("getting new {} data".format(type))
    df_cf = si.get_cash_flow(ticker,yearly=yearly)
    df_bs = si.get_balance_sheet(ticker,yearly=yearly)
    df_is = si.get_income_statement(ticker,yearly=yearly)

    if len(df_cf) == 0 or len (df_bs) == 0 or len(df_is)==0:
        print("no data for {}".format(ticker))
        save_pickle(dfname=dfname, obj=None)
        return None

    df = pd.concat([df_cf,df_bs,df_is.drop("netIncome")])

    if len(df) == 0:
        print("no data for {}".format(ticker))
        save_pickle(dfname=dfname, obj=None)
        return None

    df=df.T.astype("float").sort_index()
    df["ticker"] = ticker

    save_pickle(dfname=dfname, obj=df)

    return df

def get_financial_history(tickers, clear_cache=1, yearly=True, verbose=False):
    """Get financial history data.
    
    Following data will be downloaded.
    - return values by si.get_cash_flow()
       ['investments', 'changeToLiabilities',
       'totalCashflowsFromInvestingActivities', 'netBorrowings',
       'totalCashFromFinancingActivities', 'changeToOperatingActivities',
       'issuanceOfStock', 'netIncome', 'changeInCash', 'repurchaseOfStock',
       'totalCashFromOperatingActivities', 'depreciation',
       'otherCashflowsFromInvestingActivities', 'dividendsPaid',
       'changeToInventory', 'changeToAccountReceivables',
       'otherCashflowsFromFinancingActivities', 'changeToNetincome',
       'capitalExpenditures']
    - return values by si.get_balance_sheet()
    ['totalLiab', 'totalStockholderEquity', 'otherCurrentLiab',
       'totalAssets', 'commonStock', 'otherCurrentAssets', 'retainedEarnings',
       'otherLiab', 'treasuryStock', 'otherAssets', 'cash',
       'totalCurrentLiabilities', 'shortLongTermDebt',
       'otherStockholderEquity', 'propertyPlantEquipment',
       'totalCurrentAssets', 'longTermInvestments', 'netTangibleAssets',
       'shortTermInvestments', 'netReceivables', 'longTermDebt', 'inventory',
       'accountsPayable']
    - return values by si.get_income_statement()
    ['researchDevelopment', 'effectOfAccountingCharges', 'incomeBeforeTax',
       'minorityInterest', 'netIncome', 'sellingGeneralAdministrative',
       'grossProfit', 'ebit', 'operatingIncome', 'otherOperatingExpenses',
       'interestExpense', 'extraordinaryItems', 'nonRecurring', 'otherItems',
       'incomeTaxExpense', 'totalRevenue', 'totalOperatingExpenses',
       'costOfRevenue', 'totalOtherIncomeExpenseNet', 'discontinuedOperations',
       'netIncomeFromContinuingOps', 'netIncomeApplicableToCommonShares']

    """
    col_names = {
        "ticker" : "ticker",
        # from cash flow
        "totalCashFromOperatingActivities": "OCF",  # "operating cash flows",
        "totalCashflowsFromInvestingActivities": "ICF",  # "investing cash flows ",
        "totalCashFromFinancingActivities": "FCF",  # "financing cash flows",
        "netIncome": "earning",  # "net income"
        # from income statement
        "totalRevenue": "revenue",
        "operatingIncome": "Operating Income",
        "incomeBeforeTax": "Income Before Tax",
    }

    df = get_data(fn=_get_financial_history,tickers=tickers,clear_cache=clear_cache,verbose=verbose,yearly=yearly)
    target= [
            "ticker",
        # from cash flow
            "totalCashFromOperatingActivities",
            "totalCashflowsFromInvestingActivities",
            "totalCashFromFinancingActivities",
            "netIncome",
        # from income statement
            "totalRevenue",
            "operatingIncome"
        ]
    df = df[target].rename(columns=col_names)

    return df

def plot_financial_history(tickers, clear_cache=1, verbose=False):
    data={}
    data["years"]=get_financial_history(tickers, clear_cache=clear_cache, yearly=True, verbose=verbose)
    data["quarters"]=get_financial_history(tickers, clear_cache=clear_cache, yearly=False, verbose=verbose)

    tickers = data["years"].Ticker.unique()

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
    n_row = 4

    width = 3
    height = 2.5

#    defaultPlotting()
    fig, axes = plt.subplots(n_row, n_col, figsize=(width * n_col, height * n_row))
    fig.suptitle("Revenue history ({})".format(today()))

    for key in ["years","quarters"]:
        data[key]["OCF/revenue"]=data[key]["OCF"]/data[key]["revenue"]

    for col, ticker in enumerate(tickers):
        for row, key in enumerate(["years","quarters","years","quarters"]):
            if n_col == 1:
                ax = axes[row]
            else:
                ax = axes[row, col]

            if row <= 1:
                title = ticker if row == 0 else None
                _plot_fig(data[key],ax,target=["revenue","OCF","earning"],ylabel="revenue (4 {})".format(key), title=title)
            else:
                _plot_fig(data[key],ax,target=["OCF/revenue"],ylabel="OCF/revenue (4 {})".format(key))

    fig.tight_layout()
    plt.show()
    return data

def get_all_data(tickers, last=20, table=True):
    """
    - run the following
        1. download EPS history (`get_earnings_history()`))
        2. download valuation data (`get_valuation_data()`)
        3. shows the EPS beat ratios in 'last' quarters (`show_beat_ratio()`)
    - Args:
        - `tickers`: list of tickers 
        - `last=20`: number of quarters to be considred to get EPS beat ratio
        - `table=False`: show the table of EPS beat ratio or not
    - Returns: tuple of return values of get_earnings_history() and get_valuation_data()
    """
    # get eps history
    df_earnings = get_earnings_history(tickers)
    # get PSR and others
    df_tickers = get_valuation(tickers)

    table == True and display(show_beat_ratio(df_earnings, last))
    return (df_earnings, df_tickers)

