from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.crud.movie import search_movies_by_name, create_movies_from_csv
from app.database import get_db
from app.schemas.movie import MovieInfoSchema
import pandas as pd
import io


from typing import List

router = APIRouter()

@router.get("/search-movie/", response_model=List[MovieInfoSchema])
def search_movie(title: str, db: Session = Depends(get_db)):
    # 데이터베이스에서 부분 검색
    searched_movies = search_movies_by_name(db, keyword=title)

    if not searched_movies:
        raise HTTPException(status_code=404, detail="영화를 찾을 수 없습니다.")
    
    return searched_movies

@router.post("/upload-movies/")
async def upload_movies(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 파일 형식 확인
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드할 수 있습니다.")

    try:
        # 업로드된 파일 읽기
        contents = await file.read()
        # 판다스 데이터프레임으로 변환
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    except Exception as e:
        raise HTTPException(status_code=400, detail="CSV 파일을 읽는 중 오류가 발생했습니다.")

    try:
        # 데이터베이스에 저장
        num_movies = create_movies_from_csv(db, df)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="데이터베이스에 저장하는 중 오류가 발생했습니다.")

    return {"message": f"{num_movies}개의 영화가 성공적으로 업로드되었습니다."}


