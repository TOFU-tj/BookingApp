
# from django.urls import path
# from . import views

# app_name = 'client'

# urlpatterns = [
#     # Страница корзины
#     # path('<slug:slug_company>/<slug:slug_username>/basket_list/', views.BasketTemplateView.as_view(), name='basket_list'),

#     # Удаление товара из корзины
#     # path('<slug:slug_company>/<slug:slug_username>/basket_remove/<int:item_id>/', views.remove_from_basket, name='remove'),

#     # Страница формы для пользователя
#     # path('<slug:slug_company>/<slug:slug_username>/user_form/', views.UserBlancCreation.as_view(), name='user_form'),

#     # Добавление товара в корзину
#     # path('<slug:slug_company>/<slug:slug_username>/add_to_basket/<int:item_id>', views.add_to_basket, name='add_to_basket'),

#     # Страница с услугами
#     path('<slug:slug_company>/<slug:slug_username>/client_services/', views.ClientServicesListView.as_view(), name='client_services'),

#     # Страница успешного заказа (если она нужна)
#     # path('<slug:slug_company>/<slug:slug_username>/success/', views.SuccessOrder.as_view(), name='success_page'),
# ]

from django.urls import path
from . import views

app_name = 'client'

urlpatterns = [
    # Страница корзины
    # path('<slug:slug_company>/<slug:slug_username>/basket_list/', views.BasketView.as_view(), name='basket_list'), 

    # Страница для ввода данных пользователя
    path('<slug:slug_company>/<slug:slug_username>/user_form/', views.UserFormView.as_view(), name='user_form'),
    
    # Страница с услугами
    path('<slug:slug_company>/<slug:slug_username>/client_services/', views.ClientServicesListView.as_view(), name='client_services'),

    path('<slug:slug_company>/<slug:slug_username>/client_basket/', views.BasketTemplateView.as_view(), name='client_basket'),


    path('<slug:slug_company>/<slug:slug_username>/add_to_basket/<int:item_id>/', views.add_to_basket, name='add_to_basket'),
    
    path('<slug:slug_company>/<slug:slug_username>/success/', views.SuccessView.as_view(), name='success'),


]

