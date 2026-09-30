from django.core.mail import send_mail
from django.conf import settings


def sendEmail(username, email):
    subject = "Welcome to Invictus App"
    body = """
    This is an Onboarding message from the team.
    Welcome aboard!
    """

    send_mail(
        subject,
        body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )