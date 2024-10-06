import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rosstat.settings")
app = Celery("rosstat")
app.config_from_object(settings, namespace="CELERY")

app.conf.beat_schedule = {
    'every_second': {
        'task': 'user_files.tasks.delete_expired_files',
        'schedule': crontab(hour="12", minute="0"),
    },
}

app.autodiscover_tasks()
