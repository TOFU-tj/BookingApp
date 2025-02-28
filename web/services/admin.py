from django.contrib import admin

from services.models import ServiceModel, WorkSchedule, Appointment  

admin.site.register(ServiceModel)
admin.site.register(WorkSchedule)
admin.site.register(Appointment)
