from sqlalchemy.orm import Session, joinedload
from app.models.bookmark import Bookmark

def add_bookmark(db: Session, user_id: int, movie_id: int):
    # 중복된 북마크 확인
    existing_bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == user_id, Bookmark.movie_id == movie_id
    ).first()

    if existing_bookmark:
        raise ValueError("Bookmark already exists")

    # 새 북마크 생성
    bookmark = Bookmark(user_id=user_id, movie_id=movie_id)
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return bookmark


def get_user_bookmarks(db: Session, user_id: int):
    # 북마크와 관련된 영화 데이터를 조인하여 가져오기
    return db.query(Bookmark).filter(
        Bookmark.user_id == user_id
    ).all()

    # 관련 영화 데이터를 반환
    return [bookmark.movie for bookmark in bookmarks if bookmark.movie]

def remove_bookmark(db: Session, user_id: int, movie_id: int):
    bookmark = db.query(Bookmark).filter(Bookmark.user_id == user_id, Bookmark.movie_id == movie_id).first()
    if bookmark:
        db.delete(bookmark)
        db.commit()
        return True
    return False
