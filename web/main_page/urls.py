# urls.py
from django.urls import path
from . import views
from client_web.views import ClientServicesListView

app_name = 'main'

urlpatterns = [
    path('', views.MainViews.as_view(), name="main"),
    path('client_web_page/<slug:slug_company>/<slug:slug_username>/client_services/', 
         ClientServicesListView.as_view(), name='client_services'),
    path('generate_link/', views.generate_client_service_link, name='generate_link'),
    path('record/<int:pk>/delete/', views.RecordDeleteView.as_view(), name='delete_record'),

]

