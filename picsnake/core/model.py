"""与数据库交互的逻辑
"""

from hashlib import sha256

import databases
import ormantic as orm
import sqlalchemy

from .settings import Settings

__all__ = ("UploadedPicture", "Picture")

SHA256_LENGTH = 64

DATABASE = databases.Database("sqlite:///{}".format(Settings.DATABASE))
METADATA = sqlalchemy.MetaData()

Sha256Hex: orm.String = orm.String(primary_key=True, index=True, max_length=SHA256_LENGTH)
BedName: orm.String = orm.String(primary_key=True, max_length=127)
ShortName: orm.String = orm.String(max_length=127)
Url: orm.String = orm.String(max_length=0xffffffff)
DateTime: orm.DateTime = orm.DateTime()
CommentText: orm.String = orm.String(max_length=1023)


class UploadedPicture(orm.Model):
    """被上传的图片，记录字段

    - hash（HEX）：str
    - bed（图床的别名、用来对应解析规则）：str
    - accesser（如何访问图片）：str
    - deleter（如何删除图片）：str
    - uptime（上传时间）：datetime

    以一个对象对应一个图床上的一张图片。
    """
    hash: Sha256Hex
    bed: BedName
    accesser: Url
    deleter: Url
    uptime: DateTime

    class Mapping:
        table_name = "upload"
        metadata = METADATA
        database = DATABASE


class Picture(orm.Model):
    """一张图片

    - hash（HEX）：str
    - filename（文件名）：str
    - comment（注释）：str
    """
    hash: Sha256Hex
    filename: ShortName
    comment: CommentText

    class Mapping:
        table_name = "picture"
        metadata = METADATA
        database = DATABASE


# 创建
engine = sqlalchemy.create_engine(str(DATABASE.url))
METADATA.create_all(engine)
