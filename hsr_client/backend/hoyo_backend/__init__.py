import json
from typing import List, Union
from requests_cache import CachedSession
from datamodels.character import Character
from datamodels.searchItem import SearchItem
from errors import InvalidItemType, InvalidLanguage
from ..util import Backend
import datamodels as models
from .constants import Types
from .routes import *
from .parsers import searchItem

class HoyoBackend(Backend):

    def __init__(self) -> None:

        super().__init__()
        
        self.custom_headers =  {"x-rpc-language": "en-us",
                                "x-rpc-wiki_app": "hsr",
                                "Origin": "https://wiki.hoyolab.com",    
                                "Referer": "https://wiki.hoyolab.com/"}
        

    def __get_response(self, route, **params) -> None | dict | list[dict]:  

        '''
        
        fetches data from a hoyolab api route

        - route
            hoyolab api route
        - params
            post data in keys
            
        '''
        self.session.headers.update(self.custom_headers)
        response = self.session.post(route, json=params)

        if response.status_code < 300:
            data = response.json()
            if data['message'] == 'OK' and data['retcode'] == 0:

                return data['data'].get('list', data.get('entries', None))



    def get_entries(self, type : Types) -> list[SearchItem]:
        '''
        fetches list of all items of specified type

        - type [see hoyobackend.]
            Types.CHARACTERS, Types.MATERIALS, Types.LIGHTCONES
        
        '''


        response = self.__get_response(ENTRY_LIST, filters=[], menu_id=type, page_num=1, page_size=30, use_es=True)

        if response is not None:            
            return [SearchItem(**searchItem.make_model_compatible(item, type)) for item in response]
