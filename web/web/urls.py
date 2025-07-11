
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main_page.views import MainPage




urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', MainPage.as_view(), name='index'),
    
    path('', include('main_page.urls', namespace='main')),
     
    path('user/', include('user.urls', namespace='user')),
    
    path('services/', include('services.urls', namespace='services')),
    
    path('schedule/', include('schedule.urls', namespace='schedule')),
    
    path ('client_web_page/', include('client_web.urls', namespace='client_web')),
    
    path('subscription_page/', include('subscription.urls', namespace='subscription')), 
    
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)