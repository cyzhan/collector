from util.aiodb_util import cursor_inject


@cursor_inject
async def simple_query(sql: str, cursor):
    count = await cursor.execute(sql)
    print(f'update row = {count}')
    r = await cursor.fetchall()
    print(f'r = {r}')