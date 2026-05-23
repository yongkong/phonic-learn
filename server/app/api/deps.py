from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User


def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db),
) -> User:
    """从 Authorization header 中解析 token 并获取当前用户"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")

    token = authorization.replace("Bearer ", "").strip()
    user = db.query(User).filter(User.token == token).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user
