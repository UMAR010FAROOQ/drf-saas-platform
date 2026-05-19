from apps.audit.models import AuditLog


class AuditService:

    @staticmethod
    def log_action(
        *,
        action,
        resource_type,
        resource_id,
        request=None,
        organization=None,
        user=None,
        metadata=None
    ):

        AuditLog.objects.create(
            organization=organization,
            user=user,
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id),
            metadata=metadata or {},
            ip_address=(
                request.META.get("REMOTE_ADDR")
                if request else None
            ),
            user_agent=(
                request.META.get(
                    "HTTP_USER_AGENT",
                    ""
                )
                if request else ""
            )
        )