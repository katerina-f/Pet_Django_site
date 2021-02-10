from custom_cian.celery import app

from .logic import send_information_email


@app.task
def send_email_task(recipients, template_name, subject, **kwargs):
    send_information_email(recipients, template_name, subject, **kwargs)
