import jwt
import datetime
from typing import Optional
from dotenv import load_dotenv
import os
import bcrypt


load_dotenv()  # .env 파일 로드
SECRET_KEY = os.getenv("SECRET_KEY") # 보안상의 이유로 환경 변수로 관리하는 것이 좋음
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_refresh_token(token: str) -> Optional[dict]:
    """
    Refresh Token의 유효성을 검증하는 함수.

    Args:
        token (str): 검증할 Refresh Token.
    
    Returns:
        Optional[dict]: 유효한 경우 디코딩된 토큰의 payload를 반환, 유효하지 않은 경우 None 반환.
    """
    try:
        # 토큰 디코딩 (유효성 검증 포함)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # 유효한 경우 payload 반환
    except jwt.ExpiredSignatureError:
        # 토큰이 만료된 경우
        return None
    except jwt.InvalidTokenError:
        # 기타 토큰이 유효하지 않은 경우
        return None


def hash_password(password: str) -> str:
    # 비밀번호를 바이트 형태로 인코딩
    password_bytes = password.encode('utf-8')
    # 솔트 생성 및 비밀번호 해싱
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # 해시된 비밀번호를 문자열로 반환
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 입력한 비밀번호와 해시된 비밀번호를 바이트 형태로 인코딩
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    # 비밀번호 검증
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)