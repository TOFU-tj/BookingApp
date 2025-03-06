from django.urls import path, include
from api.views import ServiceListAPIView, WorkScheduleApiView
from rest_framework import routers


app_name = 'api'  


urlpatterns = [
    path('service/<str:username>/<slug:company_slug>/', ServiceListAPIView.as_view({'get': 'list', 'post': 'create'}), name='service-list'),
    path('work/<str:username>/<slug:company_slug>/', WorkScheduleApiView.as_view({'get': 'list', 'post': 'create'}), name='work-schedule'),
]
