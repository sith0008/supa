import csv
import requests
import json
import logging

log = logging.getLogger('root')


class PropertyTypeIngestor:
    def __init__(self, host, endpoint):
        self.url = host + endpoint
        self.headers = {'content-type': 'application/json'}

    def ingest(self, csv_file):
        raise NotImplementedError

        # csv_data = csv.reader(open(csv_file))
        #
        # title = list(map(str.lower, next(csv_data)))
        #
        # for row in csv_data:
        #     payload = json.dumps({k: v for k, v in zip(title, row) if v})
        #     r = requests.put(url=self.url, headers=self.headers, data=payload)
        #     log.info(r.text)
