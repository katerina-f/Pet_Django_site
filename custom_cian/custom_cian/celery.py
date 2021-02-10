from celery.schedulers import crontab


app.conf.beat_schedule = {
    "send_weakly_novelty_mail": {
        "task": "main.tasks.send_email_task",
        "schedule": crontab(day_of_week="mon", hour="09", minute="00"),
    },
}
