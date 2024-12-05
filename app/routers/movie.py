from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.movie import get_movies_list, search_movies_by_name, get_movie_by_id
from app.crud.bookmark import get_user_bookmarks
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.movie import MovieSchema, MovieSummarySchema
router = APIRouter()

@router.get("/", response_model=Dict)
def get_movies(
    page: int = 1,
    item: int = 10,
    detail: str = 'n',
    db: Session = Depends(get_db)
    ):
    if page < 1 or item < 1:
        raise HTTPException(status_code=400, detail="페이지 번호와 항목 수는 1 이상이어야 합니다.")

    skip = (page - 1) * item
    result = get_movies_list(db, skip=skip, limit=item)

    if not result["movies"]:
        raise HTTPException(status_code=404, detail="영화를 찾을 수 없습니다.")


    # 영화 데이터 처리
    movies = [
        (MovieSummarySchema.model_validate(movie).dict() if detail == 'n' else MovieSchema.model_validate(movie).dict())
        for movie in result["movies"]
    ]
    return {
        "total_pages": result["total_pages"],
        "total_items": result["total_items"],
        "page": page,
        "movies": movies
    }
@router.get("/secure", response_model=Dict)
def get_movies(
    page: int = 1,
    item: int = 10,
    detail: str = 'n',
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if page < 1 or item < 1:
        raise HTTPException(status_code=400, detail="페이지 번호와 항목 수는 1 이상이어야 합니다.")

    skip = (page - 1) * item
    result = get_movies_list(db, skip=skip, limit=item)

    if not result["movies"]:
        raise HTTPException(status_code=404, detail="영화를 찾을 수 없습니다.")

    # 북마크 여부 처리
    bookmarked_movie_ids = set()
    if current_user:
        user_bookmarks = get_user_bookmarks(db, current_user.id)
        bookmarked_movie_ids = {bookmark.movie_id for bookmark in user_bookmarks}

    # 영화 데이터 처리
    movies = [
        {
            **(MovieSummarySchema.model_validate(movie).dict() if detail == 'n' else MovieSchema.model_validate(movie).dict()),
            "is_bookmarked": movie.id in bookmarked_movie_ids
        }
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
@router.get("/search/secure", response_model=Dict)
def search_movie_secure(
    title: str,
    page: int = 1,
    item: int = 10,
    detail: str = 'n',
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 인증된 사용자만 접근 가능
):
    if page < 1 or item < 1:
        raise HTTPException(status_code=400, detail="페이지 번호와 항목 수는 1 이상이어야 합니다.")

    skip = (page - 1) * item
    result = search_movies_by_name(db, keyword=title, skip=skip, limit=item)

    if not result["movies"]:
        raise HTTPException(status_code=404, detail="해당 키워드로 영화를 찾을 수 없습니다.")

    # 현재 사용자의 북마크 데이터 가져오기
    user_bookmarks = get_user_bookmarks(db, current_user.id)
    bookmarked_movie_ids = {bookmark.movie_id for bookmark in user_bookmarks}

    # 영화 데이터 처리
    movies = [
        {
            **(MovieSummarySchema.model_validate(movie).dict() if detail == 'n' else MovieSchema.model_validate(movie).dict()),
            "is_bookmarked": movie["id"] in bookmarked_movie_ids  # movie["id"]로 수정
        }
        for movie in result["movies"]
    ]

    return {
        "total_pages": result["total_pages"],
        "total_items": result["total_items"],
        "page": page,
        "movies": movies
    }

@router.get("/{movie_id}", response_model=MovieSchema)
def get_movie_by_id_route(
    movie_id: int,
    db: Session = Depends(get_db),
):
    # 영화 데이터를 데이터베이스에서 가져오기
    movie = get_movie_by_id(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="영화를 찾을 수 없습니다.")
    
    return MovieSchema.model_validate(movie)

@router.get("/{movie_id}/secure", response_model=MovieSchema)
def get_movie_by_id_secure(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 인증된 사용자만 접근 가능
):
    # 영화 데이터를 데이터베이스에서 가져오기
    movie = get_movie_by_id(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="영화를 찾을 수 없습니다.")

    # 북마크 여부 확인
    user_bookmarks = get_user_bookmarks(db, current_user.id)
    bookmarked_movie_ids = {bookmark.movie_id for bookmark in user_bookmarks}
    is_bookmarked = movie.id in bookmarked_movie_ids

    # 영화 데이터 반환
    movie_data = MovieSchema.model_validate(movie).dict()
    movie_data["is_bookmarked"] = is_bookmarked

    return movie_data