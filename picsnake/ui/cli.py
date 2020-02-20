import asyncio
from argparse import ArgumentParser
from typing import *
import json
from .. import __app_name__
from ..site import INTERGRATED_BEDS
from ..upload import ImageUploader
from ..util import const_expr, split_large_list

__all__ = ("cli_main", "cli_args")


@const_expr
def parser():
    p = ArgumentParser(prog=__app_name__)

    subcmd = p.add_subparsers(title="子命令")

    upload = subcmd.add_parser("upload", aliases=["u", "up"])
    upload.add_argument("filepath", help="指定要上传的文件（可多个）", nargs="+")

    upload.add_argument("--dry-run",
                        help="如果指定此标志，则不会真实操作，只会演示效果",
                        action="store_true")
    upload.add_argument("--bed",
                        help="指定图床",
                        choices=INTERGRATED_BEDS.keys(),
                        default="sm.ms")
    upload.add_argument(
        "--bedargs",
        help=("针对图床的参数，输入 JSON"),
        metavar="{'username': 'example', 'password': 'example'}")

    # 定义子命令执行器
    upload.set_defaults(fn=upload_async)

    # todo
    search = subcmd.add_parser("search", aliases=["s"])
    search.add_argument("expr", help="搜索条件表达式，语法与 delete 所用的相同，文档见 <todo>")
    # 定义子命令执行器
    search.set_defaults(fn=search_async)

    # todo
    delete = subcmd.add_parser("delete", aliases=["d"])
    delete.add_argument("expr",
                        help="表示要删除对象的条件表达式, 语法与 search 所用的相同，文档见 <todo>")
    delete.add_argument("--dry-run",
                        help="如果指定此标志，则不会真实操作，只会演示效果",
                        action="store_true")
    # 定义子命令执行器
    delete.set_defaults(fn=delete_async)
    return p


@const_expr
def cli_args():
    return parser().parse_args()


async def main_async():
    args = cli_args()
    return await args.fn(args)


def cli_main():
    asyncio.run(main_async())


async def upload_async(args):
    """开始上传任务，args 提供参数

    - filepath: List[str]
    - dry_run: bool = False
    - bed: str = "sm.ms"
    - bedargs: List[str] = []
    """
    filepath: List[str] = args.filepath
    dry_run: bool = args.dry_run
    bed: str = args.bed
    bedargs: dict = json.loads(args.bedargs)

    if bedargs is None:
        iu = ImageUploader(bed)
    else:
        iu = ImageUploader(bed,
                           username=bedargs.get("username", None),
                           password=bedargs.get("password", None))

    aws = [iu.upload(fp) for fp in filepath]
    if len(aws) < 10:
        task = asyncio.gather(*aws)
        await task
    else:
        all_task = []
        for small_aws in split_large_list(aws):
            task = asyncio.gather(*small_aws)
            all_task.append(task)
        await asyncio.gather(*all_task)


async def search_async(args):
    raise NotImplementedError


async def delete_async(args):
    raise NotImplementedError
