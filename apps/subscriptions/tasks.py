from celery import shared_task
from django.utils.timezone import now

from apps.subscriptions.models import Subscription


@shared_task
def deactivate_expired_subscriptions():

    expired_subscriptions = Subscription.objects.filter(
        end_date__lt=now(),
        is_active=True
    )

    count = expired_subscriptions.update(
        is_active=False
    )

    return f"{count} subscriptions deactivated"