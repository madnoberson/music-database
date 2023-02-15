from fastapi import APIRouter, Depends

from ..schemas.tracks import BasicTrack, TrackIn, TrackOut

from ..services.tracks import TracksService


router = APIRouter()


@router.post(
    '/tracks/',
    response_model=TrackOut
)
async def create_track(
    create_track: TrackIn,
    tracks_service: TracksService = Depends()
) -> TrackOut:
    """
        Создаёт запись `tracks` и возвращает её
    """

    return await tracks_service.create_track(
        create_track=create_track
    )


@router.get(
    '/tracks/{track_id}/basic/',
    response_model=BasicTrack
)
async def get_basic_track(
    track_id: int,
    tracks_service: TracksService = Depends()
) -> BasicTrack:
    """
        Достаёт базовую информацию о треке
    """

    return await tracks_service.get_basic_track(
        track_id=track_id
    )


@router.get(
    '/tracks/{track_id}/',
    response_model=TrackOut
)
async def get_track(
    track_id: int,
    tracks_service: TracksService = Depends()
) -> TrackOut:
    """
        Достаёт информацию о треке
    """

    return await tracks_service.get_track(
        track_id=track_id
    )