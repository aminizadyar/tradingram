from django.urls import path

from .views import algorithmic_trading_page

urlpatterns = [
    path('algorithmic-trading', algorithmic_trading_page, name='algorithmic_trading_page'),
]
