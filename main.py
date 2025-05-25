import asyncio

from aiogram import  Bot, Dispatcher
from config import TOKEN

from app.handlers import router
from app.database.models import asunc_main

from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot = Bot(token=TOKEN)
dp = Dispatcher()

import app.schedule_task

async def main():

    await asunc_main()
    dp.include_router(router)

    # создаем экземпляр класса AsyncIOScheduler
    scheduler = AsyncIOScheduler()
    # создаем задачи
    await set_scheduled_jobs(scheduler=scheduler,bot=bot)
    
    # стартуем работу
    scheduler.start()

    await dp.start_polling(bot)

async def set_scheduled_jobs(scheduler,bot):
    # Добавляем задачи на выполнение

    scheduler.add_job(app.schedule_task.key_free_count, 'cron', hour='9', minute='10',args=[bot])
    scheduler.add_job(app.schedule_task.check_user_tarif, 'cron', hour='12', minute='01', args=[bot])
    # scheduler.add_job(some_other_regular_task, "interval", seconds=100)

async def test():
    print('reqw')

if __name__ == '__main__':


    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Éxit')