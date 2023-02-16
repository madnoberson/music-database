import pytest

from httpx import AsyncClient
from .config import client, anyio_backend, refresh_test_db, user_data_in


@pytest.mark.anyio
async def test_sign_up(client: AsyncClient):
    await refresh_test_db()

    response = await client.post(
        url='/sign_up/',
        json=user_data_in
    )

    assert response.status_code == 200


@pytest.mark.anyio
async def test_sign_in(client: AsyncClient):
    response = await client.post(
        url='/sign_in/',
        json=user_data_in
    )

    assert response.status_code == 200
    