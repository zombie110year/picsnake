"""数据模型
"""

from hashlib import sha256
import os
import databases
import orm
import sqlalchemy

if os.getenv("PICSNAKE_ENV") == "TEST":
    from .settings import TestingSettings as Settings
else:
    from .settings import Settings

__all__ = ("UploadedPicture", "Picture", "DATABASE", "METADATA")

SHA256_LENGTH = 64

DATABASE = databases.Database("sqlite:///{}".format(Settings.DATABASE))
METADATA = sqlalchemy.MetaData()

Sha256Hex: orm.String = orm.String(max_length=SHA256_LENGTH, primary_key=True)
BedName: orm.String = orm.String(max_length=127, primary_key=True)
ShortName: orm.String = orm.String(max_length=127)
Url: orm.String = orm.String(max_length=0xffffffff)
DateTime: orm.DateTime = orm.DateTime()
CommentText: orm.String = orm.String(max_length=1023)


class UploadedPicture(orm.Model):
    """被上传的图片，记录字段

    - sha256（HEX）：str
    - bed（图床的别名、用来对应解析规则）：str
    - accesser（如何访问图片）：str
    - deleter（如何删除图片）：str
    - uptime（上传时间）：datetime

    以一个对象对应一个图床上的一张图片。
    """
    __tablename__ = "upload"
    __metadata__ = METADATA
    __database__ = DATABASE

    sha256: Sha256Hex
    bed: BedName
    accesser: Url
    deleter: Url
    uptime: DateTime


class Picture(orm.Model):
    """一张图片

    - sha256（HEX）：str
    - filename（文件名）：str
    - comment（注释）：str
    """
    __tablename__ = "picture"
    __metadata__ = METADATA
    __database__ = DATABASE

    sha256: Sha256Hex
    filename: ShortName
    comment: CommentText
