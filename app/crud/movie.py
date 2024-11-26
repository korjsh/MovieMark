from sqlalchemy.orm import Session
from app.models.movie import Movie
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict

import logging

logger = logging.getLogger(__name__)

def search_movies_by_name(db: Session, keyword: str, skip: int = 0, limit: int = 10) -> Dict:
    try:
        total_items = db.query(Movie).filter(Movie.title.ilike(f"%{keyword}%")).count()
        movies = db.query(Movie).filter(Movie.title.ilike(f"%{keyword}%")).offset(skip).limit(limit).all()
        total_pages = (total_items + limit - 1) // limit  # 올림 처리
        return {
            "total_pages": total_pages,
            "total_items": total_items,
            "movies": movies
        }
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        return {
            "total_pages": 0,
            "total_items": 0,
            "movies": []
        }
    
def get_movies_list(db: Session, skip: int = 0, limit: int = 10) -> Dict:
    try:
        total_items = db.query(Movie).count()
        movies = db.query(Movie).offset(skip).limit(limit).all()
        total_pages = (total_items + limit - 1) // limit  # 올림 처리
        return {
            "total_pages": total_pages,
            "total_items": total_items,
            "movies": movies
        }
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        return {
            "total_pages": 0,
            "total_items": 0,
            "movies": []
        }