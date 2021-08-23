from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import Post

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date','profile_picture','is_post_public','is_signal_public')

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text_content',)
