import yfinance as yf
from api.models import Index


def get_index_last_data():

    indices = list(Index.objects.all().values_list('ticker', flat=True))
    for index in indices:

        obj = Index.objects.get(ticker=index)
        data = round(yf.download(tickers=("^"+index), period='1d', interval='1m').iloc[-1]['Close'],3)
        obj.last_price= data
        obj.save()

    return
