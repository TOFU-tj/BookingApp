from services.models import ServiceModel, ScheduleModel
from django import forms


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
    




class ScheduleModelForm(forms.ModelForm):
    class Meta:
        model = ScheduleModel
        fields = ['date', 'time', 'is_available']
        widgets = {
            'date': forms.TextInput(attrs={'class': 'datepicker', 'placeholder': 'Выберите дату'}),
            'time': forms.TextInput(attrs={'class': 'timepicker', 'placeholder': 'Выберите время'}),
        }
