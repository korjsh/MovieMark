from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.rating import add_or_update_rating, get_user_ratings, remove_rating
from app.schemas.movie import MovieSchema
from app.models.user import User
from app.dependencies.auth import get_current_user



router = APIRouter()

@router.post("/")
def rate_movie(movie_id: int, rating: int, review: str = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not (1 <= rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    return add_or_update_rating(db, current_user.id, movie_id, rating, review)

@router.get("/", response_model=List[MovieSchema])
def get_ratings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_ratings(db, current_user.id)

@router.delete("/")
def delete_rating(movie_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not remove_rating(db, current_user.id, movie_id):
        raise HTTPException(status_code=404, detail="Rating not found")
    return {"message": "Rating removed successfully"}
