from lib.data_containers import Top10, Stream, Start, Histogram
from lib.reader import HttpReader
from lib.messages_queue import StreamQueue, Top10Queue
import time
import threading
from lib.logger import get_logger


logger = get_logger()


class Poller(object):

    """Polls data sources and puts obtained data to message queues."""

    def __init__(self, config):
        self.config = config
        self.reader = HttpReader(config)
        self.start_page = self.__read_base_page()

    def __read_base_page(self):
        return self.reader.read(self.config.get_base_uri(), Start)

    def __read_top10(self):
        top10_path = self.config.get_top10_path()
        top10_url = '{}:{}'.format(self.config.get_schema(), self.start_page.get_url(top10_path))
        return self.reader.read(top10_url, Top10)

    def __read_stream_path(self):
        stream_path = self.config.get_stream_path()
        stream_url = '{}:{}'.format(self.config.get_schema(), self.start_page.get_url(stream_path))
        return self.reader.read(stream_url, Stream)

    def __read_histogram(self):
        histogram_path = self.config.get_histogram_path()
        histogram_url = '{}:{}'.format(self.config.get_schema(), self.start_page.get_url(histogram_path))
        return self.reader.read(histogram_url, Histogram)

    def put_top10(self):
        try:
            top10 = self.__read_top10()
            Top10Queue.put(top10)
        except Exception as e:
            error_msg = f'Cannot put top10 data to queue: {e}'
            logger.error(error_msg)
            raise e

    def put_stream(self):
        logger.debug(f'Started {threading.current_thread().getName()} thread.')
        while True:
            try:
                stream = self.__read_stream_path()
                logger.debug(f'Putting {stream} to StreamQueue')
                StreamQueue.put(stream)
                wait_for = stream.get_polling_interval() * self.config.get_refresh_multiplicator()
                logger.debug(f'Waiting for {wait_for}')
                time.sleep(wait_for)
            except Exception as e:
                error_msg = f'Cannot put stream data to queue: {e}'
                logger.error(error_msg)
                raise e

    def run(self):
        self.put_top10()
        stream_thread = threading.Thread(name=f"{self.__class__.__name__}-Stream", target=self.put_stream)
        stream_thread.start()


if __name__ == '__main__':
    from lib.config import Config
    c = Config('config.json')
    p = Poller(c)
    p.put_top10()
    el = Top10Queue.get()
    print(el.get_data())
