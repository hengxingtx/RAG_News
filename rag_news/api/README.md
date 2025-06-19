# RAG News API

RAG News系统的后端API，使用FastAPI框架构建。

## 依赖安装

### 方法1：使用安装脚本

我们提供了一个自动安装所有依赖的脚本：

```bash
# 在项目根目录下运行
python -m rag_news.api.install_dependencies
```

### 方法2：手动安装

或者，手动安装所需的Python依赖:

```bash
pip install fastapi uvicorn sqlalchemy pydantic "python-jose[cryptography]" bcrypt python-multipart
```

## 启动服务器

有几种方式可以启动开发服务器:

### 方法1：使用Python模块运行（推荐）

```bash
# 在项目根目录下运行
python -m rag_news.api.server
```

### 方法2：使用uvicorn启动

```bash
# 在项目根目录下运行
uvicorn rag_news.api.server:app --reload
```

服务器将在 `http://localhost:8000` 上运行。

## 常见问题排查

1. **导入错误**：确保您在**项目根目录**下运行服务器命令。

2. **依赖问题**：确保所有依赖都已正确安装，尤其是 `python-jose[cryptography]`。

3. **数据库问题**：首次运行会自动创建SQLite数据库文件。如果有权限问题，请检查目录权限。

4. **端口占用**：如果8000端口已被占用，可以使用不同的端口：
   ```bash
   python -m rag_news.api.server --port 8080
   ```

## API文档

服务器启动后，访问以下URL查看自动生成的API文档:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 测试账户

系统自动创建了一个测试账户:

- 用户名: admin
- 密码: password

## API端点

- `POST /api/login`: 用户登录
- `GET /api/users/me`: 获取当前登录用户信息 