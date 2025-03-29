
from django.urls import path
from . import views
from main_page.views import OrderViews
from client_web.views import ScheduleView

app_name = 'client'

urlpatterns = [
    
    
    path('<slug:slug_company>/<slug:slug_username>/schedule/get-available-slots/', ScheduleView.as_view(), name='get_available_slots'),
    
    # Страница для выбора даты и времени
    path('<slug:slug_company>/<slug:slug_username>/schedule/', ScheduleView.as_view(), name='schedule'), 
    
    
    path('<slug:slug_company>/<slug:slug_username>/user_form/', views.UserFormView.as_view(), name='user_form'),
    
    

    path('<slug:slug_company>/<slug:slug_username>/client_services/', views.ClientServicesListView.as_view(), name='client_services'),

    path('<slug:slug_company>/<slug:slug_username>/client_basket/', views.BasketTemplateView.as_view(), name='client_basket'),


    path('<slug:slug_company>/<slug:slug_username>/add_to_basket/<int:item_id>/', views.add_to_basket, name='add_to_basket'),
    
    path('<slug:slug_company>/<slug:slug_username>/success/', views.SuccessView.as_view(), name='success'),
    
    path('<slug:slug_company>/<slug:slug_username>/basket/delete/<int:item_id>/', views.BasketDeleteView.as_view(), name="basket_delete"),
]



