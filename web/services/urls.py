from django.urls import path
from .views import ServiceView, ServiceAddView, ServiceDeleteView, ServiceUpdateView, ScheduleListView, ScheduleCreateView

app_name = 'service'  

urlpatterns = [
    path('', ServiceView.as_view(), name='service_list'),
    path('schedule', ScheduleListView.as_view(), name='schedule'),
    
    
    
     path("schedule/add/", ScheduleCreateView.as_view(), name="schedule_add"),
     
     
     
    path('add/', ServiceAddView.as_view(), name='service_add'),
    path('delete/<int:pk>/', ServiceDeleteView.as_view(), name='service_delete'), 
    path('update/<int:pk>', ServiceUpdateView.as_view(), name='service_update')
]
