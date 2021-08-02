from django.shortcuts import render
from api.stock import fetch

def stocks_last_price(request):
    context = {"data" :fetch.get_stocks_last_price()}
    return render(request, 'api/stocks_last_price.html', context)


# Create your views here.
