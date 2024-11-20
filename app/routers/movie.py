from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.movie import search_movies_by_name
from app.database import get_db
from app.schemas.movie import MovieInfoSchema

from typing import List

router = APIRouter()

@router.get("/search-movie/", response_model=List[MovieInfoSchema])
def search_movie(title: str, db: Session = Depends(get_db)):
    # 데이터베이스에서 부분 검색
    searched_movies = search_movies_by_name(db, keyword=title)

    if not searched_movies:
        raise HTTPException(status_code=404, detail="영화를 찾을 수 없습니다.")
    
    return searched_movies

