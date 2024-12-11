from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

import os
import sys
import logging
logger = logging.getLogger("uvicorn")

if getattr(sys, "frozen", False):  # 패키징된 상태인지 확인
    print("packaged server")
    BASE_DIR = os.path.dirname(sys.executable)  # 실행 파일의 디렉토리
else:
    print("dev server")
    BASE_DIR = Path(__file__).resolve().parents[1]  # 상위 두 단계로 이동하여 최상위 디렉토리 참조

SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'test.db')}"
print(f"Base Directory:{BASE_DIR}")
print(f"Database Path:{SQLALCHEMY_DATABASE_URL}")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
