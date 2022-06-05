from config import settings
import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher


# Configure logging
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

# Initialize bot_client and dispatcher
bot = Bot(token=settings.TOKEN, parse_mode="HTML")   # proxy=settings.PROXY_URL,
dp = Dispatcher(bot, storage=storage)

