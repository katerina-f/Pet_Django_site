from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, get_connection


def send_information_email(recipients, template_name, subject, **kwargs):
    """Функция для отправки информационных писем пользователям """
    with get_connection() as conn:
        messages = [create_email(rec, template_name, subject, **kwargs) for rec in recipients]
        conn.send_messages(messages)


def create_email(user, template_name, subject, **kwargs):
    data = {"username": user["username"], "site_name": "Custom Cian"}
    data.update(kwargs)
    html_body = render_to_string(template_name, data)
    msg = EmailMultiAlternatives(subject=subject, to=[user["email"], ])
    msg.attach_alternative(html_body, "text/html")
    return msg
