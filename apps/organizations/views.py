from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.organizations.permissions import IsOrgMember, IsOrgAdmin, HasFeaturePermission

from .services import OrganizationService
from .serializers import OrganizationSerializer


class OrganizationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get("name")

        org = OrganizationService.create_organization(
            user=request.user,
            name=name
        )

        return Response(OrganizationSerializer(org).data)

    
class OrganizationListView(APIView):
    permission_classes = [AllowAny, IsOrgMember]

    def get(self, request):
        # API Key (single org context)
        if request.organization and request.user is None:
            data = OrganizationSerializer(request.organization).data
            return Response([data])

        # JWT user (multiple orgs)
        orgs = OrganizationService.get_user_organizations(request.user)
        data = OrganizationSerializer(orgs, many=True).data
        return Response(data)
    
    


class OrgDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsOrgMember]

    def get(self, request):
        return Response({
            "message": "Welcome member",
            "org": request.organization.name
        })    


class OrgManageView(APIView):
    permission_classes = [IsAuthenticated, IsOrgAdmin]

    def post(self, request):
        return Response({"message": "Admin action successful"})

