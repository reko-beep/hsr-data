from pydantic import BaseModel, validator, Field, Extra
from typing import Optional
from hsr_client.routes import IMAGE_ROUTE
from hsr_client.constants import Types


class SearchItem(BaseModel):

    url : Optional[str]
    iconPath : Optional[str]
    type : Optional[int]
    name : Optional[str]
    rarity : Optional[int]
    id : int | str

    class Config:
        extra = Extra.allow

   
  
    