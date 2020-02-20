"""上传图片
"""
import asyncio
from datetime import datetime
from hashlib import sha256
from pathlib import Path

import ormantic as orm

from .model import UploadedPicture
from .settings import Settings
from .site import INTERGRATED_BEDS
from .site.abc import ImageBedSessionABC
from .util import ReadableImageFile

__all__ = ("ImageUploader", )


class ImageUploader:
    """图像上传器，初始化时指定图床名称

    使用 upload(imgpath) 方法上传图片

    >>> iu = ImageUploader() # 默认采用 sm.ms 图床
    >>> imgpath = "./example.png"
    >>> await iu.upload(imgpath)
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
        key = "sha256:{}".format(hex256)
        try:
            exists: UploadedPicture = await UploadedPicture.objects.get(
                hash=key)
            print("重复的 {hash!r} @ {filename!r}, 最初上传时间 {uptime}.".format(
                **exists.dict()))
        except orm.NoMatch:
            success: UploadedPicture = await UploadedPicture.objects.create(
                hash=key,
                bed=self.bedname,
                filename=fileobj.filename,
                accesser=access,
                deleter=delete,
                uptime=datetime.now(),
            )
            Path(Path(Settings.BLOB_DIR) / hex256).write_bytes(await
                                                               fileobj.read())
            print("成功创建条目 ({bed!r}) {hash!r} @ {filename!r} {uptime}.".format(
                **success.dict()))
