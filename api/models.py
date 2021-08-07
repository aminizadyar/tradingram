from django.db import models

class Stock(models.Model):
    ticker = models.CharField(max_length=30,unique=True)
    last_price = models.FloatField(default=0)

class CryptoCurrencies(models.Model):
    ticker = models.CharField(max_length=30,unique=True)
    last_price = models.FloatField(default=0)