from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from django.utils import timezone


class TemporarySubscription(models.Model):
    session_key = models.CharField(max_length=40, blank=True, null=True)
    subscription_type = models.CharField(max_length=50)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()  # Дата окончания подписки
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "TemporarySubscription"
        verbose_name_plural = "TemporarySubscriptions"

    def save(self, *args, **kwargs):
        """
        Автоматически устанавливаем end_date при создании подписки.
        """
        if not self.end_date:
            self.end_date = now() + timedelta(days=40)  # Подписка длится 40 дней
        super().save(*args, **kwargs)

    def is_expired(self):

        return now() > self.end_date

    def renew_subscription(self):
        """
        Продлевает подписку на 40 дней.
        """
        self.end_date = now() + timedelta(days=40)
        self.is_active = True
        self.save()