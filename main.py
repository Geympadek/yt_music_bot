import loader
from loader import dp, bot, database

from aiogram.exceptions import TelegramEntityTooLarge, TelegramBadRequest
from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from mutagen.mp4 import MP4, MP4Cover
from aiogram import F

import yt_api

import menu

import config

import os
import utils

import localizations
import asyncio

from time import time

async def sleep_limit(state: FSMContext):
    last_action = await state.get_value('last_action_time')
    if last_action is not None:
        diff = (last_action + config.RATE_LIMIT) - time()
        if diff > 0:
            await state.update_data(last_action_time=time() + diff)
            print(f"Sleeping for {diff}")
            await asyncio.sleep(diff)
            return
    await state.update_data(last_action_time=time())

async def ask_language(chat_id: int, state: FSMContext):
    kb = menu.get_language_menu()
    await sleep_limit(state)
    lang_msg = await bot.send_message(chat_id, text="Select language / Выберите язык", reply_markup=kb)
    await state.update_data(lang_msg_id=lang_msg.message_id)

@dp.message(Command("start"))
async def on_start(msg: types.Message, state: FSMContext):
    await ask_language(msg.from_user.id, state)
    await state.set_state("start")

@dp.message(Command("language"))
async def on_language_command(msg: types.Message, state: FSMContext):
    await ask_language(msg.from_user.id, state)

@dp.message()
async def on_message(msg: types.Message, state: FSMContext):
    text = msg.text

    if not utils.is_url(text):
        await try_search(msg.from_user.id, text.strip(), state)
    elif not utils.is_url_playlist(text):
        await try_send_music(msg.from_user.id, text.strip(), state)
    else:
        await try_playlist_download(msg.from_user.id, text.strip(), state)

def get_language(user_id: int):
    entry = database.read("users", {"user_id": user_id})[0]
    return entry['language']

def get_localization(user_id: int):
    return localizations.localizations[get_language(user_id)]

def get_alt_link(filepath: str):
    return config.ALT_DOWNLOAD_LINK + os.path.split(filepath)[1]

async def try_send_music(chat_id: int, url: str, state: FSMContext):
    local = get_localization(chat_id)

    await sleep_limit(state)
    progress_msg = await bot.send_message(chat_id, local.fetch_progress)

    try: 
        audio_path = await yt_api.download(url)
    except:
        await sleep_limit(state)
        await bot.send_message(chat_id, local.audio_error)
        await progress_msg.delete()
        return
    
    await progress_msg.edit_text(local.send_progress)
    await bot.send_chat_action(chat_id, "upload_voice")

    audio = MP4(audio_path)
    author = audio.tags['\xa9nam'][0]
    title = audio.tags['\xa9ART'][0]
    
    file_size = os.path.getsize(audio_path)
    if file_size < config.FILE_LIMIT:
        filename = os.path.split(audio_path)[1]
        cover_path = os.path.join(config.TEMP_DIR, filename + ".jpg")

        with open(cover_path, "wb") as cover_file:
            cover_file.write(audio.tags['covr'][0])

        await sleep_limit(state)
        await bot.send_audio(
            chat_id,
            caption=f"{local.source_link}({url}) | {local.download_link}({get_alt_link(audio_path)})",
            audio=types.FSInputFile(audio_path),
            performer=author,
            title=title,
            thumbnail=types.FSInputFile(cover_path)
        )
        os.remove(cover_path)
    else:
        msg = f"[{title} | {author}]({get_alt_link(audio_path)})"
        await sleep_limit(state)
        await bot.send_message(chat_id, msg)

    await progress_msg.delete()

async def update_results(result_message: Message, results: list[dict[str,str]], min_size=0):
    kb = menu.get_search_menu(results, min_size=min_size)
    await result_message.edit_reply_markup(reply_markup=kb)

async def try_search(chat_id: int, query: str, state: FSMContext):
    local = get_localization(chat_id)
    await sleep_limit(state)
    response_msg = await bot.send_message(chat_id, local.search_results + f'\n_{query}_')
    try:
        results = await yt_api.search(query, update_func=lambda results:update_results(response_msg, results, 7))
        try:
            await update_results(response_msg, results)
        except TelegramBadRequest:
            pass
    except Exception as e:
        await sleep_limit(state)
        await bot.send_message(chat_id, local.search_error)
        await response_msg.delete()

async def try_playlist_download(chat_id: int, url: str, state:FSMContext):
    playlist = yt_api.get_playlist(url)

    local = get_localization(chat_id)

    author = playlist["author"]
    title = playlist['title']
    links = playlist["links"]
    await sleep_limit(state)
    await bot.send_message(chat_id, text=local.playlist + f"\n_{title} | {author}_")

    await asyncio.gather(*(try_send_music(chat_id, link, state) for link in links))

@dp.callback_query(F.data.startswith("video_chosen"))
async def on_video_chosen(query: CallbackQuery, state: FSMContext):
    url = query.data.split(':', 1)[1]
    await try_send_music(query.from_user.id, url, state)

@dp.callback_query(F.data.startswith("language_selected"))
async def on_language_selected(query: CallbackQuery, state: FSMContext):
    language = query.data.split(':', 1)[1]
    user_id = query.from_user.id
    filters = {"user_id": user_id}

    if len(database.read("users", filters=filters)):
        database.update("users", {"language": language}, filters=filters)
    else:
        database.create("users", {"user_id": user_id, "language": language})
    
    local = get_localization(user_id)

    lang_msg_id = await state.get_value("lang_msg_id")
    await bot.edit_message_text(text=local.language_selected, chat_id=user_id, message_id=lang_msg_id)

    if await state.get_state() == "start":
        await sleep_limit(state)
        await bot.send_message(user_id, text=local.start)
        await state.set_state(None)

async def main():
    os.makedirs(config.TEMP_DIR, exist_ok=True)
    
    await loader.launch()
    pass

import asyncio

if __name__ == "__main__":
    asyncio.run(main())