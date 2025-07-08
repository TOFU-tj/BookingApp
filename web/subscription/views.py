import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from subscription.models import TemporarySubscription
from django.utils.timezone import now
from django.utils import timezone
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
import uuid
from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_SECRET_KEY




stripe.api_key = settings.STRIPE_SECRET_KEY
def create_checkout_session(request):
    subscription = {
        'basic': 'price_1RAEB1RxJwfPKHo0UFTlcOGl'
    }

    price_id = request.POST.get('price_id')
    if not price_id:
        return render(request, 'subscription/subscription_page.html', {'error': 'Price ID is required', 'subscription': subscription})

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{'price': price_id, 'quantity': 1}],
            mode='subscription',
            success_url=request.build_absolute_uri(reverse('user:registration')) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('subscription:cancel')),
        )

        print(f"Price ID: {price_id}")
        print(f"Stripe Checkout URL: {checkout_session.url}")

        
        subscription = TemporarySubscription.objects.create(
            session_key=checkout_session.id,
            subscription_type="basic",
            end_date=timezone.now() + timezone.timedelta(days=30),
            is_active=False
        )

        
        activation_link = request.build_absolute_uri(
            reverse('subscription:activate_subscription', args=[subscription.activation_token])
        )

        
        send_mail(
            subject='Активация вашей подписки',
            message=f'Спасибо за покупку! Пожалуйста, активируйте подписку по ссылке: {activation_link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.POST.get('email')],  # Получаем email из формы
        )

        return redirect(checkout_session.url, code=303)

    except Exception as e:
        print(f"Stripe Error: {e}")
        return render(request, 'main_page/main_page.html', {'error': str(e), 'subscription': subscription})

def activate_subscription(request, token):
    subscription = get_object_or_404(TemporarySubscription, activation_token=token)

    if not subscription.is_active:
        subscription.activate()
        messages.success(request, "Ваша подписка успешно активирована!")
    else:
        messages.info(request, "Эта подписка уже была активирована.")

    return redirect('user:profile')


def cancel_subscription(request, pk):

    user = request.user
    if not user.is_authenticated:
        messages.error(request, "Вы должны быть авторизованы для отмены подписки.")
        return redirect(reverse('user:profile'))

    try:
       
        subscription = get_object_or_404(
            TemporarySubscription,
            id=pk,
            user=user 
        )
    except TemporarySubscription.DoesNotExist:
        messages.error(request, "Подписка не найдена или уже отменена.")
        return redirect(reverse('user:profile'))

    # Отменяем подписку
    subscription.cancel()
    messages.success(request, f"Ваша подписка успешно отменена. Дата окончания: {subscription.end_date.strftime('%d.%m.%Y')}")

    return redirect(reverse('user:profile'))
    
def success(request):
    return render(request, 'subscription/success.html')


def cancel(request):
    return render(request, 'subscription/cancel.html')