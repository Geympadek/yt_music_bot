class Localization:
    def __init__(
            self,
            fetch_progress,
            audio_error,
            send_progress,
            search_results,
            search_error,
            language_selected,
            start,
            source_link,
            download_link,
            playlist):
        self.fetch_progress = fetch_progress
        self.audio_error = audio_error
        self.send_progress = send_progress
        self.search_results = search_results
        self.search_error = search_error
        self.language_selected = language_selected
        self.start = start
        self.source_link = source_link
        self.download_link = download_link
        self.playlist = playlist

localizations = {
    "ru": Localization(
        fetch_progress="*Загрузка аудио...*🕒",
        audio_error="*Во время загрузки аудио произошла ошибка.*",
        send_progress="*Отправка аудио...*🚀",
        search_results="*Результаты по запросу:*",
        search_error="*Во время поиска произошла ошибка.*",
        language_selected="*Вы выбрали Русский язык.*",
        start="*Привет!*👋\n*🎹 Этот бот может скачать аудио с любого видео на Youtube. Легко качивайте музыку, плейлисты, видео или подкасты.*\n\n_Отправьте ссылку или поисковой запрос чтобы начать._",
        source_link="[оригинал]",
        download_link="[скачать]",
        playlist="*Плейлист*"
    ),
    "en": Localization(
        fetch_progress="*Loading audio...*🕒",
        audio_error="*During loading and error occured.*",
        send_progress="*Sending audio...*🚀",
        search_results="*Here are some search results for:*",
        search_error="*During the search an error occured.*",
        language_selected="*You've chosen English language.*",
        start="*Hi!*👋\n*🎹 This bot can download audio from any Youtube video. Download music, playlists, video or podcasts!*\n\n_Send a url, or a search query to start._",
        source_link="[source]",
        download_link="[download]",
        playlist="*Playlist*"
    )
}