from pydantic import BaseModel


class BasicTrack(BaseModel):
    """
        Базовая информация о треке
    """

    id: int
    name: str


class Track(BaseModel):
    """
        Информация о треке
    """

    id: int
    name: str


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
