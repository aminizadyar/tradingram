from .models import OrderOpenPosition
from .calculator import initial_margin_calculator

def open_order_match_engine(order):
    if order.direction == OrderOpenPosition.LONG and order.input_price < order.symbol.ask :
        return "Failed. You want to take a new long position in " + order.symbol.symbol +" .Your input price is lower than the market ask price."
    if order.direction == OrderOpenPosition.SHORT and order.input_price > order.symbol.bid :
        return "Failed. You want to take a new short position in " + order.symbol.symbol +" .Your input price is higher than the market bid price."
    if order.direction == OrderOpenPosition.LONG:
        matched_price = order.symbol.ask
    else:
        matched_price = order.symbol.bid
    required_margin = initial_margin_calculator(order,matched_price)
    if required_margin <= order.user.profile.free_margin:
        order.user.profile.free_margin -= required_margin
        order.user.profile.save()

        order.result = 'S'
        order.matched_price = matched_price
        order.current_quantity = order.initial_quantity
        order.initial_margin = required_margin
        order.save()
        return "Successful. You've taken a new " + order.get_direction_display() + " position in " + order.symbol.symbol
    else:
        return "Failed. You want to take a new " +  order.get_direction_display() + " position in " + order.symbol.symbol +" .You don't have enough free margin in your account."


def close_order_match_engine(order):
    if order.related_open_order.direction == OrderOpenPosition.SHORT and order.input_price < order.related_open_order.symbol.ask :
        return "Failed. You want to close a short position in " + order.related_open_order.symbol.symbol +" .Your input price is lower than the market ask price."
    if order.related_open_order.direction == OrderOpenPosition.LONG and order.input_price > order.related_open_order.symbol.bid :
        return "Failed. You want to close a long position in " + order.related_open_order.symbol.symbol +" .Your input price is higher than the market bid price."
    if order.related_open_order.direction == OrderOpenPosition.SHORT:
        close_position_price = order.related_open_order.symbol.ask
    else:
        close_position_price = order.related_open_order.symbol.bid
    if order.quantity <= order.related_open_order.current_quantity:
        freed_margin = (order.quantity / order.related_open_order.current_quantity) * order.related_open_order.blocked_margin

        order.result = 'S'
        order.close_position_price = close_position_price
        order.freed_margin = (order.quantity / order.related_open_order.current_quantity) * order.related_open_order.blocked_margin
        order.save()

        profit_or_loss=order.realized_gain
        order.related_open_order.user.profile.free_margin += freed_margin + profit_or_loss
        order.related_open_order.user.profile.save()

        order.related_open_order.current_quantity -= order.quantity
        order.related_open_order.save()
        return "Successful. You have closed " + str(order.quantity) + " of your existing " + order.related_open_order.get_direction_display() + " positions"
    else:
        return "Failed. You want to close/reduce your " +  order.related_open_order.get_direction_display() + " position in " + order.related_open_order.symbol.symbol +" .The quantity you entered is larger than your open position."






