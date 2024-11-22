# app/schemas/movie.py

from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import date, datetime

class MovieSchema(BaseModel):
    id: int
    title: str
    vote_average: Optional[float] = None
    vote_count: Optional[float] = None
    status: Optional[str] = None
    release_date: Optional[date] = None
    revenue: Optional[float] = None
    runtime: Optional[float] = None
    budget: Optional[float] = None
    imdb_id: Optional[str] = None
    original_language: Optional[str] = None
    original_title: Optional[str] = None
    overview: Optional[str] = None
    popularity: Optional[float] = None
    tagline: Optional[str] = None
    genres: Optional[List[str]] = None
    production_companies: Optional[List[str]] = None
    production_countries: Optional[List[str]] = None
    spoken_languages: Optional[List[str]] = None
    cast: Optional[List[str]] = None
    director: Optional[str] = None
    director_of_photography: Optional[str] = None
    writers: Optional[List[str]] = None
    producers: Optional[List[str]] = None
    music_composer: Optional[str] = None
    imdb_rating: Optional[float] = None
    imdb_votes: Optional[float] = None
    poster_path: Optional[str] = None

    @field_validator('release_date', mode='before')
    def parse_release_date(cls, value):
        if value and isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                return None
        return value

    @field_validator('genres', 'production_companies', 'production_countries', 'spoken_languages', 'cast', 'writers', 'producers', mode='before')
    def split_string_fields(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(',')]
        return value

    class Config:
        from_attributes = True
