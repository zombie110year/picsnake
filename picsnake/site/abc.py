from abc import ABCMeta, abstractmethod
from typing import Tuple


class ImageBedSessionABC(metaclass=ABCMeta):
    """对一个图床，至少需要实现上传与删除功能

    - upload
    - delete
    """
    @abstractmethod
    async def upload(self, filepath: str) -> Tuple[str, str]:
        "上传，并返回（访问链接，删除链接）"
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> bool:
        "删除 key 所指定的文件，返回是否成功删除"
        raise NotImplementedError
