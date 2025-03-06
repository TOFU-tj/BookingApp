
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main_page.views import MainViews
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainViews.as_view(), name='index'),
    path('', include('main_page.urls', namespace='main')), 
    path('user/', include('user.urls', namespace='user')),
    path('services/', include('services.urls', namespace='services')),
    path('api/', include('api.urls')), 
    path('api-token-auth/', obtain_auth_token)
]

if settings.DEBUG: 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)