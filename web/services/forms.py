from services.models import ServiceModel
from django import forms
from services.models import ServiceModel, WorkSchedule, Appointment  # Исправили импорт


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
        fields = ['day_of_week', 'start_time', 'end_time', 'is_available']
        widgets = {
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'client_name', 'client_phone']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'client_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
        }

