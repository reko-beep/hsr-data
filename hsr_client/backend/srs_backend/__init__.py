

import json
from typing import List, Union
from requests_cache import CachedSession

from hsr_client.constants import Languages, Types
from hsr_client.datamodels.character import Character
from hsr_client.datamodels.searchItem import SearchItem
from hsr_client.errors import InvalidItemType, InvalidLanguage
from hsr_client.routes import CHARACTERS, MAIN_ROUTE, Routes
from hsr_client.utils import base36encode, generate_t
from ..util import Backend
import hsr_client.datamodels as models
from .parsers import trace as trace_parser





# backend for starrail station.
class SRSBackend(Backend):


    def __init__(self) -> None:
            
        self.session = CachedSession(cache_name='srs.cache', backend='sqlite', expire_after=3600)

        self.session.headers.update(
            {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68',
            'referer': 'https://starrailstation.com/'}
        )



    def generate_hash_route(self, language: Languages, route: Routes, goto: bool = False, item_id : str=''):
        '''
        
        :generates hashed route for fetching data

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
        
        url = route.generate_main_lang_path(language)
        if goto:
            if route.path is not None:
                url = f"{route.generate_goto_lang_path(language)}{item_id}.json"            

        hashed_path = base36encode(generate_t(url))

        return  f"{MAIN_ROUTE}{hashed_path}"






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



