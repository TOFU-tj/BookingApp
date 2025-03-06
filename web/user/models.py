from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.text import slugify


class User(AbstractUser):
    company_name = models.CharField(max_length=255, blank=True, null=True)
    slug_username = models.SlugField(unique=True, blank=True, null=True)
    slug_company = models.SlugField(unique=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug_username:
            self.slug_username = slugify(self.username)

        if not self.slug_company and self.company_name:
            self.slug_company = slugify(self.company_name)

        super().save(*args, **kwargs)
