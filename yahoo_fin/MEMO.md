## Yahoo financeのFinancials情報

## メモ
- 売上高: net sales / operating revenue  / total revenue
- net income / earning (純利益) : 大きな問題なくても負の場合あり(有価証券の評価損による場合など)

## Yahoo financeのquote情報

基本情報
- https://finance.yahoo.com/quote/AAPL?p=AAPL

取得関数
- si.get_quote_table()
```python
> print(dct_qt.keys())
dict_keys(['1y Target Est', '52 Week Range', 'Ask', 'Avg. Volume', 'Beta (5Y Monthly)', 'Bid', "Day's Range", 'EPS (TTM)', 'Earnings Date', 'Ex-Dividend Date', 'Forward Dividend & Yield', 'Market Cap', 'Open', 'PE Ratio (TTM)', 'Previous Close', 'Quote Price', 'Volume'])
```

- si.get_valuation() (以下のstatics情報とともに取得)

## Yahoo financeのstatistics情報
- https://finance.yahoo.com/quote/NFLX/key-statistics?p=NFLX

取得関数

- si.get_stats()
```
['Beta (5Y Monthly)',
 '52-Week Change 3',
 'S&P500 52-Week Change 3',
 '52 Week High 3',
 '52 Week Low 3',
 '50-Day Moving Average 3',
 '200-Day Moving Average 3',
 'Avg Vol (3 month) 3',
 'Avg Vol (10 day) 3',
 'Shares Outstanding 5',
 'Implied Shares Outstanding 6',
 'Float',
 '% Held by Insiders 1',
 '% Held by Institutions 1',
 'Shares Short (Aug 12, 2021) 4',
 'Short Ratio (Aug 12, 2021) 4',
 'Short % of Float (Aug 12, 2021) 4',
 'Short % of Shares Outstanding (Aug 12, 2021) 4',
 'Shares Short (prior month Jul 14, 2021) 4',
 'Forward Annual Dividend Rate 4',
 'Forward Annual Dividend Yield 4',
 'Trailing Annual Dividend Rate 3',
 'Trailing Annual Dividend Yield 3',
 '5 Year Average Dividend Yield 4',
 'Payout Ratio 4',
 'Dividend Date 3',
 'Ex-Dividend Date 4',
 'Last Split Factor 2',
 'Last Split Date 3',
 'Fiscal Year Ends',
 'Most Recent Quarter (mrq)',
 'Profit Margin',
 'Operating Margin (ttm)',
 'Return on Assets (ttm)',
 'Return on Equity (ttm)',
 'Revenue (ttm)',
 'Revenue Per Share (ttm)',
 'Quarterly Revenue Growth (yoy)',
 'Gross Profit (ttm)',
 'EBITDA',
 'Net Income Avi to Common (ttm)',
 'Diluted EPS (ttm)',
 'Quarterly Earnings Growth (yoy)',
 'Total Cash (mrq)',
 'Total Cash Per Share (mrq)',
 'Total Debt (mrq)',
 'Total Debt/Equity (mrq)',
 'Current Ratio (mrq)',
 'Book Value Per Share (mrq)',
 'Operating Cash Flow (ttm)',
 'Levered Free Cash Flow (ttm)']
 ```
- si.get_stats_valuation()
```python
> print(df.columns)
Index(['Unnamed: 0', 'As of Date: 8/29/2021Current', '6/30/2021', '3/31/2021',
       '12/31/2020', '9/30/2020', '6/30/2020'],
> list(df['Unnamed: 0'])
```python
RangeIndex(start=0, stop=9, step=1)
['Market Cap (intraday) 5',
 'Enterprise Value 3',
 'Trailing P/E',
 'Forward P/E 1',
 'PEG Ratio (5 yr expected) 1',
 'Price/Sales (ttm)',
 'Price/Book (mrq)',
 'Enterprise Value/Revenue 3',
 'Enterprise Value/EBITDA 7']
