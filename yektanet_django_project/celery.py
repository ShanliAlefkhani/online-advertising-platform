from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yektanet_django_project.settings')

app = Celery('yektanet_django_project', broker='pyamqp://shanli:shanli@localhost')

# app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
