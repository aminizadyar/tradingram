from django.urls import path

from .views import algorithmic_trading_page, etf_result_page, sector_page, etf_selection_page, etf_input_page

urlpatterns = [
    path('algorithmic-trading', algorithmic_trading_page, name='algorithmic_trading_page'),
    path('intelligent-portfolio/result/', etf_result_page, name='etf_result_page'),
    path('intelligent-portfolio/sectors/', sector_page, name='sector_page'),
    path('intelligent-portfolio/ETFs/', etf_selection_page, name='etf_selection_page'),
    path('intelligent-portfolio/inputs/', etf_input_page, name='etf_input_page'),
]
