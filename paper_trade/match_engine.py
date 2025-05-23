from .models import Portfolio
from .models import Position
from .models import OpenPositionOrder
from api.models import Symbol

def simple_sell(order,user,symbol):
    if float(order.price) <= symbol.bid:

        if Portfolio.objects.filter(user=user , symbol = symbol).exists():
            portfolio= Portfolio.objects.get(user=user, symbol=symbol)

            if float(order.quantity) <= portfolio.quantity :
                cash_earned = symbol.bid * float(order.quantity)
                user.profile.cash += cash_earned
                user.profile.save()
                order.result = 'S'
                order.price_matched= symbol.bid
                order.save()

                open_position_order=OpenPositionOrder()
                open_position_order.user = user
                open_position_order.symbol = symbol
                open_position_order.price = order.price
                open_position_order.price_matched = symbol.bid
                open_position_order.quantity = order.quantity
                open_position_order.direction = order.direction
                open_position_order.save()

                state = "your order has been successful"
                portfolio.quantity -= float(order.quantity)
                portfolio.save()

                if portfolio.quantity == 0 :
                    portfolio.delete()
                    OpenPositionOrder.objects.filter(user=user, symbol=symbol).delete()

            else:
                state = "you don't have enough of this ticker in your portfolio."

        else:
            state = "you don't have this ticker in your portfolio"

    else:
        state = "your input price is higher than the market bid price"

    return state


def simple_buy(order,user,symbol):
    if float(order.price) >= symbol.ask:

        cash_required= symbol.ask * float(order.quantity)
        if cash_required <= user.profile.cash :

            user.profile.cash -= cash_required
            user.profile.save()

            order.result = 'S'
            order.price_matched = symbol.ask
            order.save()

            open_position_order = OpenPositionOrder()
            open_position_order.user = user
            open_position_order.symbol = symbol
            open_position_order.price = order.price
            open_position_order.price_matched = symbol.ask
            open_position_order.quantity = order.quantity
            open_position_order.direction = order.direction
            open_position_order.save()

            state = "your order has been successful"

            if Portfolio.objects.filter(user=user , symbol = symbol).exists():
                updated_portfolio = Portfolio.objects.get(user=user, symbol=symbol)
                updated_portfolio.quantity += float(order.quantity)
                updated_portfolio.save()
            else :
                created_portfolio = Portfolio()
                created_portfolio.symbol = symbol
                created_portfolio.user = user
                created_portfolio.quantity = order.quantity
                created_portfolio.save()
        else:
            state = "you don't have enough cash to buy this ticker"
    else:
        state = "your input price is lower than the market ask price"

    return state


# in forex match engine, we must check if one of four different scenarios happen.
def forex_match_engine_long(order,user,symbol):
    if order.price >= symbol.ask :
        # first scenario is that the user has not taken any position in that in instrument before.
        if not Position.objects.filter(user=user, symbol=symbol).exists():
            state = forex_match_engine_new_position(order,user,symbol,symbol.ask)
        else:
            existing_position = Position.objects.get(user=user, symbol=symbol)
            # second scenario is that the user is taking a same direction position
            if (order.quantity) * (existing_position.quantity) > 0 :
                state = forex_match_engine_same_direction_position(order,user,symbol,symbol.ask,existing_position)
            else :
                if order.quantity + existing_position.quantity <= 0 :
                    # third scenario is that the user is closing its current positions.
                    state = forex_match_engine_opposite_direction_closing_position(order,user,symbol,symbol.ask,existing_position)
                else:
                    # the last scenario is that the user is closing its current positions and taking opposite positions
                    state = forex_match_engine_opposite_direction_opening_position(order,user,symbol,symbol.ask,existing_position)

    else:
        state = "your input price is lower than the market ask price"
    return state



def forex_match_engine_short(order,user,symbol):
    if order.price <= symbol.bid :
        # first scenario is that the user has not taken any position in that in instrument before.
        if not Position.objects.filter(user=user, symbol=symbol).exists():
            state = forex_match_engine_new_position(order,user,symbol,symbol.bid)
        else:
            existing_position = Position.objects.get(user=user, symbol=symbol)
            # second scenario is that the user is taking a same direction position
            # order quantity * -1 is for short positions
            if (order.quantity * -1) * (existing_position.quantity) > 0:
                state = forex_match_engine_same_direction_position(order, user, symbol, symbol.bid, existing_position)
            else:
                # third scenario is that the user is closing its current positions.
                if (order.quantity * -1) + existing_position.quantity >= 0:
                    state = forex_match_engine_opposite_direction_closing_position(order, user, symbol, symbol.bid , existing_position)
                else:
                    # the last scenario is that the user is closing its current positions and taking opposite positions
                    state = forex_match_engine_opposite_direction_opening_position(order, user, symbol, symbol.bid , existing_position)

    else:
        state = "your input price is higher than the market bid price"
    return state


