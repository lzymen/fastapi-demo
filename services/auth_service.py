from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from config import settings
from models.user import User
from schemas.user import UserCreate, UserLogin, Token
from utils.security import (
    get_password_hash,
    verify_password,
    create_access_token
)


class AuthService:
    """认证服务"""

    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        """注册用户"""
        # 检查用户名是否已存在
        existing_user = db.query(User).filter(
            (User.username == user_data.username) | (User.email == user_data.email)
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered"
            )

        # 创建新用户
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, user_data: UserLogin) -> Token:
        """用户认证"""
        user = db.query(User).filter(User.username == user_data.username).first()
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 创建访问令牌
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return Token(access_token=access_token, token_type="bearer")


# 创建全局服务实例
auth_service = AuthService()
