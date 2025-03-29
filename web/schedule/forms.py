from django import forms
from .models import DaySchedule, TimeSlot

class DayScheduleForm(forms.ModelForm):
    class Meta:
        model = DaySchedule
        fields = ['date', 'is_working_day']  
        
        


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['start_time', 'end_time', 'is_available']