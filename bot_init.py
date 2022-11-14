import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()

storage = MemoryStorage()

# bot = Bot(token="5371438553:AAHE4kA1YNX_f6VhRh4bAQ3fKMqwtIBBgAk", parse_mode=types.ParseMode.HTML)
bot = Bot(token=os.getenv("TOKEN"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
