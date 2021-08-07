import yfinance as yf
from api.models import Stock


def get_stocks_last_price():
    stocks = list(Stock.objects.all().values_list('ticker', flat=True))
    tickers = yf.Tickers(stocks)
    for symbol in stocks:
        obj=Stock.objects.get(ticker=symbol)
        obj.last_price=round(tickers.tickers[symbol].history(period="1m").iloc[0]['Close'],2)
        obj.save()
    return

