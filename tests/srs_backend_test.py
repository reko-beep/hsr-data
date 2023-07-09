
import unittest
from hsr_client.backend.srs_backend import SRSBackend
from hsr_client.backend.srs_backend.parsers.trace import parse_trace_data
from hsr_client.datamodels.searchItem import SearchItem
from hsr_client.constants import Item

class Test_backend(unittest.TestCase):
    
    def test_traces(self):
        import json
        with open("tests/data/traces.json") as f:
            trace_node= json.load(f)
            print(trace_data)
            traces = []
            parse_trace_data(trace_node, traces)
            for trace in traces:
                ...

    def test_chara(self):

        srs = SRSBackend()
        chara = srs.get_character(target_name="march")
        print(chara.name)

    def test_mtrl(self):

        srs = SRSBackend()
        mtrl = srs.resolve_material(search_item=SearchItem(url='', iconPath='', type=Item.MATERIAL, name='', rarity=4, id=24001))
        print(mtrl)

if __name__ == "__main__":
    unittest.main()