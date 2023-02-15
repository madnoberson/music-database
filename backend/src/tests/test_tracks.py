import pytest

from httpx import AsyncClient
from .config import client, anyio_backend


@pytest.mark.anyio
async def test_create_track(client: AsyncClient):
    track_in = {
        "name": "heroes"
    }

    track_out = {
        "track": {
            "id": 1,
            "name": "heroes"
        }
    }

    response = await client.post(
        url='/tracks/',
        json=track_in
    )

    assert response.status_code == 200

    print(response.json(), track_out)

    assert response.json() == track_out


@pytest.mark.anyio
async def test_get_basic_track(client: AsyncClient):

    track_out = {
        "id": 1,
        "name": "heroes"
    }

    response = await client.get(
        url='/tracks/1/basic/',
    )

    print(response.json(), track_out)

    assert response.status_code == 200
    assert response.json() == track_out


@pytest.mark.anyio
async def test_get_track(client: AsyncClient):

    track_out = {
        "track": {
            "id": 1,
            "name": "heroes"
        }
    }

    response = await client.get(
        url='/tracks/1/',
    )

    assert response.status_code == 200

    print(response.json(), track_out)

    assert response.json() == track_out