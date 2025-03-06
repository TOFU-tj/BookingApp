from django.urls import path 
from . import views
from client_web.views import ClientServicesListView, WorkScheduleListView, BasketTemplateView
app_name = 'client'

urlpatterns = [
    path('<slug:slug_company>/<slug:slug_username>/basket_list/', BasketTemplateView.as_view(), name='basket_list'),
    path('<slug:slug_company>/<slug:slug_username>/basket_remove/<int:item_id>/', views.remove_from_basket, name='remove'),

     
     
     
    path('<slug:slug_company>/<slug:slug_username>/add_to_basket/', views.add_to_basket, name='add_to_basket'),
    # path('<slug:slug_company>/<slug:slug_username>/client_services/', ClientServicesListView.as_view(), name='client_services'),
    path('<slug:slug_company>/<slug:slug_username>/client_services/', views.ClientServicesListView.as_view(), name='client_services'),
    path('<slug:slug_company>/<slug:slug_username>/client_schedule/', WorkScheduleListView.as_view(), name='client_schedule' ),
]
