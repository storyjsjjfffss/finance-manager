"""用户注册与登录路由。"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from auth import create_access_token, get_password_hash, verify_password
from database import get_session
from models import User
from schemas import UserCreate


router = APIRouter()


@router.post("/register")
def register_user(
    user: UserCreate,
    session: Session = Depends(get_session),
):
    existing_user = session.exec(
        select(User).where(User.username == user.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="用户名已被注册",
        )

    new_user = User(
        username=user.username,
        password_hash=get_password_hash(user.password),
    )

    session.add(new_user)
    session.commit()

    return {"message": "注册成功"}


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    db_user = session.exec(
        select(User).where(User.username == form_data.username)
    ).first()

    if db_user is None:
        raise HTTPException(
            status_code=400,
            detail="用户名或密码错误",
        )

    if not verify_password(
        form_data.password,
        db_user.password_hash,
    ):
        raise HTTPException(
            status_code=400,
            detail="用户名或密码错误",
        )

    access_token = create_access_token(
        data={"sub": db_user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
