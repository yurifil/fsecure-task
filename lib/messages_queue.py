import queue
from lib.logger import get_logger


logger = get_logger()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


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

