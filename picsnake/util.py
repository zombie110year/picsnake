from .abc import ReadableImageFileABC
from pathlib import PurePath
from aiofiles import open as open_async

__all__ = ("ReadabelImageFile", )


class ReadableImageFile(ReadableImageFileABC):
    def __init__(self, filepath: str):
        self.path = filepath
        self.filename = PurePath(filepath).name

    async def read(self):
        with open_async(self.path, "rb") as instream:
            return await instream.read()
