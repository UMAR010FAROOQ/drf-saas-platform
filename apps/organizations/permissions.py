from rest_framework.permissions import BasePermission
from apps.organizations.models import Membership



class IsOrgMember(BasePermission):
    message = "You are not a member of this organization"

    def has_permission(self, request, view):
        return request.organization is not None




class IsOrgAdmin(BasePermission):
    message = "Admin access required"

    def has_permission(self, request, view):
        return request.role == "admin"
    



class HasFeaturePermission(BasePermission):
    message = "Feature not available in your subscription"

    def has_permission(self, request, view):
        org = request.organization

        if not org:
            return False

        # Example placeholder
        # Later: org.subscription.plan.features
        feature_required = getattr(view, "required_feature", None)

        if not feature_required:
            return True  # no feature required

        # TEMP: allow all
        return True