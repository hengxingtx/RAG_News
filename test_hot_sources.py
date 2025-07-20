#!/usr/bin/env python
"""
热榜源测试脚本，用于测试所有热榜源是否能正常工作
"""
import sys
import asyncio
import time
from typing import Dict, List, Any

def main():
    """主函数，测试热榜源"""
    # 将当前目录添加到模块搜索路径，以便导入rag_news模块
    sys.path.insert(0, ".")
    
    # 导入热榜源
    from rag_news.sources import source_manager
    
    async def test_source(source_id: str):
        """测试单个热榜源"""
        source = source_manager.get_source(source_id)
        print(f"测试 {source_id} ({source.name})...")
        start_time = time.time()
        try:
            items = await source_manager.fetch_from_source(source_id)
            end_time = time.time()
            print(f"✅ {source_id} ({source.name}) 成功获取 {len(items)} 条数据，耗时 {end_time - start_time:.2f}秒")
            return True
        except Exception as e:
            end_time = time.time()
            print(f"❌ {source_id} ({source.name}) 失败: {e}, 耗时 {end_time - start_time:.2f}秒")
            return False
    
    async def run_tests():
        """运行所有测试"""
        print("开始测试所有热榜源...")
        print(f"共有 {len(source_manager.get_all_sources())} 个热榜源")
        
        results: Dict[str, bool] = {}
        
        # 依次测试每个源
        for source_id in source_manager.get_all_sources():
            results[source_id] = await test_source(source_id)
        
        # 打印测试结果统计
        success_count = sum(1 for result in results.values() if result)
        fail_count = len(results) - success_count
        
        print("\n测试结果统计:")
        print(f"成功: {success_count} / {len(results)}")
        print(f"失败: {fail_count} / {len(results)}")
        
        if fail_count > 0:
            print("\n以下源测试失败:")
            for source_id, result in results.items():
                if not result:
                    source = source_manager.get_source(source_id)
                    print(f"- {source_id} ({source.name})")
    
    # 运行测试
    asyncio.run(run_tests())

if __name__ == "__main__":
    main() 