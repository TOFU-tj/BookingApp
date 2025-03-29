from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta, time, datetime
from schedule.models import BusinessCalendar, DaySchedule, TimeSlot
from user.models import User

from datetime import timedelta, time, datetime



@receiver(post_save, sender=User)
def create_default_calendar(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        print(f"Creating calendar for user {instance.username}")  # Отладочная информация
        BusinessCalendar.objects.create(owner=instance)


            
            

@receiver(post_save, sender=DaySchedule)
def delete_past_days_signal(sender, **kwargs):
    print("Deleting past days...")  # Отладочная информация
    DaySchedule.delete_past_days()