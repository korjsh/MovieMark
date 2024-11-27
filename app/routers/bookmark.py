from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.bookmark import add_bookmark, get_user_bookmarks, remove_bookmark
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.movie import MovieSummarySchema

router = APIRouter()

@router.post("/")
def add_user_bookmark(movie_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        movie = add_bookmark(db, current_user.id, movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[MovieSummarySchema])
def get_bookmarks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    movies = get_user_bookmarks(db, current_user.id)
    if not movies:
        raise HTTPException(status_code=404, detail="No bookmarks found for the user")
    return movies

@router.delete("/")
def delete_bookmark(movie_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not remove_bookmark(db, current_user.id, movie_id):
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return {"message": "Bookmark removed successfully"}
