from django.db import models

class Symbol(models.Model):
    MARKET_CHOICES = (
        ('FX', 'Forex'),
        ('ST', 'Stock'),
        ('CR', 'Cryptocurrency'),
        ('CF', 'CommodityFutures'),
        ('IN', 'Index'),
    )
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=30, unique=True)
    last_price = models.FloatField(default=0)
    spread = models.FloatField(default=0.001)
    market = models.CharField(max_length=2,choices=MARKET_CHOICES,default='ST')
    tick_size_of_price = models.IntegerField(default=5)
    minimum_quantity_decimal_point = models.IntegerField(default=5)
    description = models.TextField(null=True,blank=True)
    profile_picture = models.ImageField(null=False, upload_to='symbol-logo/',
                                        default='symbol_logo/default.png')
    # fields below are only useful for forex pairs
    pip = models.IntegerField(default=10000)

    def __str__(self):
        return self.symbol
    @property
    def bid(self):
        return round(self.last_price * (1 - self.spread),self.tick_size_of_price)
    @property
    def ask(self):
        return round(self.last_price * (1 + self.spread),self.tick_size_of_price)
    @property
    def numerator(self):
        return self.symbol[0:3]
    @property
    def denominator(self):
        return self.symbol[-3:]
    @property
    def pip_value(self):
        if self.denominator == 'USD':
            return 100000 / self.pip
        if self.numerator == 'USD':
            return 100000 / (self.pip * self.last_price)
        usd_indexed = self.numerator + 'USD'
        symbol_indexed = 'USD' + self.numerator
        if Symbol.objects.filter(symbol=usd_indexed).exists():
            return (100000 * Symbol.objects.get(symbol=usd_indexed).last_price) / (self.pip * self.last_price)
        else:
            return 100000 / (self.pip * Symbol.objects.get(symbol=symbol_indexed).last_price * self.last_price)
