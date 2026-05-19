import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

# explicit import (production-safe)
import apps.accounts.tasks

# AUTO DISCOVER TASKS
app.autodiscover_tasks()