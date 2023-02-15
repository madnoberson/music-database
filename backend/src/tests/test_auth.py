import pytest

from httpx import AsyncClient
from .config import db_conn, client, anyio_backend


@pytest.mark.anyio
async def test_sign_up(client: AsyncClient):
    response = await client.post(
        url='http://127.0.0.1:8000/sign_up/',
        json={
            "name": "testclient",
            "password": "testpassword"
        }
    )

    assert response.status_code == 200