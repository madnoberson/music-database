from pydantic import BaseModel


class Token(BaseModel):
    """
        Информация о токене
    """

    access_token: str
    token_type: str = 'Bearer'

