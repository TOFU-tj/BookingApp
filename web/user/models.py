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
    name_and_surname = models.TextField()
    
    
    def get_subscription_end_date(self):
        """
        Возвращает дату окончания подписки.
        """
        if self.subscription and self.subscription.end_date:
            return self.subscription.end_date.strftime('%d.%m.%Y')
        return "Нет активной подписки"

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
        
