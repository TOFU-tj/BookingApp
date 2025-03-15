from django import forms
from main_page.models import UserBlank

class UserBlankForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class" : "input-field", 
        "placeholder" : "Ваше имя"
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class" : "email-field", 
        "placeholder" : "Ваш email"
    }))
    
    text = forms.CharField(widget=forms.Textarea(attrs={
    "class": "text-field", 
    "placeholder": "Расскажите о вашем продукте и бизнесе"
    }))

    
    class Meta:
        model = UserBlank
        fields = ["name", "email", "text",]

    
