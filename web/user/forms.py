from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from user.models import User
from django.core.exceptions import ValidationError

class UserLogInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input-box',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input-box',
        'placeholder': 'Password'
    }))




class UserRegistrationForm(UserCreationForm):
    name_and_surname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-box',
            'placeholder': 'Имя Фамилия'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-box',
            'placeholder': 'Username'
        })
    )
    
    company_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-box',
            'placeholder': 'Company name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input-box',
            'placeholder': 'Email'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-box',
            'placeholder': 'Введите пароль'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-box',
            'placeholder': 'Повторите пароль'
        })
    )

    class Meta:
        model = User
        fields = (
            'name_and_surname', 'username', 'email', 
            'company_name', 'password1', 'password2'
        )
        
    def save(self, commit=True):
        user = super().save(commit=False)  # Создаем объект, но не сохраняем его в БД
        if commit:
            user.save()  # Сохраняем объект в БД
        return user
    
    def clean_company_name(self):

        company_name = self.cleaned_data.get('company_name')
        if ' ' in company_name:
            raise ValidationError("Название компании не должно содержать пробелы.")
        if not company_name.replace('_', '').isalnum():
            raise ValidationError("Название компании может содержать только буквы, цифры и символ '_'.")
        return company_name.lower()  # Приводим к нижнему регистру
