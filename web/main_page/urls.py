# urls.py
from django.urls import path
from . import views
from django.views.decorators.cache import cache_page
from main_page.views import OrderViews, MainPage

app_name = 'main'

urlpatterns = [
    path('', cache_page(30)(MainPage.as_view()), name="main"),
    path('success', views.SuccessPage.as_view(), name="success_page"),
    path('order', OrderViews.as_view(), name="order"),
    path('generate_link/', views.generate_client_service_link, name='generate_link'),
    path('record/<int:pk>/delete/', views.RecordDeleteView.as_view(), name='delete_record'),

]

