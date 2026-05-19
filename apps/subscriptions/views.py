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

    message = "Feature not available in current plan"

    def has_permission(self, request, view):

        org = request.organization

        if not org:
            return False

        feature = getattr(view, "required_feature", None)

        if not feature:
            return True

        return SubscriptionService.has_feature(
            org,
            feature
        )