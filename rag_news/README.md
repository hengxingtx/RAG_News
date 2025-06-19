# RAG News 系统

RAG News 是一个基于检索增强生成(Retrieval Augmented Generation)技术的新闻系统。

## 系统组件

系统分为两部分：

1. 后端API (FastAPI)
2. 前端界面 (React + Vite)

## 启动系统

### 第一步：启动后端API

有多种方式可以启动后端API服务：

#### 方法1：使用启动脚本（推荐）

```bash
# 在项目根目录下运行
python rag_news/start_api.py
```

此脚本会自动检测是否有端口冲突，如果默认的8000端口被占用，会自动选择一个可用的端口。

您也可以手动指定端口：

```bash
python rag_news/start_api.py --port 8001
```

#### 方法2：直接使用Python模块

```bash
python -m rag_news.api.server
```

#### 方法3：使用uvicorn

```bash
uvicorn rag_news.api.server:app --reload
```

### 第二步：启动前端

确保后端API服务器正常运行在端口8000上（默认设置）。

启动前端开发服务器：

```bash
cd rag_news/frontend
npm install  # 首次运行时安装依赖

# 以下两个命令均可启动开发服务器
npm run dev  # Vite推荐的启动方式
# 或
npm start    # 兼容方式
```

前端开发服务器启动后，通常会在浏览器中自动打开 `http://localhost:5173` 地址。

## 登录系统

系统预置了一个测试账户：

- 用户名: admin
- 密码: password

## 常见问题解决

### 端口冲突

如果遇到端口被占用的错误：

```
ERROR: [Errno 48] Address already in use
```

使用 `start_api.py` 脚本启动，它会自动查找可用端口：

```bash
python rag_news/start_api.py
```

或者手动指定一个不同的端口：

```bash
python rag_news/start_api.py --port 8001
```

### 依赖安装问题

安装所有必要的依赖：

```bash
python -m rag_news.api.install_dependencies
```

### 前端API连接问题

如果前端无法连接到后端API，请确保后端服务器运行在端口8000上。如果需要更改API地址，请修改`rag_news/frontend/src/pages/Login.tsx`文件中的`API_BASE_URL`常量。

### "Missing script: start" 错误

如果遇到 `npm ERR! Missing script: "start"` 错误，请使用 `npm run dev` 命令代替 `npm start` 命令启动前端。这是因为项目使用了Vite构建工具，其默认启动命令是 `dev`。 