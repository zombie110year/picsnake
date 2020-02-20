"""上传图片
"""
import asyncio
from datetime import datetime
from hashlib import sha256

from .model import UploadedPicture
from .site import INTERGRATED_BEDS
from .site.abc import ImageBedSessionABC
from .util import ReadableImageFile

__all__ = ("ImageUploader", )


class ImageUploader:
    """图像上传器，初始化时指定图床名称

    使用 upload(imgpath) 方法上传图片

    >>> iu = ImageUploader() # 默认采用 sm.ms 图床
    >>> imgpath = "./example.png"
    >>> await = iu.upload(imgpath)
    """
    bed: ImageBedSessionABC

    def __init__(self,
                 bed: str = "sm.ms",
                 username: str = None,
                 password: str = None):
        self.bedname = bed
        if bed in INTERGRATED_BEDS.keys():
            self.bed = INTERGRATED_BEDS[bed]() if all([
                x is None for x in (username, password)
            ]) else INTERGRATED_BEDS[bed](username=username, password=password)
        else:
            raise NotImplementedError("暂不支持自定义图床，目前支持的图床有 {}".format(
                [name for name in INTERGRATED_BEDS.keys()]))

    async def upload(self, imgpath: str):
        fileobj = ReadableImageFile(imgpath)
        task_upload = asyncio.create_task(self.bed.upload(fileobj))
        content = await fileobj.read()
        hex256: str = sha256(content).hexdigest()
        access, delete = await task_upload

        sqlitem = UploadedPicture(
            hash="sha256:{}".format(hex256),
            bed=self.bedname,
            access=access,
            delete=delete,
            uptime=datetime.now(),
        )
