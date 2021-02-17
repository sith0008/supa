import csv
import requests
import json
import logging

log = logging.getLogger('root')


class ShophouseIngestor:
    def __init__(self, host, endpoint):
        self.url = host + endpoint
        self.headers = {'content-type': 'application/json'}
        self.use_type_mapping = {
            'Industrial Showroom': 'Showroom',
            "Workers' Dormitory": "Workers' Dormitories",
            'Gym / Fitness Centre': 'Fitness Centre/Gymnasium',
            'Massage establishment / Spa': 'Massage Establishment',
            'Religious Use': 'Limited & Non-Exclusive Religious Use',
            'Bar': 'Bar/Pub',
            'Pet Shop / Vet Clinic': 'Pet Shop',
        }

    def ingest(self, shophouse):

        with open(shophouse) as shophouse_file:
            data_shophouse = json.load(shophouse_file)

        for address, info in data_shophouse.items():
            block, road = address.split(' ', maxsplit=1)
            for storey in info['StoreyList']:
                if ',' not in storey['storey']:  # ignore those with comma for now
                    floor, unit = (storey['storey'].split('-', maxsplit=1) + ['0'])[:2]

                    # # Clean data: floor
                    # Convert cardinal numbers to numbers
                    floor = floor.replace('1ST', '1').replace('2ND', '2').replace('3RD', '3')
                    # Remove hash symbol
                    floor = floor.replace('#', '')
                    # Strip leading 0s
                    floor = floor.lstrip('0')
                    # Default floor to '0' if None
                    if not floor: floor = '0'

                    # # Clean data: unit
                    # Strip leading 0s
                    unit = unit.lstrip('0')
                    # Default floor to '0' if None (ignore mezz unit for now)
                    if not unit or unit == 'N.A.' or unit == 'MEZZ': unit = '0'

                    for allowable in storey['allowableUseList']:
                        if 'allowed' in allowable:
                            use_class = allowable['useTypeDescr']
                            allowed = allowable['allowed']
                            reason = allowable['allowedReason']

                            payload = json.dumps({
                                'block': block, 'road': road, 'floor': floor, 'unit': unit,
                                'use_class': use_class, 'allowed': allowed, 'reason': reason
                            })
                            print(payload)
                            r = requests.put(url=self.url, headers=self.headers, data=payload)
                            log.info(r.text)
