import requests
import json
import logging

log = logging.getLogger('root')


class PostalCodeIngestor:
    def __init__(self, host, endpoint):
        self.url = host + endpoint
        self.headers = {'content-type': 'application/json'}
        self.land_use_to_prop_type = {
            'COMMERCIAL': 'Commercial Buildings',
            'COMMERCIAL & RESIDENTIAL': 'Mixed Commercial & Residential Developments',
            'CIVIC & COMMUNITY INSTITUTION': 'Civic and Community Institution',
            'SPORTS & RECREATION': 'Sports & Recreation Buildings',
            'HOTEL': 'Hotel',
            'BUSINESS 1': 'Industrial Buildings',
            'BUSINESS 2': 'Industrial Buildings',
            'BUSINESS PARK': 'Business Park',
            'BUSINESS 1 - White': 'Business 1-White Buildings',
            'BUSINESS 2 - White': 'Business 2-White Buildings',
            'PLACE OF WORSHIP': 'Place of Worship',
            'EDUCATIONAL INSTITUTION': 'Educational Institution',
            'HEALTH & MEDICAL CARE': 'Medical and Healthcare',
        }

    def ingest(self, postal_code, hdb_commercial, shophouse, land_use):
        with open(postal_code) as postal_code_file:
            data_postal_code = json.load(postal_code_file)

        with open(hdb_commercial) as hdb_commercial_file:
            data_hdb_commercial = json.load(hdb_commercial_file)

        with open(shophouse) as shophouse_file:
            data_shophouse = json.load(shophouse_file)

        with open(land_use) as land_use_file:
            data_land_use = json.load(land_use_file)

        for postal_code, infos in data_postal_code.items():
            seen = set()
            for info in infos:
                if (info['BLK_NO'], info['ROAD_NAME']) not in seen:
                    seen.add((info['BLK_NO'], info['ROAD_NAME']))

                    block = info['BLK_NO']
                    road = info['ROAD_NAME']
                    lat = info['LATITUDE']
                    lng = info['LONGITUDE']

                    address = block + " " + road
                    property_type = None

                    land_use_type, land_use_detail = data_land_use[postal_code]

                    # Check if hdb_commercial
                    if postal_code in data_hdb_commercial and data_hdb_commercial[postal_code] == address:
                        property_type = 'HDB Commercial Premises'

                    # Check if shophouse
                    elif postal_code in data_shophouse and [block, road] in data_shophouse[postal_code]:
                        property_type = 'Shophouses'

                    else:
                        # Handle conservation areas
                        if land_use_detail == 'Conservation Area':
                            property_type = 'Buildings within Historic Conservation Areas'

                        # Handle landed houses
                        elif land_use_detail and 'landed' in land_use_detail.lower():
                            property_type = 'Landed Houses'

                        # Map land use to property type
                        elif land_use_type in self.land_use_to_prop_type:
                            property_type = self.land_use_to_prop_type[land_use_type]

                    payload = json.dumps({
                        'block': block, 'road': road, 'postal_code': postal_code,
                        'land_use_type': land_use_type, 'property_type': property_type,
                        'latitude': lat, 'longitude': lng
                    })
                    r = requests.put(url=self.url, headers=self.headers, data=payload)
                    log.info(r.text)
