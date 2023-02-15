from fastapi import Depends, HTTPException
from asyncpg import Connection

from ..schemas.tracks import (
    BasicTrack,
    Track,
    TrackIn,
    TrackOut
)
from ..schemas.users import BasicUser
from ..database import get_db_conn

from .auth import get_current_user


class TracksService:
    def __init__(
        self,
        db_connection: Connection = Depends(get_db_conn),
        current_user: BasicUser = Depends(get_current_user)
    ) -> None:
        self.db_conn = db_connection
        self.current_user = current_user
    
    async def create_track(
        self,
        create_track: TrackIn
    ) -> TrackOut:
        """
            Создаёт запись `track` в бд и возвращает её
        """

        track = await self.db_conn.fetchrow(
            f"""
                INSERT INTO tracks (name)
                VALUES ('{create_track.name}')
                RETURNING id, name
            """
        )

        track = Track.parse_obj(dict(track))

        return TrackOut(
            track=track
        )

    async def get_basic_track(self, track_id: int) -> BasicTrack:
        """
            Достаёт базовую информацию о треке и возвращает её
        """

        track = await self.db_conn.fetchrow(
            f"""
                SELECT id, name FROM tracks
                WHERE id = {track_id}
            """
        )

        if not track:
            raise HTTPException(404)

        return BasicTrack.parse_obj(dict(track))
    
    async def get_track(self, track_id: int) -> TrackOut:
        """
            Достаёт информацию о треке и возвращает её
        """

        track = await self.db_conn.fetchrow(
            f"""
                SELECT * FROM tracks
                WHERE id = {track_id}
            """
        )

        if not track:
            raise HTTPException(404)
        
        track = Track.parse_obj(dict(track))

        return TrackOut(
            track=track
        )