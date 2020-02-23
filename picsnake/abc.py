from abc import ABCMeta
from abc import abstractmethod

__all__ = ("ReadableImageFileABC", )


class ReadableImageFileABC(metaclass=ABCMeta):
    filename: str

    @abstractmethod
    async def read(self) -> bytes:
        raise NotImplementedError
