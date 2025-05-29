## 💡 RAG_News 项目出发点

本项目基于实际案例: RAG（Retrieval-Augmented Generation）搭建完整的新闻/舆情创作系统, 来全面跟踪及学习RAG系统, 帮助初学者提供一个架构清晰的实践项目。本项目中我会提供尽可能清晰的日志、项目架构，并规范代码注释及开源文档。

## 🌟 主要功能

RAG_NEWS 致力于覆盖 RAG 应用的全流程关键环节：

● 📁 知识库管理：搭建一套完整的知识库接口，支持知识库的相关操作。

● 📁 不同类型文件解析：支持处理多种类型文档，自动进行文本分割，关联源知识及文档向量化。

● ✖️ 异步及多进程支持：embedding采用异步多进程方式实现，支持批量上传并同步向量化。

● 🧠 多种切句方式： 支持传统分句及自主迭代的针对中英文的不同切割子句并融合的方式。

● 🔍 多种检索策略：根据不同任务，利用FAISS、BM25、LLM-Embedding或融合方式进行检索，提高检索召回率和准确性。

● 🔄 重排模型：重排模型及LLM对检索结果进行重排序，优化相关性。

● 🌐 实时网页搜索与预处理： 通过配置 DuckDuckGo 或 Google Search API 等工具实时抓取网络信息，并集成预处理流程（如清洗、摘要提取）为后续处理做准备。

● 🤖 灵活的多 LLM 支持： 通过兼容 OpenAI API 规范的方式，无缝支持调用多种本地部署或云端的开源/商业大语言模型（如 GPT 系列、 Claude、 Llama 系列、 ChatGLM 等）。

● ✅ 抑制幻觉 (Hallucination Mitigation)：：在回答中提供多种信息来源。

● 🖥️ 用户友好界面：使用streamlit搭建的自定义管理界面。

● 📝 智能新闻创作引擎： 借鉴并融合业界 RAG 系统的最佳实践，设计并实现了流畅、连贯且信息丰富的新闻稿件自动生成功能。

## 🔥 更新详情  <a href="./Update.md">更新详情</a>

- 2025-05-18 项目初始化.
- 2025-05-20 项目环境搭建及readMe编写.
- 2025-05-21 项目架构搭建.
- 2025-05-30 简易Duckduckgo搜索与问句改写


## 项目TODO

- 完整项目baseline

## 🎉 关注项目

⭐️ 点击右上角的 Star 关注 RAG_NEWs，可以获取最新发布的实时通知 !🌟


## 🎬 快速开始

### 🔨 以源代码启动服务(暂不支持docker方式)，本项目使用uv管理python环境

1. 安装uv和git检查工具。如已经安装，可跳过本步骤：

   ```bash
   pipx install uv pre-commit
   export UV_INDEX=https://mirrors.aliyun.com/pypi/simple
   ```

2. 下载源代码并安装 Python 依赖：

   ```bash
   git clone https://github.com/hengxingtx/RAG_News.git
   cd RAG_News/
   uv sync --python 3.10 --all-extras
   uv run download_deps.py
   pre-commit install
   ```

<!-- 3. 启动/停止/重启服务：

   ```bash
   source .venv/bin/activate
   export PYTHONPATH=$(pwd)
   bash bin/control.sh start/stop/restart
   ``` -->
