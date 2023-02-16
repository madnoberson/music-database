import asyncpg
from asyncpg import Connection


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
                    password TEXT NOT NULL,
                    rates_number INTEGER DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS tracks (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(128) NOT NULL,
                    rate DOUBLE PRECISION,
                    rates_number INTEGER DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS users_rates (
                    user_id INTEGER REFERENCES users (id),
                    track_id INTEGER REFERENCES tracks (id),
                    rate DOUBLE PRECISION NOT NULL
                );
            """
        )

        await db_conn.execute(
            """
                CREATE OR REPLACE FUNCTION update_track_rate() RETURNS TRIGGER AS $update_track_rate$
                    -- Обновляет рейтинг трека с учетом новой оценки трека пользователем --
                    BEGIN
                        IF (TG_OP = 'DELETE') THEN
                            UPDATE tracks
                            SET rate = 
                                    CASE tracks.rates_number
                                        WHEN 1 THEN NULL
                                        ELSE ((tracks.rate * tracks.rates_number) - OLD.rate) / (tracks.rates_number - 1)
                                    END,
                                rates_number = tracks.rates_number - 1
                            WHERE tracks.id = OLD.track_id;
                        ELSIF (TG_OP = 'UPDATE') THEN
                            UPDATE tracks
                            SET rate = ((tracks.rate * tracks.rates_number) - OLD.rate + NEW.rate) / tracks.rates_number
                            WHERE tracks.id = OLD.track_id;
                        ELSIF (TG_OP = 'INSERT') THEN
                            UPDATE tracks
                            SET rate =
                                CASE
                                    WHEN tracks.rate is NULL THEN NEW.rate
                                    ELSE ((tracks.rate * tracks.rates_number) + NEW.rate) / (tracks.rates_number + 1)
                                END,
                                rates_number = tracks.rates_number + 1
                            WHERE tracks.id = NEW.track_id;     
                        END IF;
                        RETURN NEW;
                    END;
                $update_track_rate$ LANGUAGE plpgsql;

                CREATE TRIGGER update_track_rate BEFORE INSERT OR UPDATE OR DELETE ON users_rates
                    FOR EACH ROW EXECUTE FUNCTION update_track_rate();
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
            DROP TABLE IF EXISTS users, tracks, users_rates CASCADE;
            DROP SEQUENCE IF EXISTS users, tracks CASCADE;
        """
    )


if __name__ == "__main__":
    import asyncio
    asyncio.run(create_tables('test_music'))