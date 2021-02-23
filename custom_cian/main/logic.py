from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def send_information_email(rec, template_name, subject, **kwargs):
    """Функция для отправки информационных писем пользователям """
    message = create_email(rec, template_name, subject, **kwargs)
    message.send()


def create_email(user, template_name, subject, **kwargs):
    data = {"username": user["username"], "site_name": "Custom Cian"}
    data.update(kwargs)
    html_body = render_to_string(template_name, data)
    msg = EmailMultiAlternatives(subject=subject, to=[user["email"], ])
    msg.attach_alternative(html_body, "text/html")
    return msg
