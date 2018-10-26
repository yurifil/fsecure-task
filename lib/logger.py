import logging
import os


APP_NAME = 'f-secure'


def init_logger(config):

    FORMAT = '%(asctime)-15s::%(levelname)s::%(threadName)s::%(module)s::%(lineno)s::%(message)s'
    formatter = logging.Formatter(FORMAT)

    os.makedirs(config.get_logdir(), exist_ok=True)

    log_path = os.path.join(config.get_logdir(), f'{APP_NAME}.log')

    fh = logging.FileHandler(log_path)
    fh.setFormatter(formatter)
    fh.setLevel(config.get_log_level())

    logger = logging.getLogger(APP_NAME)
    logger.setLevel(config.get_log_level())
    logger.addHandler(fh)


def get_logger():
    return logging.getLogger(APP_NAME)
