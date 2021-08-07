import yfinance as yf
from api.models import ForexPair


def get_forex_live_data():
    pairs = list(ForexPair.objects.all().values_list('ticker', flat=True))

    for pair in pairs:

        obj=ForexPair.objects.get(ticker=pair)
        data = round(yf.download(tickers=(pair+'=X'), period='1d', interval='1m').iloc[-1]['Close'],5)
        obj.bid= data + 0.00028
        obj.ask= data - 0.00028
        obj.save()

    return
