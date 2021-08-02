import yfinance as yf
def get_stocks_last_price():
    stocks=['MSFT', 'AAPL' ,'GOOG','AMZN','FB','TSLA','BRK-A',
            'TSM','TCEHY','BABA','V','NVDA','005930.KS',
            'JPM','JNJ','LVMUY','WMT','UNH','MA','NSRGY','HD','PG',
            'RHHBY','BAC','PYPL','DIS','ASML','ADBE','CMCSA',
            'NKE','OR.PA','TM','KO','XOM','ORCL','PFE','CRM','LLY',
             'CSCO','VZ','NFLX','INTC','PEP','ABT','DHR']

    tickers = yf.Tickers(stocks)

    stocks_last_price={}
    for symbol in stocks:
        stocks_last_price[symbol]=round(tickers.tickers[symbol].history(period="1m").iloc[0]['Close'],2)
    return  stocks_last_price

