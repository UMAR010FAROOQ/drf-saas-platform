import pytest

from rest_framework.test import APIClient

from config.utils import response
from tests.factories import UserFactory


@pytest.mark.django_db
def test_jwt_login():

    password = "testpass123"

    user = UserFactory(password=password)

    client = APIClient()

    response = client.post(
        "/api/v1/auth/login/",
        {
            "email": user.email,
            "password": password,
        },
        format="json"
    )

    assert response.status_code == 200

    assert response.data["success"] is True
    assert "access" in response.data["data"]
    assert "refresh" in response.data["data"]