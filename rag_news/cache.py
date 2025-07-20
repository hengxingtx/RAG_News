import json
import time
import os
from pathlib import Path
from typing import Dict, Any, Optional, List

class Cache:
    """缓存基类"""
    
    def __init__(self, ttl: int = 1800):
        """
        初始化缓存
        
        Args:
            ttl: 缓存过期时间（秒），默认30分钟
        """
        self.ttl = ttl  # 缓存过期时间，单位：秒
        
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """获取缓存数据"""
        raise NotImplementedError
        
    def set(self, key: str, value: Dict[str, Any]) -> None:
        """设置缓存数据"""
        raise NotImplementedError


class MemoryCache(Cache):
    """内存缓存实现"""
    
    def __init__(self, ttl: int = 1800):
        super().__init__(ttl)
        self.cache: Dict[str, Dict[str, Any]] = {}
        
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """获取缓存数据，如果不存在或过期返回None"""
        if key not in self.cache:
            return None
            
        data = self.cache[key]
        # 检查缓存是否过期
        if time.time() - data['timestamp'] > self.ttl:
            del self.cache[key]
            return None
            
        return data['value']
        
    def set(self, key: str, value: Dict[str, Any]) -> None:
        """设置缓存数据"""
        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }


class FileCache(Cache):
    """文件缓存实现"""
    
    def __init__(self, cache_dir: str = 'cache', ttl: int = 1800):
        """
        初始化文件缓存
        
        Args:
            cache_dir: 缓存目录
            ttl: 缓存过期时间（秒）
        """
        super().__init__(ttl)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        
    def _get_cache_path(self, key: str) -> Path:
        """获取缓存文件路径"""
        return self.cache_dir / f"{key}.json"
        
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """从文件获取缓存数据"""
        cache_file = self._get_cache_path(key)
        
        if not cache_file.exists():
            return None
            
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 检查缓存是否过期
            if time.time() - data['timestamp'] > self.ttl:
                os.remove(cache_file)
                return None
                
            return data['value']
        except Exception as e:
            print(f"读取缓存失败: {e}")
            return None
            
    def set(self, key: str, value: Dict[str, Any]) -> None:
        """将数据缓存到文件"""
        cache_file = self._get_cache_path(key)
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'value': value,
                    'timestamp': time.time()
                }, f, ensure_ascii=False)
        except Exception as e:
            print(f"写入缓存失败: {e}")


# 默认使用内存缓存
memory_cache = MemoryCache()

# 文件缓存实例，默认缓存目录为 'cache'
file_cache = FileCache() 