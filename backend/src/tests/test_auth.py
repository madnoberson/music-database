import pytest

from httpx import AsyncClient
from .config import client, anyio_backend, refresh_test_db


@pytest.mark.anyio
async def test_sign_up(client: AsyncClient):
    await refresh_test_db()

    response = await client.post(
        url='/sign_up/',
        json={
            "name": "testclient",
            "password": "testpassword"
        }
    )

    assert response.status_code == 200


@pytest.mark.anyio
async def test_sign_in(client: AsyncClient):
    response = await client.post(
        url='/sign_in/',
        json={
            "name": "testclient",
            "password": "testpassword"
        }
    )

    assert response.status_code == 200
    