from lib.logger import get_logger


logger = get_logger()


class BaseContainer(object):
    def __init__(self, json_obj, refresh_func=None):
        self._json = json_obj
        self.refresh = refresh_func

    def get_data(self):
        return self._json

    def update(self, container):
        raise NotImplementedError


class Top10(BaseContainer):
    def update(self, container):
        pass


class Stream(BaseContainer):
    @staticmethod
    def __make_id(detection):
        return f'{detection["city"]}::{detection["name"]}::{detection["country"]}::{detection["long"]}::{detection["lat"]}::{detection["type"]}'

    @staticmethod
    def __make_set(detections):
        return set([Stream.__make_id(d) for d in detections])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_set = Stream.__make_set(self.get_detections())

    def get_polling_interval(self):
        return self._json['polling_interval']

    def get_detections(self):
        return self._json['detections']

    def update(self, container):
        new_json = container.get_data()
        new_detections = []
        new_set = Stream.__make_set(new_json['detections'])
        difference = new_set.difference(self.current_set)
        logger.debug(f'New detections: {difference}')
        for detection in new_json['detections']:
            if Stream.__make_id(detection) in difference:
                new_detections.append(detection)
        new_json['detections'] = new_detections
        self._json = new_json


class Histogram(BaseContainer):
    pass


class Start(BaseContainer):
    def get_url(self, path):
        return self.get_data()[path]
