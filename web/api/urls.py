from django.urls import path, include
from api.views import ServiceListAPIView
from rest_framework import routers


app_name = 'api'  


router = routers.DefaultRouter()
router.register(r'service', ServiceListAPIView, basename='service')

urlpatterns = [
    path('', include(router.urls),  )
]
