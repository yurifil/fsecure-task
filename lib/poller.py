from lib.data_containers import Top10, Stream, Start, Histogram
from lib.reader import HttpReader
from lib.messages_queue import StreamQueue, Top10Queue
import time
import threading
from lib.logger import get_logger


logger = get_logger()


class Poller(object):
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
        top10 = self.__read_top10()
        Top10Queue.put(top10)

    def put_stream(self):
        logger.debug(f'Started {threading.current_thread().getName()} thread.')
        while True:
            stream = self.__read_stream_path()
            logger.debug(f'Putting {stream} to StreamQueue')
            StreamQueue.put(stream)
            wait_for = stream.get_polling_interval() / 2
            logger.debug(f'Waiting for {wait_for}')
            time.sleep(wait_for)

    def run(self):
        self.put_top10()
        stream_thread = threading.Thread(name=f"{self.__class__.__name__}-Stream", target=self.put_stream)
        stream_thread.start()
