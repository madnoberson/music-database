from fastapi import Depends, HTTPException
from asyncpg import Connection

from ..schemas.users import BasicUser, User, UserOut
from ..schemas.tracks import BasicTrack
from ..database import get_db_conn

from .auth import get_current_user


class UsersService:
    def __init__(
        self,
        current_user: BasicUser = Depends(get_current_user),
        db_connection: Connection = Depends(get_db_conn)  
    ) -> None:
        self.db_conn = db_connection
        self.current_user = current_user
    
    async def get_basic_user(self, user_id: int) -> BasicUser:
        """
            Достаёт из бд базовую информацию о пользователе и возвращает
            её
        """

        user_record = await self.db_conn.fetchrow(
            f"""
                SELECT id, name
                FROM users
                WHERE id = {user_id}
            """
        )

        if not user_record:
            raise HTTPException(404)
        
        user = dict(user_record)
        if self.current_user and user['id'] == self.current_user.id:
            user['is_owner'] = True

        return BasicUser.parse_obj(user)

    async def get_user(self, user_id: int) -> User:
        """
            Достаёт из бд информацию о пользователе и возвращает её
        """

        user_record = await self.db_conn.fetchrow(
            f"""
                SELECT *
                FROM users
                WHERE id = {user_id}
            """
        )

        if not user_record:
            raise HTTPException(404)

        user = dict(user_record)
        if self.current_user and user['id'] == self.current_user.id:
            user['is_owner'] = True

        user = User.parse_obj(user)

        return UserOut(
            user=user
        )
    
    async def get_rated_tracks(self, user_id: int) -> list[BasicTrack]:
        """
            Возращает базовую информацию о треках, которые оценил
            пользователь

            Примеры возвращаемый значений:
                Если пользователь запрашивающий информацию является
                пользователем о котором запрашивают информацию:
                    [
                        {
                            id: int
                            name: str
                            rates_number: int
                            rate: float
                            user_rate: float
                            owner_rate: None
                        },
                            ...
                    ]

        """

        if self.current_user and self.current_user.id == user_id:
            query = f"""
                SELECT tracks.id, tracks.name, tracks.rate,
                tracks.rates_number, users_rates.rate AS user_rate, NULL AS owner_rate
                FROM users_rates
                JOIN tracks
                ON tracks.id = users_rates.track_id
                WHERE users_rates.user_id = {user_id}
            """
        elif not self.current_user:
            query = f"""
                SELECT tracks.id, tracks.name, tracks.rate,
                tracks.rates_number, users_rates.rate AS owner_rate, NULL AS user_rate
                FROM users_rates
                JOIN tracks
                ON tracks.id = users_rates.track_id
                WHERE users_rates.user_id = {user_id}
            """
        else:
            query = f"""
                SELECT tracks.id, tracks.name, tracks.rate,
                tracks.rates_number, users_rates.rate AS user_rate, owner_rates.rate AS owner_rate
                FROM tracks
                JOIN users_rates as owner_rates
                ON owner_rates.user_id = {user_id}
                JOIN users_rates
                ON users_rates.user_id = {self.current_user.id}
                WHERE tracks.id IN (SELECT track_id FROM users_rates WHERE user_id = {self.current_user.id})
            """
        
        records = await self.db_conn.fetch(query)

        return [
            BasicTrack.parse_obj(record) for record in records
        ]




