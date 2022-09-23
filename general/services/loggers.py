import logging

from ..settings import settings

logging.basicConfig(
    level=settings.LOGGING_LEVEL
)

PARSER_LOGGER = logging.getLogger('PARSER')
