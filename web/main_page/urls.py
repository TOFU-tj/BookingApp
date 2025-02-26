from django.urls import path 
from main_page.views import MainViews

app_name = 'main'

urlpatterns = [
    path('',MainViews.as_view(), name="main"),
    
]
