from django.contrib import admin
from api.models import Stock
from api.models import CryptoCurrency
from api.models import ForexPair
from api.models import FuturesContract


admin.site.register(Stock)
admin.site.register(CryptoCurrency)
admin.site.register(ForexPair)
admin.site.register(FuturesContract)