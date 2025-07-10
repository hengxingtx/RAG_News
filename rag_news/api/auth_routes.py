#! python3
# -*- encoding: utf-8 -*-
###############################################################
#          @Time    :   2025/07/09 17:40:36
#          @Author  :   heng
#          @Contact :   hengsblog@163.com
###############################################################
"""
@comment: 用户认证路由
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from rag_news.core.database import get_db
from rag_news.api.auth_utils import (
    authenticate_user, create_access_token,
    Token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user
)

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录API，验证用户并返回访问令牌
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user = Depends(get_current_active_user)):
    """
    获取当前用户信息
    """
    return {
        "username": current_user.username,
        "email": current_user.email,
        "id": current_user.id
    } 