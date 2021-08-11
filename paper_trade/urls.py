from django.urls import path

from paper_trade.views import ticker_page

urlpatterns = [
    path('tickers/<slug:ticker>/', ticker_page, name='ticker'),
]
