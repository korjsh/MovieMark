from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.user import create_user, get_user_by_email
from app.schemas.user import UserCreate, UserResponse
from app.database import get_db
from app.auth_utils import create_access_token, create_refresh_token, verify_refresh_token, hash_password, verify_password
import datetime
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 암호화 객체를 가져오기
@router.post("/signup/", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    
    # 비밀번호 해싱
    # hashed_password = hash_password(user.password)
    # user_data = user.dict()
    # user_data["password"] = hashed_password
    # new_user = create_user(db=db, user=UserCreate(**user_data))
    new_user = create_user(db=db, user=user)

    return new_user

@router.post("/login/")
def login(user: UserCreate, db: Session = Depends(get_db)):
    print(f"Request payload: {user}")
    db_user = get_user_by_email(db, email=user.email)
    print(f"db_user: {db_user.email}")
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found with this email.")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Password does not match.")

    # Access Token 및 Refresh Token 생성
    access_token_expires = datetime.timedelta(minutes=15)
    refresh_token_expires = datetime.timedelta(days=7)
    access_token = create_access_token(
        data={"id": db_user.id, "sub": db_user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"id": db_user.id, "sub": db_user.email}, expires_delta=refresh_token_expires
    )

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh/")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    # Refresh Token 검증
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    db_user = get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 새로운 Access Token 생성
    access_token_expires = datetime.timedelta(minutes=15)
    new_access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )

    return {"access_token": new_access_token, "refresh_token": refresh_token, "token_type": "bearer"}
