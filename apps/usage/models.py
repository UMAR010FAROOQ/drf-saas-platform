from django.db import models

from apps.organizations.models import Organization


class UsageRecord(models.Model):

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="usage_records"
    )

    month = models.DateField()

    total_requests = models.PositiveIntegerField(default=0)

    successful_requests = models.PositiveIntegerField(default=0)

    failed_requests = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("organization", "month")

        indexes = [
            models.Index(fields=["organization", "month"]),
        ]

    def __str__(self):
        return f"{self.organization.name} - {self.month}"


class APIRequestLog(models.Model):

    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="api_logs"
    )

    endpoint = models.CharField(max_length=255)

    method = models.CharField(max_length=10)

    status_code = models.PositiveIntegerField()

    response_time_ms = models.PositiveIntegerField()

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    user_agent = models.TextField(
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        indexes = [
            models.Index(fields=["organization"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["status_code"]),
        ]

        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.method} {self.endpoint} ({self.status_code})"