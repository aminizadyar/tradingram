from django.db import models
from api.models import Symbol
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

def profit_or_loss_calculator(current_price,open_price,quantity,symbol,direction):
    if symbol.market == 'FX':
        return ((current_price - open_price) * direction) * symbol.pip * symbol.pip_value * quantity
    else:
        return (current_price - open_price) * direction * quantity


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
    input_price = models.FloatField(blank=False,validators=[MinValueValidator(0,message="Enter a positive number")])
    matched_price = models.FloatField(blank=True,null=True)
    # quantity validators can be improved
    initial_quantity = models.FloatField(blank=False,validators=[MinValueValidator(0.000001,message="Enter a positive number")])
    current_quantity = models.FloatField(blank=True,null=True,default=0)
    initial_margin = models.FloatField(blank=True, null=True,default=0)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    direction = models.IntegerField(choices=DIRECTION_CHOICES)
    result = models.CharField(max_length=1,choices=RESULT_CHOICES,default='F')
    leverage = models.IntegerField(default=1,blank=True,validators=[MinValueValidator(0,message="Enter a positive number")])
    take_profit = models.FloatField(blank=True, null= True,validators=[MinValueValidator(0,message="Enter a positive number")])
    stop_loss = models.FloatField(blank=True, null=True,validators=[MinValueValidator(0,message="Enter a positive number")])
    signal_text = models.TextField(blank=True,null=True)

    class Meta:
        ordering = ['-created_datetime']
    def __str__(self):
        return "ID="+str(self.id) + " --- " + self.symbol.symbol + "---direction= " + self.get_direction_display() + "---initial quantity= " + str(self.initial_quantity) +  "---current quantity= " + str(self.current_quantity) +"---open price= " + str(self.matched_price) + '--blocked margin=' + str(self.blocked_margin) + '--unrealized gain='+str(self.unrealized_gain)

    @property
    def blocked_margin(self):
        if self.initial_margin == 0 or self.initial_quantity == 0:
            return 0
        else:
            return (self.current_quantity / self.initial_quantity) * self.initial_margin

    @property
    def is_an_open_position(self):
        if self.result == 'S' and self.current_quantity > 0:
            return True
        else:
            return False

    @property
    def unrealized_gain(self):
        if self.is_an_open_position:
            if self.direction == OrderOpenPosition.LONG:
                return profit_or_loss_calculator(self.symbol.bid,self.matched_price,self.current_quantity,self.symbol,self.direction)
            else:
                return profit_or_loss_calculator(self.symbol.ask, self.matched_price, self.current_quantity,self.symbol, self.direction)
        else:
            return 0

class OrderClosePosition(models.Model):
    RESULT_CHOICES = (
        ('S', 'Success'),
        ('F', 'Failure'),
    )
    related_open_order = models.ForeignKey(OrderOpenPosition, on_delete=models.CASCADE)
    input_price = models.FloatField(blank=False,validators=[MinValueValidator(0,message="Enter a positive number")])
    close_position_price = models.FloatField(blank=True,null=True)
    # quantity validators can be improved
    quantity = models.FloatField(blank=False,validators=[MinValueValidator(0.000001,message="Enter a positive number")])
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    result = models.CharField(max_length=1,choices=RESULT_CHOICES,default='F')
    freed_margin = models.FloatField(blank=True,null=True)
    def __str__(self):
        return "Close Order for: " +str(self.related_open_order.symbol)+ "---"  +self.related_open_order.get_direction_display()+'---Close price: '+ str(self.close_position_price) + " closed position "+str(self.quantity) +" Result= " + self.get_result_display()

    @property
    def realized_gain(self):
        if self.result == 'S':
            return profit_or_loss_calculator(self.close_position_price, self.related_open_order.matched_price, self.quantity,self.related_open_order.symbol, self.related_open_order.direction)
        else:
            return 0
