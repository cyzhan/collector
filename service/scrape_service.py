import time
import aiohttp
from bs4 import BeautifulSoup
from sql import lottery_sql
from util.aiodb_util import db

latest_round_info = {'round_id': None, 'ts': int(time.time())}
MEGA645_URL = "https://vietlott.vn/en/trung-thuong/ket-qua-trung-thuong/645.html"


async def aio_http_demo():
    trigger_ts = time.strftime('%Y-%m-%d %A %H:%M:%S', time.localtime())
    if latest_round_info['round_id'] is not None and (int(time.time()) - latest_round_info['ts'] < 1800):
        print(f'{trigger_ts} skip')
        return
    print(trigger_ts)
    html = None

    async with aiohttp.ClientSession() as session:
        async with session.get(MEGA645_URL) as response:
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")
    items = soup.find("h5").select('b')
    tmp_ary = []
    for item in items:
        tmp_ary.append(item.getText())

    mega645_round = tmp_ary[0]

    print(f'mega645_date = {tmp_ary[1]}')

    tmp_ary2 = tmp_ary[1].split('/')
    mega645_date = "{}-{}-{}".format(tmp_ary2[2], tmp_ary2[1], tmp_ary2[0])
    numbers = soup.find_all('span', class_='bong_tron')
    ary = []
    for number in numbers:
        ary.append(number.getText())
        print(number.getText())
    draw_result = ','.join(ary)
    update_row = await db.insert_or_update(sql=lottery_sql.INSERT_MEGA645,
                                           params=[mega645_round, draw_result, mega645_date, 1])
    if update_row > 0:
        latest_round_info['round_id'] = mega645_round
        latest_round_info['ts'] = int(time.time())
    print(f'update row = {update_row}')
