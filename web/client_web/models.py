from django.db import models
from services.models import ServiceModel, WorkSchedule
from django.contrib.auth import get_user_model

User = get_user_model()

class Basket(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, blank=True, null=True)  # Для анонимных пользователей
    service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Basket"
        verbose_name_plural = "Baskets"

    def __str__(self):
        return f"{self.service.name}"



