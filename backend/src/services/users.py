from fastapi import Depends, HTTPException
from asyncpg import Connection

from ..schemas.users import BasicUser, User, UserOut
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
                SELECT id, name FROM users
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
                SELECT * FROM users
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
