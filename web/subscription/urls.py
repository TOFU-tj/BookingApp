from django.urls import path 
from . import views 

app_name = 'subscription'

urlpatterns = [
    path('subscription/', views.create_checkout_session, name="subscription"),
    path('success/', views.success, name="success"),
    path('cancel/', views.cancel, name="cancel"),
    path('cancel_subscription/<int:pk> ', views.cancel_subscription, name='cancel_subscription'),
    path('activate/<uuid:token>/', views.activate_subscription, name='activate_subscription'),
    
]
