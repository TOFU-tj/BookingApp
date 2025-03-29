from django.db import models
from user.models import User
from django.conf import settings



class ServiceModel(models.Model):
    user = models.ForeignKey(User, verbose_name= "", on_delete=models.CASCADE)
    name = models.CharField('service', max_length=250)
    price = models.DecimalField('price',max_digits=6, decimal_places=2)
    description = models.TextField(blank = True, null=True)

    class Meta:
        verbose_name = ("Service")
        verbose_name_plural = ("Services")

    def __str__(self):
        return self.name

