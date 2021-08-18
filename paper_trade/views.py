from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import OrderForm
from api.models import Symbol
from .models import Order
from .match_engine import simple_buy , simple_sell , forex_match_engine_long, forex_match_engine_short

def markets_page(request):
    qs = Symbol.objects.all()
    context = {'qs': qs}
    return render(request, 'paper_trade/markets_page.html', context)


@login_required
@transaction.atomic
def symbol_page(request,symbol):
    state = "insert your order"
    symbol_of_interest = Symbol.objects.get(symbol__iexact=symbol)
    form = OrderForm(request.POST)
    if form.is_valid():
        order = Order()
        order.price=form.cleaned_data['price']
        order.quantity=form.cleaned_data['quantity']
        order.direction=form.cleaned_data['direction']
        order.symbol=symbol_of_interest
        order.user=request.user
        order.save()
        if symbol_of_interest.market != 'FX' :
            if order.direction == 'L':
                state = simple_buy(order,request.user,symbol_of_interest)
            else:
                state = simple_sell(order,request.user,symbol_of_interest)
        else:
            if order.direction == 'L':
                state = forex_match_engine_long(order,request.user,symbol_of_interest)
            else:
                state = forex_match_engine_short(order,request.user,symbol_of_interest)
    else:
        form = OrderForm()

    context = {"ticker": symbol_of_interest,
               "form": form ,
               "state" : state,
               "user":request.user}
    return render(request, 'paper_trade/ticker_page.html', context)
