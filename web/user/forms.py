from django import forms
from django.contrib.auth.forms import AuthenticationForm
from user.models import User

class UserLogInForm(AuthenticationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'input-box',
        'placeholder' : 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' : 'input-box',
        'placeholder' : 'Password'
    }))

    
