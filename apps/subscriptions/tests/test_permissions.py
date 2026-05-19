import pytest

from rest_framework.test import (
    APIRequestFactory
)

from apps.subscriptions.permissions import (
    HasFeatureAccess
)

from tests.factories import (
    OrganizationFactory,
    SubscriptionFactory
)


@pytest.mark.django_db
def test_feature_permission():

    org = OrganizationFactory()

    SubscriptionFactory(
        organization=org
    )

    request = APIRequestFactory().get("/")

    request.organization = org

    class MockView:
        required_feature = "analytics"

    permission = HasFeatureAccess()

    result = permission.has_permission(
        request,
        MockView()
    )

    assert result is True