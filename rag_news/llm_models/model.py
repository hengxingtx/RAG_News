#! python3
# -*- encoding: utf-8 -*-
###############################################################
#          @Time    :   2025/07/07 20:17:04
#          @Author  :   heng
#          @Contact :   hengsblog@163.com
###############################################################
"""
@comment: 模型配置
"""

from rag_news.utils.logging import logger
import yaml
import httpx
from langchain_openai import ChatOpenAI

with open("rag_news/configs/config.yaml", "r") as f:
    config = yaml.safe_load(f)

openai_api_key = config["openai_api_key"]
qwen_api_key = config["qwen_api_key"]


Qwen3_MODEL = ChatOpenAI(
    model="qwen-plus-latest",  # 或 "gpt-4o", "gpt-4o-mini" 等
    temperature=0.7,
    max_tokens=1500,
    timeout=60,
    max_retries=2,
    api_key=qwen_api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 使用联网工具
Qwen3_MODEL_WITH_WEB = ChatOpenAI(
    model="qwen-plus-latest",  # 或 "gpt-4o", "gpt-4o-mini" 等
    temperature=0.7,
    max_tokens=1500,
    timeout=60,
    max_retries=2,
    api_key=qwen_api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    extra_body={"enable_search": True},
)


client = httpx.Client(proxy="http://127.0.0.1:7890")
GPT4_MODEL = ChatOpenAI(
    model="gpt-4o-mini",  # 或 "gpt-4o", "gpt-4o-mini" 等
    temperature=0.7,
    max_tokens=1500,
    timeout=60,
    max_retries=2,
    api_key=openai_api_key,
    http_client=client,
)

# 使用联网工具
GPT4_MODEL_WITH_WEB = ChatOpenAI(
    model="gpt-4",  # 或 "gpt-4o", "gpt-4o-mini" 等
    temperature=0.7,
    max_tokens=1500,
    timeout=60,
    max_retries=2,
    api_key=openai_api_key,
    http_client=client,
    model_kwargs={"tools": [{"type": "web_search_preview"}]},
)


def parse_gpt4_web_response(resp):
    """
    从 GPT-4 联网响应中提取纯文本回答，并返回完整信息用于日志记录。
    """
    text_content = ""
    blocks = []

    if isinstance(resp.content, list):
        for block in resp.content:
            if block.get("type") == "text":
                text_content += block.get("text", "") + "\n"
                blocks.append(block)
            else:
                blocks.append(block)
    else:
        text_content = str(resp.content)

    return {
        "text": text_content.strip(),
        "blocks": blocks,
        "metadata": resp.response_metadata,
        "usage": resp.usage_metadata,
        "id": resp.id,
    }


def main():
    """main"""
    result = GPT4_MODEL_WITH_WEB.invoke("https://tieba.baidu.com/hottopic/browse/hottopic?topic_id=28343419&amp;topic_name=AL%E5%86%B3%E8%83%9C%E5%B1%80%E8%BE%93T1%E8%B0%81%E8%83%8C%E9%94%85该链接的原文是什么")
    result = parse_gpt4_web_response(result)["text"]
    print(result)


if __name__ == "__main__":
    main()
