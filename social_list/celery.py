import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_list.settings')

app = Celery('social_list')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

