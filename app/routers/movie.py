from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.movie import search_movies_by_name, get_movies_list
from app.database import get_db
from typing import Dict
from app.schemas.movie import MovieSchema, MovieSummarySchema

router = APIRouter()

@router.get("/", response_model=Dict)
def get_movies(page: int = 1, item: int = 10, detail: str = 'n', db: Session = Depends(get_db)):
    if page < 1 or item < 1:
        raise HTTPException(status_code=400, detail="페이지 번호와 항목 수는 1 이상이어야 합니다.")
    
    skip = (page - 1) * item
    result = get_movies_list(db, skip=skip, limit=item)
    
    if not result["movies"]:
        raise HTTPException(status_code=404, detail="영화를 찾을 수 없습니다.")
    
    movies = [
        MovieSummarySchema.model_validate(movie) if detail == 'n' else MovieSchema.model_validate(movie)
        for movie in result["movies"]
    ]
    
    return {
        "total_pages": result["total_pages"],
        "total_items": result["total_items"],
        "page": page,
        "movies": movies
    }

@router.get("/search", response_model=Dict)
def search_movie(title: str, page: int = 1, item: int = 10, detail: str = 'n', db: Session = Depends(get_db)):
    if page < 1 or item < 1:
        raise HTTPException(status_code=400, detail="페이지 번호와 항목 수는 1 이상이어야 합니다.")
    
    skip = (page - 1) * item
    result = search_movies_by_name(db, keyword=title, skip=skip, limit=item)
    
    if not result["movies"]:
        raise HTTPException(status_code=404, detail="해당 키워드로 영화를 찾을 수 없습니다.")
    
    movies = [
        MovieSummarySchema.model_validate(movie) if detail == 'n' else MovieSchema.model_validate(movie)
        for movie in result["movies"]
    ]
    
    return {
        "total_pages": result["total_pages"],
        "total_items": result["total_items"],
        "page": page,
        "movies": movies
    }