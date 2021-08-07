from django.urls import path

from api.views import stocks_last_price


urlpatterns = [
    path('stocks-last-price', stocks_last_price, name='stocks_last_price'),
path('stocks-last-price', stocks_last_price, name='stocks_last_price'),
]
