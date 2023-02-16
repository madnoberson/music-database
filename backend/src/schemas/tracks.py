from typing import Optional

from pydantic import BaseModel, validator, ValidationError


class BasicTrack(BaseModel):
    """
        Базовая информация о треке
    """

    id: int
    name: str
    rates_number: int
    rate: float | None
    user_rate: float | None

    owner_rate: Optional[float] = None

    @validator('rate')
    def get_pretty_rate(rate: float):
        if rate:
            return float(str(rate)[:4])
    

class Track(BasicTrack):
    """
        Информация о треке
    """


class TrackIn(BaseModel):
    """
        Ввод информации о треке
    """

    name: str


class TrackOut(BaseModel):
    """
        Вывод информации о треке
    """

    track: Track


class UpdatedTrackRateOut(BaseModel):
    """
        Вывод обновлённой ифнормации о рейтинге трека 
    """

    rates_number: int
    rate: float | None
    user_rate: float | None


class TrackUserRateIn(BaseModel):
    """
        Ввод оценки треку пользователем
    """

    track_id: int
    rate: float

    @validator('rate')
    def validate_rate(rate: float):
        if 1 <= rate <= 10 and rate % 0.5 == 0:
            return rate
        raise ValidationError





