import logging

from pydantic import BaseSettings


class Settings(BaseSettings):

    LOGGING_LEVEL: int = logging.DEBUG

    LAST_FM_URL: str = 'https://www.last.fm/ru/user/i1ame_ru'
    REQUEST_TIMEOUT: int = 15
    REQUEST_HEADERS: dict[str, str] = dict(
        user_agent=(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/103.0.0.0 Safari/537.36'
        )
    )

    COMPOSITIONS_TAG: str = 'tr'
    COMPOSITION_FIELDS_TAG: str = 'td'


settings = Settings()
