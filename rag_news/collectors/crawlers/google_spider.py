# -*- coding: utf-8 -*-
# =============================================================================
# 文件名称: google_spider.py
# 创建时间: 2025-07-21 22:59
# 作者: heng
# =============================================================================
# 使用Crawl4ai进行谷歌搜索的示例

import asyncio
import urllib.parse
from crawl4ai import AsyncWebCrawler
import json
import random
import time

# 示例1：基础Google搜索
async def basic_google_search(query):
    """基础的Google搜索爬取"""
    # 构建Google搜索URL
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    
    # 使用realistic user agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive"
    }
    
    async with AsyncWebCrawler(headless=True, verbose=True) as crawler:
        try:
            result = await crawler.arun(
                url=search_url,
                headers=headers,
                wait_for="css:div#search",  # 等待搜索结果容器加载
                delay_before_return_html=3.0,  # 等待页面完全加载
                css_selector="div.g"  # 提取搜索结果项
            )
            
            print(f"搜索查询: {query}")
            print(f"搜索URL: {search_url}")
            print(f"状态码: {result.status_code}")
            print(f"页面标题: {result.metadata.get('title', 'N/A')}")
            print(f"提取的内容长度: {len(result.extracted_content) if result.extracted_content else 0}")
            
            # 输出部分内容
            if result.extracted_content:
                print("搜索结果内容（前1000字符）:")
                print(result.extracted_content[:1000])
            else:
                print("Markdown内容（前1000字符）:")
                print(result.markdown[:1000])
                
        except Exception as e:
            print(f"搜索失败: {e}")

# 示例2：解析Google搜索结果
async def parse_google_results(query):
    """解析Google搜索结果的结构化数据"""
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&num=10"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    async with AsyncWebCrawler(headless=True) as crawler:
        try:
            result = await crawler.arun(
                url=search_url,
                headers=headers,
                wait_for="css:div#search",
                delay_before_return_html=2.0
            )
            
            # 提取搜索结果链接
            links = []
            if result.links and 'internal' in result.links:
                for link in result.links['internal']:
                    href = link.get('href', '')
                    text = link.get('text', '').strip()
                    # 过滤出真正的搜索结果链接
                    if href.startswith('/url?q=') and text and len(text) > 10:
                        # 解析实际URL
                        actual_url = urllib.parse.unquote(href.split('/url?q=')[1].split('&')[0])
                        links.append({
                            'title': text,
                            'url': actual_url
                        })
            
            print(f"找到 {len(links)} 个搜索结果:")
            for i, link in enumerate(links[:5], 1):  # 显示前5个结果
                print(f"{i}. {link['title']}")
                print(f"   URL: {link['url']}")
                print()
                
        except Exception as e:
            print(f"解析失败: {e}")

# 示例3：使用JavaScript执行更复杂的搜索
async def advanced_google_search(query):
    """使用JavaScript增强的Google搜索"""
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    
    # JavaScript代码来滚动页面并获取更多结果
    js_code = """
    // 滚动到页面底部
    window.scrollTo(0, document.body.scrollHeight);
    
    // 等待一下让内容加载
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 尝试点击"更多结果"按钮
    const moreButton = document.querySelector('a[aria-label="更多结果"]');
    if (moreButton) {
        moreButton.click();
        await new Promise(resolve => setTimeout(resolve, 2000));
    }
    """
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    async with AsyncWebCrawler(headless=True, verbose=True) as crawler:
        try:
            result = await crawler.arun(
                url=search_url,
                headers=headers,
                js_code=js_code,
                wait_for="networkidle",
                delay_before_return_html=3.0
            )
            
            print(f"高级搜索完成，内容长度: {len(result.markdown)}")
            print("页面内容片段:")
            print(result.markdown[:1500])
            
        except Exception as e:
            print(f"高级搜索失败: {e}")

