from django.contrib import admin

from services.models import ServiceModel, WorkSchedule  

admin.site.register(ServiceModel)
admin.site.register(WorkSchedule)

