import asyncio
import json
import argparse
import sys
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import time

from .sources import source_manager
from .sources.utils import NewsItem
from .cache import memory_cache, file_cache

async def fetch_source(source_id: str, use_cache: bool = True, cache_force: bool = False) -> List[Dict[str, Any]]:
    """
    获取单个源的数据
    
    Args:
        source_id: 源ID
        use_cache: 是否使用缓存
        cache_force: 是否强制刷新缓存
    """
    cache_key = f"source_{source_id}"
    
    # 如果使用缓存且不是强制刷新
    if use_cache and not cache_force:
        # 优先使用内存缓存
        cached_data = memory_cache.get(cache_key)
        if cached_data:
            print(f"使用内存缓存: {source_id}")
            return cached_data
        
        # 其次使用文件缓存
        cached_data = file_cache.get(cache_key)
        if cached_data:
            print(f"使用文件缓存: {source_id}")
            # 同步到内存缓存
            memory_cache.set(cache_key, cached_data)
            return cached_data
    
    try:
        # 获取新数据
        items = await source_manager.fetch_from_source(source_id)
        data = [item.to_dict() for item in items]
        
        # 更新缓存
        if use_cache:
            memory_cache.set(cache_key, data)
            file_cache.set(cache_key, data)
        
        return data
    except Exception as e:
        print(f"获取{source_id}失败: {e}", file=sys.stderr)
        return []

async def fetch_all_sources(use_cache: bool = True, cache_force: bool = False) -> Dict[str, List[Dict[str, Any]]]:
    """获取所有源的数据"""
    all_data = {}
    for source_id in source_manager.get_all_sources().keys():
        all_data[source_id] = await fetch_source(source_id, use_cache, cache_force)
    return all_data

def save_to_file(data: Dict[str, Any], filename: str) -> None:
    """保存数据到文件"""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"数据已保存到 {path}")

def print_items(items: List[Dict[str, Any]], title: str = None) -> None:
    """打印条目列表"""
    if title:
        print(f"\n=== {title} ===")
    
    # 检查是否设置了TOP_N环境变量
    top_n = os.environ.get("RAG_NEWS_TOP_N")
    if top_n and top_n.isdigit() and int(top_n) > 0:
        top_n = int(top_n)
        items = items[:top_n]
        if title:
            print(f"(只显示前{top_n}条)")
    
    for idx, item in enumerate(items, 1):
        print(f"{idx}. {item['title']}")
        print(f"   链接: {item['url']}")
        if item.get('extra') and item['extra'].get('info'):
            print(f"   信息: {item['extra']['info']}")
        print()

async def main():
    parser = argparse.ArgumentParser(description="热榜爬虫")
    parser.add_argument("-s", "--source", help="指定要抓取的源ID")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("-l", "--list", action="store_true", help="列出所有可用的源")
    parser.add_argument("--no-cache", action="store_true", help="不使用缓存")
    parser.add_argument("--force", action="store_true", help="强制刷新缓存")
    args = parser.parse_args()
    
    use_cache = not args.no_cache
    cache_force = args.force
    
    if args.list:
        print("可用的热榜源:")
        for idx, (source_id, source) in enumerate(source_manager.get_all_sources().items(), 1):
            print(f"{idx}. {source_id} - {source.name}")
        return
    
    if args.source:
        if args.source not in source_manager.get_all_sources():
            print(f"未知的源ID: {args.source}", file=sys.stderr)
            print("可用的源: " + ", ".join(source_manager.get_all_sources().keys()))
            return
            
        # 获取单个源的数据
        start_time = time.time()
        items = await fetch_source(args.source, use_cache, cache_force)
        end_time = time.time()
        
        source = source_manager.get_source(args.source)
        print_items(items, f"{source.name} ({len(items)}条)")
        print(f"耗时: {end_time - start_time:.2f}秒")
        
        # 保存到文件
        if args.output:
            save_to_file({args.source: items}, args.output)
    else:
        # 获取所有源的数据
        start_time = time.time()
        all_data = await fetch_all_sources(use_cache, cache_force)
        end_time = time.time()
        
        # 打印所有数据
        for source_id, items in all_data.items():
            source = source_manager.get_source(source_id)
            print_items(items, f"{source.name} ({len(items)}条)")
        
        print(f"总耗时: {end_time - start_time:.2f}秒")
        
        # 保存到文件
        if args.output:
            save_to_file(all_data, args.output)

if __name__ == "__main__":
    asyncio.run(main()) 