from services.models import ServiceModel
from django import forms
from services.models import ServiceModel, WorkSchedule  


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
    


class WorkScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkSchedule
        fields = ['schedule_date', 'start_time', 'end_time', 'is_available']
        widgets = {
            'schedule_date': forms.SelectDateWidget(attrs={'class': 'form-control'}),  
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),  
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),  
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  
        }




