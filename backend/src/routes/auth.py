from fastapi import Depends, APIRouter

from ..schemas.users import UserIn
from ..schemas.auth import Token
from ..services.auth import AuthService


router = APIRouter()


@router.post(
    '/sign_up/',
    response_model=Token
)
async def sign_up(
    create_user: UserIn,
    auth: AuthService = Depends()
) -> Token:
    """
        Регестрирует пользователя и возвращает access token
    """

    return await auth.sign_up(
        create_user=create_user
    )


@router.post(
    '/sign_in/',
    response_model=Token
)
async def sign_in(
    user_data: UserIn,
    auth: AuthService = Depends()
) -> Token:
    """
        Авторизиует пользователя и возвращает access token
    """

    return await auth.sign_in(
        user_data=user_data
    )