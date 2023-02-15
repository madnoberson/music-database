import pytest

from httpx import AsyncClient
from .config import client, anyio_backend

from ..services.auth import AuthService


@pytest.mark.anyio
async def test_get_basic_user(client: AsyncClient):
    response = await client.get(
        url='/users/1/basic/'
    )

    assert response.status_code == 200
    assert response.json()['name'] == 'testclient'
    assert response.json()['is_owner'] == False


@pytest.mark.anyio
async def test_get_your_basic_user(client: AsyncClient):
    response = await client.post(
        url='/sign_in/',
        json={
            "name": "testclient",
            "password": "testpassword"
        }
    )

    response = await client.get(
        url='/users/1/basic/',
        headers={
            "Authorization": f"Bearer {response.json()['access_token']}"
        }
    )

    assert response.status_code == 200
    assert response.json()['name'] == 'testclient'
    assert response.json()['is_owner'] == True