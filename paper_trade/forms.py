from django import forms
from .models import OrderOpenPosition
from .models import OrderClosePosition


class OrderOpenPositionForm(forms.ModelForm):
    class Meta:
        model = OrderOpenPosition
        fields = ('input_price', 'initial_quantity', 'direction','leverage','take_profit','stop_loss','signal_text')

class OrderClosePositionForm(forms.ModelForm):
    open_position_id = forms.IntegerField(label='Open_position_id', required=True)
    class Meta:
        model = OrderClosePosition
        fields = ('input_price', 'quantity')