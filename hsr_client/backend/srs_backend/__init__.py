import json
from typing import List, Union, Optional, Literal
from requests_cache import CachedSession

from hsr_client.backend.srs_backend.parsers.material import parse_material

from hsr_client.constants import Language, Item
from hsr_client.datamodels import chara
from hsr_client.datamodels.chara import Character
from hsr_client.datamodels.lightcone import Lightcone
from hsr_client.datamodels.searchItem import SearchItem
from hsr_client.datamodels.material import Material

from hsr_client.errors import InvalidLanguage, InvalidSearchItem, EmptyResponse
from hsr_client import routes
from hsr_client.utils import base36encode, generate_t, check
from hsr_client.backend.util import Backend
import hsr_client.datamodels as models



route_mapping = {
    Item.CHARACTER: routes.CHARACTERS,
    Item.PLAYERCARD: routes.PLAYERCARDS,
    Item.FOOD: routes.CONSUMABLES,
    Item.RELIC: routes.RELICS,
    Item.LIGHTCONE: routes.LIGHTCONES,
    Item.BOOK: routes.BOOKS,
    Item.MATERIAL: routes.MATERIALS,
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
        item_id: Union[int, str] = "",
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
        item_id: Union[int, str] = "",
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
        self, item_type: Optional[Item] = None, 
        language: Language = Language.EN
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
        else:
            raise EmptyResponse

    # TODO: fix this: what if searchitem was result of a search with different language
    # thatn the language passed to this function. maybe language can be a part of
    # the class itself. and fetch would simply use that language.
    # also jsut to prevent backend changing language in the middle of a function with
    # multi api calls. data structures involved in these cross api calls should also
    # have the language attribute as part of them. (stuff liek SearchItem)
    # or maybe even models?

    def resolve_lightcone(
        self, search_item: SearchItem, 
        language: Language = Language.EN
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
        from hsr_client.backend.srs_backend.parsers.lightcone import parse_lightcone

        if isinstance(search_item, SearchItem):
            if search_item.type != Item.LIGHTCONE:
                raise InvalidSearchItem(
                    "Expected Type.LIGHTCONES, found: " + str(search_item.type)
                )

            response = self.__fetch(language, routes.LIGHTCONES, True, search_item.id)
            if response is not None:
                return parse_lightcone(response, self)
            else:
                raise EmptyResponse

        else:
            raise TypeError("provided argument is not a `SearchItem`")


    def resolve_character(
        self, search_item: SearchItem, 
        language: Language = Language.EN
        ) :
        # unimplemented
        pass

    def get_lightcone_by_name(
        self, name: str,
        language: Language = Language.EN
        ) -> Lightcone:
        """Gets lightcone by name

        Args:
            name (str): name of the lightcone
            language (Languages, optional): Defaults to Languages.EN.

        Returns:
            Lightcone:
        """
        lightcones = self.search_item(Item.LIGHTCONE)

        for lightcone in lightcones:
            # use check to filter search item
            item = check(lightcone, "name", name)
            if item is not None:
                return self.resolve_lightcone(item)
   
        '''
        Function with declared type of "Lightcone" must return value on all code paths
        Type "None" cannot be assigned to type "Lightcone"
        '''
        #TODO: fix this typing issue 
        raise EmptyResponse


    def get_character_by_name(
        self, name: str, 
        language: Language = Language.EN
        ) -> Character:
        """Gets lightcone by name

        Args:
            name (str): name of the lightcone
            language (Language, optional): Defaults to Language.EN.

        Returns:
            Character:
        """
        with open("tests/data/character.json") as f:
            character_raw = json.load(f)

        from .parsers.character import parse_character
        character = parse_character(character_raw, self)


        return character
     

    def resolve_material(
            self, search_item : SearchItem,
            language : Language = Language.EN
        ) -> Material:
        """get details of a Material

        Args:
            item (SearchItem): SearchItem of Material type.
            language (Languages, optional):  Defaults to Languages.EN.

        Raises:
            InvalidItemType: if SearchItem is not of Material Type
            InvalidSearchItem: if item is not a SearchItem
        Returns:
            Material : Material object
        """

        if isinstance(search_item, SearchItem):
            if search_item.type != Item.MATERIAL:
                raise InvalidSearchItem(
                    "Expected Item.MATERIAL, found: " + str(search_item.type)
                )

            response = self.__fetch(language, routes.MATERIALS, True, search_item.id)
            if response is not None:
                return parse_material(response)
            else:
                raise EmptyResponse

        else:
            raise TypeError("provided argument is not a `SearchItem`")
        