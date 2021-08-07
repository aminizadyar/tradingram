from django.shortcuts import render
from .models import Stock

def stocks_last_price(request):

    qs = Stock.objects.all();
    context = {'qs': qs}
    return render(request, 'api/stocks_last_price.html', context)

def stocks_last_price(request):

    qs = Stock.objects.all();
    context = {'qs': qs}
    return render(request, 'api/stocks_last_price.html', context)

# Create your views here.
