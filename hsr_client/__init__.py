from abc import ABC

from hsr_client.constants import Languages, Types
from hsr_client.backend import BackendAdapter
from hsr_client import datamodels as models


# Public facing api client.
class HsrClient:
    def __init__(self):
        # abstract away multiple backends. with a single backend adapter. 
        # i guess this is too much.
        # just using SRSBackend here would have been enough.
        self.adapter = BackendAdapter()
    
        # our own api related logic goes here
        # in this case, looping and searching.
        # here we have the convinience of working with our own data models. (ex: Trace)
    def find_trace(self, trace_name) -> models.trace.Trace:
        # for trace in self.adapter().fetch_traces():
        #     if trace.name  == trace_name:
        #         return 
        ...

    def get_character(self, chara_name) -> models.chara.Character:
        # nothing else to do here.
        return self.adapter().get_character(chara_name)



    def get_lightcones(self) -> List[Lightcone]:
        return self.adapter().get_lightcones()
        # return []



if __name__ == "__main__":
    client = HsrClient()
    # print(client.get_character("march 7th")) 
    print(client.get_lightcones())
