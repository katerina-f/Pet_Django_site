from django.core.serializers import serialize

from .logic import send_information_email
from .models import Realty, Subscriber


def send_weakly_novelty_email():
    subscribers = [{"username": s.user.username, "email": s.user.email}
                   for s in Subscriber.objects.all()]
    puplished_range = [datetime.now(), datetime.now() - timedelta(days=7)]
    new_realty = serialize("json", Realty.objects.filter(published_at__range=published_range))
    new_realty = [r["fields"] for r in new_realty]
    send_information_email(subscribers, "main/email_templates/weakly_novelty_email.html",
                           "Новинки недели!", new_objects=new_realty)
