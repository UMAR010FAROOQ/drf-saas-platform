from django.urls import include, path, include
from .views import AnalyticsAPIView
urlpatterns = [
    path("analytics/", AnalyticsAPIView.as_view(), name="analytics_api"),
]