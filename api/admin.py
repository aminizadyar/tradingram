from django.contrib import admin
from api.models import Stock
from api.models import CryptoCurrencies

admin.site.register(Stock)
admin.site.register(CryptoCurrencies)