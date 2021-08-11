from django.contrib import admin
from .models import Order
from .models import PortfolioItem

admin.site.register(Order)
admin.site.register(PortfolioItem)