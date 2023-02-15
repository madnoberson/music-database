from typing import Optional

from pydantic import BaseModel


class BasicUser(BaseModel):
    """
        Схема с базовой информацией о пользователе
    """

    id: int
    name: str

    is_owner: Optional[bool] = False


class User(BasicUser):
    """
        Схема с информацией о пользователе
    """


class UserIn(BaseModel):
    """
        Схема для ввода информации о пользователе
    """

    name: str
    password: str


class UserOut(BaseModel):
    """
        Схема для вывода информации о пользователе
    """

    user: User