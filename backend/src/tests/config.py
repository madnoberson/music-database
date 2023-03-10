import pytest
from httpx import AsyncClient
from asyncpg import UndefinedTableError

from ..app import app
from ..services.auth import AuthService
from ..database import create_tables, delete_tables


user_data_in = {
    "name": "testclient",
    "password": "testpassword"
}

other_user_data_in = {
    "name": "someclient",
    "password": "testpassword"
}


async def refresh_test_db():
    try:
        await delete_tables('test_music')
    except UndefinedTableError:
        pass
    await create_tables('test_music')


@pytest.fixture(scope='function')
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"

