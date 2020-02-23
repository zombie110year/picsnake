"""sm.ms 图床 API
"""
import asyncio
import json
from datetime import datetime
from mimetypes import guess_type
from pathlib import PurePath
from typing import *

import aiofiles
from aiohttp import ClientSession
from aiohttp import CookieJar
from aiohttp import FormData

from ..abc import ReadableImageFileABC
from .abc import ImageBedSessionABC
from .exception import ImageHostingError

__all__ = ("ISession", )


class ISession(ImageBedSessionABC):
    """https://doc.sm.ms/
    """
    URL_PREFIX = "https://sm.ms/api/v2/"
    AUTH_KEYNAME = "Authorization"

    def __init__(self, username=None, password=None):
        self._headers = dict()
        self._cookies = CookieJar()
        self._token = None

        if None not in (username, password):
            # 登录账户
            asyncio.run(self._login(username, password))

    async def _login(self, username, password):
        """获取 token，添加到 Header 中

        Authorization: <token>
        """
        async with ClientSession(headers=self._headers, cookies=self._cookies) as cs:
            async with cs.post(self._api("/token"), json={"username": username, "password": password}) as response:
                if response.status == 200:
                    json: dict = await response.json()
                    self.token = json["data"]["token"]
                    self.headers[self.AUTH_KEYNAME] = self.token
                    print("[{now}] login: sm.ms - {username}".format(now=datetime.now(), username=username))
            async with cs.post(self._api("/profile"), json={self.AUTH_KEYNAME: self.token}) as response:
                if response.status == 200:
                    json: dict = await response.json()
                    print("Login    : {}".format(json["data"]["username"]))
                    dur: int = json["data"]["disk_usage_raw"]
                    du: str = json["data"]["disk_usage"]
                    dlr: int = json["data"]["disk_limit_raw"]
                    dl: str = json["data"]["disk_limit"]
                    print("Disk rest: {:.3f}%, {} / {}".format(dur / dlr, du, dl))

    async def upload(self, fileobj: ReadableImageFileABC) -> Tuple[Union[str, None], Union[str, None]]:
        """返回（访问链接，删除链接）

        sm.ms 图床的上传功能需要向 ``/upload`` POST 一个含字段 ``smfile`` 的 FormData.
        FormData 中可以分别传入参数::

            field="smfile", value=<文件内容>, filename=<文件名>, content_type=<mime type>

        来上传文件。

        .. note::

            sm.ms 返回的响应是满足 JSON 格式的字节，不能直接用 Response.json 解码。
        """

        async with ClientSession(headers=self._headers, cookies=self._cookies) as cs:
            form = FormData()
            filename = fileobj.filename
            mimetype = guess_type(filename)[0]  # 返回的是 (type, encoding)
            form.add_field(
                "smfile",
                value=(await fileobj.read()),
                content_type=mimetype,
                filename=filename,
            )
            async with cs.post(self._api("/upload"), data=form) as response:
                if response.status == 200:
                    rawdata = await response.read()
                    return_data = json.loads(rawdata)
        if not return_data["success"]:
            if return_data["code"] == "image_repeated":
                return return_data["images"], None
            else:
                raise ImageHostingError(return_data)
        return return_data["data"]["url"], return_data["data"]["delete"]

    def _api(self, name: str) -> str:
        return "{}{}".format(self.URL_PREFIX, name)

    async def delete(self, key: str) -> bool:
        return await super().delete(key)
