import pytest
from httpx import AsyncClient

from ..app import app
from ..services.auth import AuthService
from ..database import create_tables, delete_tables


async def refresh_test_db():
    await delete_tables('test_music')
    await create_tables('test_music')


@pytest.fixture(scope='function')
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"

