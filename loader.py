from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import config
from utils.db_api import Database
from utils.misc import GraphBuilder

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
scheduler = AsyncIOScheduler()
dp = Dispatcher(bot, storage=storage)
db = Database("data/stats.db", logging=False)
gb = GraphBuilder(db)
