from util import rdbms
from sql import lottery_sql


async def insert_mega645(round_id: str, date: str, draw_result: str, source: int) -> int:
    return await rdbms.db.insert(lottery_sql.INSERT_MEGA645, [round_id, draw_result, date, source])
