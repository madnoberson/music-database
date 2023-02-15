from typing import Optional

from pydantic import BaseModel


class BasicUser(BaseModel):
    """
        Базовая информация о пользователе
    """

    id: int
    name: str

    is_owner: Optional[bool] = False


class User(BaseModel):
    """
        Информация о пользователе
    """

    id: int
    name: str


class UserIn(BaseModel):
    """
        Ввод информации о пользователе
    """

    name: str
    password: str


class UserOut(BaseModel):
    """
        Вывод информации о пользователе
    """

    user: User