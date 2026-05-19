from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from apps.organizations.models import Organization, Membership


class OrganizationJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        user_auth_tuple = super().authenticate(request)

        if user_auth_tuple is None:
            return None

        user, token = user_auth_tuple

        request.organization = None
        request.role = None

        org_id = request.headers.get("X-Organization-ID")

        if org_id:
            membership = Membership.objects.filter(
                user=user,
                organization_id=org_id
            ).select_related("organization").first()

            if not membership:
                raise AuthenticationFailed("Invalid organization or access denied")

            request.organization = membership.organization
            request.role = membership.role

        return (user, token)