from django.contrib import admin
from .models import Order
from .models import OpenPositionOrder
from .models import Portfolio
from .models import Position
from .models import OrderOpenPosition
from .models import OrderClosePosition


admin.site.register(Order)
admin.site.register(OpenPositionOrder)
admin.site.register(Portfolio)
admin.site.register(Position)
admin.site.register(OrderOpenPosition)
admin.site.register(OrderClosePosition)
