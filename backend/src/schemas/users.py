from pydantic import BaseModel


class BasicUser(BaseModel):
    """
        Схема с базовой информацией о пользователе
    """

    id: int
    name: str


class UserIn(BaseModel):
    """
        Схема для ввода информации о пользователе
    """

    name: str
    password: str