# 示例4：批量Google搜索
async def batch_google_search(queries, delay=5):
    """批量进行Google搜索"""
    results = []
    
    async with AsyncWebCrawler(headless=True) as crawler:
        for i, query in enumerate(queries):
            try:
                print(f"正在搜索 {i+1}/{len(queries)}: {query}")
                
                search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
                
                result = await crawler.arun(
                    url=search_url,
                    headers={
                        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.{random.randint(1000,9999)} Safari/537.36"
                    },
                    wait_for="css:div#search",
                    delay_before_return_html=2.0
                )
                
                search_result = {
                    "query": query,
                    "url": search_url,
                    "status": result.status_code,
                    "title": result.metadata.get('title', ''),
                    "content_length": len(result.markdown),
                    "success": result.status_code == 200
                }
                
                results.append(search_result)
                
                # 添加延迟避免被封
                if i < len(queries) - 1:
                    print(f"等待 {delay} 秒...")
                    await asyncio.sleep(delay)
                    
            except Exception as e:
                print(f"搜索 '{query}' 失败: {e}")
                results.append({
                    "query": query,
                    "error": str(e),
                    "success": False
                })
    
    return results

# 示例5：使用代理进行Google搜索（如果有代理的话）
async def proxy_google_search(query, proxy_url=None):
    """使用代理进行Google搜索"""
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    
    config = {
        "headless": True,
        "verbose": True
    }
    
    # 如果提供了代理，添加到配置中
    if proxy_url:
        config["proxy"] = proxy_url
    
    async with AsyncWebCrawler(**config) as crawler:
        try:
            result = await crawler.arun(
                url=search_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                },
                wait_for="css:div#search",
                delay_before_return_html=2.0
            )
            
            print(f"代理搜索结果 - 状态码: {result.status_code}")
            print(f"内容长度: {len(result.markdown)}")
            
        except Exception as e:
            print(f"代理搜索失败: {e}")

# 示例6：搜索特定类型的内容（图片、新闻等）
async def specialized_google_search(query, search_type="web"):
    """搜索特定类型的Google内容"""
    base_url = "https://www.google.com/search"
    
    # 根据搜索类型构建URL
    if search_type == "images":
        search_url = f"{base_url}?q={urllib.parse.quote(query)}&tbm=isch"
    elif search_type == "news":
        search_url = f"{base_url}?q={urllib.parse.quote(query)}&tbm=nws"
    elif search_type == "videos":
        search_url = f"{base_url}?q={urllib.parse.quote(query)}&tbm=vid"
    else:
        search_url = f"{base_url}?q={urllib.parse.quote(query)}"
    
    async with AsyncWebCrawler(headless=True) as crawler:
        try:
            result = await crawler.arun(
                url=search_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                },
                wait_for="css:div#search",
                delay_before_return_html=3.0
            )
            
            print(f"专业搜索类型: {search_type}")
            print(f"查询: {query}")
            print(f"状态: {result.status_code}")
            print(f"页面标题: {result.metadata.get('title', 'N/A')}")
            
            # 如果是图片搜索，尝试提取图片信息
            if search_type == "images" and result.media.get('images'):
                print(f"找到 {len(result.media['images'])} 张图片")
                for i, img in enumerate(result.media['images'][:5]):
                    print(f"图片 {i+1}: {img.get('src', 'N/A')}")
            
        except Exception as e:
            print(f"专业搜索失败: {e}")

# 主函数示例
async def main():
    """主函数演示各种Google搜索方法"""
    
    # 测试查询
    test_queries = [
        "Python web scraping tutorial",
        "机器学习算法",
        "crawl4ai github"
    ]
    
    print("=== Google搜索示例 ===\n")
    
    # 基础搜索
    print("1. 基础搜索:")
    await basic_google_search(test_queries[0])
    
    print("\n" + "="*50 + "\n")
    
    # 解析搜索结果
    print("2. 解析搜索结果:")
    await parse_google_results(test_queries[1])
    
    print("\n" + "="*50 + "\n")
    
    # 专业搜索（新闻）
    print("3. 新闻搜索:")
    await specialized_google_search(test_queries[2], "news")
    
    print("\n" + "="*50 + "\n")
    
    # 批量搜索（使用较短的查询列表）
    print("4. 批量搜索:")
    batch_results = await batch_google_search(test_queries[:2], delay=3)
    
    print("批量搜索结果:")
    for result in batch_results:
        print(f"查询: {result['query']} - 成功: {result.get('success', False)}")

# 运行示例
if __name__ == "__main__":
    print("注意：Google可能会检测和阻止自动化访问")
    print("建议使用合理的延迟和真实的User-Agent\n")
    
    # 运行主函数
    asyncio.run(main())