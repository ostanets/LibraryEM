import logging

from config import LOG_LEVEL

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

LOG_FILE = 'library.log'
LOG_FILE_MODE = 'a'


def configure_logging():
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

    if LOG_FILE:
        file_handler = logging.FileHandler(LOG_FILE, mode=LOG_FILE_MODE)
        file_handler.setLevel(LOG_LEVEL)
        file_formatter = logging.Formatter(LOG_FORMAT)
        file_handler.setFormatter(file_formatter)
        logging.getLogger().addHandler(file_handler)
