import json
import logging
import requests
from shapely.geometry import shape

log = logging.getLogger('root')


class ConditionIngestor:
    def __init__(self, host, endpoint):
        self.host = host
        self.url = host + endpoint
        self.headers = {'content-type': 'application/json'}

    def ingest(self, problematic_area):

        i = 0

        with open(problematic_area) as problematic_area_file:
            data_problematic_area = json.load(problematic_area_file)

        for area, info in data_problematic_area.items():
            i += 1
            print(area)
            geom = shape(
                {
                    "coordinates": info['coords'],
                    "type": "Polygon"
                }
            )
            print(geom.wkt)
            print()
            payload = json.dumps({
                'pa_id': i, 'name': area, 'subzone': info['subzone'], 'planning_area': info['planning'],
                'polygon': geom.wkt
            })
            r = requests.put(url=self.host + '/problematic_area', headers=self.headers, data=payload)
            log.info(r.text)