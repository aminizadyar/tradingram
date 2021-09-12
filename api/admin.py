from django.contrib import admin
from api.models import Symbol
from api.models import ETF

admin.site.register(Symbol)
admin.site.register(ETF)