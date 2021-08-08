from django.urls import path

from paper_trade.views import dashboard

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
]
