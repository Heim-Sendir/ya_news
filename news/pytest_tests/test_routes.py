from http import HTTPStatus
import pytest

from django.urls import reverse


@pytest.mark.parametrize(
    'name',
    (
        'news:home',
        'users:login',
        'users:logout',
        'users:signup',
    )
)
def test_home_availability_for_anonymous_user(client, name, news):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
