from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from apps.api_keys.throttling import APIKeyRateThrottle


class ProtectedView(APIView):
    throttle_classes = [UserRateThrottle, APIKeyRateThrottle]

    def get(self, request):
        return Response({"message": "OK"})
