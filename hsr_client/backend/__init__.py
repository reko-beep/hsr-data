from typing import Union
from hsr_client.backend.hoyo_backend import HoyoBackend
from .util import Backend

from .srs_backend import SRSBackend

from requests_cache import CachedSession

class BackendAdapter():
    def __init__(self):
        self.backends = {
            SRSBackend: SRSBackend(),
        }


    def __call__(self, adapter_name=SRSBackend) -> Union[SRSBackend, HoyoBackend]:
        """allows us to  access backend directly via `client.adapter().backend_method()`
        instead of `client.adapter.backends[SRSBackend].backend_method()` or
        something like `client.adapter.default_backend.backend_method()` or """
        return self.backends[adapter_name]

