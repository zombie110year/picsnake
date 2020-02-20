from hashlib import sha256

import databases
import ormantic as orm
import sqlalchemy

__all__ = ("UploadedPicture", )

SHA256_LENGTH = 64
# TODO 读取配置
DATABASE = databases.Database("sqlite:///db.sqlite")
METADATA = sqlalchemy.MetaData()

Sha256Hex: orm.String = orm.String(primary_key=True,
                                   index=True,
                                   unique=True,
                                   max_length=SHA256_LENGTH)
BedName: orm.String = orm.String(max_length=127)
Url: orm.String = orm.String(max_length=0xffffffff)
UpTime: orm.DateTime = orm.DateTime()


class UploadedPicture(orm.Model):
    """被上传的图片，记录字段

    - hash（HEX）：str
    - bed（图床的别名、用来对应解析规则）：str
    - url（链接地址）：str
    - uptime（上传时间）：datetime
    """
    hash: Sha256Hex
    bed: BedName
    url: Url
    uptime: UpTime

    class Mapping:
        table_name = "upload"
        metadata = METADATA
        database = DATABASE


# 创建
engine = sqlalchemy.create_engine(str(DATABASE.url))
METADATA.create_all(engine)
