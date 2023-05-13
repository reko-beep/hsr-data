
import unittest
from hsr_client.backend.srs_backend import SRSBackend
from hsr_client.backend.srs_backend.parsers.trace import parse_trace_data



class Test_backend(unittest.TestCase):
    
    def test_traces(self):
        import json
        with open("tests/data/traces.json") as f:
            trace_node= json.load(f)
            # print(trace_data)
            traces = []
            parse_trace_data(trace_node, traces)
            for trace in traces:
                ...

    def test_chara(self):

        srs = SRSBackend()
        chara = srs.get_character(target_name="march")
        print(chara.name)

if __name__ == "__main__":
    unittest.main()