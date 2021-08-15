from django.db import models

class Stock(models.Model):
    ticker = models.CharField(max_length=30,unique=True)
    last_price = models.FloatField(default=0)

class CryptoCurrency(models.Model):
    name = models.CharField(max_length=30,unique=True)
    last_price = models.FloatField(default=0)

class ForexPair(models.Model):
    ticker = models.CharField(max_length=30,unique=True)
    bid = models.FloatField(default=0)
    ask = models.FloatField(default=0)

class FuturesContract(models.Model):
    name = models.CharField(max_length=30,unique=True)
    ticker = models.CharField(max_length=30, unique=True)
    last_price = models.FloatField(default=0)


class Index(models.Model):
    name = models.CharField(max_length=30,unique=True)
    ticker = models.CharField(max_length=30, unique=True)
    last_price = models.FloatField(default=0)


class Symbol(models.Model):
    MARKET_CHOICES = (
        ('FX', 'Forex'),
        ('ST', 'Stock'),
        ('CR', 'Cryptocurreny'),
        ('CF', 'CommodityFutures'),
        ('IN', 'Index'),
    )
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=30, unique=True)
    last_price = models.FloatField(default=0)
    spread = models.FloatField(default=0.001)
    market = models.CharField(max_length=2,choices=MARKET_CHOICES,default='ST')
    pip_value=models.FloatField(default=1)
    tick_size_of_price = models.IntegerField(default=5)
    minimum_quantity_decimal_point = models.IntegerField(default=5)

    def __str__(self):
        return self.symbol
    @property
    def bid(self):
        return self.last_price * (1 - self.spread)
    @property
    def ask(self):
        return self.last_price * (1 + self.spread)
    @property
    def numerator(self):
        return self.symbol[0:3]
    @property
    def denominator(self):
        return self.symbol[-3:]
