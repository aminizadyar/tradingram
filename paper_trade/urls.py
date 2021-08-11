from django.urls import path

from paper_trade.views import symbol_page

urlpatterns = [
    path('tickers/<slug:symbol>/', symbol_page, name='symbol_page'),
]
