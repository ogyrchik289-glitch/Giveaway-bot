from aiogram import Bot, Dispatcher
from handlers import handler_router
from dotenv import load_dotenv
import os
import asyncio
from aiogram.client.default import DefaultBotProperties
load_dotenv()
TOKEN = os.getenv("TOKEN")
async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dispatcher = Dispatcher()
    dispatcher.include_router(handler_router)
    await dispatcher.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
