from abc import ABC, abstractmethod
from typing import List


class TextSplitter(ABC):
    """文本分割器抽象类"""

    @abstractmethod
    def split(self, text: str, **kwargs) -> List[str]:
        """分割文本的抽象方法

        Args:
            text: 要分割的文本
            **kwargs: 其他参数

        Returns:
            分割后的文本片段列表
        """
        pass 