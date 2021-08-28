from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True

class SignInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True,  widget=forms.TextInput(attrs={'placeholder': 'Enter Your Username'}))
    password = forms.CharField(label='Password', max_length=100,required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Enter Your Password'}) )

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. enter a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username has already been taken!')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email has already been taken!')
        return email

