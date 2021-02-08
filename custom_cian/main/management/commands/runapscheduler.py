from datetime import datetime, timedelta
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from main.models import Subscriber, Realty
from main.logic import send_information_email


logger = logging.getLogger(__name__)


def send_email_job():
    subscribers = Subscriber.objects.all().select_related('user')
    puplished_range = [datetime.now(), datetime.now() - timedelta(days=7)]
    new_realty = Realty.objects.filter(published_at__range=published_range)
    send_information_email(subscribers, "main/email_templates/weakly_novelty_email.html",
                           "Новинки недели!", new_objects=new_realty)


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        scheduler.add_job(
            send_email_job,
            trigger=CronTrigger(
                day_of_week="mon", hour="09", minute="00"
            ),
            id="send_weakly_novelties",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'send_weakly_novelties'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
