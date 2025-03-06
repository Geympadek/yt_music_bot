from aiogram import types

EMPTY_BTN = types.InlineKeyboardButton(text="...", callback_data=" ")

def get_search_menu(results: list[dict[str, str]], min_size=0):
    kb = []
    for result in results:
        kb.append([
            types.InlineKeyboardButton(
                text=f"{result['author']} — {result['title']}",
                callback_data=f"video_chosen:{result['url']}"
            )
        ])
    empty_count = min_size - len(results)
    if empty_count > 0:
        for _ in range(empty_count):
            kb.append([EMPTY_BTN])

    return types.InlineKeyboardMarkup(inline_keyboard=kb)