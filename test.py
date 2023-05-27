

import unittest
from hsr_client.backend.srs_backend import SRSBackend
#from hsr_client.backend.srs_backend.parsers.trace import parse_trace_data
from hsr_client.datamodels.searchItem import SearchItem
from hsr_client.constants import Item



srs = SRSBackend()
mtrl = srs.resolve_material(search_item=SearchItem(url='', iconPath='', type=Item.MATERIAL, name='', rarity=4, id=24001))
print(mtrl)