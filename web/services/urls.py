from django.urls import path
from .views import (
    ServiceView, ServiceAddView, ServiceDeleteView, ServiceUpdateView, 
    WorkScheduleCreateView, WorkScheduleListView, WorkScheduleDelete
)


app_name = 'service'

urlpatterns = [
    path('', ServiceView.as_view(), name='service_list'),
    
    path("schedule/add/", WorkScheduleCreateView.as_view(), name="schedule_add"),
    path("schedule/delete/<int:pk>/", WorkScheduleDelete.as_view(), name="schedule_delete"),
    path("schedule/", WorkScheduleListView.as_view(), name="schedule_list"),
    
    # path("appointment/", AppointmentCreateView.as_view(), name="appointment"),
    
    path('add/', ServiceAddView.as_view(), name='service_add'),
    path('delete/<int:pk>/', ServiceDeleteView.as_view(), name='service_delete'), 
    path('update/<int:pk>/', ServiceUpdateView.as_view(), name='service_update')
]
