"""与数据库交互
"""
import sqlalchemy

from .model import *

__all__ = ("DATABASE", "METADATA")

# 创建
engine = sqlalchemy.create_engine(str(DATABASE.url))
METADATA.create_all(engine)
