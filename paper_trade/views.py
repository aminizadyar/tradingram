from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import OrderForm
from api.models import Symbol
from .models import Order
from .models import Portfolio

@login_required
@transaction.atomic
def symbol_page(request,symbol):
    obj = Symbol.objects.get(symbol__iexact=symbol)
    form = OrderForm(request.POST)
    if form.is_valid():
        order = Order()
        order.price=request.POST.get('price')
        order.quantity=request.POST.get('quantity')
        order.direction=request.POST.get('direction')
        order.symbol=obj
        order.user=request.user
        order.save()
        portfolio = Portfolio()
        portfolio.symbol = obj
        portfolio.user = request.user
        portfolio.quantity = request.POST.get('quantity')
        portfolio.save()

    else:
        form = OrderForm()

    context = {"obj": obj, "form": form}
    return render(request, 'paper_trade/ticker_page.html', context)
