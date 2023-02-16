from fastapi import Depends, HTTPException
from asyncpg import Connection, TransactionRollbackError

from ..schemas.tracks import (
    BasicTrack,
    Track,
    TrackIn,
    TrackOut,
    TrackUserRateIn,
    TrackUserRateOut

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

        if not self.current_user:
            raise HTTPException(401)

        track = await self.db_conn.fetchrow(
            f"""
                INSERT INTO tracks (name)
                VALUES ('{create_track.name}')
                RETURNING id, name, rate, rates_number
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
                SELECT id, name, rate, rates_number FROM tracks
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
    
    async def create_track_user_rate(
        self,
        create_rate: TrackUserRateIn
    ) -> TrackUserRateOut:
        """
            Создаёт запись `users_rates` и обновляет поля `rate`, `rates_number` у
            записи `tracks`
        """

        if not self.current_user:
            raise HTTPException(401)

        
        async with self.db_conn.transaction():
            user_rate = await self.db_conn.fetchrow(
                f"""
                    INSERT INTO users_rates (user_id, track_id, rate)
                    VALUES ({self.current_user.id},
                        {create_rate.track_id},
                        {create_rate.rate}
                        )
                    RETURNING rate
                """
            )

            track_rate = await self.db_conn.fetchrow(
                f"""
                    SELECT rate, rates_numbers FROM tracks
                    WHERE id = {create_rate.track_id}
                """
            )
    
        
        track_rate, user_rate = dict(track_rate), dict(user_rate)

        return TrackUserRateOut(
            track_rate=track_rate['rate'],
            track_rates_number=track_rate['rates_number'],
            user_rate=user_rate['rate']
        )
        

