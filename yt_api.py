from io import BytesIO
from pytubefix import YouTube, Search
import os
from threading import Lock
from mutagen import mp4
from PIL import Image
import requests
import config
from concurrent.futures import ProcessPoolExecutor
import asyncio
import typing

TEMP_DIR = os.path.join(config.TEMP_DIR, "yt_api")

os.makedirs(TEMP_DIR, exist_ok=True)

song_count = 0
mutex = Lock()

def soft_clear():
    """
    Cleares the temp directory, ignoring errors
    """
    for file in os.listdir(TEMP_DIR):
        path = os.path.join(TEMP_DIR, file)
        try:
            os.remove(path)
        except:
            pass

def edit_cover(original: bytes):
    img = Image.open(BytesIO(original))
    
    CROP_SIZE = 355

    width, height = img.size
    left = (width - CROP_SIZE) // 2
    top = (height - CROP_SIZE) // 2
    right = (width + CROP_SIZE) // 2
    bottom = (height + CROP_SIZE) // 2

    img_cropped = img.crop((left, top, right, bottom))
    output = BytesIO()
    img_cropped.save(output, format='JPEG')
    return output.getvalue()

def format_author(raw: str):
    return raw.replace(" - Topic", "")

def load_audio(url: str, max_retries=3, timeout = 7.5) -> str:
    """
    Takes youtube `url` as input and returns the name of downloaded file.
    """
    global song_count
    filename = ""
    with mutex:
        song_count += 1
    filename = str(song_count) + ".m4a"
        
    path = os.path.join(TEMP_DIR, filename)
    
    attempt = 0
    while True:
        yt = YouTube(url)
        ys = yt.streams.get_audio_only()

        interrupted = False

        try:
            ys.download(output_path=TEMP_DIR, filename=filename, timeout=timeout)
        except Exception:
            interrupted = True
            print("Error raised")

        if interrupted:
            attempt += 1
            if attempt >= max_retries:
                raise Exception("Exceeded number of retries.")
            print(f"Starting {attempt} retry.")
            continue

        if not os.path.exists(path):
            raise Exception("Unable to fetch the song from yt")
        break

    audio = mp4.MP4(path)
    
    audio['\xa9nam'] = yt.title  # or use a custom title
    audio['\xa9ART'] = format_author(yt.author) # or use a custom artist

    cover = requests.get(yt.thumbnail_url)
    cropped_cover = edit_cover(cover.content)

    audio['covr'] = [mp4.MP4Cover(cropped_cover)]
    audio.save()

    return filename

async def download(url: str):
    """
    Takes `url` of the yt video as input and returns path to the audio file
    """
    soft_clear()
    
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        filename = await loop.run_in_executor(executor, load_audio, url)
    return os.path.join(TEMP_DIR, filename)

async def search(query: str, limit: int = 10, update_func: typing.Callable[[list[dict[str, str]]], None] | None = None) -> list[dict]:
    raw_results = Search(query)
    videos = raw_results.videos

    results = []
    for video in videos[:limit]:
        results.append({    
            "author": format_author(video.author),
            "title": video.title,
            "url": video.watch_url
        })

        if update_func is not None:
            await update_func(results)
    return results