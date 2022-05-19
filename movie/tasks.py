from django.db.models import Sum
from celery import shared_task
from .models import Movie
from conf.celery import app


@shared_task(bind=True)
def refresh_rating(self):
    for i in Movie.objects.all():
        i.get_rating()
    return 'ratings is update!'


@app.task
def aaa():
    print('hello denis')
    return 'helloaaa'

