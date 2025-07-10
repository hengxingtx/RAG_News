#! python3
# -*- encoding: utf-8 -*-
###############################################################
#          @Time    :   2025/07/09 17:46:45
#          @Author  :   heng
#          @Contact :   hengsblog@163.com
###############################################################
"""
@comment: 知识库路由
"""

import os
import uuid
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from rag_news.core.database import get_db
from rag_news.core.models.knowledge_base import KnowledgeBase, KnowledgeFile
from rag_news.api.auth_utils import get_current_active_user
from rag_news.core.models.user import User

# 创建路由
kb_router = APIRouter(prefix="/knowledge-base", tags=["知识库"])

# 模型定义
class KnowledgeBaseCreate(BaseModel):
    name: str
    description: Optional[str] = None

class KnowledgeBaseResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    file_count: int

    class Config:
        from_attributes = True

class KnowledgeFileResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# 创建知识库
@kb_router.post("/", response_model=KnowledgeBaseResponse)
async def create_knowledge_base(
    kb: KnowledgeBaseCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 检查知识库名称是否已存在
    existing_kb = db.query(KnowledgeBase).filter(KnowledgeBase.name == kb.name).first()
    if existing_kb:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="知识库名称已存在"
        )
    
    # 创建新知识库
    new_kb = KnowledgeBase(
        name=kb.name,
        description=kb.description,
        created_by=current_user.id
    )
    
    db.add(new_kb)
    db.commit()
    db.refresh(new_kb)
    
    # 创建知识库文件夹
    kb_dir = os.path.join("rag_news", "data", "knowledge_bases", str(new_kb.id))
    os.makedirs(kb_dir, exist_ok=True)
    
    # 返回响应
    return {
        "id": new_kb.id,
        "name": new_kb.name,
        "description": new_kb.description,
        "created_at": new_kb.created_at,
        "updated_at": new_kb.updated_at,
        "file_count": 0
    }

# 获取所有知识库
@kb_router.get("/", response_model=List[KnowledgeBaseResponse])
async def get_knowledge_bases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 查询所有知识库
    knowledge_bases = db.query(KnowledgeBase).filter(
        KnowledgeBase.is_active == True
    ).all()
    
    result = []
    for kb in knowledge_bases:
        # 计算文件数量
        file_count = db.query(KnowledgeFile).filter(
            KnowledgeFile.knowledge_base_id == kb.id
        ).count()
        
        result.append({
            "id": kb.id,
            "name": kb.name,
            "description": kb.description,
            "created_at": kb.created_at,
            "updated_at": kb.updated_at,
            "file_count": file_count
        })
    
    return result

# 获取单个知识库
@kb_router.get("/{kb_id}", response_model=KnowledgeBaseResponse)
async def get_knowledge_base(
    kb_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 查询知识库
    kb = db.query(KnowledgeBase).filter(
        KnowledgeBase.id == kb_id,
        KnowledgeBase.is_active == True
    ).first()
    
    if not kb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识库不存在"
        )
    
    # 计算文件数量
    file_count = db.query(KnowledgeFile).filter(
        KnowledgeFile.knowledge_base_id == kb.id
    ).count()
    
    return {
        "id": kb.id,
        "name": kb.name,
        "description": kb.description,
        "created_at": kb.created_at,
        "updated_at": kb.updated_at,
        "file_count": file_count
    }

# 上传文件到知识库
@kb_router.post("/{kb_id}/upload", response_model=KnowledgeFileResponse)
async def upload_file(
    kb_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 查询知识库
    kb = db.query(KnowledgeBase).filter(
        KnowledgeBase.id == kb_id,
        KnowledgeBase.is_active == True
    ).first()
    
    if not kb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识库不存在"
        )
    
    # 获取文件信息
    original_filename = file.filename
    file_extension = os.path.splitext(original_filename)[1] if original_filename else ""
    file_type = file.content_type
    
    # 生成唯一文件名
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # 保存文件
    kb_dir = os.path.join("rag_news", "data", "knowledge_bases", str(kb.id))
    os.makedirs(kb_dir, exist_ok=True)
    
    file_path = os.path.join(kb_dir, unique_filename)
    
    # 写入文件
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 创建文件记录
    file_size = os.path.getsize(file_path)
    
    new_file = KnowledgeFile(
        filename=unique_filename,
        original_filename=original_filename,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
        knowledge_base_id=kb.id,
        uploaded_by=current_user.id,
        status="pending"  # 初始状态为待处理
    )
    
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    
    return new_file

# 获取知识库的所有文件
@kb_router.get("/{kb_id}/files", response_model=List[KnowledgeFileResponse])
async def get_knowledge_base_files(
    kb_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 查询知识库
    kb = db.query(KnowledgeBase).filter(
        KnowledgeBase.id == kb_id,
        KnowledgeBase.is_active == True
    ).first()
    
    if not kb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识库不存在"
        )
    
    # 查询文件
    files = db.query(KnowledgeFile).filter(
        KnowledgeFile.knowledge_base_id == kb.id
    ).all()
    
    return files

# 删除知识库
@kb_router.delete("/{kb_id}")
async def delete_knowledge_base(
    kb_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 查询知识库
    kb = db.query(KnowledgeBase).filter(
        KnowledgeBase.id == kb_id,
        KnowledgeBase.is_active == True
    ).first()
    
    if not kb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识库不存在"
        )
    
    # 标记为非活动状态（软删除）
    kb.is_active = False
    db.commit()
    
    return {"message": "知识库已删除"}

# 删除文件
@kb_router.delete("/{kb_id}/files/{file_id}")
async def delete_file(
    kb_id: int,
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 查询文件
    file = db.query(KnowledgeFile).filter(
        KnowledgeFile.id == file_id,
        KnowledgeFile.knowledge_base_id == kb_id
    ).first()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )
    
    # 删除文件
    if os.path.exists(file.file_path):
        os.remove(file.file_path)
    
    # 删除数据库记录
    db.delete(file)
    db.commit()
    
    return {"message": "文件已删除"} 