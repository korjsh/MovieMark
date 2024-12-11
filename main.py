import logging
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # CORS를 위한 미들웨어 추가
from app.routers import auth, movie, user, bookmark, rating, db_manage
from app.database import engine
from app.models import movie as movie_model, user as user_model, bookmark as bookmark_model, rating as rating_model



import os
from pathlib import Path
from dotenv import load_dotenv

# BASE_DIR = Path(getattr(sys, '_MEIPASS', Path(__file__).parent))
# ENV_FILE = BASE_DIR / ".env"

# if ENV_FILE.exists():
#     print(f"Loading environment variables from {ENV_FILE}")
#     load_dotenv(ENV_FILE)
#     print("Loaded environment variables:")
#     for key, value in os.environ.items():
#         print(f"{key}: {value}")
# else:
#     print("No .env file found!")

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

# CORS 설정 추가
origins = [
    "http://localhost:3000",  # 허용할 클라이언트 도메인
    "http://127.0.0.1:3000",
    "*",  # 모든 도메인 허용 (배포 환경에서는 적절히 제한하는 것이 좋음)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

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
app.include_router(db_manage.router, prefix="/db_manage", tags=["DbManage"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
