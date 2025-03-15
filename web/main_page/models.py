from django.db import models
from django.core.mail import send_mail

class UserBlank(models.Model):
    name = models.CharField('First name', max_length=250)
    email = models.EmailField('Email')
    text = models.TextField('Comment')

    class Meta:
        verbose_name = ("User Blank")
        verbose_name_plural = ("User Blanks")

    def __str__(self):
        return self.name



