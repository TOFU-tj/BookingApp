from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_activation_email(email, username, activation_link):
    send_mail(
        subject='Активация вашей подписки',
        message=f'Здравствуйте, {username}! Пожалуйста, подтвердите подписку, кликнув по ссылке: {activation_link}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
