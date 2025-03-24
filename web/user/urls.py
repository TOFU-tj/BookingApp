from django.urls import path
from user.views import UserLogIn, UserRegistrations
from . import views
app_name = 'user'

urlpatterns = [
    path('login/', UserLogIn.as_view(), name='login'),
    path('registration/', UserRegistrations.as_view(), name='registration'),
    path('logout/', views.logout, name='logout')
    
    
]
