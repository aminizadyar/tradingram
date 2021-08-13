from django.contrib import admin
from .models import Order
from .models import OpenPositionOrder
from .models import Portfolio

admin.site.register(Order)
admin.site.register(OpenPositionOrder)
admin.site.register(Portfolio)