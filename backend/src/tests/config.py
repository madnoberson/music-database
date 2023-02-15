import pytest
import asyncpg
from httpx import AsyncClient

from ..app import app
from ..database import create_tables, delete_tables


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope='function')
async def db_conn():
    conn = await asyncpg.connect(
        "postgresql://postgres:1234@localhost/test_music"
    )
    try:
        yield conn
    finally:
        await conn.close()


@pytest.fixture(scope='function')
async def client() -> AsyncClient:
    def get_test_db():
        yield db_conn

    await delete_tables('test_music')
    await create_tables('test_music')

    app.dependency_overrides['get_db_conn'] = get_test_db

    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client