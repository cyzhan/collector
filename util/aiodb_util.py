import os
import aiomysql
from pymysql import converters


class AioDBUtil:
    def __init__(self):
        self.__pool = None

    def get_pool(self):
        return self.__pool

    async def close_pool(self):
        self.__pool.close()
        await self.__pool.wait_closed()

    async def execute(self, sql: str):
        async with self.__pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                count = await cur.execute(sql)
                print(f'update row = {count}')
                r = await cur.fetchall()
                print(f'r = {r}')

    async def create_pool(self, loop):
        if self.__pool is None:
            conv = converters.conversions.copy()
            conv[10] = str  # convert dates to strings
            conv[7] = str  # convert datetime to strings
            self.__pool = await aiomysql.create_pool(minsize=1, maxsize=5, host=os.getenv("DB_HOST"), port=3306,
                                                     user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"),
                                                     db='lottery', loop=loop, conv=conv)
            print('mysql connection pool created')
        print('connection pool already exist')


db = AioDBUtil()


def cursor_inject(func):
    async def wrapper(*args, **kwargs):
        async with db.get_pool().acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                try:
                    result = await func(*args, **kwargs, cursor=cur)
                    await conn.commit()
                    return result
                except Exception as e:
                    await conn.rollback()
                    raise e
    return wrapper

