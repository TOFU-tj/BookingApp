from services.models import ServiceModel
from django import forms
from services.models import ServiceModel  


class ServiceModelForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'input-box',
        'placeholder' : 'Название '
    }))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'input-box', 
        'placeholder' : 'Цена', 
    }))
    description = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class' : 'input-box',
        'placeholder' : 'Описание'
    }))
    
    class Meta : 
        model = ServiceModel
        fields = ['name', 'price', 'description']
    
