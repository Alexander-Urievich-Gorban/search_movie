from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'conf.settings')
app = Celery('conf')
app.conf.enable_utc = False
app.conf.update(timezone='Europe/Moscow')

app.config_from_object(settings,
                       namespace='CELERY')


app.conf.beat_schedule = {
    'refresh-rating-every-minute':{
        'task':'movie.tasks.refresh_rating',
        'schedule': crontab(minute=1)
    }
}
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')