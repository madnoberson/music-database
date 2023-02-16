from typing import Optional

from pydantic import BaseModel, validator, ValidationError


class BasicTrack(BaseModel):
    """
        Базовая информация о треке
    """

    id: int
    name: str
    rate: Optional[float]
    rates_number: int

    @validator('rate')
    def get_pretty_rate(rate: float):
        return float(str(rate)[:4])
    

class Track(BaseModel):
    """
        Информация о треке
    """

    id: int
    name: str
    rate: Optional[float]
    rates_number: int

    @validator('rate')
    def get_pretty_rate(rate: float):
        return float(str(rate)[:4])


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


class TrackUserRate(BaseModel):
    """
        Информация об оценки трека пользователем
    """

    track_rate: float
    track_rates_number: int
    user_rate: float


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


class TrackUserRateOut(TrackUserRate):
    """
        Вывод информации об оценке трека пользователем
    """


