from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import OrderOpenPositionForm
from .forms import OrderClosePositionForm
from social_media.forms import PostForm
from api.models import Symbol
from .models import OrderClosePosition,OrderOpenPosition
from social_media.models import Post
from .match_engine import open_order_match_engine, close_order_match_engine
from .calculator import market_specific_leverages

def markets_page(request):
    qs = Symbol.objects.all()
    context = {'qs': qs}
    return render(request, 'paper_trade/markets_page.html', context)


@login_required
@transaction.atomic
def symbol_page(request,symbol):
    state_open_order_status = "Insert your order and open a new position"
    state_close_order_status = "Choose one of your existing positions and fully/partially close it "
    symbol_of_interest = Symbol.objects.get(symbol__iexact=symbol)
    state_post_status = "What do you think about " + symbol_of_interest.symbol + "? Publist it!"
    open_positions = [obj for obj in OrderOpenPosition.objects.filter(symbol=symbol_of_interest ,user = request.user) if obj.is_an_open_position]
    all_posts = Post.objects.filter(related_symbol=symbol_of_interest)

    leverage_choices = market_specific_leverages(symbol_of_interest.market)

    if request.method == 'POST':
        if 'open_order' in request.POST:
            order_open_position_form = OrderOpenPositionForm(leverage_choices,request.POST,prefix='open_order')
            if order_open_position_form.is_valid():
                open_order = OrderOpenPosition()
                open_order.input_price = order_open_position_form.cleaned_data['input_price']
                open_order.initial_quantity = order_open_position_form.cleaned_data['initial_quantity']
                open_order.direction = order_open_position_form.cleaned_data['direction']
                open_order.leverage = int(order_open_position_form.cleaned_data['leverage'])
                open_order.take_profit = order_open_position_form.cleaned_data['take_profit']
                open_order.stop_loss = order_open_position_form.cleaned_data['stop_loss']
                open_order.symbol = symbol_of_interest
                open_order.user = request.user
                open_order.signal = order_open_position_form.cleaned_data['signal_text']
                open_order.save()
                state_open_order_status = open_order_match_engine(open_order)
            order_close_position_form = OrderClosePositionForm(prefix='close_order')
            post_form = PostForm(prefix='post')
        elif 'close_order' in request.POST:
            order_close_position_form = OrderClosePositionForm(request.POST, prefix='close_order')
            if order_close_position_form.is_valid():
                close_order = OrderClosePosition()
                close_order.input_price = order_close_position_form.cleaned_data['input_price']
                close_order.quantity = order_close_position_form.cleaned_data['quantity']
                close_order.related_open_order = OrderOpenPosition.objects.get(id=order_close_position_form.cleaned_data['open_position_id'])
                close_order.save()
                state_close_order_status = close_order_match_engine(close_order)
            order_open_position_form = OrderOpenPositionForm(leverage_choices,prefix='open_order')
            post_form = PostForm(prefix='post')

        elif 'post' in request.POST:
            post_form = PostForm(request.POST, prefix='post')
            if post_form.is_valid():
                published_post = Post()
                published_post.user = request.user
                published_post.related_symbol = symbol_of_interest
                published_post.text_content = post_form.cleaned_data['text_content']
                published_post.symbol_initial_ask_price = symbol_of_interest.ask
                published_post.symbol_initial_bid_price = symbol_of_interest.bid
                published_post.save()
            order_open_position_form = OrderOpenPositionForm(leverage_choices,prefix='open_order')
            order_close_position_form = OrderClosePositionForm(prefix='close_order')
    else:
        order_open_position_form = OrderOpenPositionForm(leverage_choices,prefix='open_order')
        order_close_position_form = OrderClosePositionForm(prefix='close_order')
        post_form = PostForm(prefix='post')

    context = {"ticker": symbol_of_interest,
               "open_positions" : open_positions,
               "order_open_position_form": order_open_position_form,
               "order_close_position_form": order_close_position_form,
               "post_form" : post_form,
               "state_open_order_status": state_open_order_status,
               "state_close_order_status": state_close_order_status,
               "state_post_status": state_post_status,
               "user": request.user,
               "all_posts": all_posts,
               }
    return render(request, 'paper_trade/ticker_page.html', context)


