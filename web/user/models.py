from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify



class User(AbstractUser):
    company_name = models.CharField(max_length=255, blank=True, null=True)
    slug_username = models.SlugField(unique=True, blank=True, null=True)
    slug_company = models.SlugField(unique=False, blank=True, null=True)
    
    def clean_username(self):
        """
        Нормализует username: заменяет пробелы на '_', приводит к нижнему регистру.
        """
        if self.username:
            # Заменяем пробелы на '_'
            username = self.username.replace(' ', '_')
            # Приводим к нижнему регистру
            username = username.lower()
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