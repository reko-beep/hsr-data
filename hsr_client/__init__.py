from typing import List
from hsr_client.constants import Language, Item
from hsr_client.backend import BackendAdapter
from hsr_client import datamodels as models
from hsr_client.datamodels.chara import Character
from hsr_client.datamodels.lightcone import Lightcone
from hsr_client.datamodels.searchItem import SearchItem


# Public facing api client.
class HsrClient:
    def __init__(self):
        # abstract away multiple backends. with a single backend adapter.
        # i guess this is too much.
        # just using SRSBackend here would have been enough.
        self.adapter = BackendAdapter()

    # # our own api related logic goes here
    # # in this case, looping and searching.
    # # here we have the convinience of working with our own data models. (ex: Trace)
    # def find_trace(self, trace_name) -> models.trace.Trace:
    #     # for trace in self.adapter().fetch_traces():
    #     #     if trace.name  == trace_name:
    #     #         return
    #     ...

    # def get_character(self, chara_name) -> models.chara.Character:
    #     # nothing else to do here.
    #     return self.adapter().get_character(chara_name)

    def get_lightcone(self, name=None, searchItem=None) -> Lightcone:
        """
        get lightcone by name or with SearchItem
        """

        if name is not None:
            return self.adapter().get_lightcone_by_name(name)
        elif searchItem is not None:
            return self.adapter().resolve_lightcone(searchItem)
        else:
            raise Exception("either name or searchItem is necessary")


    def get_character(self, name=None, searchItem=None) -> Character:
        """
        Get Character by name or `SearchItem`
        """
        if name is not None:
            return self.adapter().get_character_by_name(name)
        elif searchItem is not None:
            return self.adapter().character_lightcone(searchItem)
        else:
            raise Exception("either name or searchItem is necessary")


    def search_item(
        self,
        item_type: Item,
        filter=None
    ) -> List[SearchItem]:
        return self.adapter().search_item(item_type)


if __name__ == "__main__":
    client = HsrClient()
    # print(client.get_lightcone(name="Arrows"))
    # print(client.search_item(Item.CHARACTERS))
    print(client.get_character(name="March 7th"))
