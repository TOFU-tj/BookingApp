from django.contrib import admin
from schedule.models import DaySchedule, TimeSlot, BusinessCalendar
# Register your models here.

admin.site.register(DaySchedule)
admin.site.register(BusinessCalendar)
admin.site.register(TimeSlot)
