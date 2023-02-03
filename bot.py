import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import authentication, main_menu, workout_menu, record_people, actual_peoples, upload_files
from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from database import place, users, workout_time
import os

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    redis = Redis(host = "redis")

    bot = Bot(token=str(os.environ.get("BOT_TOKEN")))
    dp = Dispatcher(storage = RedisStorage(redis=redis))

    routers = [
        authentication.router,
        main_menu.router,
        workout_menu.router,
        record_people.router,
        actual_peoples.router,
        upload_files.router,
    ]

    for router in routers:
        dp.include_router(router=router)

    db = [place.Places(), users.Users(), workout_time.WorkoutTime()]
    
    for x in db: 
        await x.create_table()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
