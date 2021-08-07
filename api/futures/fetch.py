import yfinance as yf
from api.models import FuturesContract


def get_futures_last_price():

    contracts = list(FuturesContract.objects.all().values_list('ticker', flat=True))
    for contract in contracts:

        obj=FuturesContract.objects.get(ticker=contract)
        data = round(yf.download(tickers=(contract+'=F'), period='1d', interval='1m').iloc[-1]['Close'],3)
        obj.last_price= data
        obj.save()

    return
