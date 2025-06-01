from abc import ABC, abstractmethod
from typing import List, Any


class BaseEmbedder(ABC):
    """向量化模型抽象类"""

    @abstractmethod
    async def embed(self, texts: List[str], **kwargs) -> List[Any]:
        """向量化文本的抽象方法

        Args:
            texts: 要向量化的文本列表
            **kwargs: 其他参数

        Returns:
            向量化后的结果列表
        """
        pass 