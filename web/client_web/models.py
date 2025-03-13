from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from services.models import ServiceModel, WorkSchedule
from django.contrib.auth import get_user_model

User = get_user_model()

class Basket(models.Model):
    session_key = models.CharField(max_length=40, blank=True, null=True)  
    service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    executor = models.ForeignKey(User, on_delete=models.CASCADE)  # Исполнитель (специалист)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Basket"
        verbose_name_plural = "Baskets"

    def __str__(self):
        return f"{self.service.name} для {self.executor.username}"

    def serialize(self):
        """
        Сериализует данные корзины в формат JSON.
        """
        return {
            "service": self.service.name,
            "quantity": self.quantity,
            "price": str(self.service.price),  # Преобразуем цену в строку для JSON
        }


class UserForm(models.Model):
    name = models.CharField("First name", max_length=250, unique=False)
    surname = models.CharField("Surname", max_length=250, unique=False)
    phone = PhoneNumberField("Phone", unique=False)    
    email = models.EmailField("Email", unique=False)
    text = models.TextField("Comment", blank=True, null=True)
    select_schedule = models.ForeignKey(WorkSchedule, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)  # Добавляем session_key

    class Meta:
        verbose_name = ("UserForm")
        verbose_name_plural = ("UserForms")

    def __str__(self):
        return f'basket for {self.name}'


class SuccessModel(models.Model):
    name = models.ForeignKey(UserForm, on_delete=models.CASCADE)  # Клиент, который записался
    basket_history = models.JSONField(default=dict, blank=True)  # Поле для хранения истории корзины
    executor = models.ForeignKey(User, on_delete=models.CASCADE)  # Владелец компании (исполнитель)
    session_key = models.CharField(max_length=40, blank=True, null=True)  # Добавляем session_key
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания записи

    class Meta:
        verbose_name = "SuccessModel"
        verbose_name_plural = "SuccessModels"

    def __str__(self):
        return f"Success #{self.id}: {self.name.name} записан к {self.executor.username}"