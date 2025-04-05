from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

app_name = "schedule"

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('edit/<int:pk>/', views.edit_schedule, name='edit_schedule'),
    path('create-day/', views.CreateDay.as_view(), name='create_day'),
    path('delete/<int:pk>/', views.WorkDayDelete.as_view(), name='delete'),
    path('edit-time-slot/<int:pk>/', views.edit_time_slot, name='edit_time_slot'),  # Редактирование временного слота
    path('delete-time-slot/<int:pk>/', views.delete_time_slot, name='delete_time_slot'),  # Удаление временного слота
]