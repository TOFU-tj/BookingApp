from django import forms
from client_web.models import UserForm, ClientSchedule
from schedule.models import TimeSlot, DaySchedule

class UserBlank(forms.ModelForm):

    class Meta:
        model = UserForm
        fields = ["name", "surname", "phone", "email", "text"]

        widgets = {
            "name": forms.TextInput(attrs={
                'class': 'input-field', 
                "placeholder": "Ваше имя"
            }),
            "surname": forms.TextInput(attrs={
                'class': 'input-field', 
                "placeholder": "Ваша Фамилия"
            }),
            "phone": forms.TextInput(attrs={
                'class': 'input-field', 
                "placeholder": "Ваш телефон"
            }),
            "email": forms.EmailInput(attrs={
                'class': 'input-field', 
                "placeholder": "Ваш Email"
            }),
            "text": forms.Textarea(attrs={
                'class': 'input-field', 
                "placeholder": "Дополнительная информация",
                "rows": 4
            })
        }


class ClientScheduleForm(forms.ModelForm):
    select_day = forms.ModelChoiceField(
        queryset=DaySchedule.objects.none(),
        empty_label="Выберите дату",
        widget=forms.Select(attrs={"class": "input-field"})
    )
    select_time = forms.ModelChoiceField(
        queryset=TimeSlot.objects.none(),
        empty_label="Выберите время",
        widget=forms.Select(attrs={"class": "input-field"})
    )

    class Meta:
        model = ClientSchedule
        fields = ['select_day', 'select_time']

    def __init__(self, *args, **kwargs):
        executor = kwargs.pop("executor", None)  # Берём переданного исполнителя
        super().__init__(*args, **kwargs)

        if executor:
            self.fields["select_day"].queryset = DaySchedule.objects.filter(
                calendar__owner=executor,  # Фильтруем по исполнителю
                is_working_day=True
            )
            self.fields["select_time"].queryset = TimeSlot.objects.filter(
                schedule__calendar__owner=executor,  # Только слоты этого исполнителя
                is_available=True
            )
        else:
            self.fields["select_day"].queryset = DaySchedule.objects.filter(is_working_day=True)
            self.fields["select_time"].queryset = TimeSlot.objects.filter(is_available=True)
