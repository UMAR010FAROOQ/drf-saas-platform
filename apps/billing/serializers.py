from rest_framework import serializers


class UpgradePlanSerializer(serializers.Serializer):

    plan = serializers.CharField()