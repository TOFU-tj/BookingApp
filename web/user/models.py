from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from subscription.models import TemporarySubscription

from django.utils import timezone

class User(AbstractUser):
    subscription = models.ForeignKey(TemporarySubscription, on_delete=models.CASCADE, blank=True, null=True)
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

    def is_subscription_expired(self):
        if self.subscription and self.subscription.end_date:
            return timezone.now() > self.subscription.end_date
        return False

    def extend_grace_period(self):
        if self.is_subscription_expired():
            self.subscription.end_date += timezone.timedelta(days=10)
            self.subscription.save()

    def delete_if_subscription_expired(self):
        if self.is_subscription_expired():
            self.delete()
    