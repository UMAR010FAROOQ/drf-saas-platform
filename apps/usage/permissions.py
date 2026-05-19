from rest_framework.permissions import BasePermission

from apps.usage.services import UsageService


class HasAvailableRequests(BasePermission):

    message = "Monthly API request limit exceeded"

    def has_permission(self, request, view):

        org = request.organization

        if not org:
            return False

        return UsageService.has_available_requests(org)