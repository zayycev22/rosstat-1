import datetime

from rosstat.celery import app
from user_files.models import UserFile


@app.task(bind=True)
def delete_expired_files(self):
    now = datetime.datetime.now()
    files = UserFile.objects.filter(created_exp__gt=now)
    count = files.delete()
    print(f"Удалено: {count} файлов")
