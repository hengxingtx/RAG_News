from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent.parent))

# 导入顺序很重要，先导入数据库定义
from rag_news.core.database import engine, Base, SessionLocal

# 然后导入用户模型
from rag_news.core.models.user import User
from rag_news.core.models.knowledge_base import KnowledgeBase, KnowledgeFile

# 最后导入路由
from rag_news.api.auth_routes import router as auth_router
from rag_news.api.knowledge_base_routes import kb_router

# 创建数据库表
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用程序生命周期事件处理器"""
    # 启动时执行
    create_test_user()
    yield
    # 关闭时执行
    pass


# 创建测试用户函数
def create_test_user():
    """创建测试用户，仅用于开发环境"""
    from sqlalchemy.orm import Session

    # 创建测试用户
    db = SessionLocal()
    try:
        # 检查用户是否已存在
        test_user = db.query(User).filter(User.username == "admin").first()
        if not test_user:
            new_user = User(
                username="admin",
                hashed_password=User.create_password_hash("password"),
                email="admin@example.com",
                is_active=True,
            )
            db.add(new_user)
            db.commit()
            print("已创建测试用户: admin (密码: password)")
    finally:
        db.close()


app = FastAPI(title="RAG News API", version="0.1.0", lifespan=lifespan)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(auth_router, prefix="/api")
app.include_router(kb_router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "欢迎使用RAG News API"}


# 如果直接运行此文件，则启动服务器
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8006)

# 启动命令: uvicorn rag_news.api.server:app --reload
# 或者: python -m rag_news.api.server
