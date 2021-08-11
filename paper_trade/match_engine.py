from .models import Portfolio

def simple_buy(order,user,symbol):
    if int(order.price) >= symbol.last_price:

        order.result = 'S'
        order.save()
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
        state = "your input price is lower than the market price"

    return state


