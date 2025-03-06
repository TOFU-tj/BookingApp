from django.urls import path, include
from api.views import ServiceListAPIView, WorkScheduleApiView
from rest_framework import routers


app_name = 'api'  

from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'services/(?P<username>[\w-]+)/(?P<company_slug>[\w-]+)', ServiceListAPIView, basename='service')
router.register(r'work-schedule/(?P<username>[\w-]+)/(?P<company_slug>[\w-]+)', WorkScheduleApiView, basename='work_schedule')

urlpatterns = [
    path('', include(router.urls)), 
]
