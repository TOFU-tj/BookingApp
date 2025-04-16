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
    activation_token = models.UUIDField(default=uuid.uuid4, unique=True, null=True, blank=True)
    

    
    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = timezone.now() + timezone.timedelta(days=40)
        super().save(*args, **kwargs)

    def activate(self):
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