import requests
import time
from lib.logger import get_logger

logger = get_logger()


class HttpReader(object):
    def __init__(self, config):
        self.config = config

    def read(self, path, container):
        logger.info('Reading {}'.format(path))
        retries = self.config.get_http_retries()
        while True:
            r = requests.get(path)
            if r.status_code == 200:
                return container(r.json())
            if retries <= 0:
                raise ValueError('Cannot read {}. No retries left.'.format(path))
            retries -= 1
            time.sleep(self.config.get_http_retry_timeout())

    def get_top10(self):
        pass

    def get_stream(self):
        pass
