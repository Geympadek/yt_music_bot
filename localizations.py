class Localization:
    def __init__(
            self,
            fetch_progress,
            audio_error,
            send_progress,
            file_too_large,
            search_results,
            search_error,
            language_selected):
        self.fetch_progress = fetch_progress
        self.audio_error = audio_error
        self.send_progress = send_progress
        self.file_too_large = file_too_large
        self.search_results = search_results
        self.search_error = search_error
        self.language_selected = language_selected

localizations = {
    "ru": Localization(
        fetch_progress="*Загрузка аудио...*🕒",
        audio_error="*Во время загрузки аудио произошла ошибка.*",
        send_progress="*Отправка аудио...*🚀",
        file_too_large="*Не удалось отправить аудио: размер файла превышает лимит Телеграма.*",
        search_results="*Результаты по запросу:*",
        search_error="*Во время поиска произошла ошибка.*",
        language_selected="*Вы выбрали Русский язык..*"
    ),
    "en": Localization(
        fetch_progress="*Loading audio...*🕒",
        audio_error="*During loading and error occured.*",
        send_progress="*Sending audio...*🚀",
        file_too_large="*Could not send the audio: file's size exceeds Telegram's limit.*",
        search_results="*Here are some search results for:*",
        search_error="*During the search an error occured.*",
        language_selected="*You've chosen English language..*"
    )
}