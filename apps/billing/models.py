from uuid import uuid4

from django.db import models
from django.utils.timezone import now

from apps.organizations.models import Organization
from apps.subscriptions.models import Plan


class Payment(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    transaction_id = models.UUIDField(
        default=uuid4,
        editable=False,
        unique=True
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    metadata = models.JSONField(
        default=dict,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        indexes = [
            models.Index(fields=["organization"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

        ordering = ["-created_at"]

    def mark_paid(self):

        self.status = "paid"
        self.paid_at = now()

        self.save(
            update_fields=[
                "status",
                "paid_at"
            ]
        )

    def __str__(self):

        return (
            f"{self.organization.name} - "
            f"{self.amount} - "
            f"{self.status}"
        )