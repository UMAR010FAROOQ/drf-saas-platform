import hashlib
import secrets
from django.db import models
from django.utils import timezone
from apps.organizations.models import Organization


def hash_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode()).hexdigest()


class APIKey(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="api_keys"
    )

    name = models.CharField(max_length=255)

    # store ONLY hash
    key_hash = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        editable=False
    )

    # show only prefix (for UI/debug)
    key_prefix = models.CharField(max_length=8, editable=False, default="")

    scope = models.CharField(
        max_length=10,
        choices=[("read", "Read"), ("write", "Write")],
        default="read"
    )

    is_active = models.BooleanField(default=True)

    expires_at = models.DateTimeField(null=True, blank=True)

    last_used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rate_limit = models.IntegerField(default=1000)

    def set_key(self, raw_key: str):
        self.key_hash = hash_key(raw_key)
        self.key_prefix = raw_key[:8]

    def is_expired(self):
        return self.expires_at and self.expires_at < timezone.now()

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=["is_active"])    

    def __str__(self):
        return f"{self.name} ({self.organization})"
    
