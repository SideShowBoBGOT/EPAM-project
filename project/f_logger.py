"""
Module containing factory for logger merging it with handlers and formatters.
"""
import logging
import socket
host = socket.getfqdn()
addr = socket.gethostbyname(host)

def get_logger():
    """
    Function creating logger and merging it with handlers and formatters.
    :return: logger instance
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(f'{addr} - - [%(asctime)s]'
                                  f' - - %(levelname)s - - [%(module)s] "%(message)s"',
                                  datefmt='%d/%b/%Y %H:%M:%S')
    file_handler = logging.FileHandler('log.txt')
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


logger = get_logger()
