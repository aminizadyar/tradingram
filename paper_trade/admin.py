from django.contrib import admin
from .models import OrderOpenPosition
from .models import OrderClosePosition

admin.site.register(OrderOpenPosition)
admin.site.register(OrderClosePosition)
