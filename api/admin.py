from django.contrib import admin
from api.models import Stock
from api.models import CryptoCurrency
from api.models import ForexPair


admin.site.register(Stock)
admin.site.register(CryptoCurrency)
admin.site.register(ForexPair)