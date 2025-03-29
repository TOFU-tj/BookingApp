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



class WorkSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Work Schedule"
        verbose_name_plural = "Work Schedules"
        ordering = ["schedule_date", "start_time"]

    def save(self, *args, **kwargs):

        if self.is_available is False: 
            self.is_available = True
        super(WorkSchedule, self).save(*args, **kwargs)

    def __str__(self):
        status = "✅ Рабочий" if self.is_available else "❌ Выходной"
        return f"{self.user} - {self.schedule_date}: {self.start_time} - {self.end_time} ({status})"




