from custom_cian.celery import app

from .logic import send_information_email


@app.task
def send_email_task(rec, template_name, subject, **kwargs):
    send_information_email(rec, template_name, subject, **kwargs)
