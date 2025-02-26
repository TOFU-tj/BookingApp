from django.shortcuts import render
from django.views.generic.base import TemplateView

class MainViews(TemplateView): 
    template_name = 'main_page/main.html'