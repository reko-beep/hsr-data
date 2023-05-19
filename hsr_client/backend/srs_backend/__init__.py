import json
from typing import List, Union
from requests_cache import CachedSession
from hsr_client.backend.srs_backend.parsers.lightcone import parse_lightcone

from hsr_client.constants import Language, Item
from hsr_client.datamodels.character import Character
from hsr_client.datamodels.lightcone import Lightcone
from hsr_client.datamodels.searchItem import SearchItem
from hsr_client.errors import InvalidLanguage, InvalidSearchItem
from hsr_client import routes
from hsr_client.utils import base36encode, generate_t, check
from hsr_client.backend.util import Backend
import hsr_client.datamodels as models
from .parsers import trace as trace_parser


route_mapping = {
    Item.CHARACTERS: routes.CHARACTERS,
    Item.PLAYERCARDS: routes.PLAYERCARDS,
    Item.FOODS: routes.CONSUMABLES,
    Item.RELICS: routes.RELICS,
    Item.LIGHTCONES: routes.LIGHTCONES,
    Item.BOOKS: routes.BOOKS,
    Item.MATERIALS: routes.MATERIALS,
}


# backend for starrail station.
class SRSBackend(Backend):
    def __init__(self) -> None:
        super().__init__()
        # self.session = CachedSession(cache_name='srs.cache', backend='sqlite', expire_after=3600)

    def generate_hash_route(
        self,
        language: Language,
        route: routes.Routes,
        goto: bool = False,
        item_id: str = "",
    ):
        """

        :generates hashed route for fetching data

        --
        params
        --

        - language: Languages Enum
             Languages.ENG, Languages.RU etc
        - route: a Routes object
        - goto: if you want to search in a specific route [True]
             defaults to False

        - item_id : id of the item you want to search in a route

        """

        if not isinstance(language, Language):
            raise InvalidLanguage

        url = route.generate_main_lang_path(language)
        if goto:
            if route.path is not None:
                url = f"{route.generate_goto_lang_path(language)}{item_id}.json"

        hashed_path = base36encode(generate_t(url))

        return f"{routes.MAIN_ROUTE}{hashed_path}"

    def __fetch(
        self,
        language: Language,
        route: routes.Routes,
        goto: bool = False,
        item_id: str = "",
    ) -> List[dict] | dict | None:
        """

        :fetches data from the api route
        --
        params
        --

        - language: Languages Enum
             Languages.EN, Languages.RU etc

        - route: a Routes object

        - goto: if you want to search in a specific route [True]
             defaults to False

        - item_id : id of the item you want to search in a route

        """

        if not isinstance(language, Language):
            raise InvalidLanguage

        self.session.headers.update({"referer": "https://starrailstation.com/"})

        response = self.session.get(
            self.generate_hash_route(language, route, goto, item_id)
        )

        if response.status_code < 300:
            data = response.json()
            if "entries" in data:
                return data["entries"]
            else:
                return data

    def search_item(
        self, item_type: Item = None, language: Language = Language.EN
    ) -> list[SearchItem]:
        """

        :fetches all items from api route
        --
        params
        --

        - language: Languages Enum
            Languages.EN, Languages.RU etc
        - type : a type object
            Item.MATERIALS, Item.PLAYERCARDS, Item.CHARACTERS etc


        """

        if not isinstance(language, Language):
            raise InvalidLanguage

        response = self.__fetch(language, routes.SEARCH, False)

        if response is not None:
            all_items = [
                SearchItem(
                    **{
                        **d,
                        **{"id": d["url"].split("/")[1]},
                        "iconPath": routes.IMAGE_ROUTE.format(assetId=d["iconPath"]),
                    }
                )
                for d in response
            ]
            if item_type is not None:
                return list(filter(lambda x: x.type == item_type, all_items))

            return all_items

    # TODO: fix this: what if searchitem was result of a search with different language
    # thatn the language passed to this function. maybe language can be a part of
    # the class itself. and fetch would simply use that language.
    # also jsut to prevent backend changing language in the middle of a function with
    # multi api calls. data structures involved in these cross api calls should also
    # have the language attribute as part of them. (stuff liek SearchItem)
    # or maybe even models?

    def resolve_lightcone(
        self, search_item: SearchItem, language: Language = Language.EN
    ) -> Lightcone:
        """get details of a light cone

        Args:
            item (SearchItem): SearchItem of Lightcone type.
            language (Languages, optional):  Defaults to Languages.EN.

        Raises:
            InvalidItemType: if SearchItem is not of Lightcone Type
            InvalidSearchItem: if item is not a SearchItem
        Returns:
            Lightcone: Lightcone object
        """

        if isinstance(search_item, SearchItem):
            if search_item.type != Item.LIGHTCONES:
                raise InvalidSearchItem(
                    "Expected Type.LIGHTCONES, found: " + search_item.type
                )

            response = self.__fetch(language, routes.LIGHTCONES, True, search_item.id)
            if response is not None:
                return parse_lightcone(response)

        else:
            raise TypeError("provided argument is not a `SearchItem`")

    def get_lightcone_by_name(
        self, name: str, language: Language = Language.EN
    ) -> Lightcone:
        """Gets lightcone by name

        Args:
            name (str): name of the lightcone
            language (Languages, optional): Defaults to Languages.EN.

        Returns:
            Lightcone:
        """
        lightcones = self.search_item(Item.LIGHTCONES)

        for lightcone in lightcones:
            # use check to filter search item
            item = check(lightcone, "name", name)
            if item is not None:
                return self.resolve_lightcone(item)

    def get_character(self, target_name) -> models.chara.Character:
        import json

        # get this from ROUTE
        with open("tests/data/character.json") as f:
            character_raw = json.load(f)

        chara_name = character_raw["name"]
        traces_raw = character_raw["skillTreePoints"]
        traces = []
        trace_parser.parse_trace_data(traces_raw, traces)

        return models.chara.Character(name=chara_name, traces=traces)
