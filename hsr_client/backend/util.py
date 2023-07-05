# for VS Code intellisense only.
from typing import List
import hsr_client.datamodels as models
from requests_cache import CachedSession

class Backend():

    def __init__(self) -> None:
        super().__init__()

        self.session = CachedSession(
                                    cache_name='hsr.cache',
                                    backend='sqlite',
                                    expire_after=3600)
        
        self.session.headers.update(
            {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
            }
   
        )
