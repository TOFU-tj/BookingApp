import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from subscription.models import TemporarySubscription
from django.utils.timezone import now
from django.utils import timezone
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    subscription = {
        'basic': 'price_1RAEB1RxJwfPKHo0UFTlcOGl'
    }

    price_id = request.POST.get('price_id')
    if not price_id:
        return render(request, 'subscription/subscription_page.html', {'error': 'Price ID is required', 'subscription': subscription})

    try:
        # Создаем сессию Stripe Checkout
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=request.build_absolute_uri(reverse('user:registration')) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('subscription:cancel')),
        )

        # Отладочный вывод
        print(f"Price ID: {price_id}")
        print(f"Stripe Checkout URL: {checkout_session.url}")

        # Сохраняем данные о подписке во временную модель
        TemporarySubscription.objects.create(
            session_key=checkout_session.id,
            subscription_type="basic",
            end_date=now() + timezone.timedelta(days=30),
            is_active=True
        )

        # Перенаправляем пользователя на страницу оплаты
        return redirect(checkout_session.url, code=303)

    except Exception as e:
        print(f"Stripe Error: {e}")
        return render(request, 'main_page/main_page.html', {'error': str(e), 'subscription': subscription})
    
    

def cancel_subscription(request, pk):
    """
    Отменяет подписку пользователя.
    """
    user = request.user
    if not user.is_authenticated:
        messages.error(request, "Вы должны быть авторизованы для отмены подписки.")
        return redirect(reverse('user:profile'))

    try:
        # Находим подписку, связанную с текущим пользователем
        subscription = get_object_or_404(
            TemporarySubscription,
            id=pk,
            user=user  # Убедитесь, что подписка принадлежит текущему пользователю
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