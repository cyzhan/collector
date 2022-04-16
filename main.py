import asyncio

from apscheduler.schedulers.blocking import BlockingScheduler
from service import demo_service, scrape_service
from util.aiodb_util import db


def scheduler_task():
    scheduler = BlockingScheduler()
    # scheduler.add_job(lambda: asyncio.run(my_demo()), 'interval', seconds=300)
    scheduler.add_job(lambda: asyncio.run(scrape_service.aio_http_demo()), 'cron', day_of_week='wed,fri,sun', hour=18,
                      minute='1-30')
    scheduler.start()


async def init_aiodb(evloop):
    await db.create_pool(evloop)


if __name__ == '__main__':
    print('start')
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_aiodb(evloop=loop))

    print('aiodb test-----------------------------------------------------')
    loop.run_until_complete(demo_service.simple_query('select * from rabbit.user'))

    # print('scrape test-----------------------------------------------------')
    # loop.run_until_complete(scrape_service.aio_http_demo())
    #
    # loop.run_until_complete(db.close_pool())
    # loop.close()
    # print('end')


