from datetime import timedelta

from django.db import models
from django.utils import timezone

from apps.organizations.models import Organization


class Plan(models.Model):

    PLAN_TYPES = (
        ("free", "Free"),
        ("pro", "Pro"),
        ("enterprise", "Enterprise"),
    )

    name = models.CharField(
        max_length=50,
        unique=True
    )

    code = models.CharField(
        max_length=20,
        choices=PLAN_TYPES,
        unique=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    request_limit_per_month = models.PositiveIntegerField(
        default=1000
    )

    features = models.JSONField(
        default=dict,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Subscription(models.Model):

    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
        related_name="subscription"
    )

    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name="subscriptions"
    )

    start_date = models.DateTimeField(
        default=timezone.now
    )

    end_date = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    auto_renew = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def is_expired(self):
        return timezone.now() > self.end_date

    def remaining_days(self):
        delta = self.end_date - timezone.now()
        return max(delta.days, 0)

    def __str__(self):
        return f"{self.organization.name} -> {self.plan.name}"