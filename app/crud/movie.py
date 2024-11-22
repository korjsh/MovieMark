from sqlalchemy.orm import Session
from app.models.movie import Movie
from sqlalchemy.exc import SQLAlchemyError

import logging

logger = logging.getLogger(__name__)

def search_movies_by_name(db: Session, keyword: str):
    try:
        movies = db.query(Movie).filter(Movie.title.ilike(f"%{keyword}%")).all()
        return movies
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        return []
