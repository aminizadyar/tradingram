from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import OrderForm
from api.models import Symbol
from .models import Order
from .match_engine import simple_buy

@login_required
@transaction.atomic
def symbol_page(request,symbol):
    state = "insert your order"
    symbol_of_interest = Symbol.objects.get(symbol__iexact=symbol)
    form = OrderForm(request.POST)
    if form.is_valid():
        order = Order()
        order.price=request.POST.get('price')
        order.quantity=request.POST.get('quantity')
        order.direction=request.POST.get('direction')
        order.symbol=symbol_of_interest
        order.user=request.user
        order.save()
        print (order.direction)
        if order.direction == 'L':
            state = simple_buy(order,request.user,symbol_of_interest)


    else:
        form = OrderForm()

    context = {"ticker": symbol_of_interest,
               "form": form ,
               "state" : state,
               "user":request.user}
    return render(request, 'paper_trade/ticker_page.html', context)
