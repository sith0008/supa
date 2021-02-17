import json
from collections import defaultdict

with open('Shophouse_Guidelines.json') as f:
    data_shophouse = json.load(f)

with open('Shophouse.json') as g:
    data_shophouse_2 = json.load(g)

correct_list = data_shophouse_2.values()

for k in data_shophouse.keys():
    block, road = k.split(maxsplit=1)
    if [block, road] not in correct_list:
        print([block, road])

# storeyList = data['2 NORTH CANAL ROAD']['StoreyList']
#
# for storey in storeyList:
#     print(storey)
