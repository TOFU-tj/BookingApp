from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from services.models import ServiceModel, WorkSchedule
from django.contrib.auth import get_user_model


User = get_user_model()

class Basket(models.Model):
    session_key = models.CharField(max_length=40, blank=True, null=True)  
    service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Basket"
        verbose_name_plural = "Baskets"

    def __str__(self):
        return f"{self.service.name}"


class UserForm(models.Model):
    name = models.CharField("First name", max_length=250, unique=False)
    surname = models.CharField("Surname", max_length=250, unique=False)
    phone = PhoneNumberField("Phone", unique=False)    
    email = models.EmailField("Email", unique=False)
    text = models.TextField("Comment", blank=True, null=True)
    select_schedule = models.ForeignKey(WorkSchedule, on_delete=models.CASCADE, blank=True, null=True)
    Basket = models.ForeignKey(Basket, on_delete=models.CASCADE)


    class Meta:
        verbose_name = ("UserForm")
        verbose_name_plural = ("UserForms")

    def __str__(self):
        return f'basket for {self.name}'



