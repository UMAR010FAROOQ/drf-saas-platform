from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from datetime import timedelta

from apps.api_keys.models import APIKey, hash_key


class APIKeyAuthentication(BaseAuthentication):

    def authenticate(self, request):
        raw_key = request.headers.get("X-API-KEY")

        if not raw_key:
            return None

        hashed = hash_key(raw_key)

        try:
            api_key = APIKey.objects.select_related("organization").get(
                key_hash=hashed,
                is_active=True
            )
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid API Key")

        if api_key.is_expired():
            raise AuthenticationFailed("API Key expired")

        # attach context
        request.organization = api_key.organization
        request.user = None
        request.role = "api"
        request.scope = api_key.scope

        if not api_key.last_used_at or (
        timezone.now() - api_key.last_used_at > timedelta(minutes=5)
    ):
            api_key.last_used_at = timezone.now()
            api_key.save(update_fields=["last_used_at"])

        return (None, None)