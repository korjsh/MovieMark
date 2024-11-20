from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.user import create_user, get_user_by_email
from app.schemas.user import UserCreate, UserResponse
from app.database import get_db
from app.auth_utils import create_access_token, create_refresh_token
from passlib.context import CryptContext
import datetime

router = APIRouter()

# 암호화 객체를 가져오기
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup/", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = create_user(db=db, user=user)
    return new_user

@router.post("/login/")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Access Token 및 Refresh Token 생성
    access_token_expires = datetime.timedelta(minutes=15)
    refresh_token_expires = datetime.timedelta(days=7)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": db_user.email}, expires_delta=refresh_token_expires
    )

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
