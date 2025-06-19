from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite数据库URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./rag_news.db"

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 定义基本模型
Base = declarative_base()

# 获取数据库会话的依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 