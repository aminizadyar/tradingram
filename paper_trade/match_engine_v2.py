def open_order_match_engine(order,user,symbol):
    state = "you have entered open order match engine"
    return state

def close_order_match_engine(order,user,symbol):
    state = "you have entered close order match engine"
    return state

def profit_or_loss_calculator(current_price,open_price,quantity,symbol,direction):
    if symbol.market == 'FX':
        return ((current_price - open_price) * direction) * symbol.pip * symbol.pip_value * quantity
    else:
        return (current_price - open_price) * direction * quantity


def margin_calculator(ticker,order_quantity):
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

    def initial_margin(self):
        if self.symbol.market == 'FX':
            if self.symbol.numerator == 'USD':
                return (100000 * self.initial_quantity) / self.leverage
            if self.symbol.denominator == 'USD':
                return (self.symbol.last_price * 100000 * self.initial_quantity) / self.leverage
            usd_indexed = self.symbol.numerator + 'USD'
            symbol_indexed = 'USD' + self.symbol.numerator
            if Symbol.objects.filter(symbol=usd_indexed).exists():
                return ((Symbol.objects.get(symbol=usd_indexed).last_price) * 100000 * (self.initial_quantity)) / self.leverage
            else:
                return (100000 * self.initial_quantity) / (self.leverage * (Symbol.objects.get(symbol=symbol_indexed).last_price))
        else:
            return (self.initial_quantity * self.price_matched) / self.leverage