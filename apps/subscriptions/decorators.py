from functools import wraps

from rest_framework.exceptions import (
    PermissionDenied
)

from apps.subscriptions.services import (
    SubscriptionService
)


def require_feature(feature_name):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(
            view,
            request,
            *args,
            **kwargs
        ):

            org = getattr(
                request,
                "organization",
                None
            )

            if not org:
                raise PermissionDenied(
                    "Organization not found"
                )

            has_feature = (
                SubscriptionService.resolve_feature(
                    org,
                    feature_name
                )
            )

            if not has_feature:
                raise PermissionDenied(
                    f"{feature_name} feature required"
                )

            return view_func(
                view,
                request,
                *args,
                **kwargs
            )

        return wrapper

    return decorator