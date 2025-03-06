from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties

from config import TG_TOKEN

bot = Bot(
    token=TG_TOKEN,
    default=DefaultBotProperties(
        parse_mode="Markdown"
    )
)
dp = Dispatcher()

async def launch():
    await dp.start_polling(bot)