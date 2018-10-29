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


class Histogram(BaseContainer):
    pass


class Start(BaseContainer):
    def get_url(self, path):
        return self.get_data()[path]


class DetectionsContainer(BaseContainer):
    def get_polling_interval(self):
        return self._json['polling_interval']

    def get_detections(self):
        return self._json['detections']


class Top10(DetectionsContainer):

    """Contains data for TOP-10 detections."""

    def update(self, container):
        pass


class Stream(DetectionsContainer):

    """Contains data for newest detections stream."""

    @staticmethod
    def __make_id(detection):
        return f'{detection["city"]}::{detection["name"]}::{detection["country"]}::{detection["long"]}::{detection["lat"]}::{detection["type"]}'

    @staticmethod
    def __make_set(detections):
        return set([Stream.__make_id(d) for d in detections])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_set = Stream.__make_set(self.get_detections())

    def update(self, container):
        """Replaces current detections with newest detections from stream that are not found in previous poll."""
        new_json = container.get_data().copy()
        new_detections = []
        new_set = Stream.__make_set(new_json['detections'])
        difference = new_set.difference(self.current_set)
        logger.debug(f'New detections: {difference}')
        for detection in new_json['detections']:
            if Stream.__make_id(detection) in difference:
                new_detections.append(detection)
        new_json['detections'] = new_detections
        self._json = new_json


if __name__ == '__main__':
    obj1 = {'detections':
            [{'city': '', 'name': 'Suspicious:W32/Riskware.0abd19df41!Online', 'country': 'FI', 'long': '24.9375', 'lat': '60.1708', 'type': 'Suspicious:W32/Riskware'},
             {'city': 'Dornstadt', 'name': 'Trojan.Exploit.ANXM', 'country': 'DE', 'long': '9.95', 'lat': '48.4667', 'type': 'Trojan'},
             {'city': 'Ponda', 'name': 'Trojan:W32/Downadup.AL', 'country': 'IN', 'long': '74.0167', 'lat': '15.4', 'type': 'Trojan:W32/Downadup'},
             {'city': 'Beograd', 'name': 'Trojan.JAVA.Agent.MP', 'country': 'RS', 'long': '20.4681', 'lat': '44.8186', 'type': 'Trojan'},
             {'city': '', 'name': 'Trojan.Generic.23025481', 'country': 'JP', 'long': '139.69', 'lat': '35.69', 'type': 'Trojan'}]
            }
    obj2 = {'detections':
                [{'city': '', 'name': 'Suspicious:W32/Riskware.0abd19df41!Online', 'country': 'FI', 'long': '24.9375', 'lat': '60.1708', 'type': 'Suspicious:W32/Riskware'},
                 {'city': 'asdfg', 'name': 'Ugly.Malware', 'country': '', 'long': '24.9375', 'lat': '60.1708', 'type': 'Ugly'}]
            }
    s = Stream(obj1)
    assert len(s.get_detections()) == 5
    s2 = Stream(obj2)
    s.update(s2)
    assert len(s.get_detections()) == 1
