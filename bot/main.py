import asyncio

from aiogram import Bot, Dispatcher


from config import settings
from handlers.user_private import user_router
from db.db import DBSession
from db.engine import async_session, create_db

ALLOWED_UPDATES = ['message, edited_message']

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()
dp.update.middleware(DBSession(session_pool=async_session))
dp.include_router(user_router)


async def main():
    await create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    asyncio.run(main())