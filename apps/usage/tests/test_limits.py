import pytest

from apps.usage.services import UsageService

from tests.factories import (
    OrganizationFactory,
    PlanFactory,
    SubscriptionFactory
)


@pytest.mark.django_db
def test_usage_limit():

    org = OrganizationFactory()

    plan = PlanFactory(
        request_limit_per_month=5
    )

    SubscriptionFactory(
        organization=org,
        plan=plan
    )

    allowed = (
        UsageService.has_available_requests(
            org
        )
    )

    assert allowed is True