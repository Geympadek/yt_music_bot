import loader
from loader import dp, bot

from aiogram.exceptions import TelegramEntityTooLarge, TelegramBadRequest
from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from mutagen.mp4 import MP4, MP4Cover
from aiogram import F

import yt_api

import menu

import requests
import config

import io
import os
import utils

@dp.message(Command("start"))
async def on_start(msg: types.Message, state: FSMContext):
    await msg.answer(text="Добро пожаловать")

@dp.message()
async def on_message(msg: types.Message, state: FSMContext):
    text = msg.text

    if (utils.is_url(text)):
        await try_send_music(msg.from_user.id, text.strip(), state)
    else:
        await try_search(msg.from_user.id, text.strip(), state)

async def try_send_music(chat_id: int, url: str, state: FSMContext):
    progress_msg = await bot.send_message(chat_id, "*Загрузка аудио...*🕒")

    try: 
        audio_path = await yt_api.download(url)
    except None:
        await bot.send_message(chat_id, "*Во время загрузки аудио произошла ошибка.*")
        await progress_msg.delete()
        return
    
    await progress_msg.edit_text("*Отправка аудио...*🚀")
    await bot.send_chat_action(chat_id, "upload_voice")
    cover_path = os.path.join(config.TEMP_DIR, "cover.jpg")

    audio = MP4(audio_path)
    author = audio.tags['\xa9nam'][0]
    title = audio.tags['\xa9ART'][0]
    
    with open(cover_path, "wb") as cover_file:
        cover_file.write(audio.tags['covr'][0])

    try:
        await bot.send_audio(
            chat_id,
            audio=types.FSInputFile(audio_path),
            performer=author,
            title=title,
            thumbnail=types.FSInputFile(cover_path)
        )
    except TelegramEntityTooLarge:
        await bot.send_message(chat_id, "*Не удалось отправить аудио: размер файл превышает лимит Телеграма.*")
    await progress_msg.delete()

async def update_results(result_message: Message, results: list[dict[str,str]], min_size=0):
    kb = menu.get_search_menu(results, min_size=min_size)
    await result_message.edit_reply_markup(reply_markup=kb)

async def try_search(chat_id: int, query: str, state: FSMContext):
    response_msg = await bot.send_message(chat_id, f'*Результаты по запросу:*\n_{query}_')
    try:
        results = await yt_api.search(query, update_func=lambda results:update_results(response_msg, results, 10))
        try:
            await update_results(response_msg, results)
        except TelegramBadRequest:
            pass
    except Exception as e:
        await bot.send_message(chat_id, "*Во время поиска произошла ошибка.*")
        await response_msg.delete()

@dp.callback_query(F.data.startswith("video_chosen"))
async def on_query(query: CallbackQuery, state: FSMContext):
    url = query.data.split(':', 1)[1]
    await try_send_music(query.from_user.id, url, state)

async def main():
    os.makedirs(config.TEMP_DIR, exist_ok=True)
    
    await loader.launch()
    pass

import asyncio

if __name__ == "__main__":
    asyncio.run(main())