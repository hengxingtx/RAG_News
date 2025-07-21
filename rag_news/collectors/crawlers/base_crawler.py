#! python3
# -*- encoding: utf-8 -*-
###############################################################
#          @Time    :   2025/06/01 15:02:58
#          @Author  :   heng
#          @Contact :   hengsblog@163.com
###############################################################
"""
@comment
"""
# Crawl4ai 简单使用示例

# 1. 安装crawl4ai
# pip install crawl4ai
# 或者如果需要完整功能：pip install crawl4ai[all]

import json
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai import JsonCssExtractionStrategy

# 基础示例1：简单爬取网页内容
async def basic_crawl():
    """基础爬取示例"""
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url="https://easyai.tech/ai-definition/machine-learning/")
        
        print("页面标题:", result.metadata.get('title', 'N/A'))
        print("页面URL:", result.url)
        print("状态码:", result.status_code)
        print("内容长度:", len(result.markdown))
        print("文章内容:")
        print(result.markdown)

# 基础示例2：提取特定内容
async def extract_content():
    """使用CSS选择器提取特定内容"""
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://quotes.toscrape.com/",
            css_selector="div.quote"  # 提取引用内容
        )
        
        print("提取的内容:")
        print(result.extracted_content)

# 基础示例3：等待页面加载
async def wait_for_content():
    """等待动态内容加载"""
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://example.com",
            wait_for="css:div.content",  # 等待特定元素出现
            delay_before_return_html=2.0  # 额外等待2秒
        )
        
        print("动态内容:", result.markdown)

# 基础示例4：处理JavaScript渲染的页面
async def handle_js_content():
    """处理需要JavaScript渲染的页面"""
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://httpbin.org/delay/2",
            js_code="window.scrollTo(0, document.body.scrollHeight);",  # 执行JS代码
            wait_for="networkidle"  # 等待网络空闲
        )
        
        print("JS渲染后的内容:", result.markdown)

# 基础示例5：批量爬取多个URL
async def batch_crawl():
    """批量爬取多个页面"""
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/user-agent",
        "https://httpbin.org/headers"
    ]
    
    async with AsyncWebCrawler() as crawler:
        for url in urls:
            result = await crawler.arun(url=url)
            print(f"\n=== {url} ===")
            print(f"状态: {result.status_code}")
            print(f"内容长度: {len(result.markdown)}")

# 基础示例6：使用自定义请求头
async def custom_headers():
    """使用自定义请求头"""
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://httpbin.org/headers",
            headers={
                "User-Agent": "Mozilla/5.0 (Custom Bot)",
                "Accept": "text/html,application/xhtml+xml"
            }
        )
        
        print("响应内容:", result.markdown)

# 基础示例7：提取链接
async def extract_links():
    """提取页面中的所有链接"""
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://quotes.toscrape.com/")
        
        print("页面中的链接:")
        for link in result.links['internal'][:10]:  # 显示前10个内部链接
            print(f"文本: {link['text']}")
            print(f"URL: {link['href']}")
            print("---")

# 基础示例8：保存媒体文件
async def extract_media():
    """提取页面中的图片和媒体"""
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://quotes.toscrape.com/")
        
        print("页面中的图片:")
        for img in result.media['images'][:5]:  # 显示前5张图片
            print(f"图片URL: {img['src']}")
            print(f"Alt文本: {img.get('alt', 'N/A')}")
            print("---")

# 基础示例9：错误处理
async def error_handling():
    """错误处理示例"""
    async with AsyncWebCrawler() as crawler:
        try:
            result = await crawler.arun(url="https://nonexistent-site-12345.com")
            print("爬取成功:", result.url)
        except Exception as e:
            print(f"爬取失败: {e}")

# 基础示例10：完整的爬取流程
async def complete_example():
    """完整的爬取示例"""
    config = {
        "headless": True,  # 无头模式
        "verbose": True    # 详细日志
    }
    
    async with AsyncWebCrawler(**config) as crawler:
        # 爬取页面
        result = await crawler.arun(
            url="https://quotes.toscrape.com/",
            css_selector="div.quote",
            wait_for="css:div.quote",
            delay_before_return_html=1.0
        )
        
        # 输出结果
        data = {
            "url": result.url,
            "title": result.metadata.get('title'),
            "status": result.status_code,
            "content_length": len(result.markdown),
            "links_count": len(result.links['internal']),
            "images_count": len(result.media['images']),
            "extracted_content": result.extracted_content[:200] + "..." if result.extracted_content else None
        }
        
        print("爬取结果:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

# 运行示例
if __name__ == "__main__":
    print("=== Crawl4ai 基础示例 ===\n")
    
    # 运行基础爬取
    print("1. 基础爬取示例:")
    asyncio.run(basic_crawl())
    
    print("\n" + "="*50 + "\n")
    
    # # 运行完整示例
    # print("2. 完整爬取示例:")
    # asyncio.run(complete_example())

    # print("3. 提取特定内容:")
    # asyncio.run(extract_content())

    # print("\n" + "="*50 + "\n")

    # print("4. 等待页面加载:")
    # asyncio.run(wait_for_content())

    # print("\n" + "="*50 + "\n")

    # print("5. 处理JavaScript渲染的页面:")
    # asyncio.run(handle_js_content())

    # print("\n" + "="*50 + "\n")

    # print("6. 批量爬取多个URL:")
    # asyncio.run(batch_crawl())

    # print("\n" + "="*50 + "\n")