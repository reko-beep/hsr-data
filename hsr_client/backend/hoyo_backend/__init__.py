import json
from typing import List, Union
from requests_cache import CachedSession
from hsr_client.datamodels.character import Character
from hsr_client.datamodels.searchItem import SearchItem
from hsr_client.errors import  InvalidLanguage
from ..util import Backend
import hsr_client.datamodels as models
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
        

    def __get_response(self, method: str, route, **params) -> None | dict | list[dict]:  
        """Fetches response data from the api route

        Args:
            method (str): GET, POST
            route (str): api route
            params (kwargs) : request payload 

        Returns:
            None | dict | list[dict]: returns the response
        """        
      
      
        self.session.headers.update(self.custom_headers)

        payload = {'json' : params} if method == 'POST' else {'params': params}
        response = self.session.request(method, route,force_refresh=True, **payload)   
        if response.status_code < 300:
            data = response.json()
            if data['message'] == 'OK' and data['retcode'] == 0:
                return data['data'].get('list', data['data'].get('entries', data['data'].get('page', None)))



    def __entries(self, type : Types, **params) -> list[SearchItem]:
        """gets all entries from api route of given type

        Args:
            type (Types): type enum. Types.CHARACTERS, Types.MATERIALS
            ---
            allowed kwargs
            ---
            page_num : int [1..... 99]
            page_size : int [number of items in one page]


        Returns:
            list[SearchItem]: returns a list of SearchItem
        """       

        params.update({'user_es': True})
        response = self.__get_response('POST', ENTRY_LIST, filters=[], menu_id=type, **params)

        if response is not None:            
            return [SearchItem(**searchItem.make_model_compatible(item, type)) for item in response]

    def __entry_detail(self, item : Union[SearchItem, int]) -> dict:
        """gets the detail of a search item
        item passed should be either a SearchItem, or the id of the entry

        Args:
            item (SearchItem, int): SearchItem [from __entries] or ID of the entry.

        Returns:
            dict: returns the data fetched
        """        
        entry_page_id = item
        if isinstance(entry_page_id, SearchItem):
            entry_page_id = entry_page_id.id

        response = self.__get_response('GET', ENTRY_PAGE, entry_page_id=entry_page_id)

        if response is not None:            
            return response

    