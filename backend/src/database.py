import asyncpg
from asyncpg import Connection


async def get_db_conn() -> Connection:
    db_conn = await asyncpg.connect(
        "postgresql://postgres:1234@localhost/music"
    )
    try:
        yield db_conn
    finally:
        await db_conn.close()


async def create_tables(
    db_name: str
) -> None:
    async with asyncpg.connect(
        f"postgresql://postgres:1234@localhost/{db_name}"
    ) as conn:
        async with conn.transaction():
            await conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(64) NOT NULL UNIQUE,
                        password TEXT NOT NULL
                    );
                """
            )

    
