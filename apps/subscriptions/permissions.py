from rest_framework.permissions import BasePermission

from apps.subscriptions.services import SubscriptionService



class HasActiveSubscription(BasePermission):

    message = "Active subscription required"

    def has_permission(self, request, view):

        org = request.organization

        if not org:
            return False

        return SubscriptionService.has_active_subscription(org)



class HasFeatureAccess(BasePermission):

    message = (
        "Feature not available in your subscription"
    )

    def has_permission(self, request, view):

        org = getattr(request, "organization", None)

        if not org:
            return False

        required_feature = getattr(
            view,
            "required_feature",
            None
        )

        # endpoint requires no feature
        if not required_feature:
            return True

        return SubscriptionService.resolve_feature(
            org,
            required_feature
        )