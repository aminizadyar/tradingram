from django.urls import path

from .views import symbol_page
from .views import markets_page

urlpatterns = [
    path('markets', markets_page, name='markets_page'),
    path('markets/<slug:symbol>/', symbol_page, name='symbol_page'),
    path('markets/<int:position_id>/', symbol_page, name='symbol_page'),
]
