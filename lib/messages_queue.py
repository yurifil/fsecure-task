import queue
from lib.logger import get_logger


"""This module contains queue classes for messages exchange."""


logger = get_logger()


class BaseQueue(object):

    @classmethod
    def put(cls, element):
        logger.debug(f'Putting element {element} to {cls.__name__} queue.')
        cls._queue.put(element)

    @classmethod
    def get(cls):
        logger.debug(f'Getting element from {cls.__name__} queue.')
        return cls._queue.get()


class StreamQueue(BaseQueue):
    _queue = queue.Queue()


class Top10Queue(BaseQueue):
    _queue = queue.Queue()

