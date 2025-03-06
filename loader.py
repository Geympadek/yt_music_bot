from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
import database

from config import TG_TOKEN

bot = Bot(
    token=TG_TOKEN,
    default=DefaultBotProperties(
        parse_mode="Markdown"
    )
)
database = database.FileDatabase("database.db")
dp = Dispatcher()

async def launch():
    await dp.start_polling(bot)