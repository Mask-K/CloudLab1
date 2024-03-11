
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, BufferedInputFile

import config
from apiCalls import detect_labels, localize_objects


bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hello!')


@dp.message(F.photo)
async def photo_handler(message: Message):

    photo_data = message.photo[-1]

    file_id = photo_data.file_id

    file_info = await bot.get_file(file_id)

    file_path = file_info.file_path
    file_bytes_io = await bot.download_file(file_path)
    file_bytes_io.seek(0)
    file_bytes = file_bytes_io.read()

    annotated_image_bytes_io = localize_objects(file_bytes)
    annotated_image_bytes = annotated_image_bytes_io.getvalue()
    annotated_image_file = BufferedInputFile(annotated_image_bytes, filename="annotated_image.png")
    await message.answer_photo(annotated_image_file)

    await message.answer(detect_labels(file_bytes))


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
asyncio.run(main())
