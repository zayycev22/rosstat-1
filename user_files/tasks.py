import datetime

from django.db.models import ExpressionWrapper, DateTimeField, F

from global_settings.models import GlobalSettings
from rosstat.celery import app
from user_files.models import UserFile


@app.task(bind=True)
def delete_expired_files(self):
    now = datetime.datetime.now()
    settings = GlobalSettings.objects.get(id=1)
    lifetime_seconds = settings.file_lifetime_seconds
    files = UserFile.objects.annotate(
        expiry_date=ExpressionWrapper(F('created_exp') + datetime.timedelta(seconds=lifetime_seconds),
                                      output_field=DateTimeField())
    ).filter(expiry_date__lte=now)
    count, _ = files.delete()
    print(f"Удалено: {count} файлов")
