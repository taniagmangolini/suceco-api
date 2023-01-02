from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from app import settings
from .constants import RESET_PASSWORD_SUBJECT, EMAIL_TEMPLATE


def send_reset_password_email(data):
    """Send the reset password email."""
    data['subject'] = RESET_PASSWORD_SUBJECT
    data['template'] = EMAIL_TEMPLATE
    data['template_params'] = {
                               'url': data['url'],
                               'subject': RESET_PASSWORD_SUBJECT
                               }
    send_email(data)


def send_email(data):
    """Send email service."""
    html_message = render_to_string(data['template'],
                                    data['template_params'])
    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(data['subject'],
                                   plain_message,
                                   settings.EMAIL_FROM,
                                   [data['email']])

    email.attach_alternative(html_message, 'text/html')
    email.send()
