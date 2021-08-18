from django.db import models
from api.models import Symbol
from django.contrib.auth.models import User

class OrderOpenPosition(models.Model):
    LONG = 1
    SHORT = -1
    DIRECTION_CHOICES = (
        (LONG,'Long'),
        (SHORT,'Short'),
    )
    RESULT_CHOICES = (
        ('S', 'Success'),
        ('F', 'Failure'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    input_price = models.FloatField(blank=False)
    price_matched = models.FloatField(blank=True,null=True)
    quantity = models.FloatField(blank=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    direction = models.IntegerField(choices=DIRECTION_CHOICES)
    result = models.CharField(max_length=1,choices=RESULT_CHOICES,default='F')
    leverage = models.IntegerField(default=1,blank=True)
    take_profit = models.FloatField(blank=True , null= True)
    stop_loss = models.FloatField(blank=True,null=True)

    def __str__(self):
        return str(self.id) + " -- " + self.user.username + " -- " + self.symbol.symbol +  " -- " +str(self.created_datetime) +"--" + self.get_result_display()+ "--" +self.get_direction_display() +"  Order"

class OrderClosePosition(models.Model):
    LONG = 1
    SHORT = -1
    DIRECTION_CHOICES = (
        (LONG,'Long'),
        (SHORT,'Short'),
    )
    RESULT_CHOICES = (
        ('S', 'Success'),
        ('F', 'Failure'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    input_price = models.FloatField(blank=False)
    close_position_price = models.FloatField(blank=True,null=True)
    open_position_price = models.FloatField(blank=True,null=True)
    quantity = models.FloatField(blank=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    direction = models.IntegerField(choices=DIRECTION_CHOICES,blank=True, null=True)
    result = models.CharField(max_length=1,choices=RESULT_CHOICES,default='F')
    freed_margin = models.FloatField(blank=True,null=True)

    def __str__(self):
        return str(self.id) + " -- " + self.user.username + " -- " + self.symbol.symbol +  " -- " +str(self.created_datetime) +"--" + self.get_result_display()+ "--" +self.get_direction_display() +"  Order"



class OpenPosition(models.Model):
    LONG = 1
    SHORT = -1
    DIRECTION_CHOICES = (
        (LONG, 'Long'),
        (SHORT, 'Short'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    quantity = models.FloatField(blank=False)
    direction = models.IntegerField(choices=DIRECTION_CHOICES)
    matched_price = models.FloatField(blank=False)
    blocked_margin = models.FloatField(blank=False,null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    take_profit = models.FloatField(blank=True, null=True)
    stop_loss = models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(self.id) + " -- " + self.user.username + " --- " + self.symbol.symbol + " quantity= " + str(self.quantity) + " open price= " + str(self.matched_price) + " direction= " + self.get_direction_display()

class Position(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    quantity = models.FloatField(blank=False)
    average_price = models.FloatField(blank=False)
    blocked_margin = models.FloatField(blank=False,null=True)

    def __str__(self):
        return self.user.username + " --- " + self.symbol.symbol + " --- Portfolio"

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    quantity = models.FloatField(blank=False)

    def __str__(self):
        return  self.user.username + " --- " + self.symbol.symbol + " --- Portfolio"


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
