from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from django.utils import timezone
import uuid

class TemporarySubscription(models.Model):
    session_key = models.CharField(max_length=100, blank=True, null=True)
    subscription_type = models.CharField(max_length=50)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()  # Дата окончания подписки
    is_active = models.BooleanField(default=False)
    

    def save(self, *args, **kwargs):
        """
        Автоматически устанавливаем end_date при создании подписки.
        """
        if not self.end_date:
            self.end_date = timezone.now() + timezone.timedelta(days=40)  # Подписка длится 40 дней
        super().save(*args, **kwargs)

    def activate(self):
        """
        Активирует подписку.
        """
        self.is_active = True
        self.save()

    def cancel(self):
        """
        Отменяет подписку.
        """
        if self.is_active:
            self.is_active = False
            self.save()

    def is_expired(self):
        """
        Проверяет, истек ли срок действия подписки.
        """
        return timezone.now() > self.end_date

    def update_status(self):
        """
        Обновляет статус подписки: если срок истек, делает её неактивной.
        """
        if self.is_expired():
            self.is_active = False
            self.save()