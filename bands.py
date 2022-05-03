import datetime
from typing import Iterable
import uuid

from django.db import models

# region Models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Band(BaseModel):
    name = models.CharField(max_length=128)


class Album(BaseModel):
    band = models.ForeignKey(to="Band", on_delete=models.CASCADE)
    name = models.CharField()
    release = models.DateField()


class Song(BaseModel):
    album = models.ForeignKey(to="Album", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    duration_seconds = models.PositiveIntegerField()


class Artist(BaseModel):
    name = models.CharField(max_length=128)


class BandArtist(BaseModel):
    band = models.ForeignKey(to="Band", on_delete=models.CASCADE)
    artist = models.ForeignKey(to="Artist", on_delete=models.CASCADE)
    joined = models.DateField()
    left = models.DateField(null=True, blank=True)


class Stream(BaseModel):
    user = models.ForeignKey(to="auth.User", on_delete=models.SET_NULL)
    song = models.ForeignKey(to="Song", on_delete=models.CASCADE)
    stream_date = models.DateField()
    duration_seconds = models.PositiveIntegerField()


# endregion

# region Utils


def get_band_formation(band_id: str, date: datetime.date) -> Iterable[str]:
    
    band_artists: Iterable[BandArtist] = BandArtist.objects.filter(band_id=band_id, joined__lte=date, left__gt=date)
    for band_artist in band_artists:
        yield band_artist.artist


def get_song_revenue(song_id: str, day: datetime.date, price_per_second: float) -> float:
    song: Song = Song.objects.get(id=song_id)
    revenue = 0
    for stream in song.stream_set.all():
        revenue += stream.duration_seconds * price_per_second
    return revenue


# endregion
