from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from price_app.config import UPDATE_PRICES_CRON_SCHEDULE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lr_server.settings")

app = Celery("lr_server")
app.conf.enable_utc = True

app.config_from_object(settings, namespace="CELERY")

# Celery Beat Settings

app.conf.beat_schedule = {
    "update-prices-task": {
        "task": "price_app.tasks.update_cryptocurrency_prices",
        "schedule": UPDATE_PRICES_CRON_SCHEDULE,
        "description": "Task updates the token prices in db to the latest available from DefiLlama. NOTE: Only updates prices for tokens in TOKEN_ADDRESS_LIST, not any tokens added to db via GraphQL Mutations.",
    }
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
