import pytest

from tests.factories import UserFactory


@pytest.mark.django_db
def test_create_user():

    user = UserFactory()

    assert user.email is not None

    assert user.is_active is True