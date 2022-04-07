import aiomysql
from pymysql import converters


class AioDBUtil:
    def __init__(self):
        self.__pool = None

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
            self.__pool = await aiomysql.create_pool(minsize=1, maxsize=5, host='inno.codimd.com', port=3306,
                                                     user='root', password='qwer', db='lottery',
                                                     loop=loop, conv=conv)




