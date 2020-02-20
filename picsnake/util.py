import asyncio
from pathlib import PurePath
from typing import Union

from aiofiles import open as open_async

from .abc import ReadableImageFileABC

__all__ = ("ReadabelImageFile", )


class ReadableImageFile(ReadableImageFileABC):
    def __init__(self, filepath: str):
        self.path: str = filepath
        self.filename: str = PurePath(filepath).name
        self.content: Union[bytes, None] = None
        self.lock = asyncio.Lock()

    async def read(self):
        if self.content is None:
            with self.lock:
                with open_async(self.path, "rb") as instream:
                    self.content = await instream.read()
        return self.content
