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
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=30, unique=True)
    last_price = models.FloatField(default=0)

    def __str__(self):
        return self.symbol
