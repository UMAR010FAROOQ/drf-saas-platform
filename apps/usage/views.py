import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.subscriptions.permissions import (
    HasActiveSubscription,
    HasFeatureAccess
)

from apps.usage.permissions import (
    HasAvailableRequests
)

from apps.usage.services import UsageService
from apps.usage.models import APIRequestLog


class BaseAPIView(APIView):

    def dispatch(self, request, *args, **kwargs):

        request._start_time = time.time()

        response = super().dispatch(
            request,
            *args,
            **kwargs
        )

        # SAFE PLACE AFTER DRF RESPONSE
        org = getattr(request, "organization", None)

        if org:

            response_time_ms = int(
                (time.time() - request._start_time) * 1000
            )

            UsageService.increment_usage(
                org=org,
                status_code=response.status_code
            )

            APIRequestLog.objects.create(
                organization=org,
                endpoint=request.path,
                method=request.method,
                status_code=response.status_code,
                response_time_ms=response_time_ms,
                ip_address=request.META.get(
                    "REMOTE_ADDR"
                ),
                user_agent=request.META.get(
                    "HTTP_USER_AGENT",
                    ""
                )
            )

        return response


class AnalyticsAPIView(BaseAPIView):

    permission_classes = [
        IsAuthenticated,
        HasActiveSubscription,
        HasAvailableRequests,
        HasFeatureAccess,
    ]

    required_feature = "analytics"

    def get(self, request):

        return Response({
            "message": "Analytics access granted"
        })