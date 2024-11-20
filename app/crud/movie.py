from sqlalchemy.orm import Session
from app.models.movie import Movie

def search_movies_by_name(db: Session, keyword: str):
    return db.query(Movie).filter(Movie.movie_nm.like(f"%{keyword}%")).all()
