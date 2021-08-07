from django.shortcuts import render
from .models import Stock
from .models import CryptoCurrency
from .models import ForexPair
from .models import FuturesContract


def stocks_last_price(request):

    qs = Stock.objects.all();
    context = {'qs': qs}
    return render(request, 'api/stocks_last_price.html', context)

def cryptocurrencies_last_price(request):

    qs = CryptoCurrency.objects.all();
    context = {'qs': qs}
    return render(request, 'api/cryptocurrencies_last_price.html', context)

def forex_live_data(request):

    qs = ForexPair.objects.all();
    context = {'qs': qs}
    return render(request, 'api/forex_live_data.html', context)

def futures_last_price(request):

    qs = FuturesContract.objects.all();
    context = {'qs': qs}
    return render(request, 'api/futures_last_price.html', context)