def forex_margin_calculator(ticker,order_quantity,user):
    if ticker.numerator == 'USD':
        return (100000 * order_quantity) / user.profile.leverage
    if ticker.denominator == 'USD':
        return ((ticker.last_price) * 100000 * (order_quantity)) / user.profile.leverage
    usd_indexed = ticker.numerator +'USD'
    symbol_indexed = 'USD' + ticker.numerator
    if Symbol.objects.filter(symbol=usd_indexed).exists():
        return ((Symbol.objects.get(symbol=usd_indexed).last_price) * 100000 * (order_quantity)) / user.profile.leverage
    else :
        return (100000 * order_quantity) / (user.profile.leverage * (Symbol.objects.get(symbol=symbol_indexed).last_price))

def forex_match_engine_new_position(order,user,symbol,matched_price):
    # short positions must have negative quantity. in this part, we check the direction.
    if order.direction == 'L':
        direction = 1
    else:
        direction = -1
    required_margin = forex_margin_calculator(symbol,order.quantity,user)

    if required_margin <= user.profile.free_margin:

        user.profile.free_margin -= required_margin
        user.profile.save()

        order.result = 'S'
        order.price_matched = matched_price
        order.save()

        new_position = Position()
        new_position.user = user
        new_position.symbol = symbol
        new_position.quantity = order.quantity * direction
        new_position.average_price = matched_price
        new_position.blocked_margin = required_margin
        new_position.save()

        state = "your order has been successful, you have taken a new " + order.get_direction_display() + " position in " + symbol.name
    else:
        state = "you don't have enough free margin in your account to take this position"
    return state


def forex_match_engine_same_direction_position(order,user,symbol,matched_price,existing_position):
# short positions must have negative quantity. in this part, we check the direction.
    if order.direction == 'L':
        direction = 1
    else:
        direction = -1
    required_margin = forex_margin_calculator(symbol,order.quantity,user)

    if required_margin <= user.profile.free_margin:
        user.profile.free_margin -= required_margin
        user.profile.save()

        order.result = 'S'
        order.price_matched = matched_price
        order.save()

        existing_position.average_price = ((order.quantity*direction * matched_price) + (existing_position.quantity * existing_position.average_price)) / (existing_position.quantity + (order.quantity*direction))
        existing_position.quantity += order.quantity * direction
        existing_position.blocked_margin += required_margin
        existing_position.save()

        state = "your order has been successful, you have added to your " + order.get_direction_display() + " position in " + symbol.name

    else:
        state = "you don't have enough free margin in your account to take this position"
    return state

def forex_match_engine_opposite_direction_closing_position(order,user,symbol,matched_price,existing_position):
    if order.direction == 'L':
        closed_position = 'Short'
        direction = 1
    else:
        closed_position = 'Long'
        direction = -1

    order.result = 'S'
    order.price_matched = matched_price
    order.save()

    profit_or_loss = ((existing_position.average_price - matched_price) * direction) * symbol.pip * symbol.pip_value * order.quantity
    freed_margin = ((order.quantity * -1 * direction) / existing_position.quantity) * existing_position.blocked_margin
    user.profile.cash += profit_or_loss
    user.profile.free_margin += profit_or_loss + freed_margin
    user.profile.save()

    existing_position.quantity += order.quantity * direction
    existing_position.blocked_margin -= freed_margin
    if existing_position.quantity == 0 :
        existing_position.delete()
        state = "your order has been successful. you have closed all of your " + closed_position + " positions"
    else:
        existing_position.save()
        state = "your order has been successful. you have closed " + str(order.quantity) + " of your " + closed_position + " positions"


    return state


def forex_match_engine_opposite_direction_opening_position(order, user, symbol, matched_price, existing_position):
    if order.direction == 'L':
        direction = 1
        closed_position = 'Short'
    else:
        direction = -1
        closed_position = 'Long'

    opposite_position_quantity = order.quantity + existing_position.quantity * direction
    required_margin = forex_margin_calculator(symbol, opposite_position_quantity ,user)
    if required_margin <= (user.profile.free_margin + existing_position.blocked_margin) :

        order.result = 'S'
        order.price_matched = matched_price
        order.save()

        profit_or_loss = ((existing_position.average_price - matched_price) * -1) * symbol.pip * symbol.pip_value * existing_position.quantity
        user.profile.cash += profit_or_loss
        user.profile.free_margin += (profit_or_loss + existing_position.blocked_margin - required_margin)
        user.profile.save()

        existing_position.average_price = matched_price
        existing_position.quantity = opposite_position_quantity * direction
        existing_position.blocked_margin = required_margin
        existing_position.save()


        state = "your order has been successful. you have closed all of your previous " + closed_position + " positions. you have now opended " + str(opposite_position_quantity) + " new " + order.get_direction_display() + " positions"

    else:
        state = "you don't have enough free margin in your account to do this transaction"

    return state