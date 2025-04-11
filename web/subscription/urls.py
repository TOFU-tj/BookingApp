from django.urls import path 
from . import views 

app_name = 'subscription'

urlpatterns = [
    path('subscription/', views.create_checkout_session, name="subscription"),
    path('success/', views.success, name="success"),
    path('cancel/', views.cancel, name="cancel"),
    
]
