from sqlalchemy.orm import Session
from app.models.user import User  # 수정: models에서 직접 User 모델만 import
from app.schemas.user import UserCreate
from passlib.context import CryptContext

# 암호화 객체 생성
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 이메일로 사용자 검색
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# 사용자 ID로 검색
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# 새 사용자 생성
def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        is_active=True,
        # is_verified=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
