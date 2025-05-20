## 💡 RAG_News 项目出发点

本项目基于实际案例: RAG（Retrieval-Augmented Generation）搭建完整的新闻/舆情创作系统, 来全面跟踪及学习RAG系统, 帮助初学者提供一个架构清晰的实践项目。本项目中我会提供尽可能清晰的日志、项目架构，并规范代码注释及开源文档。

## 🌟 主要功能

*   📁 **知识库管理**：搭建一套完整的知识库接口，支持知识库的相关操作。
*   📁 **解析不同类型文件**：支持处理多种类型文档，自动进行文本分割，关联源知识及文档向量化。
*   ✖️ **异步及多进程支持**：embedding采用异步多进程方式实现，支持批量上传并同步向量化。
*   🧠 **多种切句方式**： 支持传统分句及自主迭代的针对中英文的不同切割子句并融合的方式。
*   🔍 **多种检索策略**：根据不同任务，利用FAISS、BM25、LLM-Embedding或融合方式进行检索，提高检索召回率和准确性。
*   🔄 **重排模型**：重排模型及LLM对检索结果进行重排序，优化相关性。
*   🕸️ **网页搜索及预处理**：通过配置duckduckgo或googleSearch实时爬取网络信息，并进行预处理。
*   🗣️ **多LLM支持**：通过符合openai规范的接口方式实现本地及在线llm的支持。
*   📄 **有理有据、最大程度降低幻觉（hallucination）**：在回答中提供多种信息来源。
*   🖥️ **用户友好界面**：使用streamlit搭建的自定义管理界面。
*   🖥️ **流畅的AI新闻创作**：借鉴业界主流的不同RAG系统中的优秀实现，实现新闻创作功能。

## 🔥 更新详情

<a href="./Update.md">更新详情</a>

## 🎉 关注项目

⭐️ 点击右上角的 Star 关注 RAG_NEWs，可以获取最新发布的实时通知 !🌟


## 🎬 快速开始

### 🔨 以源代码启动服务(暂不支持docker方式)，本项目使用uv管理python环境

1. 安装 uv和git检查工具。如已经安装，可跳过本步骤：

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

3. 启动/停止/重启服务：

   ```bash
   source .venv/bin/activate
   export PYTHONPATH=$(pwd)
   bash bin/control.sh start/stop/restart
   ```
