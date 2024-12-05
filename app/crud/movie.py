from sqlalchemy.orm import Session
from app.models.movie import Movie
from app.models.bookmark import Bookmark
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, Optional

import logging

logger = logging.getLogger(__name__)

def search_movies_by_name(
    db: Session, 
    keyword: str, 
    skip: int = 0, 
    limit: int = 10, 
    user_id: Optional[int] = None  # 사용자 ID 추가
) -> Dict:
    try:
        total_items = db.query(Movie).filter(Movie.title.ilike(f"%{keyword}%")).count()
        movies = db.query(Movie).filter(Movie.title.ilike(f"%{keyword}%")).offset(skip).limit(limit).all()
        total_pages = (total_items + limit - 1) // limit  # 올림 처리

        # 북마크 여부 확인
        bookmarked_movie_ids = set()
        if user_id:
            bookmarks = db.query(Bookmark.movie_id).filter(Bookmark.user_id == user_id).all()
            bookmarked_movie_ids = {bm.movie_id for bm in bookmarks}

        movies_with_bookmarks = [
            {**movie.__dict__, "is_bookmarked": movie.id in bookmarked_movie_ids}
            for movie in movies
        ]

        return {
            "total_pages": total_pages,
            "total_items": total_items,
            "movies": movies_with_bookmarks
        }
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        return {
            "total_pages": 0,
            "total_items": 0,
            "movies": []
        }

def get_movies_list(
    db: Session, 
    skip: int = 0, 
    limit: int = 10
    ) -> Dict:
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
def get_movies_list_with_bookmark(
    db: Session, 
    skip: int = 0, 
    limit: int = 10, 
    user_id: Optional[int] = None  # 사용자 ID 추가
) -> Dict:
    try:
        total_items = db.query(Movie).count()
        movies = db.query(Movie).offset(skip).limit(limit).all()
        total_pages = (total_items + limit - 1) // limit  # 올림 처리

        # 북마크 여부 확인
        bookmarked_movie_ids = set()
        if user_id:
            bookmarks = db.query(Bookmark.movie_id).filter(Bookmark.user_id == user_id).all()
            bookmarked_movie_ids = {bm.movie_id for bm in bookmarks}

        movies_with_bookmarks = [
            {**movie.__dict__, "is_bookmarked": movie.id in bookmarked_movie_ids}
            for movie in movies
        ]

        return {
            "total_pages": total_pages,
            "total_items": total_items,
            "movies": movies_with_bookmarks
        }
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        return {
            "total_pages": 0,
            "total_items": 0,
            "movies": []
        }
    
def get_movie_by_id(db: Session, movie_id: int) -> Movie:
    return db.query(Movie).filter(Movie.id == movie_id).first()