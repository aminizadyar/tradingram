from .models import Portfolio
from .models import OpenPositionOrder

def simple_sell(order,user,symbol):
    if float(order.price) <= symbol.bid:

        if Portfolio.objects.filter(user=user , symbol = symbol).exists():
            portfolio= Portfolio.objects.get(user=user, symbol=symbol)

            if int(order.quantity) <= portfolio.quantity :
                cash_earned = symbol.bid * int(order.quantity)
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
                portfolio.quantity -= int(order.quantity)
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

        cash_required= symbol.ask * int(order.quantity)
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
                updated_portfolio.quantity += int(order.quantity)
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


