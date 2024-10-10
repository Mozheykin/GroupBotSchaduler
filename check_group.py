import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from config import BOT_TOKEN


logging.basicConfig(level=logging.INFO)

if BOT_TOKEN is not None:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()


@dp.message(CommandStart())
async def send_welcome(message: types.Message) -> None:
    """Check id grop"""
    await message.reply(f"ID group: {message.chat.id}")
    if message.message_thread_id is not None:
        await message.reply(f"ID subgroup: {message.message_thread_id}")

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
