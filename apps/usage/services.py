from django.db import transaction
from django.db.models import F
from django.utils.timezone import now

from apps.subscriptions.services import SubscriptionService
from apps.usage.models import UsageRecord


class UsageService:

    @staticmethod
    def get_current_month():
        """
        Returns:
        2026-05-01
        """

        today = now().date()

        return today.replace(day=1)

    @staticmethod
    @transaction.atomic
    def increment_usage(org, status_code=None):

        month = UsageService.get_current_month()

        usage, created = UsageRecord.objects.get_or_create(
            organization=org,
            month=month,
            defaults={
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
            }
        )

        update_fields = {
            "total_requests": F("total_requests") + 1
        }

        if status_code:

            if 200 <= status_code < 400:
                update_fields["successful_requests"] = (
                    F("successful_requests") + 1
                )
            else:
                update_fields["failed_requests"] = (
                    F("failed_requests") + 1
                )

        UsageRecord.objects.filter(
            id=usage.id
        ).update(**update_fields)

    @staticmethod
    def get_current_usage(org):

        month = UsageService.get_current_month()

        usage = UsageRecord.objects.filter(
            organization=org,
            month=month
        ).first()

        if not usage:
            return 0

        return usage.total_requests

    @staticmethod
    def has_available_requests(org):

        subscription = (
            SubscriptionService.get_active_subscription(org)
        )

        if not subscription:
            return False

        limit = (
            subscription.plan.request_limit_per_month
        )

        current_usage = (
            UsageService.get_current_usage(org)
        )

        return current_usage < limit

    @staticmethod
    def get_remaining_requests(org):

        subscription = (
            SubscriptionService.get_active_subscription(org)
        )

        if not subscription:
            return 0

        limit = (
            subscription.plan.request_limit_per_month
        )

        current_usage = (
            UsageService.get_current_usage(org)
        )

        return max(limit - current_usage, 0)