from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_activation_email_task(subscription_id, activation_link):
    subscription = TemporarySubscription.objects.get(id=subscription_id)
    subject = "Активация подписки"
    message = (
        f"Здравствуйте!\n\n"
        f"Для активации вашей подписки перейдите по следующей ссылке:\n\n"
        f"{activation_link}\n\n"
        f"Спасибо, что выбрали наш сервис!"
    )
    recipient_list = [subscription.user.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)