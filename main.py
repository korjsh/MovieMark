import logging
from typing import AsyncIterator

from fastapi import FastAPI
from app.routers import auth, movie, user, bookmark, rating  # 각 라우터 가져오기
from app.database import engine
from app.models import movie as movie_model, user as user_model, bookmark as bookmark_model, rating as rating_model   # 모델 가져오기
logger = logging.getLogger("uvicorn.info")

async def lifespan_handler(app: FastAPI) -> AsyncIterator[None]:
    # 애플리케이션 시작 시 실행
    logger.info("Starting MovieMark API server...")
    logger.info("Swagger UI available at: http://0.0.0.0:8000/docs")
    logger.info("ReDoc available at: http://0.0.0.0:8000/redoc")

    yield  # 앱이 실행 중인 동안 여기서 대기

    # 애플리케이션 종료 시 실행
    logger.info("Shutting down MovieMark API server...")
app = FastAPI(lifespan=lifespan_handler)

# 데이터베이스 초기화
movie_model.Base.metadata.create_all(bind=engine)
user_model.Base.metadata.create_all(bind=engine)
bookmark_model.Base.metadata.create_all(bind=engine)
rating_model.Base.metadata.create_all(bind=engine)


# 라우터 등록
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(movie.router, prefix="/movies", tags=["Movies"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(bookmark.router, prefix="/bookmarks", tags=["Bookmarks"])
app.include_router(rating.router, prefix="/ratings", tags=["Ratings"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
