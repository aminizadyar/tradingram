from .models import OrderOpenPosition
from .calculator import initial_margin_calculator

def open_order_match_engine(order,user):
    if order.direction == OrderOpenPosition.LONG and order.input_price < order.symbol.ask :
        return "Failed. You want to take a new long position in " + order.symbol.symbol +" .Your input price is lower than the market ask price."
    if order.direction == OrderOpenPosition.SHORT and order.input_price > order.symbol.bid :
        return "Failed. You want to take a new short position in " + order.symbol.symbol +" .Your input price is higher than the market bid price."
    if order.direction == OrderOpenPosition.LONG:
        matched_price = order.symbol.ask
    else:
        matched_price = order.symbol.bid
    required_margin = initial_margin_calculator(order,matched_price)
    if required_margin <= user.profile.free_margin:
        user.profile.free_margin -= required_margin
        user.profile.save()

        order.result = 'S'
        order.matched_price = matched_price
        order.current_quantity = order.initial_quantity
        order.initial_margin = required_margin
        order.save()
        return "Successful. You've taken a new " + order.get_direction_display() + " position in " + order.symbol.symbol
    else:
        return "Failed. You want to take a new " +  order.get_direction_display() + " position in " + order.symbol.symbol +" .You don't have enough free margin in your account."


def close_order_match_engine(order):
    state = "you have entered close order match engine"
    return state





