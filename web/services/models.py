from django.db import models
from user.models import User


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



class ScheduleModel(models.Model):
    date = models.DateField()
    time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('date', 'time')
        verbose_name = ("ScheduleModel")
        verbose_name_plural = ("ScheduleModels")

    def __str__(self):
        return f"{self.date} {self.time} - {'Свободно' if self.is_available else 'Занято'}"
    
    

    
class BookingModel(models.Model):
    client_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE)
    schedule = models.ForeignKey(ScheduleModel, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = ("BookingModel")
        verbose_name_plural = ("BookingModels")

    def __str__(self):
        return f"{self.client_name} записан на {self.service.name} в {self.schedule.date} {self.schedule.time}"
