from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from apps.usage.models import (
    UsageRecord,
    APIRequestLog
)


@shared_task
def cleanup_old_logs():

    cutoff_date = now() - timedelta(days=30)

    deleted_count, _ = APIRequestLog.objects.filter(
        created_at__lt=cutoff_date
    ).delete()

    return f"{deleted_count} logs deleted"


@shared_task
def reset_old_usage_records():

    current_month = now().date().replace(day=1)

    deleted_count, _ = UsageRecord.objects.exclude(
        month=current_month
    ).delete()

    return f"{deleted_count} usage records deleted"