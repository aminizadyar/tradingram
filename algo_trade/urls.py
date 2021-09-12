from django.urls import path

from .views import algorithmic_trading_page, etf_optimizer_page

urlpatterns = [
    path('algorithmic-trading', algorithmic_trading_page, name='algorithmic_trading_page'),
    path('fund-of-funds-result', etf_optimizer_page, name='etf_optimizer_page'),
]
