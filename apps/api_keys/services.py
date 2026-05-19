import secrets
from apps.api_keys.models import APIKey
from apps.audit.services import AuditService

def create_api_key(org, name, scope="read", request=None):
    raw_key = secrets.token_hex(32)

    api_key = APIKey(
        organization=org,
        name=name,
        scope=scope,
    )
    api_key.set_key(raw_key)
    api_key.save()

    AuditService.log_action(
        action="create_api_key",
        resource_type="api_key",
        resource_id=api_key.id,
        organization=org,
        user=request.user if request else None,
        request=request,
        metadata={
            "name": name,
            "scope": scope,
        }
    )

    return raw_key, api_key