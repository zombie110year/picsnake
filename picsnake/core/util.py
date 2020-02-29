"""Core 包通用工具
"""

import asyncio
from hashlib import sha256
from pathlib import PurePath
from typing import *

from aiofiles import open as open_async

from .abc import ReadableImageFileABC

__all__ = ("ReadabelImageFile", "const_expr")


class ReadableImageFile(ReadableImageFileABC):
    def __init__(self, filepath: str):
        self.path: str = filepath
        self.filename: str = PurePath(filepath).name

        self.__content: Union[bytes, None] = None
        self.__lock = asyncio.Lock()
        self.__sha256: Union[str, None] = None

    async def read(self):
        if self.__content is None:
            async with self.__lock:
                async with open_async(self.path, "rb") as instream:
                    self.__content = await instream.read()
        return self.__content

    async def sha256(self) -> str:
        if self.__sha256 is None:
            content = await self.read()
            self.__sha256 = sha256(content).hexdigest()
        return self.__sha256


def const_expr(func):
    """将接下来的函数设定为伪常量表达式

    1. 整个程序的生命周期内只会执行一次
    2. 保存第一次运行的返回值

    >>> @const_expr
    >>> def one():
    >>>     return 1
    """
    result = None

    def inner():
        nonlocal result

        if result is None:
            result = func()

        return result

    return inner


T = TypeVar("T")


def split_large_list(seq: List[T], limit: int = 10) -> Generator[List[T], None, None]:
    """（生成器）将过长的列表拆分成最大 limit 长度的小段
    """
    length = len(seq)
    ll, rl = 0, limit
    while ll < length:
        yield seq[ll:rl]
        ll += limit
        rl += limit
