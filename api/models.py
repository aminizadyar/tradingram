from django.db import models

class Stock(models.Model):
    ticker = models.CharField(max_length=30,unique=True)
    last_price = models.IntegerField(default=0)
