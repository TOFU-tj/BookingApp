from django.urls import path
from user.views import UserLogIn
from . import views
app_name = 'user'

urlpatterns = [
    path('login/', UserLogIn.as_view(), name='login'),
    path('logout/', views.logout, name='logout')
    
]
