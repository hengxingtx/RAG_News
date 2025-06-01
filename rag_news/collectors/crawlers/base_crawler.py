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

class BaseCrawler(ABC):
    """基础爬虫抽象类"""

    @abstractmethod
    async def crawl(self, url: str, **kwargs):
        """爬取数据的抽象方法

        Args:
            url: 要爬取的URL
            **kwargs: 其他参数

        Returns:
            爬取的内容
        """
        pass 