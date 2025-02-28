from django.contrib import admin

from services.models import ServiceModel, ScheduleModel

admin.site.register(ScheduleModel)

admin.site.register(ServiceModel)
