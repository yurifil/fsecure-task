import json


class Config(object):
    def __init__(self, path):
        self._config = None
        self._path_to_config = path
        self._parse_json(self._path_to_config)

    def _parse_json(self, path_to_json):
        with open(path_to_json) as json_fp:
            self._config = json.load(json_fp)

    def get_base_uri(self):
        return self._config['base_uri']

    def get_stream_path(self):
        return self._config['stream_path']

    def get_top10_path(self):
        return self._config['top10_path']

    def get_histogram_path(self):
        return self._config['histogram_path']

    def get_http_retry_timeout(self):
        return self._config['http']['retry_timeout']

    def get_http_retries(self):
        return self._config['http']['retries']

    def get_log_level(self):
        return self._config['log_level']

    def get_schema(self):
        return self._config['schema']

    def get_refresh_multiplicator(self):
        return self._config['refresh_multiplicator']

    def get_logdir(self):
        return self._config['logdir']
