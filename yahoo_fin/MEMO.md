## Yahoo financeのFinancials情報

## メモ
- 売上高: net sales / operating revenue  / total revenue
- net income / earning (純利益) : 大きな問題なくても負の場合あり(有価証券の評価損による場合など)

## Yahoo financeのquote情報

基本情報
- https://finance.yahoo.com/quote/AAPL?p=AAPL

取得関数
- si.get_quote_table()
- mi.get_valuation() (以下のstatics情報とともに取得)

## Yahoo financeのstatistics情報
- https://finance.yahoo.com/quote/NFLX/key-statistics?p=NFLX

取得関数

- i.get_stats_valuation()
- mi.get_valuation() (以下のstatics情報とともに取得)


## Yahoo financeのFinancials情報
### Income Statement

- https://finance.yahoo.com/quote/AAPL/financials?p=AAPL

取得関数
- si.get_revenue() <= こちらの利用はやめる
- si.get_income_statement(ticker, yearly = True)

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


