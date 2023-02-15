from pydantic import BaseModel


class Token(BaseModel):
    """
        Схема с информацией о токене
    """

    access_token: str
    token_type: str = 'Bearer'

