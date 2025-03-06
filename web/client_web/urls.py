from django.urls import path 
from client_web.views import ClientServicesListView, WorkScheduleListView
app_name = 'client'

urlpatterns = [
    path('client/', ClientServicesListView.as_view(), name='client_services' ),
    path('client_schedule/', WorkScheduleListView.as_view(), name='client_schedule' ),
]
