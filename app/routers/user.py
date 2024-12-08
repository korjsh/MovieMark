from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.user import get_user_by_id
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
from app.database import get_db

router = APIRouter()

# @router.get("/{user_id}/", response_model=UserResponse)
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     user = get_user_by_id(db, user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
@router.get("/", response_model=UserResponse)
def get_user(db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
):
    user = get_user_by_id(db, current_user.id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
