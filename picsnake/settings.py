from os import getenv
from pathlib import Path
from platform import system

from . import __app_name__

__all__ = ("Settings", )


def windows_appdata() -> str:
    """获取 Windows %APPDATA%/picsnake 路径

    如果出问题，就用与 Linux 类似的配置
    """
    prefix = getenv("APPDATA")
    if isinstance(prefix, str):
        return "{}/{}".format(prefix, __app_name__)
    else:
        return linux_config()


def linux_config() -> str:
    """获取 ~/.config/picsnake 路径
    """
    return str(Path.home() / __app_name__)


def unknown_system():
    """既不是 Windows 也不是 Linux"""
    raise RuntimeError("无法在此系统上运行，你的系统是 {}".format(repr(system())))


class Settings:
    """应用程序的“静态”设置，动态设置通过 yaml 读取
    """
    CONF_DIR: str = {
        "Windows": windows_appdata,
        "Linux": linux_config
    }.get(system(), unknown_system)()
    PLUGIN_DIR: str = "{}/plugins".format(CONF_DIR)
    BLOB_DIR: str = "{}/bolbs".format(CONF_DIR)

    DATABASE: str = "{}/db.sqlite".format(CONF_DIR)

    # ensure_path
    for directory in [CONF_DIR, PLUGIN_DIR, BLOB_DIR]:
        if not Path(directory).exists():
            Path(directory).mkdir(parents=True)
