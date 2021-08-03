from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(label='username', max_length=100, required=True,  widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))
    email = forms.EmailField(label='email', max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(label='password', max_length=100,required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}) )