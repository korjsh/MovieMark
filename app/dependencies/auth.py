from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import decode, ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
import os

auth_scheme = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_current_user(db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    # Authorization 헤더에서 Bearer 토큰 추출
    token = token.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # JWT 디코딩
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # 사용자 계정 (email)
        
        if not email:
            raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise credentials_exception

    # 데이터베이스에서 사용자 검색
    user = db.query(User).filter(User.email == email).first()  # 이메일 기반 검색
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
