import asyncio
import time
import aiohttp
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup
from service import lottery_service


latest_round_info = {'round_id': None, 'ts': int(time.time())}
MEGA645_URL = "https://vietlott.vn/en/trung-thuong/ket-qua-trung-thuong/645.html"


def my_job():
    print(time.strftime('%Y-%m-%d %A %H:%M:%S', time.localtime()))


def my_demo2():
    scheduler = BlockingScheduler()
    # scheduler.add_job(lambda: asyncio.run(my_demo()), 'interval', seconds=300)
    scheduler.add_job(lambda: asyncio.run(aio_http_demo()), 'cron', day_of_week='wed,fri,sun', hour=18, minute='1-30')
    scheduler.start()


async def aio_http_demo():
    trigger_ts = time.strftime('%Y-%m-%d %A %H:%M:%S', time.localtime())
    if latest_round_info['round_id'] is not None and (int(time.time()) - latest_round_info['ts'] < 1800):
        print(f'{trigger_ts} skip')
        return
    print(trigger_ts)

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
            update_row = await lottery_service.insert_mega645(mega645_round, mega645_date, draw_result, 1)
            if update_row > 0:
                latest_round_info['round_id'] = mega645_round
                latest_round_info['ts'] = int(time.time())
            print(f'update row = {update_row}')


if __name__ == '__main__':
    print('start')
    my_demo2()
    print('end')

