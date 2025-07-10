from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from rag_news.core.database import Base

class KnowledgeBase(Base):
    __tablename__ = "knowledge_bases"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    user = relationship("User", backref="knowledge_bases")
    files = relationship("KnowledgeFile", back_populates="knowledge_base", cascade="all, delete-orphan")

class KnowledgeFile(Base):
    __tablename__ = "knowledge_files"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    original_filename = Column(String)
    file_path = Column(String)
    file_type = Column(String)
    file_size = Column(Integer)  # 文件大小（字节）
    knowledge_base_id = Column(Integer, ForeignKey("knowledge_bases.id"))
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")  # pending, processing, completed, error
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    knowledge_base = relationship("KnowledgeBase", back_populates="files")
    user = relationship("User", backref="uploaded_files") 