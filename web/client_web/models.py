from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from services.models import ServiceModel
from django.contrib.auth import get_user_model
from schedule.models import TimeSlot , DaySchedule
from django.urls import reverse

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
        """Сериализация данных для передачи в JSON."""
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
    date = models.DateField(null=True, blank=True)  # Добавляем поле для даты
    session_key = models.CharField(max_length=40, blank=True, null=True)  # Добавляем session_key

    class Meta:
        verbose_name = "UserForm"
        verbose_name_plural = "UserForms"

    def __str__(self):
        return f'Запись для {self.name}'




class SuccessModel(models.Model):
    name = models.ForeignKey(UserForm, on_delete=models.CASCADE)  # Клиент, который записался
    basket_history = models.JSONField(default=dict, blank=True)  # Поле для хранения истории корзины
    time_history = models.JSONField(default=dict, blank=True)  # Поле для хранения истории времени
    executor = models.ForeignKey(User, on_delete=models.CASCADE)  # Владелец компании (исполнитель)
    session_key = models.CharField(max_length=40, blank=True, null=True)  # Добавляем session_key
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания записи
    scheduled_date = models.DateField(null=True, blank=True)
    scheduled_time_slot = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "SuccessModel"
        verbose_name_plural = "SuccessModels"

    def __str__(self):
        return f"Запись #{self.id}: {self.name.name} записан к {self.executor.username}"

    def get_full_details(self):
    
        return {
            "client": {
                "name": self.name.name,
                "surname": self.name.surname,
                "email": self.name.email,
                "phone": self.name.phone,
            },
            "services": [
                {
                    "service": item.get("service"),
                    "quantity": item.get("quantity"),
                    "price": item.get("price"),
                }
                for item in self.basket_history.get("services", [])
            ],
            "selected_time": {
                "date": self.time_history.get("selected_date"),
                "time_slot": self.time_history.get("selected_time_slot"),
            },
            "executor": {
                "username": self.executor.username,
                "company": self.executor.company.name if hasattr(self.executor, "company") else None,
            },
            "created_at": str(self.created_at),
        }
    
    
class ClientSchedule(models.Model):
    
    executor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True  # Разрешаем пустые значения
    )
    date = models.ForeignKey(
        DaySchedule, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    time_slot = models.ForeignKey(
        TimeSlot, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    session_key = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        verbose_name = "ClientSchedule"
        verbose_name_plural = "ClientSchedules"

    def __str__(self):
        return f"Выбранное время для {self.executor}, дата: {self.date}, слот: {self.time_slot}"

    def serialize(self):
        return {
            "executor": self.executor.username if self.executor else None,
            "date": str(self.date.date) if self.date else None,
            "time_slot": f"{self.time_slot.start_time} - {self.time_slot.end_time}" if self.time_slot else None,
            "session_key": self.session_key,
        }