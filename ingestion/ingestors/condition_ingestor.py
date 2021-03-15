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

    def ingest(self, problematic_area, problematic_traffic_area_json, activity_generating_use_json):

        # Problematic Traffic Areas
        with open(problematic_traffic_area_json) as problematic_traffic_area_file:
            data_problematic_traffic_area = json.load(problematic_traffic_area_file)

        for area, info in data_problematic_traffic_area.items():
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
                'name': area, 'subzone': info['subzone'], 'planning_area': info['planning_area'],
                'polygon': geom.wkt
            })
            r = requests.put(url=self.host + '/problematic_traffic_area', headers=self.headers, data=payload)
            log.info(r.text)

        # Problematic Areas
        with open(problematic_area) as problematic_area_file:
            data_problematic_area = json.load(problematic_area_file)

        for area, info in data_problematic_area.items():
            geom = shape(
                {
                    "coordinates": info['coords'],
                    "type": "Polygon"
                }
            )
            print(geom.wkt)
            print()
            payload = json.dumps({
                'name': area, 'subzone': info['subzone'], 'planning_area': info['planning_area'],
                'polygon': geom.wkt
            })
            r = requests.put(url=self.host + '/problematic_area', headers=self.headers, data=payload)
            log.info(r.text)

        # Activity Generating Use
        with open(activity_generating_use_json) as activity_generating_use_file:
            data_activity_generating_use = json.load(activity_generating_use_file)

        for area, info in data_activity_generating_use.items():
            geom = shape(
                {
                    "coordinates": info['coords'],
                    "type": "Polygon"
                }
            )
            print(geom.wkt)
            print()
            payload = json.dumps({
                'name': area, 'subzone': info['subzone'], 'planning_area': info['planning_area'],
                'polygon': geom.wkt
            })
            r = requests.put(url=self.host + '/activity_generating_use', headers=self.headers, data=payload)
            log.info(r.text)
