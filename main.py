# from apiCalls import detect_labels
#
# with open("img6.jpeg", "rb") as image_file:
#     print(detect_labels(image_file.read()))


import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

import config
from apiCalls import detect_labels

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hello!')


@dp.message(F.photo)
async def photo_handler(message: Message):
    # photo_data = message.photo[-1]
    # await message.answer(f'{photo_data}')
    photo_data = message.photo[-1]

    # Get the file ID of the photo
    file_id = photo_data.file_id

    # Use the bot.get_file method to get information about the file
    file_info = await bot.get_file(file_id)

    # Download the file using file_path from file_info
    file_path = file_info.file_path
    file_bytes_io = await bot.download_file(file_path)
    file_bytes_io.seek(0)
    file_bytes = file_bytes_io.read()
    await message.answer(detect_labels(file_bytes))


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main():
    await dp.start_polling(bot)


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
asyncio.run(main())

# with open("img6.jpeg", "rb") as image_file:
#     print(image_file.read())
