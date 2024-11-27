from sqlalchemy.orm import Session
from app.models.rating import Rating

def add_or_update_rating(db: Session, user_id: int, movie_id: int, rating: int, review: str = None):
    existing_rating = db.query(Rating).filter(Rating.user_id == user_id, Rating.movie_id == movie_id).first()
    if existing_rating:
        existing_rating.rating = rating
        existing_rating.review = review
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
    else:
        new_rating = Rating(user_id=user_id, movie_id=movie_id, rating=rating, review=review)
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        return new_rating

def get_user_ratings(db: Session, user_id: int):
    return db.query(Rating).filter(Rating.user_id == user_id).all()

def remove_rating(db: Session, user_id: int, movie_id: int):
    rating = db.query(Rating).filter(Rating.user_id == user_id, Rating.movie_id == movie_id).first()
    if rating:
        db.delete(rating)
        db.commit()
        return True
    return False
