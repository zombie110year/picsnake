__all__ = ("PicSnakeException", "ImageHostingError", "DataBaseError", "BlobError")


class PicSnakeException(Exception):
    "PicSnake 内部发生的错误"
    pass


class ImageHostingError(PicSnakeException):
    "与图床交互时发生的错误"
    pass


class DataBaseError(PicSnakeException):
    "与数据库交互时发生的错误"
    pass


class BlobError(PicSnakeException):
    "与图像文件交互时发生的错误"
    pass
