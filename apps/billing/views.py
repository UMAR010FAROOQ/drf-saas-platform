from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.response import Response
from rest_framework import status

from apps.billing.serializers import (
    UpgradePlanSerializer
)

from apps.billing.services import (
    BillingService
)

from apps.subscriptions.models import Plan


class UpgradePlanView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):
        x = undefined_variable

        serializer = UpgradePlanSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        org = request.organization

        plan_code = serializer.validated_data["plan"]

        plan = Plan.objects.filter(
            code=plan_code,
            is_active=True
        ).first()

        if not plan:

            return Response(
                {
                    "error": "Invalid plan"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        result = BillingService.change_plan(
            org=org,
            new_plan=plan,
            request=request
        )

        return Response(
            {
                "message": (
                    "Plan updated successfully"
                ),
                "data": result
            }
            
        )