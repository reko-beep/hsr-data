from requests_cache import CachedSession
from datamodels.searchItem import *
from routes import *
from typing import Union, List
from utils import generate_t, base36encode

class SRSClient:
    '''
    StarRailStation Website Client

    : initializes the client



    '''
    def __init__(self) -> None:
        
        self.__session = CachedSession(cache_name='srs.cache', backend='sqlite', expire_after=3600)

        self.__session.headers.update(
            {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68',
             'referer': 'https://starrailstation.com/'}
        )

    def generate_hash_route(self, language: str, route: Routes, goto: bool = False, item_id : str=''):
        '''
        
        :generates hashed route for fetching data

        --
        params
        --

        language: en, vi, de, etc
        route: a Routes object
        goto: if you want to search in a specific route [True] 
            - defaults to False
        
        item_id : id of the item you want to search in a route
        
        '''
        
        url = route.generate_main_lang_path(language)
        if goto:
            url = f"{route.generate_goto_lang_path(language)}{item_id}.json"
        print(url)
        hashed_path = base36encode(generate_t(url))

        return  f"{MAIN_ROUTE}{hashed_path}"




        
    
    def fetch(self, language: str , route: Routes, goto: bool = False, item_id : str = '') -> List[dict] | dict | None:
        '''
        
        :fetches data from the api route
        --
        params
        --

        language: en, vi, de, etc
        route: a Routes object
        goto: if you want to search in a specific route [True] 
            - defaults to False
        
        item_id : id of the item you want to search in a route
        
        '''


        response = self.__session.get(self.generate_hash_route(language, route, goto, item_id))
    

        if response.status_code  < 300:
            data = response.json()
            if 'entries' in data:
                return data['entries']
            else:
                return data
            

    def get_all_items(self, language: str = 'en') -> list[SearchItem]:

        pass