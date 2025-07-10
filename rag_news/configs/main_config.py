#! python3
# -*- encoding: utf-8 -*-
###############################################################
#          @Time    :   2025/07/07 18:48:28
#          @Author  :   heng
#          @Contact :   hengsblog@163.com
###############################################################
"""
@comment: 使用中的配置信息
"""
from model import Qwen3, GPT4, Qwen3Thinking
import os


# 知识库配置
DEFAULT_KNOWLEDGE_BASE = "test"
EMBEDDING_MODEL_PATH = "./embedding_models/embedding_fengkong"
EMBEDDING_DEVICE = "auto"
RERANK_MODEL_PATH = "./embedding_models/rerank_model"


KB_ROOT_PATH = "../ai_write/knowledge_db_save"
if not os.path.exists(KB_ROOT_PATH):
    os.mkdir(KB_ROOT_PATH)


# 检索配置
OUTLINE_TOP_K = 30  # 生成大纲时抽取的关联文章数量(这里每篇文章摘要大概200字)
GEN_TOP_K = 20  # 生成事件详情时抽取的关联文章数量
EVENT_INFOS_TOP_K = 100  # 事件信息检索时抽取的关联片段数量
OVERVIEW_TOP_K = 20
ANALYSIS_TOP_K = 10  # 分析研判时用到的topk关联文档

TITLE_RERANK_TOP_K = 1
ZH_chunk_size = 600
EN_chunk_size = 1500

# 分割配置
CHUNK_SIZE = 400
PARENT_CHUNK_SIZE = 800
SENTENCE_SIZE = 100

# 阈值配置
THRESHOLD = 0.35
THRESHOLD_Summary = 0.1

# 生成配置
LOCAL_EMBED_PATH = "./embedding_models/embedding_fengkong"
LOCAL_RERANK_PATH = "./embedding_models/rerank_model"

LOCAL_RERANK_SERVICE_URL = "localhost:8001"
LOCAL_RERANK_MODEL_NAME = "rerank"
LOCAL_RERANK_MAX_LENGTH = 512
LOCAL_RERANK_BATCH = 1
LOCAL_RERANK_THREADS = 1

LOCAL_EMBED_MODEL_NAME = "embed"
LOCAL_EMBED_MAX_LENGTH = 512
LOCAL_EMBED_BATCH = 1
LOCAL_EMBED_THREADS = 1

HOSTNAME = "localhost"

# port配置
KNOWLEDGE_DB_PORT = 8001

# 模型配置
Device = 'cpu'
UsedModel = Qwen3
UsedModel_Thinking = Qwen3Thinking