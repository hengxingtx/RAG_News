#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
from rag_news.sources.tieba import TiebaHotList

async def test_tieba():
    """测试百度贴吧热榜爬虫"""
    print("开始测试百度贴吧热榜爬虫...")
    
    tieba_crawler = TiebaHotList()
    items = await tieba_crawler.fetch_items()
    
    print(f"获取到 {len(items)} 条热门话题")
    
    # 打印前5条数据
    for i, item in enumerate(items[:5]):
        print(f"\n--- 话题 {i+1} ---")
        print(f"标题: {item.title}")
        print(f"链接: {item.url}")
        print(f"ID: {item.id}")
        extra_info = json.dumps(item.extra, ensure_ascii=False, indent=2)
        print(f"额外信息: {extra_info}")
    
    print("\n测试完成")

if __name__ == "__main__":
    asyncio.run(test_tieba()) 