

import json
from typing import List, Union
from requests_cache import CachedSession

from constants import Languages, Types
from datamodels.character import Character
from datamodels.searchItem import SearchItem
from errors import InvalidItemType, InvalidLanguage
from routes import  MAIN_ROUTE, Routes, IMAGE_ROUTE, SEARCH
from utils import base36encode, generate_t
from ..util import Backend
import datamodels as models
from .parsers import trace as trace_parser





# backend for starrail station.
class SRSBackend(Backend):


    def __init__(self) -> None:
        super().__init__()
        #self.session = CachedSession(cache_name='srs.cache', backend='sqlite', expire_after=3600)

        


    def generate_hash_route(self, language: Languages, route: Routes, goto: bool = False, item_id : str=''):
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

        return  f"{MAIN_ROUTE}{hashed_path}"


    def __fetch(self, language: Languages , route: Routes, goto: bool = False, item_id : str = '') -> List[dict] | dict | None:
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

    def get_all_items(self,  type: Types = None, language: Languages = Languages.ENG) -> list[SearchItem]:
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

            response = self.__fetch(language, SEARCH, False)

            if response is not None:
                all_items = [SearchItem(**{ **d, **{'id': d['url'].split("/")[1]}, 'iconPath': IMAGE_ROUTE.format(assetId=d['iconPath'])}) for d in response]
                if type is not None:
                    return list(filter(lambda x: x.type == type, all_items))
            
        
                return all_items




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



