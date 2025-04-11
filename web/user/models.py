from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from subscription.models import TemporarySubscription
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class User(AbstractUser):
    subscription = models.OneToOneField(
        TemporarySubscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    company_name = models.CharField(max_length=255, blank=True, null=True)
    slug_username = models.SlugField(unique=True, blank=True, null=True)
    slug_company = models.SlugField(unique=False, blank=True, null=True)

    def clean_username(self):
        if self.username:
            username = self.username.replace(' ', '_').lower()
            return username
        return self.username

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_staff = True

        if not self.slug_username:
            self.slug_username = slugify(self.username)

        if not self.slug_company and self.company_name:
            self.slug_company = slugify(self.company_name)

        super().save(*args, **kwargs)

    def delete_if_subscription_expired(self):
        """
        Удаляет пользователя, если подписка истекла.
        """
        if self.subscription and self.subscription.is_expired():
            logger.info(f"Deleting user with expired subscription: {self.username}")
            self.delete()