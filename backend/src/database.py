import asyncpg
from asyncpg import Connection
from asyncpg.transaction import Transaction


async def get_db_conn() -> Connection:
    db_conn = await asyncpg.connect(
        "postgresql://postgres:1234@localhost/test_music"
    )
    try:
        yield db_conn
    finally:
        await db_conn.close()


async def create_tables(
    db_name: str
) -> None:
    db_conn = await asyncpg.connect(
        f"postgresql://postgres:1234@localhost/{db_name}"
    )
    
    async with db_conn.transaction():
        await db_conn.execute(
            """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(64) NOT NULL UNIQUE,
                    password TEXT NOT NULL
                );
            """
        )


async def delete_tables(
    db_name: str
) -> None:
    db_conn = await asyncpg.connect(
        f"postgresql://postgres:1234@localhost/{db_name}"
    )

    await db_conn.execute(
        """
            DROP TABLE IF EXISTS users CASCADE;
            DROP SEQUENCE IF EXISTS users CASCADE;
        """
    )


if __name__ == "__main__":
    import asyncio
    asyncio.run(create_tables('music'))