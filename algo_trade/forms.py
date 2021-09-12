from django import forms
from api.models import ETF

class SectorForm(forms.Form):
    OPTIONS = ETF.SECTOR_CHOICES
    sectors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)


class ETFForm(forms.Form):
    etfs = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                        choices=[])
    def __init__(self, CHOICES =None , *args, **kwargs):
        super(ETFForm, self).__init__(*args, **kwargs)
        if CHOICES:
            self.fields['etfs'] = forms.MultipleChoiceField(choices=CHOICES)