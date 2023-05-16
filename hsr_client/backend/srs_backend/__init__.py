

import json
from typing import List, Union
from requests_cache import CachedSession
from hsr_client.backend.srs_backend.parsers.lightcone import parse_lightcone

from hsr_client.constants import Languages, Types
from hsr_client.datamodels.character import Character
from hsr_client.datamodels.lightcone import Lightcone
from hsr_client.datamodels.searchItem import SearchItem
from hsr_client.errors import InvalidItemType, InvalidLanguage
from hsr_client import routes
from hsr_client.utils import base36encode, generate_t
from hsr_client.backend.util import Backend
import hsr_client.datamodels as models
from .parsers import trace as trace_parser


route_mapping = {
    Types.CHARACTERS : routes.CHARACTERS,
    Types.PLAYERCARDS : routes.PLAYERCARDS,
    Types.FOODS : routes.CONSUMABLES,
    Types.RELICS : routes.RELICS,
    Types.LIGHTCONES : routes.LIGHTCONES,
    Types.BOOKS : routes.BOOKS,
    Types.MATERIALS : routes.MATERIALS,    

}



# backend for starrail station.
class SRSBackend(Backend):


    def __init__(self) -> None:
        super().__init__()
        #self.session = CachedSession(cache_name='srs.cache', backend='sqlite', expire_after=3600)

        


    def generate_hash_route(self, language: Languages, route: routes.Routes, goto: bool = False, item_id : str=''):
        '''
        
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
        
        '''

        if not isinstance(language, Languages):
            raise InvalidLanguage
        
        url = route.generate_main_lang_path(language)
        if goto:
            if route.path is not None:
                url = f"{route.generate_goto_lang_path(language)}{item_id}.json"            

        hashed_path = base36encode(generate_t(url))

        return  f"{routes.MAIN_ROUTE}{hashed_path}"


    def __fetch(self, language: Languages , route: routes.Routes, goto: bool = False, item_id : str = '') -> List[dict] | dict | None:
        '''
        
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
        
        '''

        if not isinstance(language, Languages):
            raise InvalidLanguage

        self.session.headers.update(
            {'referer': 'https://starrailstation.com/'}
        )

        response = self.session.get(self.generate_hash_route(language, route, goto, item_id))
    

        if response.status_code  < 300:
            data = response.json()
            if 'entries' in data:
                return data['entries']
            else:
                return data

    def get_all_items(self,  type: Types = None, language: Languages = Languages.EN) -> list[SearchItem]:
            '''
            
            :fetches all items from api route
            --
            params
            --

            - language: Languages Enum
                Languages.EN, Languages.RU etc
            - type : a type object 
                Types.MATERIALS, Types.PLAYERCARDS, Types.CHARACTERS etc
            
            
            '''

            if not isinstance(language, Languages):
                raise InvalidLanguage

            response = self.__fetch(language, routes.SEARCH, False)

            if response is not None:
                all_items = [SearchItem(**{ **d, **{'id': d['url'].split("/")[1]}, 'iconPath': routes.IMAGE_ROUTE.format(assetId=d['iconPath'])}) for d in response]
                if type is not None:
                    return list(filter(lambda x: x.type == type, all_items))
            
        
                return all_items


    def get_lightcones(self, language: Languages = Languages.EN) -> List[SearchItem]:

        """gets all lightcones from api

        Returns:
            List[SearchItem]: SearchItem of Lightcones type.
        """        

        lightcones = self.get_all_items(Types.LIGHTCONES, language)

        return lightcones
    
    def get_lightcone_detail(self, item : SearchItem, language: Languages = Languages.EN) -> Lightcone:
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

        if isinstance(item, SearchItem):
            
            if item.type != Types.LIGHTCONES:
                raise InvalidItemType
            
            response = self.__fetch(language, LIGHTCONES, True, item.id)  
            if response is not None:

                #todo: parse lightcone raw data here
                return Lightcone(**response)
        
        else:

            raise InvalidSearchItem

    def get_character(self, target_name) -> models.chara.Character:


        import json

        # get this from ROUTE
        with open("tests/data/character.json") as f:
            character_raw = json.load(f)

        chara_name = character_raw["name"]
        traces_raw = character_raw["skillTreePoints"]
        traces = []
        trace_parser.parse_trace_data(traces_raw, traces)

        return models.chara.Character(
            name = chara_name,
            traces=traces
        )



