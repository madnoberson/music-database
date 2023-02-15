from fastapi import APIRouter, Depends

from ..schemas.users import BasicUser, UserOut

from ..services.users import UsersService


router = APIRouter()


@router.get(
    '/users/{user_id}/basic/',
    response_model=BasicUser
)
async def get_basic_user(
    user_id: int,
    users_service: UsersService = Depends()
) -> BasicUser:
    """
        Возвращает базовую информацию о пользователе
    """

    return await users_service.get_basic_user(
        user_id=user_id
    )


@router.get(
    '/users/{user_id}/',
    response_model=UserOut
)
async def get_user(
    user_id: int,
    users_service: UsersService = Depends()
) -> UserOut:
    """
        Возвращает информацию о пользователе
    """

    return await users_service.get_user(
        user_id=user_id
    )