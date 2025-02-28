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
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Кто работает (мастер)
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('Monday', 'Понедельник'),
            ('Tuesday', 'Вторник'),
            ('Wednesday', 'Среда'),
            ('Thursday', 'Четверг'),
            ('Friday', 'Пятница'),
            ('Saturday', 'Суббота'),
            ('Sunday', 'Воскресенье'),
        ]
    )
    start_time = models.TimeField()  # Начало работы
    end_time = models.TimeField()    # Конец работы
    is_available = models.BooleanField(default=True)  # Рабочий ли день?

    def __str__(self):
        status = "✅ Рабочий" if self.is_available else "❌ Выходной"
        return f"{self.user} - {self.day_of_week}: {self.start_time} - {self.end_time} ({status})"


class Appointment(models.Model):
    master = models.ForeignKey(User, on_delete=models.CASCADE)  # К кому записались
    date = models.DateField()  
    time = models.TimeField()
    client_name = models.CharField(max_length=100)
    client_phone = models.CharField(max_length=20)
    is_confirmed = models.BooleanField(default=False)  # Подтверждена ли запись?

    class Meta:
        unique_together = ('master', 'date', 'time')  # Запрет на повторное бронирование одного времени

    def __str__(self):
        status = "✅ Подтверждено" if self.is_confirmed else "⏳ Ожидает подтверждения"
        return f"{self.client_name} записан к {self.master} на {self.date} {self.time} ({status})"

    
    
    
    
    
# class BookingModel(models.Model):
#     client_name = models.CharField(max_length=255)
#     phone = models.CharField(max_length=20)
#     service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE)
#     schedule = models.ForeignKey(ScheduleModel, on_delete=models.CASCADE)
    
#     class Meta:
#         verbose_name = ("BookingModel")
#         verbose_name_plural = ("BookingModels")

#     def __str__(self):
#         return f"{self.client_name} записан на {self.service.name} в {self.schedule.date} {self.schedule.time}"
