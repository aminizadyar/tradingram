from django.urls import path

from .views import *

urlpatterns = [
    path('markets', markets_page, name='markets_page'),
    path('markets/<slug:symbol>/', symbol_page, name='symbol_page'),
]
