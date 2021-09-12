from django import forms
from api.models import ETF

class SectorForm(forms.Form):
    OPTIONS = ETF.SECTOR_CHOICES
    sectors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)