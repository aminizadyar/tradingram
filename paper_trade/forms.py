from django import forms
from .models import Order
from .models import OrderOpenPosition
from .models import OrderClosePosition


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('price', 'quantity', 'direction')


class OrderOpenPositionForm(forms.ModelForm):
    class Meta:
        model = OrderOpenPosition
        fields = ('input_price', 'initial_quantity', 'direction','leverage','take_profit','stop_loss')

class OrderClosePositionForm(forms.ModelForm):
    open_position_id = forms.IntegerField(label='open_position_id', required=True)
    class Meta:
        model = OrderClosePosition
        fields = ('input_price', 'quantity')