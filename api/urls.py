from django.urls import path

from api.views import stocks_last_price
from api.views import cryptocurrencies_last_price
from api.views import forex_live_data


urlpatterns = [
    path('stocks-last-price', stocks_last_price, name='stocks_last_price'),
    path('cryptocurrencies-last-price', cryptocurrencies_last_price, name='cryptocurrencies_last_price'),
    path('forex-live-data', forex_live_data , name='forex_live_data'),
]
