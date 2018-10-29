import requests
import time
from lib.logger import get_logger

logger = get_logger()


class HttpReader(object):

    """Sends HTTP GET requests to given URL and returns specified container with retrieved JSON."""

    def __init__(self, config):
        self.config = config

    def read(self, path, container):
        logger.info('Reading {}'.format(path))
        retries = self.config.get_http_retries()
        while True:
            try:
                r = requests.get(path)
            except Exception as e:
                logger.error(f'Cannot read {path}. Error: {e}')
                raise e
            if r.status_code == 200:
                try:
                    return container(r.json())
                except Exception as e:
                    logger.error(f'Cannot decode JSON from {path}: {e}')
                    raise e
            logger.warning('Non-200 http code received. Retrying.')
            if retries <= 0:
                error_msg = f'Cannot read {path}. No retries left.'
                logger.error(error_msg)
                raise ValueError(error_msg)
            retries -= 1
            time.sleep(self.config.get_http_retry_timeout())


if __name__ == '__main__':
    from lib.config import Config
    from lib.data_containers import BaseContainer
    from lib.logger import init_logger
    config = Config('config.json')
    init_logger(config)
    reader = HttpReader(config)
    try:
        reader.read('blahblah', BaseContainer)
    except requests.exceptions.MissingSchema as e:
        print(f'Missing schema. {e}')
    try:
        reader.read('http://yandex.ru', BaseContainer)
    except Exception as e:
        print(e)