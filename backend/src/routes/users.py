from fastapi import APIRouter, Depends

from ..schemas.users import BasicUser, UserOut
from ..schemas.tracks import BasicTrack

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


@router.get(
    '/users/{user_id}/rates/',
    response_model=list[BasicTrack]
)
async def get_rated_tracks(
    user_id: int,
    users_service: UsersService = Depends()
) -> list[BasicTrack]:
    """
        Возвращает информацию о треках, которые оценил пользователь
    """

    return await users_service.get_rated_tracks(
        user_id=user_id
    )
