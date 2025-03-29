from django.db import models
from datetime import timedelta, time, datetime, date
from user.models import User
from django.conf import settings

class BusinessCalendar(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='calendar')
    name = models.CharField(max_length=255, default="Основной календарь")

    def __str__(self):
        return f"Календарь {self.owner.username}"


class DaySchedule(models.Model):
    calendar = models.ForeignKey(BusinessCalendar, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    is_working_day = models.BooleanField(default=True)

    def __str__(self):
        return f"Расписание на {self.date}"

    @property
    def status(self):
        return "Рабочий день" if self.is_working_day else "Выходной"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            self.create_time_slots()

    def create_time_slots(self):
        """Создает временные слоты с интервалом 15 минут от 6:00 до 23:00."""
        start_time = time(6, 0)  # Начало с 6:00
        end_time = time(23, 0)   # Конец до 23:00

        current_time = start_time
        while current_time < end_time:
            next_time = (datetime.combine(date.today(), current_time) + timedelta(minutes=15)).time()
            TimeSlot.objects.get_or_create(
                schedule=self,
                start_time=current_time,
                defaults={
                    'end_time': next_time,
                    'is_available': True
                }
            )
            current_time = next_time

    @staticmethod
    def delete_past_days():
        """
        Удаляет все прошедшие дни и связанные с ними временные слоты.
        """
        today = date.today()
        past_days = DaySchedule.objects.filter(date__lt=today)  # Все дни до сегодняшнего
        for day in past_days:
            day.time_slots.all().delete()  # Удаляем временные слоты
        past_days.delete()  # Удаляем сами дни

class TimeSlot(models.Model):
    schedule = models.ForeignKey(DaySchedule, on_delete=models.CASCADE, related_name='time_slots')
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"