```       
- mi.get_valuation() (以下のstatics情報とともに取得)


## Yahoo financeのFinancials情報
### Income Statement

- https://finance.yahoo.com/quote/AAPL/financials?p=AAPL

取得関数
- si.get_revenue() <= こちらの利用はやめる
- si.get_income_statement(ticker, yearly = True)
```
> df.columns
DatetimeIndex(['2020-12-31', '2019-12-31', '2018-12-31', '2017-12-31'], dtype='datetime64[ns]', name='endDate', freq=None)
> df.index
Index(['researchDevelopment', 'effectOfAccountingCharges', 'incomeBeforeTax',
       'minorityInterest', 'netIncome', 'sellingGeneralAdministrative',
       'grossProfit', 'ebit', 'operatingIncome', 'otherOperatingExpenses',
       'interestExpense', 'extraordinaryItems', 'nonRecurring', 'otherItems',
       'incomeTaxExpense', 'totalRevenue', 'totalOperatingExpenses',
       'costOfRevenue', 'totalOtherIncomeExpenseNet', 'discontinuedOperations',
       'netIncomeFromContinuingOps', 'netIncomeApplicableToCommonShares'],
      dtype='object', name='Breakdown')
```      
主要な情報
- Total revenue (売上高, totalRevenue) : revenue
- Operating Income (営業利益, operatingIncome)
- Pretax Income (税引き前利益, incomeBeforeTax)
- Net Income Common Stockholders (当期利益, netIncome) : earnings


### Balance Sheet

取得関数 : si.get_balance_sheet(ticker, yearly = True)

- Share Issued (発行株式数) <= これの取得は現状不可らしい

### Cash Flow

主要な情報

- Operating Cash Flows (営業キャッシュフロー) : 売上高(revenue)から原材料費などの支出を引いた現金収支
- Investing Cash Flows (投資キャッシュフロー) : 保有資産(土地，株)の売却による入金
- Financing Cash Flows (財務キャッシュフロー): 借入金や社債発行による入金
- Net Income from Continuing Operation (当期利益(?) 上の"Income Statement"のNet Income Common Stockholdersと同じ額)


## スクリーニング

参考資料
- [【外国株式】営業キャッシュフローによる銘柄選び
](https://www.sbisec.co.jp/ETGate/?OutSide=on&_ControlID=WPLETmgR001Control&_PageID=WPLETmgR001Mdtl20&_DataStoreID=DSWPLETmgR001Control&_ActionID=DefaultAID&getFlg=on&burl=search_market&cat1=market&cat2=report&dir=report&file=market_report_fo_hiro_161121.html)

主要な情報

1. operating cash flows (営業キャッシュフロー) 
    - その年の純利益よりも大きくないといけない。(operating cash flow vs earnings)
    - 毎年増えてないといけない。
    - ここまでは1株あたりで評価すると良い
    - 「営業キャッシュフロー/売上高」(営業キャッシュフロー・マージン)が15-30%あること(OCF/revenue)
        - ODF: https://www.investopedia.com/terms/o/operating-cash-flow-margin.asp
2. investing cash flows (投資キャッシュフロー) 
3. financing cash flows (財務キャッシュフロー) 
- (1,2,3)が(+,-,+)はgood

## そのほか
- gross profit margin = (revenue - "Cost of goods sold")/revenue
- operating margin
    - operating income/revenue
    - 高いのは大事。倒産しにくい(by 高橋ダン)
- [profit margin vs operating margin](https://www.investopedia.com/ask/answers/010815/what-difference-between-gross-profit-margin-and-operating-profit-margin.asp)
- operating cash flow margin
    - oprating cash flow/revenue
    - measures how efficiently a company converts sales into cash. It is a good indicator of earnings quality
    - operating marginには減価償却費が含まれるが，operating cash flow marginには減価償却費などの非現金支出は含まれない

## Yahoo finance での記載
- profit margin = Net Income Avi to Common/revenue


