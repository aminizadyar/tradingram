from pycoingecko import CoinGeckoAPI
from api.models import CryptoCurrency
coin_gecko = CoinGeckoAPI()


def get_cryptocurrencies_last_price():

    cryptocurrencies=list(CryptoCurrency.objects.all().values_list('name', flat=True))
    cryptocurrencies_last_price = coin_gecko.get_price(ids=cryptocurrencies, vs_currencies='usd')
    for cryptocurrency in cryptocurrencies_last_price :
        obj=CryptoCurrency.objects.get(name=cryptocurrency)
        obj.last_price=round(cryptocurrencies_last_price[cryptocurrency]['usd'],4)
        obj.save()
    return


