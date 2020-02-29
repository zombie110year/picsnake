"""与数据库交互
"""
import sqlalchemy

from .model import *

# 创建
engine = sqlalchemy.create_engine(str(DATABASE.url))
METADATA.create_all(engine)
