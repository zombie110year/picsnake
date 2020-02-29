"""PicSnake Core 包需要用到的抽象类
"""

from abc import ABCMeta
from abc import abstractmethod

__all__ = ("ReadableImageFileABC", )


class ReadableImageFileABC(metaclass=ABCMeta):
    """一个可读的文件对象，包含文件名，
    可通过 read 方法读取其内容，
    可通过 sha256 方法获取其 HASH 值的十六进制表示
    """
    filename: str

    @abstractmethod
    async def read(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    async def sha256(self) -> str:
        raise NotImplementedError
