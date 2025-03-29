from django.urls import path
from .views import (
    ServiceView, ServiceAddView, ServiceDeleteView, ServiceUpdateView, 
)


app_name = 'service'

urlpatterns = [
    path('', ServiceView.as_view(), name='service_list'), 
    path('add/', ServiceAddView.as_view(), name='service_add'),
    path('delete/<int:pk>/', ServiceDeleteView.as_view(), name='service_delete'), 
    path('update/<int:pk>/', ServiceUpdateView.as_view(), name='service_update')
]
