from django import forms
from api.models import ETF

class SectorForm(forms.Form):
    STYLE_CHOICES = (
        ('MD', 'Minimum Drawdown'),
        ('MG', 'Maximum Gain'),
        ('MV', 'Minimum Volatility'),
        ('MO', 'Maximum Outperform Duration'),
    )
    RISK_PREFERENCE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    METHOD_CHOICES = (
        ('CD', 'Customized Markowitz'),
        ('ES', 'Expected Shortfall'),
        ('LR', 'Linear Regression'),
        ('PR', 'Logistic Regression'),
        ('NN', 'Neural Networks'),
        ('TL', 'Transfer Learning'),
        ('RL', 'Reinforcement Learning'),
        ('SM', 'Support Vector Machines'),
    )

    OPTIONS = ETF.SECTOR_CHOICES
    sectors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)
    risk_preference = forms.ChoiceField(choices=RISK_PREFERENCE_CHOICES)
    style = forms.ChoiceField(choices=STYLE_CHOICES)
    method = forms.ChoiceField(choices=METHOD_CHOICES)
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
