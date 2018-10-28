from lib.messages_queue import StreamQueue, Top10Queue
import threading
from lib.logger import get_logger

logger = get_logger()


class BaseRepresentation(object):
    queue = None

    def __init__(self):
        self.container = None

    def _read_queue(self):
        container = self.__class__.queue.get()
        if self.container is not None:
            logger.debug(f'Updating container with {container.get_data()}')
            self.container.update(container)
        else:
            logger.debug(f'Setting container to {container.get_data()}')
            self.container = container

    def represent(self):
        raise NotImplementedError

    def run(self):
        read_thread = threading.Thread(name=self.__class__.__name__, target=self.represent)
        read_thread.start()


class Top10Representation(BaseRepresentation):

    """This class prints top10 detections."""

    __header = ('Name', 'Count')
    queue = Top10Queue

    def __setup_table(self):
        self.max_left_length = max([len(k['name']) for k in self.container.get_detections()])
        if self.max_left_length < len(Top10Representation.__header[0]):
            self.max_left_length = len(Top10Representation.__header[0])
        self.max_right_length = max([len(str(k['count'])) for k in self.container.get_detections()])
        if self.max_right_length < len(Top10Representation.__header[1]):
            self.max_right_length = len(Top10Representation.__header[1])

    def __print_horizontal_delimiter(self, symbol):
        l = 2 + self.max_left_length + 2 + self.max_right_length + 2
        print(symbol * l)

    def __print_line(self, left, right):
        print('| {left:{fill}<{width_1}} | {right:{fill}>{width_2}} |'.format(left=left,
                                                                              fill=' ',
                                                                              width_1=self.max_left_length,
                                                                              right=right,
                                                                              width_2=self.max_right_length))

    def represent(self):
        logger.debug(f'Started {threading.current_thread().getName()} thread.')
        self._read_queue()
        self.__setup_table()
        self.__print_horizontal_delimiter('-')
        self.__print_line(Top10Representation.__header[0], Top10Representation.__header[1])
        self.__print_horizontal_delimiter('-')
        for r in self.container.get_detections():
            self.__print_line(r['name'], r['count'])
        self.__print_horizontal_delimiter('-')

    def run(self):
        self.represent()


class StreamRepresentation(BaseRepresentation):

    """This class prints newest detections from stream."""

    queue = StreamQueue

    def __print_line(self, row):
        print(f'Country: {row["country"]}; Place: {row["city"]}({row["long"]} {row["lat"]}); Type: {row["type"]}; Name: {row["name"]}')

    def represent(self):
        logger.debug(f'Started {threading.current_thread().getName()} thread.')
        print("New virus detections:")
        while True:
            logger.debug(f"Reading from {self.queue} queue")
            self._read_queue()
            logger.debug(f"Printing detections")
            for r in self.container.get_detections():
                self.__print_line(r)
