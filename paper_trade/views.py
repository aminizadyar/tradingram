from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import OrderOpenPositionForm
from .forms import OrderClosePositionForm
from api.models import Symbol
from .models import OpenPosition,OrderClosePosition,OrderOpenPosition
from .match_engine_v2 import open_order_match_engine, close_order_match_engine

def markets_page(request):
    qs = Symbol.objects.all()
    context = {'qs': qs}
    return render(request, 'paper_trade/markets_page.html', context)


@login_required
@transaction.atomic
def symbol_page(request,symbol):
    state_open_order_status = "insert your order and open a new position"
    state_close_order_status = "choose one of your existing positions and fully/partially close it "
    symbol_of_interest = Symbol.objects.get(symbol__iexact=symbol)
    open_positions = OpenPosition.objects.filter(user=request.user,symbol=symbol_of_interest)

    if request.method == 'POST':
        if 'open_order' in request.POST:
            order_open_position_form = OrderOpenPositionForm(request.POST,prefix='open_order')
            if order_open_position_form.is_valid():
                open_order = OrderOpenPosition()
                open_order.input_price = order_open_position_form.cleaned_data['input_price']
                open_order.quantity = order_open_position_form.cleaned_data['quantity']
                open_order.direction = order_open_position_form.cleaned_data['direction']
                open_order.leverage = order_open_position_form.cleaned_data['leverage']
                open_order.take_profit = order_open_position_form.cleaned_data['take_profit']
                open_order.stop_loss = order_open_position_form.cleaned_data['stop_loss']
                open_order.symbol = symbol_of_interest
                open_order.user = request.user
                open_order.save()
                state_open_order_status = open_order_match_engine(open_order,request.user,symbol_of_interest)
            order_close_position_form = OrderClosePositionForm(prefix='close_order')
        elif 'close_order' in request.POST:
            order_close_position_form = OrderClosePositionForm(request.POST, prefix='close_order')
            if order_close_position_form.is_valid():
                close_order = OrderClosePosition()
                close_order.input_price = order_close_position_form.cleaned_data['input_price']
                close_order.quantity = order_close_position_form.cleaned_data['quantity']
                close_order.symbol = symbol_of_interest
                close_order.user = request.user
                close_order.save()
                state_close_order_status = close_order_match_engine(close_order, request.user, symbol_of_interest)
            order_open_position_form = OrderOpenPositionForm(prefix='open_order')
    else:
        order_open_position_form = OrderOpenPositionForm(prefix='open_order')
        order_close_position_form = OrderClosePositionForm(prefix='close_order')

    context = {"ticker": symbol_of_interest,
               "open_positions" : open_positions,
               "order_open_position_form": order_open_position_form,
               "order_close_position_form": order_close_position_form,
               "state_open_order_status": state_open_order_status,
               "state_close_order_status": state_close_order_status,
               "user": request.user}
    return render(request, 'paper_trade/ticker_page.html', context)


