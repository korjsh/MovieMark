from pydantic import BaseModel
from datetime import datetime

class BookmarkSchema(BaseModel):
    id: int
    user_id: int
    movie_id: int
    created_at: datetime