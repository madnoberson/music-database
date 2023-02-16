import pytest

from httpx import AsyncClient
from .config import client, anyio_backend, user_data_in


@pytest.mark.anyio
async def test_create_track(client: AsyncClient):
    response = await client.post(
        url='/sign_in/',
        json=user_data_in
    )
    access_token = response.json()['access_token']

    track_in = {
        "name": "heroes"
    }

    track_out = {
        "track": {
            "id": 1,
            "name": "heroes",
            "rate": None,
            "rates_number": 0 
        }
    }

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = await client.post(
        url='/tracks/',
        json=track_in,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json() == track_out


@pytest.mark.anyio
async def test_get_basic_track(client: AsyncClient):

    track_out = {
        "id": 1,
        "name": "heroes",
        "rate": None,
        "rates_number": 0
    }

    response = await client.get(
        url='/tracks/1/basic/',
    )

    assert response.status_code == 200
    assert response.json() == track_out


@pytest.mark.anyio
async def test_get_track(client: AsyncClient):

    track_out = {
        "track": {
            "id": 1,
            "name": "heroes",
            "rate": None,
            "rates_number": 0
        }
    }

    response = await client.get(
        url='/tracks/1/',
    )

    assert response.status_code == 200
    assert response.json() == track_out


@pytest.mark.anyio
async def test_create_track_user_rate(client: AsyncClient):
    track_user_rate_in = {
        "track_id": 1,
        "rate": 7
    }

    track_user_rate_out = {
        "track_rate": 7,
        "track_rates_number": 1,
        "user_rate": 7
    }

    response = await client.post(
        url='/tracks/1/rates/',
        json=track_user_rate_in
    )

    assert response.status_code == 401

    # Тест с авторизованным пользователем

    response = await client.post(
        url='/sign_in/',
        json=user_data_in
    )
    access_token = response.json()['access_token']

    response = await client.post(
        url='/tracks/1/rates/',
        json=track_user_rate_in,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    assert response.json() == track_user_rate_out
    