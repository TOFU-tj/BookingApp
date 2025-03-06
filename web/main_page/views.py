from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.urls import reverse

class MainViews(TemplateView): 
    template_name = 'main_page/main.html'
    
    


def generate_client_service_link(request):
    user = request.user

    # Ensure only the necessary fields are being used for URL reversal
    if user.is_authenticated and user.slug_company and user.slug_username:
        # Generate the link with the correct parameters only
        link = request.build_absolute_uri(reverse(
            'client:client_services', 
            kwargs={'slug_company': user.slug_company, 'slug_username': user.slug_username}
        ))
        return render(request, 'main_page/link.html', {'link': link})
    else:
        # If the necessary data is missing, return an error
        return render(request, 'main_page/link.html', {'error': 'Не удалось создать ссылку.'})
