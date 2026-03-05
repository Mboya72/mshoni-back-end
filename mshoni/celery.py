import os
from celery import Celery

# This MUST match the inner folder name too
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mshoni.settings')

app = Celery('mshoni')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()