from django.urls import path

from apps.billing.views import (
    UpgradePlanView
)

urlpatterns = [

    path(
        "upgrade/",
        UpgradePlanView.as_view(),
        name="upgrade-plan"
    ),

]