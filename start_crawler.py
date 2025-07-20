#!/usr/bin/env python
"""
热榜爬虫启动脚本
"""
import sys
import asyncio
import argparse

def main():
    """主函数，启动爬虫"""
    # 将当前目录添加到模块搜索路径，以便导入rag_news模块
    sys.path.insert(0, ".")
    
    # 导入rag_news模块
    from rag_news.sources import source_manager
    
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="热榜爬虫")
    parser.add_argument("-s", "--source", help="指定要抓取的源ID")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("-l", "--list", action="store_true", help="列出所有可用的源")
    parser.add_argument("--no-cache", action="store_true", help="不使用缓存")
    parser.add_argument("--force", action="store_true", help="强制刷新缓存")
    parser.add_argument("--top", type=int, default=0, help="只显示前N条结果，默认显示全部")
    args = parser.parse_args()
    
    # 传递命令行参数给main函数
    from rag_news.main import main as crawler_main
    
    # 如果指定了--top参数，设置环境变量
    if args.top > 0:
        sys.environ["RAG_NEWS_TOP_N"] = str(args.top)
    
    # 运行爬虫
    asyncio.run(crawler_main())

if __name__ == "__main__":
    main() 