from lib.poller import Poller
from lib.config import Config
from lib.logger import init_logger
from lib.representation import Top10Representation, StreamRepresentation


if __name__ == '__main__':
    config = Config('config.json')
    init_logger(config)
    poller = Poller(config)
    poller.run()
    top10_representation = Top10Representation()
    top10_representation.run()
    stream_representation = StreamRepresentation()
    stream_representation.run()
