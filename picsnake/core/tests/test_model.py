import tempfile
import unittest.mock as mock
from datetime import datetime
from pathlib import Path

import pytest
import sqlalchemy

from ..model import *


@pytest.fixture(scope="module")
def db_test():
    from ..settings import TestingSettings
    db_path = Path(TestingSettings.DATABASE)
    if db_path.exists():
        db_path.unlink()
    engine = sqlalchemy.create_engine(f"sqlite:///{db_path.as_posix()}")
    METADATA.create_all(engine)
    yield db_path


@pytest.mark.asyncio
async def test_add_picture(db_test):
    a = Picture(sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e3649b934ca495991b7852b855", filename="heihei.png", comment="无注释")
    await a.insert()
    pictures = await Picture.objects.filter(sha256__icontains="e3b0c4").all()
    assert a in pictures

@pytest.mark.asyncio
async def test_add_upload_picture(db_test):
    a = UploadedPicture(sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                        bed="sm.ms",
                        accesser="https://sm.ms/2020/02/29/e3b0c44298fc1c149af",
                        deleter="https://sm.ms/delete/e3b0c44298fc1c149af",
                        uptime=datetime(2020, 2, 29, 12, 0, 0))
    await a.insert()
    pictures = await UploadedPicture.objects.all()
    assert a in pictures
