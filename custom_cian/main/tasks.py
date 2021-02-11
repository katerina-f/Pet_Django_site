from datetime import datetime, timedelta

from custom_cian.celery import app
from .logic import send_information_email
from .models import Realty, Subscriber


@app.task
def send_weakly_novelty_email():
    published_range = [datetime.now() - timedelta(days=7), datetime.now()]
    new_realty = Realty.objects.filter(published_at__range=published_range)
    for s in Subscriber.objects.all():
        send_information_email({"username": s.user.username, "email": s.user.email},
                                "main/email_templates/weakly_novelty_email.html",
                                "Новинки недели!", new_objects=new_realty)

@app.task
def send_email_task(rec, template_name, subject, **kwargs):
    send_information_email(rec, template_name, subject, **kwargs)
