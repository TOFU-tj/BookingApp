from django import forms
from client_web.models import Order, WorkSchedule
from phonenumber_field.widgets import PhoneNumberPrefixWidget





class UserBlank(forms.ModelForm):
    select_schedule = forms.ModelChoiceField(
        queryset=WorkSchedule.objects.filter(is_available=True),
        empty_label="Выберите дату",
        widget=forms.Select(attrs={"class": "input-field"})
    )

    class Meta:
        model = Order
        fields = ["name", "surname", "phone", "email", "text", "select_schedule"]

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




# class UserBlank(forms.ModelForm):
#     select_schedule = forms.ModelChoiceField(
#         queryset=WorkSchedule.objects.filter(is_available=True),
#         empty_label="Выберите дату",
#         widget=forms.Select(attrs={"class": "input-field"})
#     )

#     class Meta:
#         model = UserForm
#         fields = ["name", "surname", "phone", "email", "text", "select_schedule"]

#         widgets = {
#             "name": forms.TextInput(attrs={
#                 'class': 'input-field', 
#                 "placeholder": "Ваше имя"
#             }),
#             "surname": forms.TextInput(attrs={
#                 'class': 'input-field', 
#                 "placeholder": "Ваша Фамилия"
#             }),
#             "phone": forms.TextInput(attrs={
#                 'class': 'input-field', 
#                 "placeholder": "Ваш телефон"
#             }),
#             "email": forms.EmailInput(attrs={
#                 'class': 'input-field', 
#                 "placeholder": "Ваш Email"
#             }),
#             "text": forms.Textarea(attrs={
#                 'class': 'input-field', 
#                 "placeholder": "Дополнительная информация",
#                 "rows": 4
#             })
#         }
