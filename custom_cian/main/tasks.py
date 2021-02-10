from datetime import datetime, timedelta

from .logic import send_information_email
from .models import Realty, Subscriber


def send_weakly_novelty_email():
    subscribers = [{"username": s.user.username, "email": s.user.email}
                   for s in Subscriber.objects.all()]
    published_range = [datetime.now() - timedelta(days=7), datetime.now()]
    new_realty = Realty.objects.filter(published_at__range=published_range)
    send_information_email(subscribers, "main/email_templates/weakly_novelty_email.html",
                           "Новинки недели!", new_objects=new_realty)
