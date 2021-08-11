from django.db import models
from api.models import Ticker
from django.contrib.auth.models import User


class PortfolioItem(User,Ticker):
    quantity = models.IntegerField(blank=False)


class Order(models.Model):
    DIRECTION_CHOICES = (
        ('L','Long'),
        ('S','Short'),
    )
    RESULT_CHOICES = (
        ('S', 'Success'),
        ('F', 'Failure'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    price = models.FloatField(blank=False)
    quantity = models.IntegerField(blank=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    direction = models.CharField(max_length=1,choices=DIRECTION_CHOICES)
    result = models.CharField(max_length=1,choices=RESULT_CHOICES,default='F')
