# RAG_News 热榜爬虫

这是一个用于获取各大网站热榜数据的Python爬虫项目。目前支持以下热榜源：

- 知乎热榜
- 微博热搜
- B站热搜
- B站热门视频

## 安装依赖

```bash
uv pip install httpx
```

## 使用方法

### 列出所有可用的热榜源

```bash
python -m rag_news.main -l
```

### 获取特定热榜源的数据

```bash
python -m rag_news.main -s zhihu
```

### 获取所有热榜源的数据

```bash
python -m rag_news.main
```

### 将结果保存到文件

```bash
python -m rag_news.main -o data/hotlist.json
```

## 项目结构

```
rag_news/
├── __init__.py      # 包初始化文件
├── main.py          # 主程序入口
└── sources/         # 热榜源实现
    ├── __init__.py  # 源模块初始化
    ├── base.py      # 源基类定义
    ├── utils.py     # 工具类
    ├── zhihu.py     # 知乎热榜
    ├── weibo.py     # 微博热搜
    └── bilibili.py  # B站热搜和热门视频
```

## 扩展新的热榜源

1. 在`sources/`目录下创建新的源文件，例如`toutiao.py`
2. 实现新的源类，继承自`HotListSource`或`Source`
3. 在`sources/__init__.py`中注册新源

示例：

```python
# sources/toutiao.py
from typing import Dict, List, Any, TypedDict
from .base import HotListSource
from .utils import NewsItem, my_fetch

class ToutiaoHotSearch(HotListSource):
    """今日头条热搜"""
    
    def __init__(self, interval: int = 300):
        url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
        super().__init__("今日头条热搜", url, interval)
        
    async def fetch_items(self) -> List[NewsItem]:
        # 实现爬取逻辑...
        pass

# sources/__init__.py 中注册
source_manager.register("toutiao", ToutiaoHotSearch())
``` 