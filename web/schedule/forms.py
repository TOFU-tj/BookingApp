from django import forms
from .models import DaySchedule, TimeSlot

class DayScheduleForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)  # Теперь обрабатываем user правильно
        self.user = user  # Если надо использовать его в логике формы

    class Meta:
        model = DaySchedule
        fields = ['date', 'is_working_day']
        


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['start_time', 'end_time', 'is_available']