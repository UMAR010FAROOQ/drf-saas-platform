import pytest

from apps.organizations.services import (
    OrganizationService
)

from apps.organizations.models import Membership

from tests.factories import UserFactory


@pytest.mark.django_db
def test_create_organization():

    user = UserFactory()

    org = (
        OrganizationService.create_organization(
            user=user,
            name="Test Organization"
        )
    )

    membership_exists = (
        Membership.objects.filter(
            user=user,
            organization=org
        ).exists()
    )

    assert org.name == "Test Organization"

    assert membership_exists is True