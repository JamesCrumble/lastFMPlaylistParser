import httpx
import time as time_

from bs4 import BeautifulSoup, Tag
from datetime import time, datetime
from typing import Iterator, Iterable

from .settings import settings
from .schemas import (
    FieldMapping,
    CompositionMeta
)
from .services.loggers import PARSER_LOGGER


def execute_request(timeout: int = settings.REQUEST_TIMEOUT) -> str:
    with httpx.Client() as client:

        return client.get(
            settings.LAST_FM_URL,
            headers=settings.REQUEST_HEADERS,
            timeout=timeout
        ).text


def parse_request_to_compositions(request_html: str) -> Tag | None:

    # Can be parsed into two sections of compositions
    # raw_last_compositions, raw_best_compositions = BeautifulSoup(
    #     request_html, 'html.parser'
    # ).find_all('tbody')

    return BeautifulSoup(request_html, 'html.parser').find('tbody')


def parse_timestamp_field(composition_field: Tag, field_name: str) -> dict[str, str]:

    extra_fields: dict[str, str] = dict()

    if last_played := composition_field.span.attrs.get('title'):
        hours, minutes = last_played.split(
            ', '
        )[-1].split(':')
        extra_fields[field_name] = time(
            hour=int(hours),
            minute=int(minutes)
        )
    elif 'chartlist-now-scrobbling' in composition_field.span.attrs.get('class', []):
        extra_fields[field_name] = datetime.now().time()
        extra_fields['listening_now'] = True

    return extra_fields


def parse_raw_compositions(compositions_html_block: Tag) -> Iterator[CompositionMeta]:
    for raw_last_composition in compositions_html_block.find_all(settings.COMPOSITIONS_TAG):
        raw_last_composition: Tag

        parsed_fields: dict[str, str] = dict()

        for composition_field in raw_last_composition.find_all(settings.COMPOSITION_FIELDS_TAG):
            composition_field: Tag

            if field_labels := composition_field.attrs.get(FieldMapping.fields_key):
                if field_name := FieldMapping.map(field_labels):

                    if field_name == 'last_played':
                        parsed_fields.update(
                            parse_timestamp_field(
                                composition_field, field_name
                            )
                        )
                        continue

                    parsed_fields[field_name] = composition_field.text.strip()

        if parsed_fields:
            yield CompositionMeta(**parsed_fields)


def get_compositions() -> Iterable[CompositionMeta] | None:
    request_st = time_.monotonic()
    html_page_data = execute_request()

    if html_page_data is not None:
        PARSER_LOGGER.debug(
            f'REQUEST EXECUTED WITHIN "{time_.monotonic() - request_st:.2f}" SECONDS'
        )

        compositions_finding_st = time_.monotonic()
        raw_compositions = parse_request_to_compositions(html_page_data)
        PARSER_LOGGER.debug(
            f'COMPOSITIONS SECTION PARSED WITHIN "{time_.monotonic() - compositions_finding_st:.2f}" SECONDS'
        )

        if raw_compositions is not None:
            parsing_compositions_st = time_.monotonic()
            parsed_compositions = sorted(parse_raw_compositions(
                raw_compositions
            ), key=lambda v: v.last_played or 0, reverse=True)
            PARSER_LOGGER.debug(
                f'COMPOSITIONS PARSED WITHIN "{time_.monotonic() - parsing_compositions_st:.2f}" SECONDS'
            )

            return parsed_compositions
