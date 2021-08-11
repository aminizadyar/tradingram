from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import OrderForm
from api.models import Ticker
from .models import Order

@login_required
@transaction.atomic
def ticker_page(request,ticker):
    obj = Ticker.objects.get(ticker=ticker.upper())
    form = OrderForm(request.POST)
    if form.is_valid():
        order = Order()
        order.price=request.POST.get('price')
        order.quantity=request.POST.get('quantity')
        order.direction=request.POST.get('direction')
        order.ticker=obj
        order.user=request.user
        order.save()

    else:
        form = OrderForm()

    context = {"obj": obj, "form": form}
    return render(request, 'paper_trade/ticker_page.html', context)
