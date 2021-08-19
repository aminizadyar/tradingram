from api.models import Symbol
from .models import OrderOpenPosition

# there is a copy of this function in .models. I did it to handle a bug. maybe the need for a copy can be eliminated later.
def profit_or_loss_calculator(current_price,open_price,quantity,symbol,direction):
    if symbol.market == 'FX':
        return ((current_price - open_price) * direction) * symbol.pip * symbol.pip_value * quantity
    else:
        return (current_price - open_price) * direction * quantity

def initial_margin_calculator(order,matched_price):
    ticker = order.symbol
    order_quantity = order.initial_quantity
    leverage = order.leverage
    direction = order.direction
    if ticker.market == 'FX':
        if ticker.numerator == 'USD':
            return (100000 * order_quantity) / leverage
        if ticker.denominator == 'USD':
            return (matched_price * 100000 * order_quantity) / leverage
        usd_indexed = ticker.numerator +'USD'
        symbol_indexed = 'USD' + ticker.numerator
        if Symbol.objects.filter(symbol=usd_indexed).exists():
            if direction == OrderOpenPosition.LONG:
                return ((Symbol.objects.get(symbol=usd_indexed).ask) * 100000 * (order_quantity)) / leverage
            else:
                return ((Symbol.objects.get(symbol=usd_indexed).bid) * 100000 * (order_quantity)) / leverage
        else :
            if direction == OrderOpenPosition.LONG:
                return (100000 * order_quantity) / (leverage * (Symbol.objects.get(symbol=symbol_indexed).bid))
            else:
                return (100000 * order_quantity) / (leverage * (Symbol.objects.get(symbol=symbol_indexed).ask))
    else:
        return (order_quantity * matched_price) / leverage