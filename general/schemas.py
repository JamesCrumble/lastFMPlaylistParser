from datetime import time
from pydantic import BaseModel
from dataclasses import dataclass, fields


MAPPED_FIELD_NAME = str


@dataclass
class FieldMapping:

    fields_key: str = 'class'

    name: str = 'chartlist-name'
    artist: str = 'chartlist-artist'
    last_played: str = 'chartlist-timestamp'

    def __new__(cls, *_, **__):
        raise NotImplementedError()

    @classmethod
    def map(cls, field_labels: list[str]) -> MAPPED_FIELD_NAME | None:
        for field in fields(cls):
            if field.default in field_labels:
                return field.name


class CompositionMeta(BaseModel):

    name: str
    artist: str
    last_played: time | None = None  # should be datetime but need more work on it
    listening_now: bool = False
