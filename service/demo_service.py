import time

from util.aiodb_util import db


def my_job():
    print(time.strftime('%Y-%m-%d %A %H:%M:%S', time.localtime()))


async def simple_query(sql: str):
    r = await db.query_once(sql)
    print(f'{r}')
