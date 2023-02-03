from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def detectUser(user):
    # to detect user type on login
    if user.role == 1:
        redirectUrl = 'sellerDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'customerDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = 'admin'
        return redirectUrl


def send_notification_email(mail_subject, mail_template, to_email, context):
    from_email = settings.DEFAUTL_FROM_EMAIL
    message = render_to_string(mail_template, context)
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()
