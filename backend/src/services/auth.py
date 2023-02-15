from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from asyncpg import Connection
from jose import jwt, JWTError
from passlib.hash import bcrypt

from ..schemas.auth import Token
from ..schemas.users import BasicUser, UserIn
from ..database import get_db_conn

from ..settings import settings


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/sign-in/',
    auto_error=False
)


async def get_current_user(
        token: str = Depends(oauth2_scheme)
    ) -> BasicUser | None:
        """
            Возвращает информацию о пользователе, которая содержится
            в токене. В случае отсутсивя токена пользовател считается гостем
        """

        if not token:
            return None
        
        return AuthService.validate_token(token)


class AuthService: 
    def __init__(
        self,
        db_connection: Connection = Depends(get_db_conn)
    ):
        self.db_conn = db_connection

    async def sign_up(
        self,
        create_user: UserIn
    ) -> Token:
        """
            Создаёт пользователя в бд и возвращает access token
        """

        hashed_password = self.hash_password(
            plain_password=create_user.password
        )
        
        user = await self.db_conn.fetchrow(
            f"""
                INSERT INTO users (name, password)
                VALUES ({create_user.name}, {create_user.password})
                RETURNING id, name
            """
        )

        return self.create_token(dict(user))
    
    async def sign_in(
        self,
        user_data: UserIn
    ) -> Token:
        """
            Проверяет введённые данные и возвращает acess token если
            данные валидны
        """
        
        exception = HTTPException(
            status_code=401,
            headers={'WWW-Authenticate'}
        )

        user = await self.db_conn.fetchrow(
            f"""
                SELECT id, name, password FROM users
                WHERE name = {user_data.name}
            """
        )

        if not user:
            raise exception
        
        user = dict(user).pop('password')

        if not self.verify_password(
            plain_password=user_data.password,
            hashed_password=user['password']
        ):
            raise exception
        
        return self.create_token(user)
    
    @staticmethod
    def create_token(
        user_data: dict
    ) -> Token:
        """
            Создаёт access token
        """

        now = datetime.utcnow()
        expires = now + timedelta(
            hours=settings.jwt_expires
        )

        payload = {
            "iat": now,
            "nbf": now,
            "exp": expires,
            "sub": user_data.pop('id'),
            "user": user_data
        }

        token = jwt.encode(
            claims=payload,
            key=settings.jwt_secret,
            algorithm=[settings.jwt_algorithm]
        )

        return Token(token)
    
    @staticmethod
    def validate_token(
        token: str
    ) -> BasicUser:
        """
            Валидирует токен и возвращает из него данные
            о пользователе
        """

        exception = HTTPException(
            status_code=401,
            headers={'WWW-Authenticate': 'Bearer'}
        )

        try:
            payload = jwt.decode(
                token=token,
                key=settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )

            user = BasicUser.parse_obj(
                payload.get('user')
            )

        except (JWTError, ValidationError):
            raise exception
        
        return user
    
    @staticmethod
    def verify_password(
        plain_password: str | bytes,
        hashed_password: str | bytes
    ) -> bool:
        """ Верифицирует пароль """
        return bcrypt.verify(
            plain_password, hashed_password
        )
    
    @staticmethod
    def hash_password(
        plain_password: str | bytes
    ) -> str:
        """ Возвращает хэш пароля """
        return bcrypt.hash(plain_password)

