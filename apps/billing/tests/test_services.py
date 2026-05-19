import pytest

from apps.billing.services import BillingService

from tests.factories import (
    OrganizationFactory,
    PlanFactory
)


@pytest.mark.django_db
def test_process_payment():

    org = OrganizationFactory()

    plan = PlanFactory()

    result = BillingService.process_payment(
        org=org,
        plan=plan
    )

    assert result["payment"].status == "paid"

    assert (
        result["subscription"].plan == plan
    )