from django.db import models
from api.models import Symbol
from django.contrib.auth.models import User


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    quantity = models.FloatField(blank=False)

    def __str__(self):
        return self.user.username + " --- " + self.symbol.symbol + " --- Portfolio"

class Position(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    quantity = models.FloatField(blank=False)
    average_price = models.FloatField(blank=False)

    def __str__(self):
        return self.user.username + " --- " + self.symbol.symbol + " --- Portfolio"


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
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    price = models.FloatField(blank=False)
    price_matched = models.FloatField(blank=True,null=True)
    quantity = models.FloatField(blank=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    direction = models.CharField(max_length=1,choices=DIRECTION_CHOICES)
    result = models.CharField(max_length=1,choices=RESULT_CHOICES,default='F')

    def __str__(self):
        return self.user.username + " -- " + self.symbol.symbol +  " -- " +str(self.created_datetime) +"--" + self.get_result_display()+ "--" +self.get_direction_display() +"  Order"


class OpenPositionOrder(models.Model):
    DIRECTION_CHOICES = (
        ('L','Long'),
        ('S','Short'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    price = models.FloatField(blank=False)
    price_matched = models.FloatField(blank=True,null=True)
    quantity = models.IntegerField(blank=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    direction = models.CharField(max_length=1,choices=DIRECTION_CHOICES)

    def __str__(self):
        return self.user.username + " -- " + self.symbol.symbol +  " -- " +str(self.created_datetime) + "--" +self.get_direction_display() +"  Order"
