from django.urls import path 
from client_web.views import ClientServicesListView, WorkScheduleListView, basket_page
app_name = 'client'

urlpatterns = [
     path('basket_list/', basket_page, name='basket_list'),
    path('<slug:slug_company>/<slug:slug_username>/client_services/', ClientServicesListView.as_view(), name='client_services'),
    path('<slug:slug_company>/<slug:slug_username>/client_schedule/', WorkScheduleListView.as_view(), name='client_schedule' ),
]
