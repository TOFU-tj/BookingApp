# urls.py
from django.urls import path
from . import views
from client_web.views import ClientServicesListView

app_name = 'main'

urlpatterns = [
    path('', views.MainPage.as_view(), name="main"),
    path('success', views.SuccessPage.as_view(), name="success_page"),
    path('order', views.OrderViews.as_view(), name="order"),
    path('client_web_page/<slug:slug_company>/<slug:slug_username>/client_services/', 
         ClientServicesListView.as_view(), name='client_services'),
    path('generate_link/', views.generate_client_service_link, name='generate_link'),
    path('record/<int:pk>/delete/', views.RecordDeleteView.as_view(), name='delete_record'),

]

