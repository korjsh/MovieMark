from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RatingSchema(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: int
    review: Optional[str] = None
    created_at: datetime
    updated_at: datetime


